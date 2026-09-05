# 0001 — Decision notes live in Ops `decisions/`

Date: 2026-08-29
Related: _(root — no older note)_

## Chose
Keep decision notes as append-only markdown files in the Ops project at `decisions/`, named `NNNN-slug.md`. Each note records what we chose, why, what we rejected, and what we are unsure about.

## Why
Ops is the shared team workspace (BOARD, STATUS, ROADMAP, INTAKE). There is no product repo yet, so this is the only place every agent can already see. Numbered files are easy to link and never require rewriting an older note.

## Rejected
- Agent memory or chat history as the source of truth (not shared, not linkable, easy to overwrite)
- Waiting for a git repo (Forge is blocked on one; decisions are needed now)
- A single rolling log file (harder to point one decision at another)

## Unsure
- Whether these notes should move into the product repo once one exists
- Whether other agents will write here, or only Ledger
