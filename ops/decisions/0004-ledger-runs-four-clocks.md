# 0004 — Ledger also runs the four clocks

Date: 2026-08-29
Related: [0001](./0001-decision-notes-live-in-ops.md), [0003](./0003-no-merge-deploy-or-scope-change.md)
Supersedes: —

## Chose
Ledger keeps the decision log, and also:
- Weekday 7am brief: board, open PRs, failing CI. Three buckets only (shipped overnight / blocked / needs a decision today).
- Webhook catcher for newly opened issues labeled `bug`: reproduce if possible, attach findings, assign sev1/sev2/sev3, never close.
- Every night at 1am: one top unblocked board task, implement on a branch, tests, open a PR. Quiet if nothing unblocked or no repo.
- Friday 5pm: what shipped, what slipped, what we decided, and update CHANGELOG.

0003 still holds: no merge to main, no production deploy, no unprompted scope change.

## Why
The user assigned these four automations here. Clocks should exist even before a repo exists, so they no-op cleanly instead of being forgotten.

## Rejected
- Waiting for a repo before scheduling (the 7am brief can already report the board)
- Splitting these jobs back out to Chief / Forge / Ship without a new note (the spec landed on Ledger)
- A GitHub `issues.opened` listener (that event is not available; webhook until a repo exists)
- Native GitHub issue-label polling around the clock

## Unsure
- Whether Forge still implements on demand, or only this 1am pass does
- Whether Friday CHANGELOG lives in Ops or moves into the product repo
- Which GitHub repo to attach the bug webhook to (none exist on `prosmoon-hash` yet)
