# 0030 — Live close is +50% ROI on 20x; HOLD only after that print

Date: 2026-09-01
Related: [0007](./0007-exit-up-10-one-open-trade.md), [0011](./0011-hold-past-plus10-if-scout-and-critic-agree.md), [0026](./0026-paper-plus10-vs-live-50pct-roi.md), [0022](./0022-second-position-needs-approval.md)
Supersedes: 0007, 0011

## Chose
Every live Binance USDT-M fill closes at +50% ROI on 20x (a 2.5% price move), not +10%. HOLD only after that print: if Research Agent and Market Analysis Agent both call HOLD on book stats (long: bid notional > ask at 0.5% and 1%, 15m taker-buy share > 50%, 5m return still positive; short: invert), Trading desk holds; when any of those fails, close still above +50% ROI. Live BCHUSDT SHORT close is mark/last ≤ 240.5060. Paper miss-alert stays +10% coin from proposed mid (0026). 0022's second-position rule is unchanged. Not a fill. No orders. Never withdraw.

## Why
Operator lock ~17:41–17:42 BST 1 Sep 2026, on the board as standing live close and already treated as standing in 0026's Unsure. 0007's +10% default and 0011's hold-past-+10% floor are the old exit. This note is the current exit.

## Rejected
- Keeping +10% as the live take-profit (0007)
- HOLD before a +50% ROI print (0011's old floor)
- Changing the paper miss-alert to +50% ROI / 2.5% (0026)
- Rewriting 0022 (second still needs its own rule; do not restamp it)

## Unsure
- Whether 0022's restated “close at +10%” line is treated as stale without a rewrite (chose: yes, this note is the close rule; 0022 stays for second-position approval)
