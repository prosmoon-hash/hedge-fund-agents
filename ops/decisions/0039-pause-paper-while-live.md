# 0039 — Pause Verification paper loops while any live is open

Date: 2026-09-05
Related: [0010](./0010-report-only-on-plus10.md), [0009](./0009-paper-mark-24-7.md)
Supersedes: —

## Chose
While any Binance USDT-M position is open, Verification Desk pauses the Research proposal paper P&L cron and other proposal process loops. Only Trading Desk monitors/closes. Resume when Trading Desk wakes Verification Desk (book flat or a seat frees so scanning may resume). Existing paper marks on already-logged proposals stay quiet. Never orders. Never withdraw.

## Why
Hedge Fund Manager relayed a Operator rule ~13:43 BST 5 Sep 2026. Book was TWO LIVE (GIGGLE+LINK). Research scan cadence when FLAT becomes every 10 minutes (separate desk rule); Verification follows the pause.

## Rejected
- Keeping 5-min paper-mark while lives are open
- Verification Desk monitoring live positions itself

## Unsure
- Whether evening 18:00 backtest and weekday 14:25 re-vet also pause while live (chose: pause the 5-min paper loop for sure; evening/re-vet stay armed unless HFM says otherwise — they are daily digests, not proposal process loops)
