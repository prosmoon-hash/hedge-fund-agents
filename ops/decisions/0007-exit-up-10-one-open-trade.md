# 0007 — Close at +10%; only one trade open

Date: 2026-08-31
Related: [0006](./0006-ship-only-execution-cysusdt-not-a-fill.md), [0005](./0005-trades-log-proposals-only.md)
Supersedes: —

## Chose
Execution Agent (Ship) will close a fill once it is up 10%, and may only have one trade open. Trading Journal logs those closes and the realized gain in Ops `TRADES.md` when Ship reports them. The 10% take-profit is not the same 10% as max funds committed (0006). Still invent nothing. Still no withdrawals. Still no orders from this agent.

## Why
Hedge Fund Manager assigned the exit rule. Realized P&L exists at close, not at an open mark. One open trade keeps the book simple and matches the 10% commitment cap.

## Rejected
- Logging an open position's mark as realized gain before Ship closes it
- Treating a +10% move we did not hear from Ship as a close
- Multiple concurrent opens

## Unsure
- Whether +10% is on price, notional, or margin
- Whether there is a stop besides the take-profit
