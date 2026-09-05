# 0014 — 24h window: email each Market Analysis Agent verdict

Date: 2026-08-31
Related: [0012](./0012-current-names-only.md), [0005](./0005-trades-log-proposals-only.md), [0006](./0006-ship-only-execution-cysusdt-not-a-fill.md)
Supersedes: —

## Chose
From 12:07 BST 31 Aug 2026 until 12:07 BST 1 Sep 2026, Communication Agent emails each Market Analysis Agent verdict to operator@example.com. Those emails are proposals, not fills. After 12:07 BST 1 Sep 2026, Communication Agent reverts to open/close emails only. Do not write those verdicts into TRADES.md. No fill to log. 0001–0012 not rewritten.

## Why
Hedge Fund Manager assigned a 24-hour exception so Operator sees each verdict in the inbox without changing the fill log or the standing open/close mail job.

## Rejected
- Treating a verdict email as a fill
- Making the extra emails permanent
- Rewriting 0001–0012

## Unsure
- Whether a verdict that arrives a minute after 12:07 BST 1 Sep still gets the extra email (chose: no, window closed)
