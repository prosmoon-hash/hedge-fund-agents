# 0032 — Dual-book scan: futures fail-closed primary, spot second

Date: 2026-09-01
Related: [0021](./0021-scan-every-3-minutes.md), [0015](./0015-cmc-into-research.md), [0005](./0005-trades-log-proposals-only.md)
Supersedes: —

## Chose
Research Agent samples both Binance futures and spot books. Futures is fail-closed primary. Spot is a second sample only. Execution stays USDT-M fapi; Trading desk does not place spot orders. Scan cadence, one-proposal, book-then-flow-then-TA-then-CMC, and the withdrawal ban are unchanged.

## Why
Board marked dual-book done at 21:16 BST 31 Aug 2026. Morning related-decisions did not capture it. Futures remaining fail-closed keeps a thin futures book from becoming a live name just because spot looks fine.

## Rejected
- Making spot the primary book
- Dropping the spot sample (futures-only)
- Executing on spot
- Treating a spot-only print as a fill

## Unsure
- Whether a name that fail-closes on futures can still be proposed from a strong spot book (chose: no; futures fail-closed is primary)
