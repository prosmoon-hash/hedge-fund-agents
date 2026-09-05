# 0005 — Ledger logs fills in Ops TRADES.md; proposals-only until confirmed

Date: 2026-08-31
Related: [0001](./0001-decision-notes-live-in-ops.md), [0002](./0002-append-only-supersede.md), [0003](./0003-no-merge-deploy-or-scope-change.md)
Supersedes: —

## Chose
Ledger owns an append-only fill log at Ops `TRADES.md`. Each confirmed fill: time BST, venue (Binance USDT-M unless told otherwise), symbol, side, size, entry, exit or mark, realized P&L, fees if known, source of the fill. The book is proposals-only as of 31 Aug 2026, 10:29 BST, with zero logged fills until Operator confirms a fill or a read-only trade-history source exists. Scout proposes; nobody executes. Never place an order. Never touch withdrawals. Never use API keys or signed-in session cookies. A once-a-day check after Scout's window (21:15 BST, all week) looks for confirmed fills; stay quiet if none.

## Why
Operator assigned this as a standing job, additive to decision notes. Public fapi cannot see account fills, so guessing P&L would be invented data. Append-only matches 0002. Hard ban on withdrawals matches the board.

## Rejected
- Logging Scout proposals as fills (they are not executions)
- Scraping a signed-in Binance session or using API keys
- Polling every 5 minutes (Scout already has that cadence; Ledger's check stays coarse)
- Inventing mark-to-market P&L with no fill

## Unsure
- When the first real fill will exist (Operator confirm, or a read-only history source)
- Whether Friday close should recap P&L from this file
