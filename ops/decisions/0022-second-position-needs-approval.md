# 0022 — Second position only with Operator approval

Date: 2026-08-31
Related: [0007](./0007-exit-up-10-one-open-trade.md), [0020](./0020-10pct-cap-unchanged.md), [0011](./0011-hold-past-plus10-if-scout-and-critic-agree.md)
Supersedes: [0007](./0007-exit-up-10-one-open-trade.md)

## Chose
Default remains one live Binance USDT-M trade. Close at +10% unless 0011 HOLD. If Research Agent identifies another trade while a position is already open, Hedge Fund Manager requests Operator approval before Trading desk may open a second. Trading desk never auto-opens a second. Research still proposes the second name (label SECOND-CANDIDATE) and still sends it to Market Analysis Agent; it is not a live order. Combined size still ≤10% of futures funds (~12.87 USDT) unless that approval says otherwise. Any approved second is still 20x cross. Never withdraw.

## Why
Operator locked this at 14:46 BST 31 Aug 2026: going forward, request approval to take a second position rather than refuse it outright.

## Rejected
- Auto-opening a second
- Silent queue-behind-close with no ask
- Raising the 10% cap by default to make room for two

## Unsure
- Whether an approved second may exceed leftover room under the 10% cap; default no unless that approval says so
