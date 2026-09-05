# 0019 — 20x cross on every Trading desk open

Date: 2026-08-31
Related: [0006](./0006-ship-only-execution-cysusdt-not-a-fill.md), [0007](./0007-exit-up-10-one-open-trade.md), [0017](./0017-open-next-sound.md)
Supersedes: —

## Chose
Every Binance USDT-M open by Trading desk is 20x leverage and cross margin. Before placing, Trading desk must set leverage 20 and margin type CROSS on that symbol. Do not inherit the account default (BTC is 50x, ETH is 40x, most names 20x). Crypto and TradFi. Isolated is banned. Other leverages are banned. Size still at most 10% of futures-account funds (~12.87 USDT). One open. Close at +10% unless 0011 HOLD. Never withdraw. No CYS/SUI/TRUMP backfill. Set 20x cross only on the symbol being opened, not on the whole universe.

## Why
Operator locked this at 14:35 BST 31 Aug 2026 after the account was found on exchange defaults (cross, mostly 20x, BTC 50x, ETH 40x) with no desk leverage rule.

## Rejected
- Isolated margin
- Inheriting per-symbol Binance defaults
- Changing the 10% size cap, one-open, +10% close, HOLD, or withdrawal ban
- Pre-setting leverage on every USDT-M symbol

## Unsure
- Whether the 10% cap is notional or initial margin at 20x; left as the existing ~12.87 USDT size figure until Operator says otherwise
