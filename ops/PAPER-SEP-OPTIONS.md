# Paper book: 10 Sep 2026 weeklies (not live)

Opened: 2026-09-01 ~20:14 BST by Hedge Fund Manager on Operator instruction.
Owner: Research Desk (expiry mark + assignment). Not Trading desk. Not Binance. Never withdraw.
Size: 1 standard contract each (×100). Long the listed option (buy).
Fill source: Yahoo Finance quotes from `/workspace/sep-2026-options-summary.md` evening 1 Sep 2026. Investing.com was 429.
Fill rule: last if last>0 and last ≤ ask; else ask. CIFR last 0.68 was above ask 0.62 → paper 0.62.

Expiry: Friday 2026-09-04 US listed-equity options close (typically 16:00 ET / 21:00 BST).
Assignment (paper only):
- Call ITM if official close > strike → long 100 shares at strike.
- Put ITM if official close < strike → short 100 shares at strike.
- OTM / at-the-money per OCC (usually close strictly beyond strike) → expire worthless.
P&L at expiry (if not assigned into a stock book): intrinsic×100 − debit. If assigned, also log stock entry at strike and option debit.

GLNK 10p and RXT 3c were NOT included (thin / wide spread).

| # | ticker | side | strike | expiry | spot at open | fill | debit USDT/$ | bid/ask at open | notes |
|---|--------|------|--------|--------|--------------|------|--------------|-----------------|-------|
| 1 | QBTS | PUT | 16.5 | 2026-09-04 | 16.465 | 0.47 | 47 | 0.45 / 0.49 | 0.21% ITM |
| 2 | ONDS | CALL | 7 | 2026-09-04 | 7.025 | 0.20 | 20 | 0.21 / 0.22 | last 0.20 vs ask 0.22 |
| 3 | SOFI | CALL | 17 | 2026-09-04 | 17.085 | 0.37 | 37 | 0.36 / 0.37 | 0.50% ITM |
| 4 | LAC | PUT | 3 | 2026-09-04 | 2.985 | 0.08 | 8 | 0.07 / 0.10 | 0.50% ITM |
| 5 | BMNR | PUT | 23.5 | 2026-09-04 | 23.295 | 0.85 | 85 | 0.81 / 0.84 | last 0.85 vs ask 0.84 |
| 6 | CIFR | CALL | 14.5 | 2026-09-04 | 14.645 | 0.62 | 62 | 0.57 / 0.62 | last 0.68 ignored (through ask) |
| 7 | EOSE | CALL | 3 | 2026-09-04 | 3.035 | 0.14 | 14 | 0.12 / 0.15 | 1.15% ITM |
| 8 | SMR | CALL | 9 | 2026-09-04 | 9.105 | 0.36 | 36 | 0.32 / 0.36 | 1.15% ITM |
| 9 | WULF | CALL | 14.5 | 2026-09-04 | 14.685 | 0.53 | 53 | 0.53 / 0.57 | 1.26% ITM |
| 10 | OPEN | CALL | 3 | 2026-09-04 | 3.045 | 0.10 | 10 | 0.08 / 0.09 | last 0.10 slightly through ask |

Total debit: **$372** (10 contracts).

Do not invent marks. Append daily marks and the Friday expiry/assignment report below.

## Marks

### 2026-09-01 ~21:15 BST (Yahoo last/bid/ask)

- Source: Yahoo Finance `quoteResponse` OCC option symbols + equity underlyings (`/workspace/yahoo_opts/opts_batch.json`, `und_batch.json`).
- Market: US session POST; underlying regularMarketTime ~21:00 BST (16:00 ET close). Fetch mtime 2026-09-01T21:15:28.762999+01:00.
- Paper only. No orders. No withdrawals. Not Binance.
- Mark for MTM column = option last when last>0; else mid(bid,ask). MTM = mark×100 − debit.
- Missing: none (10/10).

| # | ticker | side | strike | spot | opt last | bid | ask | mark | debit $ | MTM $ | notes |
|---|--------|------|--------|------|----------|-----|-----|------|---------|-------|-------|
| 1 | QBTS | PUT | 16.5 | 16.54 | 0.4 | 0.39 | 0.48 | 0.4 | 47 | -7.00 | spot slightly above strike (OTM put) |
| 2 | ONDS | CALL | 7.0 | 7.04 | 0.22 | 0.2 | 0.22 | 0.22 | 20 | +2.00 |  |
| 3 | SOFI | CALL | 17.0 | 17.05 | 0.36 | 0.35 | 0.36 | 0.36 | 37 | -1.00 |  |
| 4 | LAC | PUT | 3.0 | 2.97 | 0.08 | 0.07 | 0.08 | 0.08 | 8 | +0.00 |  |
| 5 | BMNR | PUT | 23.5 | 23.37 | 0.78 | 0.75 | 0.77 | 0.78 | 85 | -7.00 | last 0.78 through ask 0.77 (reported raw) |
| 6 | CIFR | CALL | 14.5 | 14.61 | 0.56 | 0.5 | 0.61 | 0.56 | 62 | -6.00 |  |
| 7 | EOSE | CALL | 3.0 | 3.04 | 0.14 | 0.11 | 0.16 | 0.14 | 14 | +0.00 |  |
| 8 | SMR | CALL | 9.0 | 9.21 | 0.36 | 0.34 | 0.41 | 0.36 | 36 | +0.00 |  |
| 9 | WULF | CALL | 14.5 | 14.65 | 0.59 | 0.52 | 0.61 | 0.59 | 53 | +6.00 |  |
| 10 | OPEN | CALL | 3.0 | 3.04 | 0.1 | 0.09 | 0.1 | 0.1 | 10 | +0.00 |  |

Total debit $372. Mark-to-market vs debit sum ≈ **-13.00** (last-based marks).

Expiry pass still due after Friday 2026-09-04 US listed close (~16:00 ET / 21:00 BST).


## Expiry / assignment (due after 2026-09-04 US close)

(pending Research Desk)
