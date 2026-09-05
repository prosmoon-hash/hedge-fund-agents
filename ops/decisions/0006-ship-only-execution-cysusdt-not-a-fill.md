# 0006 — Ship is the only executor; CYSUSDT short is not a fill

Date: 2026-08-31
Related: [0005](./0005-trades-log-proposals-only.md), [0003](./0003-no-merge-deploy-or-scope-change.md)
Supersedes: [0005](./0005-trades-log-proposals-only.md)

## Chose
Ship (`58ae82b2-544f-4093-9833-1faeb0792b66`) is the only agent allowed to execute. Max 10% of futures-account funds committed at a time. Ledger logs fills and gains in Ops `TRADES.md` only when Ship reports an execution. The CYSUSDT short was skipped; it is not a fill and is recorded under Skipped, not Fills. Still invent nothing. Still no withdrawals. Ledger still never places orders.

## Why
Chief assigned Ship as the sole executor. 0005 said nobody executes until Operator confirms a fill; that source-of-truth is now Ship's reported fills. Treating a skip as a fill would invent an execution.

## Rejected
- Logging the CYSUSDT short as a fill
- Scout or Ledger placing orders
- Inventing P&L from a skipped proposal

## Unsure
- Whether "10% committed" is notional or margin
- How Ship will hand Ledger a fill (direct message vs board)
