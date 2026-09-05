#!/usr/bin/env python3
"""Public unsigned Binance USDT-M paper-mark. No keys, no cookies, no orders."""
import json
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta

BASE = "https://www.binance.com/fapi/v1"
BST = timezone(timedelta(hours=1))
TIMEOUT = 15
SLEEP_S = 0.08

def bst_ms(y, m, d, H, M, S=0):
    dt = datetime(y, m, d, H, M, S, tzinfo=BST)
    return int(dt.timestamp() * 1000)

def ms_to_bst(ms):
    dt = datetime.fromtimestamp(ms / 1000, tz=BST)
    return dt.strftime("%Y-%m-%d %H:%M BST")

# (symbol, side, mid, scan, prop_bst_label, start_ms)
PROPOSALS = [
    ("CYSUSDT", "SHORT", 0.9679, "(none)", "2026-08-31 10:37:00", bst_ms(2026, 8, 31, 10, 37)),
    ("SUIUSDT", "LONG", 0.72175, "(none)", "2026-08-31 11:00:00", bst_ms(2026, 8, 31, 11, 0)),
    ("TRUMPUSDT", "SHORT", 2.3615, "(none)", "2026-08-31 12:00:00", bst_ms(2026, 8, 31, 12, 0)),
    ("UAIUSDT", "SHORT", 0.4005, "(none)", "2026-08-31 16:00:00", bst_ms(2026, 8, 31, 16, 0)),
    ("DASHUSDT", "SHORT", 47.285, "(none)", "2026-08-31 19:05:00", bst_ms(2026, 8, 31, 19, 5)),
    ("NVDAUSDT", "LONG", 220.395, "(none)", "2026-08-31 20:54:00", bst_ms(2026, 8, 31, 20, 54)),
    ("NVDAUSDT", "LONG", 220.745, "(none)", "2026-08-31 22:29:00", bst_ms(2026, 8, 31, 22, 29)),
    ("MUUSDT", "LONG", 956.055, "(none)", "2026-08-31 22:44:00", bst_ms(2026, 8, 31, 22, 44)),
    ("BICOUSDT", "LONG", 0.023385, "(none)", "2026-08-31 22:59:00", bst_ms(2026, 8, 31, 22, 59)),
    ("UNITREEUSDT", "SHORT", 83.135, "(none)", "2026-08-31 23:04:00", bst_ms(2026, 8, 31, 23, 4)),
    ("OPUSDT", "LONG", 0.091475, "(none)", "2026-08-31 23:46:00", bst_ms(2026, 8, 31, 23, 46)),
    ("PUMPUSDT", "LONG", 0.0044515, "(none)", "2026-09-01 00:20:00", bst_ms(2026, 9, 1, 0, 20)),
    ("TSLAUSDT", "SHORT", 366.475, "0254", "2026-09-01 02:56:58", bst_ms(2026, 9, 1, 2, 56, 58)),
    ("XMRUSDT", "SHORT", 507.285, "0321", "2026-09-01 03:21:00", bst_ms(2026, 9, 1, 3, 21)),
    ("TSLAUSDT", "SHORT", 366.245, "0336", "2026-09-01 03:36:00", bst_ms(2026, 9, 1, 3, 36)),
    ("CLUSDT", "SHORT", 86.575, "0433", "2026-09-01 04:36:00", bst_ms(2026, 9, 1, 4, 36)),
    ("LITEUSDT", "SHORT", 914.42, "0529", "2026-09-01 05:31:00", bst_ms(2026, 9, 1, 5, 31)),
    ("CBRSUSDT", "SHORT", 183.715, "0618", "2026-09-01 06:21:00", bst_ms(2026, 9, 1, 6, 21)),
    ("ZHIPUUSDT", "SHORT", 153.475, "0651", "2026-09-01 06:54:00", bst_ms(2026, 9, 1, 6, 54)),
    ("AXTIUSDT", "LONG", 60.695, "0705", "2026-09-01 07:08:40", bst_ms(2026, 9, 1, 7, 8, 40)),
    ("LITEUSDT", "SHORT", 920.08, "0758", "2026-09-01 08:01:00", bst_ms(2026, 9, 1, 8, 1)),
    ("BCHUSDT", "SHORT", 247.485, "1709", "2026-09-01 17:14:00", bst_ms(2026, 9, 1, 17, 14)),
    ("XPLUSDT", "SHORT", 0.084915, "1743", "2026-09-01 17:47:00", bst_ms(2026, 9, 1, 17, 47)),
    ("XLMUSDT", "LONG", 0.176195, "1757", "2026-09-01 17:59:00", bst_ms(2026, 9, 1, 17, 59)),
    ("PUMPUSDT", "SHORT", 0.0042825, "1822", "2026-09-01 18:29:00", bst_ms(2026, 9, 1, 18, 29)),
    ("APTUSDT", "SHORT", 0.55135, "1926", "2026-09-01 19:31:00", bst_ms(2026, 9, 1, 19, 31)),
    ("POLUSDT", "SHORT", 0.090415, "1936", "2026-09-01 19:40:00", bst_ms(2026, 9, 1, 19, 40)),
    ("GRAMUSDT", "SHORT", 1.3175, "2036", "2026-09-01 20:42:00", bst_ms(2026, 9, 1, 20, 42)),
    ("SKRUSDT", "LONG", 0.0234045, "2129", "2026-09-01 21:33:00", bst_ms(2026, 9, 1, 21, 33)),
    ("CRCLUSDT", "LONG", 89.325, "2136", "2026-09-01 21:39:00", bst_ms(2026, 9, 1, 21, 39)),
    ("XAUUSDT", "LONG", 4336.975, "2149", "2026-09-01 21:52:00", bst_ms(2026, 9, 1, 21, 52)),
]

ALT_SYMBOLS = {
    "SKRUSDT": ["SKRUSDT", "SKR"],
    "CRCLUSDT": ["CRCLUSDT", "CRCL"],
    "XAUUSDT": ["XAUUSDT", "XAU"],
    "UNITREEUSDT": ["UNITREEUSDT", "UNITREE", "UNITREUSDT"],
    "ZHIPUUSDT": ["ZHIPUUSDT", "ZHIPU", "ZHIUSDT"],
    "AXTIUSDT": ["AXTIUSDT", "AXTI"],
    "XPLUSDT": ["XPLUSDT", "XPL"],
    "LITEUSDT": ["LITEUSDT", "LITE"],
    "CBRSUSDT": ["CBRSUSDT", "CBRS"],
    "UAIUSDT": ["UAIUSDT", "UAI"],
    "CYSUSDT": ["CYSUSDT", "CYS"],
    "GRAMUSDT": ["GRAMUSDT", "GRAM"],
}

ALREADY_ALERTED_10 = {("CYSUSDT", "SHORT"), ("OPUSDT", "LONG")}


def curl_get(url):
    cmd = [
        "curl", "-sS", "-m", str(TIMEOUT),
        "-H", "Accept: application/json",
        "-A", "Mozilla/5.0 (paper-mark; public unsigned GET)",
        url,
    ]
    p = subprocess.run(cmd, capture_output=True, text=True)
    body = p.stdout
    err = p.stderr.strip()
    if p.returncode != 0:
        return None, f"curl_exit={p.returncode} err={err} body={body[:200]}"
    if not body:
        return None, f"empty_body err={err}"
    try:
        return json.loads(body), None
    except json.JSONDecodeError:
        return None, f"not_json status_or_body={body[:300]}"


def fetch_json(path_q):
    url = BASE + path_q
    data, err = curl_get(url)
    return data, err, url


def resolve_symbol(sym):
    candidates = ALT_SYMBOLS.get(sym, [sym])
    last_err = None
    for cand in candidates:
        time.sleep(SLEEP_S)
        data, err, url = fetch_json(f"/premiumIndex?symbol={cand}")
        if isinstance(data, dict) and data.get("markPrice"):
            return cand, data, None
        last_err = err or (str(data)[:200] if data is not None else "no_data")
        if isinstance(data, dict) and data.get("code"):
            last_err = f"code={data.get('code')} msg={data.get('msg')}"
            continue
    return None, None, last_err


def fetch_book(sym):
    time.sleep(SLEEP_S)
    data, err, url = fetch_json(f"/ticker/bookTicker?symbol={sym}")
    return data, err


def fetch_klines(sym, start_ms):
    all_klines = []
    cursor = start_ms
    pages = 0
    while True:
        pages += 1
        time.sleep(SLEEP_S)
        q = f"/klines?symbol={sym}&interval=1m&startTime={cursor}&limit=1500"
        data, err, url = fetch_json(q)
        if err:
            return all_klines, err
        if not isinstance(data, list):
            return all_klines, f"klines_not_list={str(data)[:200]}"
        if not data:
            break
        all_klines.extend(data)
        last_open = int(data[-1][0])
        if len(data) < 1500:
            break
        nxt = last_open + 60_000
        if nxt <= cursor:
            break
        cursor = nxt
        if pages >= 8:
            break
    return all_klines, None


def fmt(x, n=8):
    if x is None:
        return ""
    if isinstance(x, str):
        return x
    s = f"{x:.{n}f}".rstrip("0").rstrip(".")
    return s


def main():
    out_tsv = sys.argv[1] if len(sys.argv) > 1 else "/workspace/paper-mark-2358.tsv"
    fail_path = sys.argv[2] if len(sys.argv) > 2 else "/workspace/paper-mark-2358-failures.txt"
    out_json = sys.argv[3] if len(sys.argv) > 3 else "/workspace/paper-mark-2358.json"
    rows = []
    json_rows = []
    failures = []
    header = [
        "symbol", "side", "mid", "scan", "prop_bst", "mark", "last",
        "paper_pct", "kline_low", "kline_high", "mfe_pct", "mae_pct",
        "hit_10", "hit_2p5", "need_10", "already_alerted", "first_time_10",
    ]
    now = datetime.now(timezone.utc)
    now_bst = now.astimezone(BST)

    prior = {}
    for prior_path in ("/workspace/paper-mark-2224.tsv", "/workspace/paper-mark-2247.tsv", "/workspace/paper-mark-2258.tsv", "/workspace/paper-mark-2316.tsv", "/workspace/paper-mark-2325.tsv", "/workspace/paper-mark-2329.tsv", "/workspace/paper-mark-2333.tsv", "/workspace/paper-mark-2338.tsv", "/workspace/paper-mark-2346.tsv"):
        try:
            with open(prior_path) as pf:
                hdr = pf.readline().rstrip("\n").split("\t")
                for line in pf:
                    cols = line.rstrip("\n").split("\t")
                    if len(cols) < 5:
                        continue
                    rec = dict(zip(hdr, cols))
                    key = (rec.get("symbol"), rec.get("side"), rec.get("mid"))
                    lo = rec.get("kline_low") or rec.get("lo") or ""
                    hi = rec.get("kline_high") or rec.get("hi") or ""
                    try:
                        lo_f = float(lo) if lo else None
                        hi_f = float(hi) if hi else None
                    except ValueError:
                        continue
                    old = prior.get(key, (None, None))
                    plo, phi = old
                    if lo_f is not None:
                        plo = lo_f if plo is None else min(plo, lo_f)
                    if hi_f is not None:
                        phi = hi_f if phi is None else max(phi, hi_f)
                    prior[key] = (plo, phi)
        except FileNotFoundError:
            pass

    for i, (sym, side, mid, scan, prop_bst, start_ms) in enumerate(PROPOSALS, 1):
        print(f"[{i}/{len(PROPOSALS)}] {sym} {side} mid={mid} start={start_ms}", file=sys.stderr, flush=True)
        used_sym, prem, err = resolve_symbol(sym)
        mark = None
        last = None
        k_low = None
        k_high = None
        k_low_bar = None
        k_high_bar = None
        n_bars = 0
        paper_pct = None
        mfe_pct = None
        mae_pct = None
        hit_10 = ""
        hit_2p5 = ""

        if used_sym is None:
            failures.append(f"{sym}: premiumIndex fail: {err}")
            need_10 = 0.90 * mid if side == "SHORT" else 1.10 * mid
            already = "YES" if (sym, side) in ALREADY_ALERTED_10 else "NO"
            rows.append([
                sym, side, fmt(mid), scan, prop_bst, "", "", "",
                "", "", "", "", "", "", fmt(need_10, 10), already, "False",
            ])
            json_rows.append({"symbol": sym, "side": side, "mid": mid, "scan": scan, "prop_bst": prop_bst, "error": err})
            continue

        try:
            mark = float(prem["markPrice"])
        except Exception as e:
            failures.append(f"{sym}: mark parse fail {e} data={prem}")

        book, berr = fetch_book(used_sym)
        if berr or not isinstance(book, dict):
            failures.append(f"{used_sym}: bookTicker fail: {berr or book}")
        else:
            try:
                bid = float(book["bidPrice"])
                ask = float(book["askPrice"])
                last = (bid + ask) / 2.0
            except Exception as e:
                failures.append(f"{used_sym}: book parse fail {e} data={book}")

        klines, kerr = fetch_klines(used_sym, start_ms)
        if kerr:
            failures.append(f"{used_sym}: klines fail: {kerr}")
        if klines:
            try:
                n_bars = len(klines)
                low_bar = min(klines, key=lambda k: float(k[3]))
                high_bar = max(klines, key=lambda k: float(k[2]))
                k_low = float(low_bar[3])
                k_high = float(high_bar[2])
                k_low_bar = ms_to_bst(int(low_bar[0]))
                k_high_bar = ms_to_bst(int(high_bar[0]))
                pk = prior.get((sym, side, str(mid))) or prior.get((sym, side, fmt(mid)))
                if pk:
                    plo, phi = pk
                    if plo is not None:
                        k_low = min(k_low, plo)
                    if phi is not None:
                        k_high = max(k_high, phi)
            except Exception as e:
                failures.append(f"{used_sym}: kline parse fail {e}")
                k_low = None
                k_high = None
        elif not kerr:
            failures.append(f"{used_sym}: klines empty since {start_ms}")

        if mark is not None:
            if side == "SHORT":
                paper_pct = (mid - mark) / mid * 100.0
            else:
                paper_pct = (mark - mid) / mid * 100.0

        if k_low is not None and k_high is not None:
            if side == "SHORT":
                mfe_pct = (mid - k_low) / mid * 100.0
                mae_pct = (mid - k_high) / mid * 100.0
                hit_10 = "YES" if k_low <= 0.90 * mid else "NO"
                hit_2p5 = "YES" if k_low <= 0.975 * mid else "NO"
            else:
                mfe_pct = (k_high - mid) / mid * 100.0
                mae_pct = (k_low - mid) / mid * 100.0
                hit_10 = "YES" if k_high >= 1.10 * mid else "NO"
                hit_2p5 = "YES" if k_high >= 1.025 * mid else "NO"

        need_10 = 0.90 * mid if side == "SHORT" else 1.10 * mid
        out_sym = used_sym if used_sym == sym else f"{sym}->{used_sym}"
        first_10 = hit_10 == "YES" and (sym, side) not in ALREADY_ALERTED_10
        already = "YES" if (sym, side) in ALREADY_ALERTED_10 else "NO"
        rows.append([
            out_sym, side, fmt(mid), scan, prop_bst,
            fmt(mark, 10), fmt(last, 10),
            fmt(paper_pct, 6) if paper_pct is not None else "",
            fmt(k_low, 10), fmt(k_high, 10),
            fmt(mfe_pct, 6) if mfe_pct is not None else "",
            fmt(mae_pct, 6) if mae_pct is not None else "",
            hit_10, hit_2p5, fmt(need_10, 10), already, str(first_10),
        ])
        json_rows.append({
            "symbol": out_sym,
            "side": side,
            "mid": mid,
            "scan": scan,
            "prop_bst": prop_bst,
            "prop_utc_ms": start_ms,
            "mark": mark,
            "last": last,
            "paper_pct": paper_pct,
            "kline_low": k_low,
            "kline_high": k_high,
            "kline_low_bar_bst": k_low_bar,
            "kline_high_bar_bst": k_high_bar,
            "n_bars": n_bars,
            "mfe_pct": mfe_pct,
            "mae_pct": mae_pct,
            "hit_10": hit_10,
            "hit_2p5": hit_2p5,
            "need_10": need_10,
            "first_time_10": first_10,
        })
        extra = f" resolved={used_sym}" if used_sym != sym else ""
        print(
            f"  mark={mark} last={last} low={k_low} high={k_high} "
            f"paper={paper_pct} mfe={mfe_pct} mae={mae_pct} hit10={hit_10} hit2p5={hit_2p5} first10={first_10}{extra}",
            file=sys.stderr, flush=True,
        )

    with open(out_tsv, "w") as f:
        f.write("\t".join(header) + "\n")
        for r in rows:
            f.write("\t".join(r) + "\n")
    with open(fail_path, "w") as f:
        if failures:
            f.write("\n".join(failures) + "\n")
        else:
            f.write("NONE\n")
    payload = {
        "fetched_at_utc": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "fetched_at_bst": now_bst.strftime("%Y-%m-%d %H:%M:%S BST"),
        "endpoint_used": BASE,
        "unsigned": True,
        "api_keys": False,
        "mac_used": False,
        "reason": "Box www.binance.com/fapi/v1 public unsigned only; no Mac; no keys/cookies; no orders.",
        "already_alerted_10": ["CYSUSDT SHORT", "OPUSDT LONG"],
        "baseline_tsv": "/workspace/paper-mark-2346.tsv",
        "new_proposal_since_2149": None,
        "last_noted_proposal": {
            "symbol": "XAUUSDT",
            "side": "LONG",
            "mid": 4336.975,
            "scan_id": "2149",
            "proposal_bst": "2026-09-01 21:52:00",
            "paper_10_level": 4770.6725,
            "note": "Already noted. Post-2149 still SILENCE/flag_only only through ~23:42 BST (2157 SILENCE; 2232 SILENCE; 2240 PLTR LONG flag_only; 2256/2312 AAVE SHORT flag_only; 2324 ASTER LONG flag_only; 2340 SILENCE). Aug31 folders 2213/2224/2238 are stale mtimes, not new Sep1 publishes. No new ONE_PICK/SECOND-CANDIDATE since XAU 2149.",
        },
        "trades_md_new_close_after_2028_bst": False,
        "trades_md_note": "No newer CLOSE after BCH/APT iOS 20:28. OPEN rows only after that: CRCLUSDT LONG 1.36 @ 89.17 at 21:48:25 BST; XAUUSDT LONG 0.028 @ 4335.80 at 22:10:46 BST (5% second). Book two-live, no third.",
        "book": "TWO-LIVE CRCLUSDT LONG + XAUUSDT LONG (desk fills); not paper fills",
        "failures": failures,
        "rows": json_rows,
    }
    with open(out_json, "w") as f:
        json.dump(payload, f, indent=2)
    first10 = [r for r in json_rows if r.get("first_time_10")]
    print(f"wrote {out_tsv} rows={len(rows)} failures={len(failures)} first_time_10={len(first10)}", file=sys.stderr)
    for r in first10:
        print(f"FIRST10 {r['symbol']} {r['side']} mfe={r['mfe_pct']} need={r['need_10']} low={r['kline_low']} high={r['kline_high']}", file=sys.stderr)
    # closest unalerted
    unalerted = [r for r in json_rows if r.get("hit_10") == "NO" and r.get("mfe_pct") is not None]
    unalerted.sort(key=lambda r: r["mfe_pct"], reverse=True)
    print("closest_unalerted:", file=sys.stderr)
    for r in unalerted[:5]:
        print(f"  {r['symbol']} {r['side']} MFE {r['mfe_pct']:.3f}% need={r['need_10']} low={r['kline_low']} high={r['kline_high']}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
