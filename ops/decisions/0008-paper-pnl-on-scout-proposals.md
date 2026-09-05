# 0008 — Paper-mark Scout proposals, even if unfilled

Date: 2026-08-31
Related: [0007](./0007-exit-up-10-one-open-trade.md), [0005](./0005-trades-log-proposals-only.md)
Supersedes: —

## Chose
Verification Agent marks every Scout Binance USDT-M proposal to market from Scout's stated mid, whether or not Ship filled it. Paper P&L is vs live mark (public fapi on operator workstation). Also track MFE/MAE since the proposal and whether price would have hit the desk +10% exit. Report to Hedge Fund Manager on new proposals, sign flips, a hypothetical +10% hit, or a move of about 2%+. Do not write paper P&L into TRADES.md (that file is fills only).

## Why
Operator asked for real-time profitability of proposed trades, executed or not. Using Scout's mid keeps the score on the call that was actually made. Critic's later mid is a different timestamp. Ledger's TRADES.md stays fills-only (0005, 0007).

## Rejected
- Scoring from Critic's re-check mid instead of Scout's proposal mid
- Treating paper P&L as a fill or writing it into TRADES.md
- Pinging Hedge Fund Manager every 5 minutes when nothing moved

## Unsure
- Horizon to stop marking a dead proposal (same session, until +10% or stop, or end of day)
