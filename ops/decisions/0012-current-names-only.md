# 0012 — Use current names only

Date: 2026-08-31
Related: [0006](./0006-ship-only-execution-cysusdt-not-a-fill.md), [0007](./0007-exit-up-10-one-open-trade.md), [0011](./0011-hold-past-plus10-if-scout-and-critic-agree.md)
Supersedes: —

## Chose
Operator sunsetted old nicknames. From now on use current names only. Roles are unchanged.

- Trading Journal (this agent; was called Ledger)
- Research Agent (was called Scout)
- Market Analysis Agent (was called Critic)
- Trading desk (was called Ship / Execution Agent) — still the only executor
- Hedge Fund Manager (was called Chief)
- Verification Agent
- Communication Agent

Do not use Scout, Critic, Ship, Ledger, Forge, Chief, or Execution Agent in new writing. Existing decision notes keep their original wording (0002). TRADES.md stays append-only.

## Why
Hedge Fund Manager relayed a Operator rule. Nicknames and live names were colliding.

## Rejected
- Rewriting 0001–0011 to swap names
- Treating a rename as a role change
- Logging a fill because of this note

## Unsure
- Whether Forge's old implement-on-branch job has a new named owner besides the nightly cloud-agent path
