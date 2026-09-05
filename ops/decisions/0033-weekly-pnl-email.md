# 0033 — Weekly P&L email every Friday 18:00 BST

Date: 2026-09-01
Related: [0005](./0005-trades-log-proposals-only.md), [0024](./0024-approval-emails.md), [0004](./0004-ledger-runs-four-clocks.md)
Supersedes: —

## Chose
Trading Journal owns a weekly P&L report to operator@example.com, copied to Hedge Fund Manager in chat. Cadence: every Friday 18:00 BST. Window: trailing 7 days (prior Friday 18:00 → this Friday 18:00). Standing Friday 18:00 routine. One email per week, no nag. Source: Ops TRADES.md only. Closed names: side, size, entry, exit, realized USDT (fees if logged), time BST, then net realized. Open positions listed separately (symbol, side, size, entry, mark, unrealized, close target), not mixed into realized net. If no fills: still send a one-line “flat week / still open: …”. First send Friday 4 Sep 2026 18:00 BST; partial week from 1 Sep is fine. Emails stay on. Not a fill. No orders. Never withdraw.

## Why
Operator lock ~18:19 BST 1 Sep 2026, assigned by Hedge Fund Manager.

## Rejected
- Mixing open mark-to-market into realized net
- Inventing fills or skipping the email on a flat week
- Nags or extra test mail

## Unsure
- Whether Trading Journal sends the mail directly or hands the body to Communication Agent (chose: either; Communication Agent if that is the existing mail path)
