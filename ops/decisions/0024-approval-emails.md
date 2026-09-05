# 0024 — Email Operator when an approval is needed

Date: 2026-08-31
Related: [0014](./0014-24h-verdict-emails.md), [0022](./0022-second-position-needs-approval.md)
Supersedes: —

## Chose
Whenever Operator must approve something before work continues, Communication Agent emails operator@example.com. One email per distinct ask. No nag. Hedge Fund Manager (or the waiting agent) sends Communication Agent the payload: time BST, what, who is waiting, why. Open/close emails, the 24h MA-verdict window (0014), and the 18:00 backtest emails stay. No test mail. Do not invent asks. Do not place trades. Never withdraw.

## Why
Operator locked this at 14:58 BST 31 Aug 2026 so an ask still reaches the inbox if the screen is locked or idle.

## Rejected
- Relying on in-app cards only
- Nags/reminders
- Backfilling parked asks (Investing.com sign-in stays unemailed unless a new ask is made)

## Unsure
- Whether a declined ask gets a confirmation email (chose: no, unless Operator asks)
