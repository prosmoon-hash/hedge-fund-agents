# 0011 — Hold past +10% only if Scout and Critic both agree HOLD

Date: 2026-08-31
Related: [0007](./0007-exit-up-10-one-open-trade.md), [0006](./0006-ship-only-execution-cysusdt-not-a-fill.md)
Supersedes: —

## Chose
Default close is still +10% (0007). Exception: if Scout and Critic both agree HOLD on Scout book stats (bid vs ask at 0.5% and 1%, 15m taker-buy share, 5m return), Execution Agent (Ship) may hold past +10%. When that dual HOLD breaks, Ship must still close above +10%. Trading Journal logs that close and the realized gain in `TRADES.md` only when Ship reports it. No fill to log today. Still no orders. Still no withdrawals.

## Why
Hedge Fund Manager assigned the exception. Book stats can justify riding a winner past the default take-profit, but only when both Scout and Critic say HOLD. One-sided HOLD is not enough. Closing still has to be above +10% so the exception cannot turn a winner into a loser versus the 0007 floor.

## Rejected
- Superseding 0007 (the default close at +10% still stands)
- Holding past +10% on Scout-only or Critic-only HOLD
- Logging a paper HOLD or unfilled proposal as a close
- Treating this as a fill

## Unsure
- Who posts the dual HOLD in time for Ship (Scout, Critic, or Hedge Fund Manager)
- Exact HOLD thresholds on those four stats
