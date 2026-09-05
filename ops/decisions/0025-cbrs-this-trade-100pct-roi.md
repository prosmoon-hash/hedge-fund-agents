# 0025 — CBRS this-trade close at +100% ROI

Date: 2026-08-31
Related: [0007](./0007-exit-up-10-one-open-trade.md), [0011](./0011-hold-past-plus10-if-scout-and-critic-agree.md), [0006](./0006-ship-only-execution-cysusdt-not-a-fill.md), [0022](./0022-second-position-needs-approval.md)
Supersedes: —

## Chose
This-trade exception only, for the already-live CBRSUSDT LONG 3.49 (20x cross, entry 183.8969). Close at +100% ROI on the 20x position: mark/last ≥ 193.0918, or uPNL ≥ this position’s initial margin. Ignore 367.7938. Do not close this position at +10% coin (202.29). No exchange take-profit. 0011 HOLD applies only after that +100% ROI print, then close still above 193.0918 when HOLD breaks. Standing +10% close (0007) remains for every other name. CBRS is not a Market Analysis Agent SOUND fill and stays out of `TRADES.md` until Trading desk reports an execution. Over the 10% cap (~32 USDT margin vs ~13); do not add size; a second still needs Operator approval (0022). Cap not lifted (0020 / 0023). Never withdraw. 0001–0024 not rewritten.

## Why
Board Done at 17:50 BST 31 Aug 2026 (Trading desk). STATUS at 18:24 BST locked the numbers: +100% means 100% ROI at 20x (about +5% coin), not a 100% coin move and not the usual +10% coin take-profit.

## Rejected
- Closing this CBRS at +10% coin (202.29)
- Treating 367.7938 (2× entry) as the target
- Attaching an exchange take-profit
- Logging CBRS as a SOUND fill in `TRADES.md`
- Lifting the 10% cap because this position is oversized
- Adding size or auto-opening a second
- Rewriting 0007 or 0011 (standing rules stay; this is this-trade only)
- Applying +100% ROI close to any other name

## Unsure
- Whether Trading desk will report a close at 193.0918 as a fill for `TRADES.md` (CBRS was not a SOUND open; log only on a reported execution)
