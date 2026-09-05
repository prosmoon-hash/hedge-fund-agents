# Paper TA/SMC secondary gate (Operator lock 5 Sep 2026)

Secondary only. Does NOT replace book+flow. Does NOT live-veto during this window.
Started: 2026-09-05 ~13:34 BST. Window: 7–14 days. Compare due to Hedge Fund Manager after ~7 days (or 14).

## Rules (summary)
- After each book+flow one-pick, score 1H OHLCV from `https://www.binance.com/fapi` klines (not fapi.binance.com). No look-ahead past timestamp t.
- Chart images optional; image failure must not block the scan.
- Patterns: H&S bearish, Double bottom, Bullish flag, Ascending triangle (strict defs from HFM brief).
- ICT/SMC: bullish/bearish FVG, order blocks.
- 1H engine: no setups against 4H/Daily unless H&S or Double Bottom fully confirmed on close; long Price>20EMA>50EMA; short Price<20EMA<50EMA; SL 1.0–1.5×ATR(14); TP opposing liquidity; reject R:R < 1:2; weekend flag Sat 00:00–Sun 20:00 UTC.
- Tags: `TA_PASS` / `TA_FAIL` / `TA_NA` + pattern list, R:R, EMA stack, weekend flag.
- Live path unchanged: still send MAD book+flow names. TA_FAIL must NOT veto live SOUND or block a Operator/MAD-cleared second during paper window.

## Log (append-only)

| scan_id | time BST | symbol | side | mid | book_flow | TA tag | patterns | R:R | EMA stack | weekend | paper +10% coin | paper +50% ROI 20x | notes |
|---------|----------|--------|------|-----|-----------|--------|----------|-----|-----------|---------|-----------------|--------------------|-------|
| 1332 | 2026-09-05 13:33 | LINKUSDT | LONG | 11.7905 | sound | TA_FAIL | bull_FVG; bear_FVG; no TP/R:R | n/a | Price>EMA20>EMA50 | yes |  |  | MAD SOUND first; paper only |
| 1338 | 2026-09-05 13:44 | — | — | — | none/SILENCE | TA_NA | no one-pick | n/a | n/a | yes |  |  | ONE OPEN GIGGLE FAR_FROM_CLOSE; no SOUND second; DELL weak / PUMP+LINK fade |
