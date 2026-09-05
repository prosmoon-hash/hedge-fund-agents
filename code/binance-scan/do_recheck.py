#!/usr/bin/env python3
"""Fresh recheck + proposal check for first-pass aligned names."""
import json, os, time, statistics, urllib.request, ssl, concurrent.futures
from datetime import datetime, timezone, timedelta

base = "/workspace/binance-scan-2340"
UA = "Mozilla/5.0 (compatible; ResearchDesk/2312)"
ctx = ssl.create_default_context()
BST = timezone(timedelta(hours=1))

def get_json(url, retries=1):
    last_err = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=20, context=ctx) as r:
                data = r.read()
            if not data or data[:1] not in (b"{", b"["):
                last_err = f"bad body {data[:80]!r}"
                time.sleep(0.3)
                continue
            return json.loads(data), None
        except Exception as e:
            last_err = str(e)
            time.sleep(0.4)
    return None, last_err

def save(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f)

def book_of(d):
    if not d or not d.get("bids") or not d.get("asks"):
        return None
    bb = float(d["bids"][0][0]); ba = float(d["asks"][0][0])
    mid = (bb + ba) / 2.0
    if mid <= 0:
        return None
    spread_bps = (ba - bb) / mid * 1e4
    def band(pct):
        lo = mid * (1 - pct); hi = mid * (1 + pct)
        bid = sum(float(p) * float(q) for p, q in d["bids"] if float(p) >= lo)
        ask = sum(float(p) * float(q) for p, q in d["asks"] if float(p) <= hi)
        tot = bid + ask
        imb = (bid - ask) / tot if tot else 0.0
        return bid, ask, imb, tot
    b05, a05, i05, t05 = band(0.005)
    b1, a1, i1, t1 = band(0.01)
    levels = []; walls = []
    for side, book in (("bid", d["bids"]), ("ask", d["asks"])):
        for p, q in book:
            p = float(p); q = float(q); n = p * q
            levels.append(n)
            dist_bps = abs(p - mid) / mid * 1e4
            walls.append((n, dist_bps, side, p))
    med = statistics.median(levels) if levels else 0
    spoof = []; wall_notes = []
    for n, dist, side, p in sorted(walls, key=lambda x: -x[0])[:12]:
        if med > 0 and n >= 8 * med and dist <= 8:
            wall_notes.append(f"{side} {n/1000:.0f}k @{p} ({dist:.1f}bps, {n/med:.0f}x med)")
            if n >= 20 * med and dist <= 5:
                spoof.append(f"{side} {n/med:.0f}x at {dist:.1f}bps")
    return {
        "mid": mid, "bb": bb, "ba": ba, "spread_bps": spread_bps,
        "bid05": b05, "ask05": a05, "i05": i05, "t05": t05,
        "bid1": b1, "ask1": a1, "i1": i1, "t1": t1,
        "n_bids": len(d["bids"]), "n_asks": len(d["asks"]),
        "med": med, "spoof": bool(spoof), "spoof_why": spoof,
        "wall_note": "; ".join(wall_notes[:6]),
        "thin": t05 < 80000, "caution_thin": t05 < 150000,
        "wide": spread_bps > 8, "caution_spread": spread_bps > 5,
    }

def flow_of(kl):
    if not kl or len(kl) < 6:
        return None
    def close_n(n):
        if len(kl) < n + 1:
            return None
        c0 = float(kl[-n - 1][4]); c1 = float(kl[-1][4])
        return (c1 - c0) / c0 * 100 if c0 else None
    last15 = kl[-15:]
    tb = sum(float(x[10]) for x in last15)
    qv = sum(float(x[7]) for x in last15)
    taker = tb / qv if qv else None
    return {"taker15": taker, "r5": close_n(5), "r15": close_n(15),
            "r60": close_n(min(59, len(kl) - 1)), "last": float(kl[-1][4])}

def rsi14(closes):
    if len(closes) < 15:
        return None
    changes = [closes[i] - closes[i-1] for i in range(1, len(closes))]
    g = [max(c, 0) for c in changes]
    l = [max(-c, 0) for c in changes]
    ag = sum(g[:14]) / 14; al = sum(l[:14]) / 14
    for i in range(14, len(g)):
        ag = (ag * 13 + g[i]) / 14
        al = (al * 13 + l[i]) / 14
    if al == 0:
        return 100.0
    rs = ag / al
    return 100 - (100 / (1 + rs))

def ema(closes, n):
    if len(closes) < n:
        return None
    k = 2 / (n + 1)
    e = sum(closes[:n]) / n
    for c in closes[n:]:
        e = c * k + e * (1 - k)
    return e

def macd(closes):
    if len(closes) < 35:
        return None
    def ema_series(n):
        k = 2 / (n + 1)
        e = sum(closes[:n]) / n
        out = [None] * (n - 1) + [e]
        for c in closes[n:]:
            e = c * k + e * (1 - k)
            out.append(e)
        return out
    e12 = ema_series(12); e26 = ema_series(26)
    macd_line = []
    for a, b in zip(e12, e26):
        macd_line.append(None if a is None or b is None else a - b)
    vals = [x for x in macd_line if x is not None]
    if len(vals) < 9:
        return None
    k = 2 / (9 + 1)
    sig = sum(vals[:9]) / 9
    hist = None; macd_now = None
    for i, v in enumerate(vals):
        if i >= 9:
            sig = v * k + sig * (1 - k)
        macd_now = v; hist = v - sig
    return {"macd": macd_now, "signal": sig, "hist": hist}

def swings(kl, n=40):
    bars = kl[-n:]
    highs = [float(b[2]) for b in bars]
    lows = [float(b[3]) for b in bars]
    return max(highs), min(lows)

def equity_session(sym, contractType):
    if contractType != "TRADIFI_PERPETUAL":
        return None
    metals = {"XAUUSDT","XAGUSDT","XPDUSDT","XPTUSDT","CLUSDT","BZUSDT","NATGASUSDT","COPPERUSDT"}
    if sym in metals:
        return "tradfi_commodity_24h"
    now_utc = datetime.now(timezone.utc)
    hhmm = now_utc.hour * 60 + now_utc.minute
    us_open = 14 * 60 + 30 <= hhmm < 21 * 60
    kr_open = 0 <= hhmm < 6 * 60 + 30
    hk_open = 1 * 60 + 30 <= hhmm < 8 * 60
    if any(k in sym for k in ("SAMSUNG","SKHY","KODEX","KORU","HYUNDAI","NAVER","HANMI","LGELECTRONICS","EWY")):
        return "KR in-session" if kr_open else "KR off-hours"
    if any(k in sym for k in ("TENCENT","MEITUAN","KUAISHOU","HK0700","HK1810","POPMART")):
        return "HK in-session" if hk_open else "HK off-hours"
    return "US cash in-session" if us_open else "US cash off-hours"


# Load first-pass aligned + near-miss strong books + forced XAU stale recheck.
# CRCLUSDT is LIVE seat only — HOLD check separately; never a candidate.
scores = json.load(open(f"{base}/scores.json"))
aligned_fp = [r for r in scores if r.get("aligned")]
print("first_pass_aligned", [(r["symbol"], r["side"]) for r in aligned_fp])

LIVE_SEATS = {"CRCLUSDT", "XAUUSDT"}  # both live opens — pulse only, never candidates
FORCE_RECHECK = set()  # XAU is live second, not stale force-recheck candidate

def near_miss_ok(r):
    if r.get("symbol") in LIVE_SEATS:
        return False
    if r.get("aligned"):
        return False
    if r.get("thin") or r.get("wide") or r.get("spoof") or r.get("extreme24"):
        return False
    i05 = abs(r.get("i05") or 0)  # stored as percent
    t05 = r.get("t05") or 0
    if i05 < 25.0 or t05 < 150000:
        return False
    # Prefer names that had a book side (long/short) even if flow mismatched
    if not (r.get("book_long") or r.get("book_short")):
        return False
    return True

near_misses = [r for r in scores if near_miss_ok(r)]
near_misses.sort(key=lambda r: (-abs(r.get("i05") or 0), -(r.get("t05") or 0)))
near_misses = near_misses[:8]
print("near_miss_recheck", [(r["symbol"], r.get("side"), r.get("i05"), r.get("t05"), r.get("fail")) for r in near_misses])

# Build recheck set: aligned + near-miss + force XAU; exclude CRCL
by_sym = {}
for r in aligned_fp:
    if r["symbol"] in LIVE_SEATS:
        continue
    by_sym[r["symbol"]] = {"row": r, "origin": "first_pass_aligned", "side": r.get("side")}
for r in near_misses:
    if r["symbol"] in by_sym:
        continue
    side = "long" if r.get("book_long") else ("short" if r.get("book_short") else r.get("side"))
    by_sym[r["symbol"]] = {"row": r, "origin": "near_miss", "side": side}
for sym in FORCE_RECHECK:
    if sym in LIVE_SEATS:
        continue
    if sym in by_sym:
        continue
    row = next((r for r in scores if r["symbol"] == sym), None)
    if row is None:
        print("FORCE_RECHECK missing from scores", sym)
        continue
    side = "long" if row.get("book_long") else ("short" if row.get("book_short") else (row.get("side") or "long"))
    # XAU was LONG in 2149; if book flipped, still use book side
    by_sym[sym] = {"row": row, "origin": "force_stale_2149", "side": side}

recheck_list = list(by_sym.values())
print("recheck_targets", [(v["row"]["symbol"], v["origin"], v["side"]) for v in recheck_list])
if not recheck_list:
    print("no recheck targets; will still do CRCL HOLD")

# CMC once
cmc_data = None
cmc_status = "unavailable"
cmc_url = "https://pro-api.coinmarketcap.com/trial-pro-api/v1/cryptocurrency/listings/latest?limit=100&convert=USDT"
for attempt in range(3):
    cmc_raw, err = get_json(cmc_url, retries=0)
    if cmc_raw and isinstance(cmc_raw, dict) and "data" in cmc_raw:
        cmc_data = cmc_raw
        cmc_status = "ok"
        save(f"{base}/cmc_listings.json", cmc_raw)
        print("CMC ok n=", len(cmc_raw["data"]))
        break
    if err and "429" in str(err):
        print("CMC 429 backoff", attempt)
        time.sleep(2 * (attempt + 1))
        continue
    print("CMC fail", err)
    save(f"{base}/cmc_listings.json", {"error": str(err)})
    break

# exchangeInfo for contractType
ex = json.load(open(f"{base}/exchangeInfo.json"))
info = {s["symbol"]: s for s in ex["symbols"]}

def fetch_recheck(sym):
    R = f"{base}/recheck/{sym}"
    os.makedirs(R, exist_ok=True)
    endpoints = {
        "depth": f"https://www.binance.com/fapi/v1/depth?symbol={sym}&limit=500",
        "klines_1m": f"https://www.binance.com/fapi/v1/klines?symbol={sym}&interval=1m&limit=60",
        "ticker24hr": f"https://www.binance.com/fapi/v1/ticker/24hr?symbol={sym}",
        "premiumIndex": f"https://www.binance.com/fapi/v1/premiumIndex?symbol={sym}",
        "bookTicker": f"https://www.binance.com/fapi/v1/ticker/bookTicker?symbol={sym}",
        "klines_15m": f"https://www.binance.com/fapi/v1/klines?symbol={sym}&interval=15m&limit=100",
        "klines_1h": f"https://www.binance.com/fapi/v1/klines?symbol={sym}&interval=1h&limit=100",
    }
    out = {}
    fails = []
    for name, url in endpoints.items():
        data, err = get_json(url, retries=1)
        if data is None:
            fails.append((name, err))
        else:
            save(f"{R}/{name}.json", data)
            out[name] = data
        time.sleep(0.05)
    # spot
    spot_data, spot_err = get_json(f"https://www.binance.com/api/v3/depth?symbol={sym}&limit=500", retries=1)
    if spot_data and isinstance(spot_data, dict) and spot_data.get("bids"):
        save(f"{base}/spot/{sym}.json", spot_data)
        out["spot"] = spot_data
        out["spot_status"] = "ok"
    else:
        out["spot"] = None
        if spot_err and ("400" in str(spot_err) or "Invalid" in str(spot_err)):
            out["spot_status"] = "n/a"
        elif spot_data and isinstance(spot_data, dict) and spot_data.get("code"):
            out["spot_status"] = "n/a" if spot_data.get("code") in (-1121, -1100) else "unavailable"
            save(f"{base}/spot/{sym}.json", spot_data)
        else:
            out["spot_status"] = "unavailable"
            save(f"{base}/spot/{sym}.json", {"error": str(spot_err), "body": spot_data})
    out["_fails"] = fails
    return sym, out

# Fetch all candidate rechecks + CRCL HOLD
fetch_syms = [v["row"]["symbol"] for v in recheck_list] + sorted(LIVE_SEATS)
fetch_syms = list(dict.fromkeys(fetch_syms))
results_raw = {}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    futs = [pool.submit(fetch_recheck, s) for s in fetch_syms]
    for fut in concurrent.futures.as_completed(futs):
        sym, data = fut.result()
        results_raw[sym] = data
        print("fetched recheck", sym, "fails", data.get("_fails"), "spot", data.get("spot_status"))

# --- Dual LIVE HOLD/CLOSE pulse (not candidates) ---
LIVE_META = {
    "CRCLUSDT": {
        "side": "LONG", "entry": 89.17, "size": 1.36, "order": 1099123376,
        "close_px": 91.39925, "margin_note": "5% Operator-instructed first",
    },
    "XAUUSDT": {
        "side": "LONG", "entry": 4335.80, "size": 0.028, "order": 13906003826,
        "close_px": 4444.195, "margin_note": "5% second",
    },
}
live_holds = {}
for live_sym, meta in LIVE_META.items():
    raw = results_raw.get(live_sym, {})
    hold_obj = {
        "symbol": live_sym, "side": meta["side"], "entry": meta["entry"],
        "size": meta["size"], "order": meta["order"], "leverage": "20x CROSS",
        "margin_note": meta["margin_note"], "close_px": meta["close_px"],
        "hold": "none", "status": "LIVE_OPEN_FAR_FROM_CLOSE", "action_hint": None,
    }
    try:
        d = raw.get("depth"); kl = raw.get("klines_1m")
        t24 = raw.get("ticker24hr") or {}; pi = raw.get("premiumIndex") or {}
        b = book_of(d); f = flow_of(kl)
        mark = float(pi.get("markPrice") or 0)
        last = float(t24.get("lastPrice") or 0)
        mid = b["mid"] if b else None
        entry = meta["entry"]; close_px = meta["close_px"]
        roi20x = (mark - entry) / entry * 20 * 100 if mark else None  # percent
        at_close = (mark and mark >= close_px) or (last and last >= close_px)
        bid05 = b["bid05"] if b else 0; ask05 = b["ask05"] if b else 0
        bid1 = b["bid1"] if b else 0; ask1 = b["ask1"] if b else 0
        tb15 = f["taker15"] if f else None; r5 = f["r5"] if f else None
        hold_gates = (
            bid05 > ask05 and bid1 > ask1
            and tb15 is not None and tb15 > 0.50
            and r5 is not None and r5 > 0
        )
        if not at_close:
            hold = "none"; status = "LIVE_OPEN_FAR_FROM_CLOSE"; action_hint = None
        elif hold_gates:
            hold = "HOLD"; status = "AT_CLOSE_HOLD"; action_hint = "HOLD"
        else:
            hold = "none"; status = "AT_CLOSE_GATES_FAIL"; action_hint = "CLOSE_PING"
        hold_obj.update({
            "mark": mark, "last": last, "mid": mid,
            "i05": None if not b else round(b["i05"] * 100, 2),
            "i1": None if not b else round(b["i1"] * 100, 2),
            "tb15": None if tb15 is None else round(tb15 * 100, 2),
            "r5": None if r5 is None else round(r5, 3),
            "t05": None if not b else round(b["t05"]),
            "spread_bps": None if not b else round(b["spread_bps"], 2),
            "bid05": None if not b else round(bid05),
            "ask05": None if not b else round(ask05),
            "bid1": None if not b else round(bid1),
            "ask1": None if not b else round(ask1),
            "roi20x": None if roi20x is None else round(roi20x, 2),
            "dist_to_close": None if not mark else round(close_px - mark, 5),
            "at_close": bool(at_close),
            "hold_gates": bool(hold_gates) if at_close else None,
            "hold": hold,
            "status": status,
            "action_hint": action_hint,
            "note": "Research never places; flag/HOLD/CLOSE_PING only",
        })
        save(f"{base}/recheck/{live_sym}/hold.json", hold_obj)
        print(f"{live_sym} LIVE", {k: hold_obj.get(k) for k in ("mark","last","mid","roi20x","hold","status","action_hint","dist_to_close","i05","i1","tb15","r5")})
    except Exception as e:
        hold_obj["error"] = str(e)
        print(f"{live_sym} LIVE error", e)
    live_holds[live_sym] = hold_obj
    save(f"{base}/recheck/{live_sym}_hold.json", hold_obj)

crcl_hold = live_holds.get("CRCLUSDT", {})
xau_hold = live_holds.get("XAUUSDT", {})
save(f"{base}/recheck/crcl_hold.json", crcl_hold)
save(f"{base}/recheck/xau_hold.json", xau_hold)
save(f"{base}/recheck/live_holds.json", live_holds)
save(f"{base}/recheck/xau_hold.json", xau_hold)
save(f"{base}/recheck/live_holds.json", live_holds)

def evaluate(fp_meta):
    fp = fp_meta["row"]
    sym = fp["symbol"]
    first_side = fp_meta["side"]
    origin = fp_meta["origin"]
    data = results_raw[sym]
    meta = info.get(sym, {})
    ct = meta.get("contractType")
    session = equity_session(sym, ct)

    d = data.get("depth"); kl = data.get("klines_1m")
    t24 = data.get("ticker24hr") or {}; pi = data.get("premiumIndex") or {}
    bt = data.get("bookTicker") or {}
    kl15 = data.get("klines_15m") or []; kl1h = data.get("klines_1h") or []
    spot_raw = data.get("spot")
    spot_status = data.get("spot_status", "unavailable")

    b = book_of(d)
    f = flow_of(kl)
    if not b or not f:
        ev = {
            "symbol": sym, "first_side": first_side, "origin": origin, "fail_recheck": True,
            "aligned": False, "side": None, "fail": "missing book/flow on recheck",
            "proposal_check": {"verdict": "skip", "reason": "missing book/flow on recheck"},
            "session": session, "spot": {"status": spot_status}, "ta": None, "cmc": None,
        }
        return ev

    pct24 = float(t24.get("priceChangePercent") or 0)
    qvol = float(t24.get("quoteVolume") or 0)
    fund = float(pi.get("lastFundingRate") or 0)
    mark = float(pi.get("markPrice") or 0)
    last = float(t24.get("lastPrice") or 0)

    i05 = b["i05"]; i1 = b["i1"]
    tb = f["taker15"]; r5 = f["r5"]
    book_long = i05 >= 0.18 and i1 > 0
    book_short = i05 <= -0.18 and i1 < 0
    flow_long = tb is not None and r5 is not None and tb > 0.50 and r5 > 0
    flow_short = tb is not None and r5 is not None and tb < 0.50 and r5 < 0
    # Near-miss / book-primary soft path (how 2149 caught XAU with r5≈0):
    # strong book + taker confirms side + r5 not strongly against
    book_primary_long = (
        origin in ("near_miss", "force_stale_2149")
        and book_long and abs(i05) >= 0.25 and b["t05"] >= 150000
        and tb is not None and tb > 0.50
        and r5 is not None and r5 >= -0.05
    )
    book_primary_short = (
        origin in ("near_miss", "force_stale_2149")
        and book_short and abs(i05) >= 0.25 and b["t05"] >= 150000
        and tb is not None and tb < 0.50
        and r5 is not None and r5 <= 0.05
    )
    aligned_strict = (book_long and flow_long) or (book_short and flow_short)
    aligned_soft = book_primary_long or book_primary_short
    aligned = aligned_strict or aligned_soft
    if book_long and flow_long:
        side = "long"
    elif book_short and flow_short:
        side = "short"
    elif book_primary_long:
        side = "long"
    elif book_primary_short:
        side = "short"
    else:
        side = "long" if book_long else ("short" if book_short else None)

    fail = None
    if b["thin"]:
        fail = "thin 0.5% book"
    elif b["wide"]:
        fail = "wide spread"
    elif b["spoof"]:
        fail = "spoof wall near mid"
    elif abs(pct24) >= 15:
        fail = "extreme crowded 24h chase"
    elif pct24 >= 15 and fund <= -0.001 and f["r15"] is not None and f["r60"] is not None and f["r15"] < 0 and f["r60"] < 0:
        fail = "squeeze-exhaust"
        aligned = False
    elif not aligned:
        fail = "book/flow mismatch or fade"
    elif first_side and side and side != first_side:
        fail = f"side flipped {first_side}->{side}"
        aligned = False

    # spot
    spot_out = {"status": spot_status}
    sb = book_of(spot_raw) if spot_raw else None
    if sb:
        gap = (sb["mid"] - b["mid"]) / b["mid"] * 1e4
        agrees = False
        if side == "short":
            agrees = sb["i05"] <= -0.12
        elif side == "long":
            agrees = sb["i05"] >= 0.12
        agrees_strong = (side == "short" and sb["i05"] <= -0.18 and sb["i1"] < 0) or (side == "long" and sb["i05"] >= 0.18 and sb["i1"] > 0)
        against = (side == "short" and sb["i05"] >= 0.12) or (side == "long" and sb["i05"] <= -0.12)
        vs = "agrees" if agrees_strong or (agrees and not against) else ("against" if against else "neutral")
        spot_out = {
            "status": "ok",
            "mid": sb["mid"],
            "i05": round(sb["i05"] * 100, 2),
            "i1": round(sb["i1"] * 100, 2),
            "spread_bps": round(sb["spread_bps"], 2),
            "t05": round(sb["t05"]),
            "bid05": round(sb["bid05"]),
            "ask05": round(sb["ask05"]),
            "thin": sb["thin"], "wide": sb["wide"], "spoof": sb["spoof"],
            "wall_note": sb["wall_note"],
            "spot_futures_gap_bps": round(gap, 2),
            "agrees_with_futures_side": agrees_strong or agrees,
            "direction": "bid-heavy" if sb["i05"] > 0 else "ask-heavy",
            "vs_futures": vs,
        }
    elif ct == "TRADIFI_PERPETUAL":
        spot_out = {"status": "n/a", "note": "TradFi typically no USDT spot pair"}

    # TA 15m
    ta = None
    ta_1h = None
    if kl15:
        closes15 = [float(x[4]) for x in kl15]
        rsi = rsi14(closes15)
        e20 = ema(closes15, 20); e50 = ema(closes15, 50)
        m = macd(closes15)
        sh, sl = swings(kl15, 40)
        mid = b["mid"]
        ta = {
            "interval": "15m",
            "rsi14": None if rsi is None else round(rsi, 2),
            "ema20": None if e20 is None else round(e20, 6),
            "ema50": None if e50 is None else round(e50, 6),
            "price_vs_ema20": None if e20 is None else ("above" if mid > e20 else "below"),
            "price_vs_ema50": None if e50 is None else ("above" if mid > e50 else "below"),
            "macd_hist": None if not m else round(m["hist"], 7),
            "macd_hist_sign": None if not m else ("+" if m["hist"] > 0 else "-"),
            "swing_high": sh, "swing_low": sl,
            "dist_to_swing_high_bps": round((sh - mid) / mid * 1e4, 1),
            "dist_to_swing_low_bps": round((mid - sl) / mid * 1e4, 1),
            "n_bars": len(kl15),
            "last": closes15[-1] if closes15 else None,
        }
        against = False; reasons = []
        if aligned and side == "short":
            if rsi is not None and rsi < 30:
                against = True; reasons.append("RSI oversold")
            if e20 is not None and mid > e20:
                against = True; reasons.append("price above EMA20")
            if m and m["hist"] > 0:
                against = True; reasons.append("MACD hist +")
            if ta["dist_to_swing_low_bps"] is not None and ta["dist_to_swing_low_bps"] < 40:
                against = True; reasons.append("near 15m swing low")
        elif aligned and side == "long":
            if rsi is not None and rsi > 75:
                against = True; reasons.append("RSI overbought")
            if e20 is not None and mid < e20:
                against = True; reasons.append("price below EMA20")
            if m and m["hist"] < 0:
                against = True; reasons.append("MACD hist -")
            if ta["dist_to_swing_high_bps"] is not None and ta["dist_to_swing_high_bps"] < 40:
                against = True; reasons.append("near 15m swing high")
        ta["vs_book"] = "against" if against else ("aligned" if aligned else "n/a")
        ta["vs_book_why"] = reasons

    if kl1h:
        closes1h = [float(x[4]) for x in kl1h]
        m1 = macd(closes1h)
        ta_1h = {
            "rsi14": None if rsi14(closes1h) is None else round(rsi14(closes1h), 2),
            "ema20": None if ema(closes1h,20) is None else round(ema(closes1h,20), 6),
            "ema50": None if ema(closes1h,50) is None else round(ema(closes1h,50), 6),
            "macd_hist_sign": None if not m1 else ("+" if m1["hist"] > 0 else "-"),
        }

    # CMC
    cmc_out = None
    if ct == "TRADIFI_PERPETUAL":
        cmc_out = {"status": "n/a", "note": "TradFi"}
    elif cmc_status != "ok":
        cmc_out = {"status": "unavailable"}
    else:
        base_sym = sym.replace("USDT", "")
        if base_sym.startswith("1000"):
            base_sym_cmc = base_sym[4:]
        else:
            base_sym_cmc = base_sym
        found = None
        for row in cmc_data["data"]:
            if row.get("symbol") == base_sym or row.get("symbol") == base_sym_cmc:
                found = row; break
        if found:
            q = found.get("quote", {}).get("USDT") or found.get("quote", {}).get("USD") or {}
            movers = []
            for row in cmc_data["data"]:
                qq = row.get("quote", {}).get("USDT") or row.get("quote", {}).get("USD") or {}
                p = qq.get("percent_change_24h")
                if p is not None:
                    movers.append((abs(p), row.get("symbol")))
            movers.sort(reverse=True)
            top5 = {m[1] for m in movers[:5]}
            pct24_cmc = q.get("percent_change_24h")
            cmc_out = {
                "status": "ok",
                "cmc_rank": found.get("cmc_rank"),
                "name": found.get("name"),
                "mcap": q.get("market_cap"),
                "pct24": pct24_cmc,
                "pct7d": q.get("percent_change_7d"),
                "circ": found.get("circulating_supply"),
                "top_mover": found.get("symbol") in top5,
            }
        else:
            cmc_out = {"status": "not_in_top100"}

    # Proposal check
    pc_verdict = "skip"
    pc_reason = fail or "not aligned"
    merely_ok_book = False
    side_ok = (first_side is None) or (side == first_side)
    if aligned and fail is None and side_ok:
        liquid = (not b["thin"] and not b["caution_thin"]) or b["t05"] >= 80000
        extreme_wall = abs(i05) >= 0.70
        merely_ok_book = b["caution_thin"] or b["caution_spread"] or abs(i05) < 0.25
        ta_against = ta and ta.get("vs_book") == "against"
        spot_against = spot_out.get("vs_futures") == "against"
        cmc_extreme = False
        if cmc_out and cmc_out.get("status") == "ok" and cmc_out.get("pct24") is not None:
            if abs(cmc_out["pct24"]) >= 20:
                cmc_extreme = True

        if b["spoof"]:
            pc_verdict = "skip"; pc_reason = "spoofable wall near mid"
        elif not liquid and b["thin"]:
            pc_verdict = "skip"; pc_reason = "thin book"
        elif extreme_wall:
            pc_verdict = "weak"; pc_reason = "extreme |i05| one-sided wall that can vanish (wall-pull risk)"
        elif cmc_extreme:
            pc_verdict = "skip"; pc_reason = f"extreme CMC 24h extension {cmc_out['pct24']:.1f}%"
        elif ta_against and merely_ok_book:
            pc_verdict = "weak"; pc_reason = "TA against merely-ok book: " + ", ".join(ta.get("vs_book_why") or [])
        elif spot_against and merely_ok_book and spot_out.get("status") == "ok":
            pc_verdict = "weak"; pc_reason = "spot against merely-ok futures book"
        elif ta_against and not merely_ok_book:
            why = ta.get("vs_book_why") or []
            if any("swing" in w for w in why) or any("RSI" in w for w in why):
                pc_verdict = "weak"; pc_reason = "TA against book: " + ", ".join(why)
            else:
                pc_verdict = "sound"; pc_reason = "book+flow aligned; TA soft-against but book strong"
                if aligned_soft and not aligned_strict:
                    pc_reason = "book-primary (near-miss) + mild flow; TA soft-against but book strong"
        else:
            pc_verdict = "sound"
            if aligned_soft and not aligned_strict:
                pc_reason = "liquid book-primary near-miss + taker confirm; r5 flat/soft; proposal checks pass"
            else:
                pc_reason = "liquid book + flow aligned; no spoof/squeeze; proposal checks pass"
            if ta and ta.get("vs_book") == "aligned":
                pc_reason += "; TA aligned (plus)"
            if spot_out.get("vs_futures") == "agrees":
                pc_reason += "; spot agrees"
            if session:
                pc_reason += f"; session={session}"

    fail_recheck = not (aligned and fail is None and side_ok and pc_verdict == "sound")

    ev = {
        "symbol": sym,
        "first_side": first_side,
        "origin": origin,
        "fail_recheck": fail_recheck,
        "mid": b["mid"],
        "bb": b["bb"], "ba": b["ba"],
        "mark": mark, "last": last,
        "spread_bps": round(b["spread_bps"], 2),
        "i05": round(i05 * 100, 2),
        "i1": round(i1 * 100, 2),
        "bid05": round(b["bid05"]), "ask05": round(b["ask05"]), "t05": round(b["t05"]),
        "bid1": round(b["bid1"]), "ask1": round(b["ask1"]), "t1": round(b["t1"]),
        "taker15": None if tb is None else round(tb * 100, 2),
        "r5": None if r5 is None else round(r5, 3),
        "r15": None if f["r15"] is None else round(f["r15"], 3),
        "r60": None if f["r60"] is None else round(f["r60"], 3),
        "pct24": pct24, "qvolM": round(qvol / 1e6, 1), "fund": fund,
        "thin": b["thin"], "wide": b["wide"], "spoof": b["spoof"],
        "spoof_why": b["spoof_why"], "wall_note": b["wall_note"],
        "book_long": book_long, "book_short": book_short,
        "flow_long": flow_long, "flow_short": flow_short,
        "aligned_strict": aligned_strict, "aligned_soft": aligned_soft,
        "aligned": aligned and fail is None and side_ok,
        "side": side, "fail": fail,
        "spot": spot_out, "ta": ta, "ta_1h": ta_1h, "cmc": cmc_out,
        "proposal_check": {"verdict": pc_verdict, "reason": pc_reason},
        "session": session,
        "contractType": ct,
        "merely_ok_book": merely_ok_book,
    }
    save(f"{base}/recheck/{sym}/eval.json", ev)
    print(f"EVAL {sym} [{origin}]: aligned={ev['aligned']} side={side} fail={fail} pc={pc_verdict}: {pc_reason}")
    print(f"  i05={ev['i05']} i1={ev['i1']} tb={ev['taker15']} r5={ev['r5']} t05={ev['t05']} spr={ev['spread_bps']}")
    if ta:
        print(f"  TA vs_book={ta.get('vs_book')} why={ta.get('vs_book_why')} rsi={ta.get('rsi14')} swing_low_bps={ta.get('dist_to_swing_low_bps')}")
    print(f"  spot={spot_out.get('status')} vs={spot_out.get('vs_futures')} cmc={cmc_out}")
    return ev

evals = []
for meta in recheck_list:
    evals.append(evaluate(meta))

save(f"{base}/recheck/evals.json", evals)
print("wrote evals", len(evals))
sound = [e for e in evals if e.get("proposal_check", {}).get("verdict") == "sound"]
print("SOUND count", len(sound), [e["symbol"] for e in sound])

save(f"{base}/recheck/crcl_hold.json", crcl_hold)
save(f"{base}/recheck/xau_hold.json", xau_hold)
save(f"{base}/recheck/live_holds.json", live_holds)
