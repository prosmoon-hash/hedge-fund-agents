# hedge-fund-agents

**Private backup/export** of Operator's Grok Bot trading-desk agents, skills, ops docs, and Binance scan Python helpers.

> This is **not** an executable Grok Bot runtime. It does not run agents, place trades, or connect to Binance. It is a clean snapshot for version history and disaster recovery.

## Layout

```
agents/<Desk-Slug>/
  profile.json          # name, description, title only
  memory/profile.md     # standing rules (if present)
  automations/<routine>/
    PROMPT.md           # job prompt text
    schedule.json       # cron/trigger summary (no secrets)

skills/                 # user workflow SKILL.md trees
ops/                    # BOARD, STATUS, ROADMAP, TRADES, PAPER-*, INTAKE, decisions/
code/binance-scan/      # canonical Python scan scripts (+ optional paper_mark example)
```

## Desks included

| Slug | Role |
|------|------|
| Hedge-Fund-Manager | Board, checkpoints, nightly ship/stall |
| Research-Desk | Intake, Binance scans, paper options |
| Market-Analysis-Desk | PR review, proposal re-vet |
| Trading-Desk | Preview deploys / execution desk (never withdraw / paper-safe policies apply live) |
| Trading-Journal | Trade log, decision notes, briefs |
| Communication-Agent | Approval / fill notification emails |
| Verification-Desk | Paper-mark, backtests, post-trade learning |

Skipped: **New Bot** (empty stub).

## Excluded on purpose

- Conversation DBs, `store.db`, `audit.jsonl`, conversation-blobs, attachments
- Tokens, cookies, `.env`, `hosts.yml`, API key screenshots (`binance-api-management*.png`)
- Large JSON scan dumps / paper-mark TSV dumps / agent transcripts
- Live agent UUIDs as folder names (slugs used instead)
- Ops `memory/` shards and `decisions/by-agent/`

## Safety

- **Never withdraw** / **never place trades** from this repo alone — it is documentation + scripts for review.
- Do not treat copied prompts as live credentials; schedules are informational.

## Source note

Exported from the Grok Bot box agent-data tree. Scan code sourced primarily from `binance-scan-2340` (newest coherent package with `score.py`, `build_universe.py`, `finalize.py`, `do_recheck.py`, `fetch_books.py`), plus unique helpers from `binance-scan-0838`.
