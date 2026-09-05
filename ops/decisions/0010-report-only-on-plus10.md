# 0010 — Report paper P&L only on a hypothetical +10% hit

Date: 2026-08-31
Related: [0008](./0008-paper-pnl-on-scout-proposals.md), [0009](./0009-paper-mark-24-7.md), [0007](./0007-exit-up-10-one-open-trade.md)
Supersedes: 0008

## Chose
Keep marking Scout proposals to market 24/7. Do not send another paper-mark report until a proposal would have hit +10% from Scout's proposed mid. Then report immediately to Hedge Fund Manager and Operator: symbol, side, proposal time BST, proposed mid, last, paper P&L, MFE/MAE, and that +10% was hit. New Scout proposals may be noted once, then wait for +10%. Stay quiet on 2% moves and sign flips. Still not fills. Still no orders. Still no withdrawals.

## Why
Hedge Fund Manager relayed a Operator rule. The desk's live exit is +10% (0007); paper-mark reporting should match that threshold instead of ticking on every 2% wiggle.

## Rejected
- Reporting on ~2% moves or sign flips (the 0008 notify set)
- Sending another full book snapshot on request of cadence rather than a +10% event
- Writing paper P&L into TRADES.md

## Unsure
- Whether a name that already printed MFE +1.5% (CYSUSDT short) gets a one-time catch-up if it later tags +10%, or only a first-touch print (chose first-touch: report when it hits)
