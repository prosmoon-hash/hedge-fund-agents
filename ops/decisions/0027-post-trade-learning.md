# 0027 — Verification Desk owns post-trade learning

Date: 2026-09-01
Related: [0010](./0010-report-only-on-plus10.md), [0018](./0018-evening-untaken-backtest.md), [0026](./0026-paper-plus10-vs-live-50pct-roi.md)
Supersedes: —

## Chose
Verification Desk extracts lessons from TRADES.md fills/closes and the paper book of unused Research proposals, then proposes one concrete strategy change to Hedge Fund Manager. Does not change live rules. Does not ping Trading desk. Cadence: after each logged close, with the 18:00 backtest if a cluster appears, ad-hoc on a large paper win/loss.

First proposal (not applied): if Research one-pick is sound and the book is FLAT, a non-directional MA SKIP should not block a half-size open (5% of funds, 20x cross, live +50% ROI close). Grounded in CYSUSDT short @ 0.9679 SKIP 31 Aug vs CBRS iOS close net −0.8339 USDT.

## Why
Hedge Fund Manager relayed a Operator standing task ~17:59 BST 1 Sep 2026. CYS skip vs +50% ROI close was named as fair game.

## Rejected
- Verification Desk changing live rules itself
- Pinging Trading desk to trade from a lesson
- Repeating the full paper book as a lesson

## Unsure
- Whether MA's CYS SKIP was liquidity, timing, or something else (log only says skipped, not a fill)
