#!/usr/bin/env python3
"""Write RESULT.json / SUMMARY.txt for scan 2312. Proposals/flags only. Never orders/withdrawals."""
import json
from datetime import datetime, timezone, timedelta

base = "/workspace/binance-scan-2340"
BST = timezone(timedelta(hours=1))
now = datetime.now(BST)
now_utc = datetime.now(timezone.utc)

scores = json.load(open(f"{base}/scores.json"))
evals = json.load(open(f"{base}/recheck/evals.json"))
live_holds = json.load(open(f"{base}/recheck/live_holds.json"))
fetch_log = json.load(open(f"{base}/fetch_books_log.json"))
univ = json.load(open(f"{base}/universe.json"))

aligned_fp = [r for r in scores if r.get("aligned")]
sound = [e for e in evals if e.get("proposal_check", {}).get("verdict") == "sound"]

def rank_key(e):
    i05 = abs((e.get("i05") or 0) / 100)
    tb = e.get("taker15")
    t05 = e.get("t05") or 0
    if tb is None:
        return 0
    return i05 * abs(tb / 100 - 0.5) * t05

sound_sorted = sorted(sound, key=rank_key, reverse=True)

crcl = live_holds.get("CRCLUSDT", {})
xau = live_holds.get("XAUUSDT", {})

def live_block(h):
    return {
        "symbol": h.get("symbol"),
        "side": h.get("side"),
        "entry": h.get("entry"),
        "size": h.get("size"),
        "order": h.get("order"),
        "leverage": h.get("leverage"),
        "margin_note": h.get("margin_note"),
        "mark": h.get("mark"),
        "last": h.get("last"),
        "mid": h.get("mid"),
        "i05": h.get("i05"),
        "i1": h.get("i1"),
        "tb15": h.get("tb15"),
        "r5": h.get("r5"),
        "t05": h.get("t05"),
        "spread_bps": h.get("spread_bps"),
        "roi20x": h.get("roi20x"),
        "ROI20x_pct": h.get("roi20x"),
        "close_px": h.get("close_px"),
        "close_target": h.get("close_px"),
        "dist_to_close": h.get("dist_to_close"),
        "at_close": h.get("at_close"),
        "hold_gates": h.get("hold_gates"),
        "hold": h.get("hold"),
        "status": h.get("status"),
        "action_hint": h.get("action_hint"),
    }

live = {
    "crcl": live_block(crcl),
    "xau": live_block(xau),
    "two_open": True,
    "no_third": True,
    "combined_cap_note": "15% (10% first + 5% second); both currently 5%",
}

# HOLD/CLOSE only after +50% print
hold_overall = "none"
action = "SILENCE"
wake = False
wake_why = None
candidate = None

crcl_at = bool(crcl.get("at_close"))
xau_at = bool(xau.get("at_close"))
crcl_hint = crcl.get("action_hint")
xau_hint = xau.get("action_hint")

if crcl_hint == "CLOSE_PING" or xau_hint == "CLOSE_PING":
    action = "CLOSE_PING"
    hold_overall = "none"
    wake = True
    names = []
    if crcl_hint == "CLOSE_PING":
        names.append("CRCLUSDT")
    if xau_hint == "CLOSE_PING":
        names.append("XAUUSDT")
    wake_why = "AT_CLOSE_GATES_FAIL " + "+".join(names)
elif crcl_hint == "HOLD" or xau_hint == "HOLD":
    action = "HOLD_CALL"
    hold_overall = "HOLD"
    wake = True
    names = []
    if crcl_hint == "HOLD":
        names.append("CRCLUSDT")
    if xau_hint == "HOLD":
        names.append("XAUUSDT")
    wake_why = "AT_CLOSE_HOLD " + "+".join(names)

# Flag-only candidate: never openable while two live. Stay quiet unless HOLD/CLOSE.
# Prior scan 2240 FLAG'd PLTR; this run stays silent on flags (routine: stay quiet if no edge and no +50% hold/close).
if sound_sorted:
    e = sound_sorted[0]
    candidate = {
        "symbol": e["symbol"],
        "side": (e.get("side") or "").upper(),
        "mid": e.get("mid"),
        "mark": e.get("mark"),
        "last": e.get("last"),
        "i05": e.get("i05"),
        "i1": e.get("i1"),
        "tb15": e.get("taker15"),
        "r5": e.get("r5"),
        "t05": e.get("t05"),
        "spread_bps": e.get("spread_bps"),
        "qvolM": e.get("qvolM"),
        "pct24": e.get("pct24"),
        "fund": e.get("fund"),
        "contractType": e.get("contractType"),
        "session": e.get("session"),
        "origin": e.get("origin"),
        "aligned_strict": e.get("aligned_strict"),
        "aligned_soft": e.get("aligned_soft"),
        "wall_note": e.get("wall_note"),
        "spoof": e.get("spoof"),
        "ta": e.get("ta"),
        "spot": e.get("spot"),
        "cmc": e.get("cmc"),
        "proposal_check": e.get("proposal_check"),
        "flag_only": True,
        "not_openable": True,
        "why_flag_only": "TWO OPEN (CRCL 5% + XAU 5%); combined cap 15% used; no third without new ask",
        "note": "FLAG only — Research never places; do not send to Trading desk",
    }
    if action == "SILENCE":
        action = "FLAG"  # two-open FLAG_ONLY; do not wake parent

post_recheck_sound = []
for e in sound_sorted:
    post_recheck_sound.append({
        "symbol": e["symbol"],
        "side": e.get("side"),
        "origin": e.get("origin"),
        "mid": e.get("mid"),
        "i05": e.get("i05"),
        "i1": e.get("i1"),
        "taker15": e.get("taker15"),
        "r5": e.get("r5"),
        "t05": e.get("t05"),
        "spread_bps": e.get("spread_bps"),
        "qvolM": e.get("qvolM"),
        "pct24": e.get("pct24"),
        "contractType": e.get("contractType"),
        "session": e.get("session"),
        "proposal_check": e.get("proposal_check"),
        "ta_vs": (e.get("ta") or {}).get("vs_book"),
        "ta_why": (e.get("ta") or {}).get("vs_book_why"),
        "flag_only": True,
        "not_openable": True,
    })

recheck_detail = []
for e in evals:
    recheck_detail.append({
        "symbol": e.get("symbol"),
        "origin": e.get("origin"),
        "first_side": e.get("first_side"),
        "aligned": e.get("aligned"),
        "side": e.get("side"),
        "fail": e.get("fail"),
        "proposal_check": e.get("proposal_check"),
        "mid": e.get("mid"),
        "i05": e.get("i05"),
        "i1": e.get("i1"),
        "taker15": e.get("taker15"),
        "r5": e.get("r5"),
        "t05": e.get("t05"),
        "spread_bps": e.get("spread_bps"),
        "ta_vs": (e.get("ta") or {}).get("vs_book"),
        "ta_why": (e.get("ta") or {}).get("vs_book_why"),
        "spot_status": (e.get("spot") or {}).get("status"),
        "cmc_status": (e.get("cmc") or {}).get("status"),
        "session": e.get("session"),
        "contractType": e.get("contractType"),
        "pct24": e.get("pct24"),
        "qvolM": e.get("qvolM"),
    })

near_misses = []
for r in scores:
    if r.get("aligned"):
        continue
    if r.get("symbol") in ("CRCLUSDT", "XAUUSDT"):
        continue
    if r.get("thin") or r.get("wide") or r.get("spoof") or r.get("extreme24"):
        continue
    i05 = abs(r.get("i05") or 0)
    t05 = r.get("t05") or 0
    if i05 < 25.0 or t05 < 150000:
        continue
    if not (r.get("book_long") or r.get("book_short")):
        continue
    near_misses.append({
        "symbol": r["symbol"],
        "side": r.get("side"),
        "i05": r.get("i05"),
        "i1": r.get("i1"),
        "tb15": r.get("taker15"),
        "r5": r.get("r5"),
        "t05": r.get("t05"),
        "spread_bps": r.get("spread_bps"),
        "qvolM": r.get("qvolM"),
        "pct24": r.get("pct24"),
        "contractType": r.get("contractType"),
        "session": r.get("session"),
        "fail": r.get("fail"),
        "book_long": r.get("book_long"),
        "book_short": r.get("book_short"),
    })
near_misses.sort(key=lambda r: (-abs(r.get("i05") or 0), -(r.get("t05") or 0)))
near_misses = near_misses[:8]

first_pass_aligned = []
for r in aligned_fp:
    if r["symbol"] in ("CRCLUSDT", "XAUUSDT"):
        continue
    first_pass_aligned.append({
        "symbol": r["symbol"],
        "side": r.get("side"),
        "i05": r.get("i05"),
        "i1": r.get("i1"),
        "tb15": r.get("taker15"),
        "r5": r.get("r5"),
        "t05": r.get("t05"),
        "spread_bps": r.get("spread_bps"),
        "qvolM": r.get("qvolM"),
        "pct24": r.get("pct24"),
        "contractType": r.get("contractType"),
        "session": r.get("session"),
    })

result = {
    "scan_id": 2340,
    "time_bst": now.strftime("%Y-%m-%d %H:%M BST"),
    "timestamp_bst": now.strftime("%Y-%m-%d %H:%M BST"),
    "time_utc": now_utc.strftime("%Y-%m-%d %H:%M UTC"),
    "time_bst_iso": now.isoformat(),
    "live": live,
    "live_list": [live["crcl"], live["xau"]],
    "HOLD": hold_overall,
    "action": action,
    "candidate": candidate,
    "first_pass_aligned": first_pass_aligned,
    "first_pass_aligned_n": len(first_pass_aligned),
    "post_recheck_sound": post_recheck_sound,
    "post_recheck_sound_n": len(post_recheck_sound),
    "recheck_detail": recheck_detail,
    "near_misses": near_misses,
    "stale_priors_not_reused": [
        "SKR 2129 / CRCL 2136 MA SKIP / XAU 2149 MA SKIP stale as Research/MAD opens",
        "XAUUSDT force_stale_2149 skipped — now live second open",
        "Scan 2256 SILENCE ~23:07 BST (AAVE SHORT flag) not recycled",
        "Scan 2240 PLTR/LIT/AXTI flags not recycled",
        "No CYS/SUI/TRUMP/UAI backfill",
    ],
    "independent_recheck": True,
    "independent_recheck_bst": now.strftime("%Y-%m-%d %H:%M BST"),
    "candidate_overridden": None,
    "hard_skips": ["CYSUSDT", "SUIUSDT", "TRUMPUSDT", "UAIUSDT"],
    "screened": len(univ),
    "scored": len(scores),
    "screened_n": len(univ),
    "scored_n": len(scores),
    "fetch_failures": fetch_log.get("fails") or [],
    "data_path": "www.binance.com/fapi",
    "need_mac_fallback": False,
    "orders_placed": False,
    "withdrawals": False,
    "wake_parent_needed": wake,
    "wake_why": wake_why,
    "notes": [
        "TWO OPEN: CRCLUSDT LONG + XAUUSDT LONG — flag other names only; no third",
        "CLOSE targets +50% ROI on 20x: CRCL>=91.39925 XAU>=4444.195",
        "HOLD only after +50% print with long gates (bid>ask 0.5%&1%, tb15>50%, r5>0)",
        "Research Desk proposals/flags only; never places or withdraws",
        f"US cash off-hours at scan time (~{now.strftime('%H:%M')} BST)",
        f"post_recheck_sound={len(post_recheck_sound)} flag-only (not openable)",
        "FLAG_ONLY while two open; wake only on HOLD_CALL/CLOSE_PING",
    ],
}

json.dump(result, open(f"{base}/RESULT.json", "w"), indent=2)

cand_s = "none"
if candidate:
    cand_s = f"{candidate['symbol']} {candidate['side']} @ {candidate['mid']} (flag_only)"
fp_s = [(r['symbol'], r['side']) for r in first_pass_aligned]
prs = [(e['symbol'], e.get('side'), (e.get('proposal_check') or {}).get('verdict')) for e in post_recheck_sound]
summary = (
    f"Scan 2340 ({now.strftime('%Y-%m-%d %H:%M BST')}): action={action}, wake_parent_needed={wake}"
    + (f" ({wake_why})" if wake_why else "")
    + f". TWO OPEN — CRCLUSDT LONG 1.36 @ 89.17 (order 1099123376): mark={crcl.get('mark')} last={crcl.get('last')} mid={crcl.get('mid')} ROI20x={crcl.get('roi20x')}% hold={crcl.get('hold')} status={crcl.get('status')} close≥91.39925;"
    + f" XAUUSDT LONG 0.028 @ 4335.80 (order 13906003826): mark={xau.get('mark')} last={xau.get('last')} mid={xau.get('mid')} ROI20x={xau.get('roi20x')}% hold={xau.get('hold')} status={xau.get('status')} close≥4444.195."
    + f" first_pass_aligned={len(first_pass_aligned)} {fp_s}; post_recheck_sound={len(post_recheck_sound)} {prs}; candidate={cand_s}."
    + f" screened={len(univ)} scored={len(scores)}; data_path=www.binance.com/fapi; orders_placed=false; withdrawals=false. No third."
)
open(f"{base}/SUMMARY.txt", "w").write(summary + "\n")
print(summary)
print("wake_parent_needed", wake, wake_why)
print("wrote RESULT.json")
