# 0016 — TA as a consideration on Research Agent scans

Date: 2026-08-31
Related: [0015](./0015-cmc-into-research.md), [0006](./0006-ship-only-execution-cysusdt-not-a-fill.md), [0007](./0007-exit-up-10-one-open-trade.md), [0011](./0011-hold-past-plus10-if-scout-and-critic-agree.md)
Supersedes: —

## Chose
As of 12:48 BST 31 Aug 2026, Operator added TA as a consideration on Research Agent scans. Weight order: book, then flow, then TA, then CMC. Indicators: 15m RSI14, EMA20/50 vs mid, MACD(12,26,9) histogram sign, 15m swing high/low. TA never overrides a fail-closed book. Trading size, one-open, +10% close, and the withdrawal ban are unchanged. 0001–0015 not rewritten. No fill to log.

## Why
Hedge Fund Manager relayed Operator's direction. TA is extra scan input, ranked below book and flow, so it cannot open a name the book already fail-closed.

## Rejected
- TA overriding a fail-closed book
- Reordering weight so TA or CMC outranks book or flow
- Changing size, one-open, +10% close, or the withdrawal ban
- Treating a TA print as a fill

## Unsure
- Exact RSI/MACD thresholds Research Agent uses to tilt a proposal vs only reporting the values
