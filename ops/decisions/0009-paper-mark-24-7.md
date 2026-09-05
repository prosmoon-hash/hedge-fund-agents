# 0009 — Paper-mark 24/7

Date: 2026-08-31
Related: [0008](./0008-paper-pnl-on-scout-proposals.md)
Supersedes: —

## Chose
Verification Agent paper-marks Scout proposals every 5 minutes around the clock (`2-59/5 * * * *` Europe/London), not only 08:00–21:00 BST.

## Why
Hedge Fund Manager relayed a Operator rule: all agents operate 24/7, no sleep. Crypto prints overnight and existing paper trades can hit +10% or flip sign outside Scout's proposal window.

## Rejected
- Keeping the 08:00–21:00 BST window
- Pinging on every 5-minute tick with no material move

## Unsure
- Whether Scout will also propose outside 08:00–21:00
