import json, os, statistics
from datetime import datetime, timezone

base = "/tmp/binance-scan-0838"
ex = json.load(open(f"{base}/exchangeInfo.json"))
tick = {t["symbol"]: t for t in json.load(open(f"{base}/ticker24hr.json"))}
pmap = {p["symbol"]: p for p in json.load(open(f"{base}/premiumIndex.json"))}

info = {}
for s in ex["symbols"]:
    if s.get("contractType") in ("PERPETUAL", "TRADIFI_PERPETUAL") and s.get("quoteAsset") == "USDT":
        info[s["symbol"]] = s

SKIP_HARD = {"CYSUSDT", "SUIUSDT", "TRUMPUSDT", "UAIUSDT"}
now_utc = datetime.now(timezone.utc)


def equity_session(sym, contractType):
    if contractType != "TRADIFI_PERPETUAL":
        return None
    metals = {
        "XAUUSDT",
        "XAGUSDT",
        "XPDUSDT",
        "XPTUSDT",
        "CLUSDT",
        "BZUSDT",
        "NATGASUSDT",
        "COPPERUSDT",
    }
    if sym in metals:
        return "tradfi_commodity_24h"
    hhmm = now_utc.hour * 60 + now_utc.minute
    us_open = 14 * 60 + 30 <= hhmm < 21 * 60
    kr_open = 0 <= hhmm < 6 * 60 + 30
    hk_open = 1 * 60 + 30 <= hhmm < 8 * 60
    if any(
        k in sym
        for k in (
            "SAMSUNG",
            "SKHY",
            "KODEX",
            "KORU",
            "HYUNDAI",
            "NAVER",
            "HANMI",
            "LGELECTRONICS",
            "EWY",
        )
    ):
        return "KR in-session" if kr_open else "KR off-hours"
    if any(k in sym for k in ("TENCENT", "MEITUAN", "KUAISHOU", "HK0700", "HK1810", "POPMART")):
        return "HK in-session" if hk_open else "HK off-hours"
    return "US cash in-session" if us_open else "US cash off-hours"


def book_of(d):
    if not d.get("bids") or not d.get("asks"):
        return None
    bb = float(d["bids"][0][0])
    ba = float(d["asks"][0][0])
    mid = (bb + ba) / 2.0
    if mid <= 0:
        return None
    spread_bps = (ba - bb) / mid * 1e4

    def band(pct):
        lo = mid * (1 - pct)
        hi = mid * (1 + pct)
        bid = sum(float(p) * float(q) for p, q in d["bids"] if float(p) >= lo)
        ask = sum(float(p) * float(q) for p, q in d["asks"] if float(p) <= hi)
        tot = bid + ask
        imb = (bid - ask) / tot if tot else 0.0
        return bid, ask, imb, tot

    b05, a05, i05, t05 = band(0.005)
    b1, a1, i1, t1 = band(0.01)
    levels = []
    walls = []
    for side, book in (("bid", d["bids"]), ("ask", d["asks"])):
        for p, q in book:
            p = float(p)
            q = float(q)
            n = p * q
            levels.append(n)
            dist_bps = abs(p - mid) / mid * 1e4
            walls.append((n, dist_bps, side, p))
    med = statistics.median(levels) if levels else 0
    spoof = []
    wall_notes = []
    for n, dist, side, p in sorted(walls, key=lambda x: -x[0])[:12]:
        if med > 0 and n >= 8 * med and dist <= 8:
            wall_notes.append(f"{side} {n/1000:.0f}k @{p} ({dist:.1f}bps, {n/med:.0f}x med)")
            if n >= 20 * med and dist <= 5:
                spoof.append(f"{side} {n/med:.0f}x at {dist:.1f}bps")
    return {
        "mid": mid,
        "bb": bb,
        "ba": ba,
        "spread_bps": spread_bps,
        "bid05": b05,
        "ask05": a05,
        "i05": i05,
        "t05": t05,
        "bid1": b1,
        "ask1": a1,
        "i1": i1,
        "n_bids": len(d["bids"]),
        "n_asks": len(d["asks"]),
        "med": med,
        "spoof": bool(spoof),
        "spoof_why": spoof,
        "wall_note": "; ".join(wall_notes[:6]),
        "thin": t05 < 80000,
        "caution_thin": t05 < 150000,
        "wide": spread_bps > 8,
        "caution_spread": spread_bps > 5,
    }


def flow_of(kl):
    if not kl or len(kl) < 6:
        return None

    def close_n(n):
        if len(kl) < n + 1:
            return None
        c0 = float(kl[-n - 1][4])
        c1 = float(kl[-1][4])
        return (c1 - c0) / c0 * 100 if c0 else None

    last15 = kl[-15:]
    tb = sum(float(x[10]) for x in last15)
    qv = sum(float(x[7]) for x in last15)
    taker = tb / qv if qv else None
    return {
        "taker15": taker,
        "r5": close_n(5),
        "r15": close_n(15),
        "r60": close_n(min(59, len(kl) - 1)),
        "last": float(kl[-1][4]),
    }


rows = []
depth_dir = f"{base}/depth"
for fn in sorted(os.listdir(depth_dir)):
    if not fn.endswith(".json") or fn.startswith("._"):
        continue
    sym = fn[:-5]
    d = json.load(open(f"{depth_dir}/{fn}"))
    b = book_of(d)
    if b is None:
        rows.append({"symbol": sym, "fail": "missing book", "aligned": False})
        continue
    kl = json.load(open(f"{base}/klines_1m/{sym}.json"))
    f = flow_of(kl)
    t = tick.get(sym, {})
    p = pmap.get(sym, {})
    meta = info.get(sym, {})
    pct24 = float(t.get("priceChangePercent") or 0)
    qvol = float(t.get("quoteVolume") or 0)
    fund = float(p.get("lastFundingRate") or 0)
    ct = meta.get("contractType")
    i05 = b["i05"]
    i1 = b["i1"]
    book_long = i05 >= 0.18 and i1 > 0
    book_short = i05 <= -0.18 and i1 < 0
    mild_long = i05 >= 0.12 and i1 > 0
    mild_short = i05 <= -0.12 and i1 < 0
    tb = f["taker15"] if f else None
    r5 = f["r5"] if f else None
    flow_long = tb is not None and r5 is not None and tb > 0.50 and r5 > 0
    flow_short = tb is not None and r5 is not None and tb < 0.50 and r5 < 0
    aligned = False
    side = None
    fail = None
    extreme = abs(pct24) >= 15
    if sym in SKIP_HARD:
        fail = "hard skip (no backfill)"
    elif b["thin"]:
        fail = "thin 0.5% book"
    elif b["wide"]:
        fail = "wide spread"
    elif b["spoof"]:
        fail = "spoof wall near mid"
    elif extreme:
        fail = "extreme crowded 24h chase"
    elif book_long and flow_long:
        aligned = True
        side = "long"
    elif book_short and flow_short:
        aligned = True
        side = "short"
    elif book_long and not flow_long:
        fail = "book/flow mismatch (tb/r5 not long)"
        side = "long"
    elif book_short and not flow_short:
        fail = "book/flow mismatch (tb/r5 not short)"
        side = "short"
    elif mild_long or mild_short:
        fail = "imb0.5 under 18% band"
        side = "long" if mild_long else "short"
    else:
        fail = "no aligned book+flow edge"
    squeeze = False
    if pct24 >= 15 and fund <= -0.001 and f and f["r15"] is not None and f["r60"] is not None:
        if f["r15"] < 0 and f["r60"] < 0:
            squeeze = True
            if aligned:
                fail = "squeeze-exhaust"
                aligned = False
    rec = {
        "symbol": sym,
        "mid": b["mid"],
        "spread_bps": round(b["spread_bps"], 2),
        "i05": round(i05 * 100, 2),
        "i1": round(i1 * 100, 2),
        "bid05": round(b["bid05"]),
        "ask05": round(b["ask05"]),
        "t05": round(b["t05"]),
        "bid1": round(b["bid1"]),
        "ask1": round(b["ask1"]),
        "taker15": None if not f or f["taker15"] is None else round(f["taker15"] * 100, 2),
        "r5": None if not f else (None if f["r5"] is None else round(f["r5"], 3)),
        "r15": None if not f else (None if f["r15"] is None else round(f["r15"], 3)),
        "r60": None if not f else (None if f["r60"] is None else round(f["r60"], 3)),
        "pct24": pct24,
        "qvolM": round(qvol / 1e6, 1),
        "fund": fund,
        "thin": b["thin"],
        "caution_thin": b["caution_thin"],
        "wide": b["wide"],
        "caution_spread": b["caution_spread"],
        "spoof": b["spoof"],
        "spoof_why": b["spoof_why"],
        "wall_note": b["wall_note"],
        "extreme24": extreme,
        "squeeze": squeeze,
        "contractType": ct,
        "tradifi": ct == "TRADIFI_PERPETUAL",
        "session": equity_session(sym, ct),
        "book_long": book_long,
        "book_short": book_short,
        "mild_long": mild_long,
        "mild_short": mild_short,
        "flow_long": flow_long,
        "flow_short": flow_short,
        "aligned": aligned,
        "side": side,
        "fail": fail,
        "n_bids": b["n_bids"],
        "n_asks": b["n_asks"],
        "bb": b["bb"],
        "ba": b["ba"],
    }
    rows.append(rec)

rows.sort(key=lambda r: -abs(r.get("i05") or 0))
json.dump(rows, open(f"{base}/scores.json", "w"))
aligned = [r for r in rows if r.get("aligned")]
books = [r for r in rows if r.get("book_long") or r.get("book_short")]
print("now_utc", now_utc.isoformat())
print("aligned", len(aligned))
print("strong books", len(books))
print("=== ALIGNED ===")
for r in aligned:
    print(
        r["symbol"],
        r["side"],
        "mid",
        r["mid"],
        "i05",
        r["i05"],
        "i1",
        r["i1"],
        "t05",
        r["t05"],
        "spr",
        r["spread_bps"],
        "tb",
        r["taker15"],
        "r5",
        r["r5"],
        "qvolM",
        r["qvolM"],
        "pct24",
        r["pct24"],
        r["fail"],
        r["contractType"],
        r["session"],
    )
print("=== STRONG BOOKS ===")
for r in books:
    print(
        r["symbol"],
        "side",
        r["side"],
        "i05",
        r["i05"],
        "i1",
        r["i1"],
        "t05",
        r["t05"],
        "spr",
        r["spread_bps"],
        "tb",
        r["taker15"],
        "r5",
        r["r5"],
        "fail",
        r["fail"],
        "qvol",
        r["qvolM"],
        "pct",
        r["pct24"],
        r["contractType"],
    )
print("=== TOP |i05| 30 ===")
for r in rows[:30]:
    print(
        r["symbol"],
        "i05",
        r["i05"],
        "i1",
        r["i1"],
        "t05k",
        round(r["t05"] / 1000),
        "spr",
        r["spread_bps"],
        "tb",
        r["taker15"],
        "r5",
        r["r5"],
        "pct24",
        r["pct24"],
        r["fail"],
    )
print("wrote", len(rows))
