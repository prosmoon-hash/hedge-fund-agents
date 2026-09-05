# 0031 — Market Analysis verdict emails stay always on

Date: 2026-09-01
Related: [0014](./0014-24h-verdict-emails.md), [0024](./0024-approval-emails.md), [0018](./0018-evening-untaken-backtest.md)
Supersedes: 0014

## Chose
Communication Agent emails every Market Analysis Agent verdict (SOUND / SKIP / WEAK) to operator@example.com with no timed cutover. Open/close emails, approval-ask emails (0024, one per distinct ask), and the 18:00 missed-trade backtest email stay. Verdicts are proposals, not fills. Do not write them into TRADES.md. No orders. Never withdraw.

## Why
Operator cancelled the 0014 cutover ~17:22 BST 1 Sep 2026. Emails stay on: MA verdicts, trade opens/closes, approval asks, and the 18:00 backtest.

## Rejected
- Reverting to open/close emails only after 12:07 BST 1 Sep 2026 (0014)
- Treating a verdict email as a fill
- Nags or a second email for the same verdict

## Unsure
- Whether SKIP and WEAK each always get their own email when Research posts several names in one scan window (chose: one email per distinct MA verdict, same grain as 0024)
