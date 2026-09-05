# 0003 — No merge to main, no deploy, no unprompted scope change

Date: 2026-08-29
Related: [0001](./0001-decision-notes-live-in-ops.md), [0002](./0002-append-only-supersede.md)
Supersedes: —

## Chose
Agents do not merge to main, do not deploy, and do not add, drop, or reorder roadmap items on their own. Money, external messages, and off-roadmap decisions go to the user. Preview deploys after merge stay with Ship, production does not.

## Why
Chief's standing guardrails (STATUS.md) and each specialist's stop-line. The board is a file; there is no repo yet, so merge/deploy is not even available — the rule is set before that changes.

## Rejected
- Agents merging their own PRs (Forge's stop-line)
- Production deploys, DNS, or env changes (Ship's stop-line)
- Scout opening, closing, or commenting on issues (report only)

## Unsure
- When a repo exists, whether Ship's preview deploy after merge still counts as "no deploy" in STATUS, or only production is banned
- Who tells Ledger a task finished, so the next decision actually gets written
