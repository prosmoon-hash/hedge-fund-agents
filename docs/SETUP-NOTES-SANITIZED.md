# Multi-agent trading desk — setup notes (sanitized)

These notes describe how a **Grok Bot / Cursor multi-agent desk** was wired for crypto USDT‑M style futures research and execution.  
**Personal identifiers, emails, IPs, account numbers, balances, and secrets are omitted or replaced with placeholders.**

> Not financial advice. This is an operations template, not a strategy guarantee.

---

## 1. Goal

Run a small futures desk **24/7** with:

- Clear **separation of duties** (propose ≠ vet ≠ execute ≠ log ≠ notify)
- Hard **risk caps** and **no withdrawals**
- A single **orchestrator** that assigns work and escalates money / external / off-roadmap decisions
- An **Ops project** as the shared file system of record

---

## 2. Agent roster (roles)

| Agent | Owns | Must never |
|---|---|---|
| **Orchestrator** (“Hedge Fund Manager”) | Morning board, nightly summary, `STATUS.md` / `BOARD.md`, one owner per task, approvals routing | Merge, deploy, change roadmap scope, place orders, withdraw |
| **Research** | Market scans / proposals only; optional morning intake notes | Place/cancel/close; withdraw |
| **Market Analysis** | SOUND / SKIP / WEAK on each proposal; direction-veto tags | Place orders; merge; withdraw |
| **Trading Desk** | Sole venue order placer/closer; TP/SL watches; optional preview deploys after merge | Withdraw; open without cleared path |
| **Trading Journal** | Append-only `TRADES.md` + `decisions/NNNN-*.md` | Invent fills; place orders |
| **Communication** | Email operator on opens/closes/verdicts/scheduled digests | Place orders; invent fills |
| **Verification** | Paper-mark proposals; post-trade lessons; scheduled backtests | Place orders; change live rules |

Optional: other bots (prediction markets, etc.) stay **out of band** unless explicitly wired into the same risk book.

---

## 3. Shared Ops project

Create one project folder (example name: `ops`) joined by every trading agent:

```
ops/
  BOARD.md          # orchestrator-maintained task board
  ROADMAP.md        # ordered scope (orchestrator does not invent items)
  STATUS.md         # daily snapshot
  TRADES.md         # append-only executed trades
  decisions/        # append-only numbered decision notes
  INTAKE.md         # optional morning intake (report-only)
```

**Conventions**

- Decisions are **append-only**; supersede with a new number instead of editing history.
- `TRADES.md` only grows when **Desk reports a real fill** — never invent.
- Orchestrator refreshes `STATUS.md` on morning/nightly passes.

---

## 4. Message bus (how agents talk)

- Agents message each other asynchronously (`SendToAgent` style).
- Orchestrator talks to the **operator** in chat; desks do not spam the operator except via Communication emails for opens/closes/verdicts.
- FYI acks between agents often stay silent at the orchestrator (no need to re-narrate every ack).

---

## 5. Venue wiring (conceptual)

### Primary: USDT‑M futures venue

- **Public** market data: order books / marks (fail-closed if futures book unavailable; spot only as confirmation).
- **Signed** account calls (positions, place/close): run from a **trusted workstation** whose outbound IP is allowlisted on the API key.
- Shared automation host (“box”) may be **geo-blocked** on some venue endpoints — treat workstation as primary for signed traffic.
- API secrets: store via **secure secret input / local HMAC file**, never paste into chat transcripts.
- **Never withdraw** — strip withdrawal scope on API keys when the venue allows.

### Secondary venues (optional)

Lock separately before live use:

- Authority (who may place)
- IP allowlist(s): `<WORKSTATION_IP>` primary; `<AUTOMATION_HOST_IP>` optional
- Product scope (e.g. BTC/ETH perps only)
- First *N* fills require operator confirm in orchestrator chat
- Research/MAD scans off until explicitly wired

---

## 6. Seat / size / close rules (template)

Tune numbers to taste; keep them **written as decision notes**.

| Rule | Template used here |
|---|---|
| First while flat | Risk desk **SOUND** only, size ≤ **10%** of futures equity |
| Second while one live | **5%**; requires MA clear (SOUND, or SKIP with **no** direction veto) |
| Combined | ≤ **15%**; **max 2** seats (exception thirds only by explicit lock) |
| Leverage / margin | Fixed policy (example: **20× cross**) |
| Take profit | **+50% ROI** on that leverage (≈ 2.5% favorable price) |
| Stop loss | **−30% ROI** on **new** opens only (grandfather already-open seats if needed) |
| Discretionary early close | Operator confirms in orchestrator chat → orchestrator sends Desk a message starting with `CLOSE` naming symbol + order id |
| Withdrawals | **Forbidden** always |

### Process cadence by book state

- **FLAT:** Research scans for a **first** on a fixed interval.
- **ONE live:** Research may hunt a **second candidate** only; Desk monitors the open.
- **TWO live:** Desk-only (TP/SL watches); Research / MAD / Verification **proposal loops pause** until a seat frees.

### Filters worth writing down

- Weekend block for certain asset classes (example: no TradFi/commodity perps Sat–Sun in operator TZ).
- News gates for specific underlyings (example: oil only with explicit geopolitical headline rules).
- Fresh-flow recheck before placing a veto-path second beside a deeply red first.
- MAD “veto-set” rule: among names MAD *would* hard-veto, optionally pass ~**50% of the strongest** through as SOUND (rank by Research strength) — document carefully so it is not “50% of all proposals.”

### Paper / advisory sleeves

- Secondary TA/SMC tags on Research proposals for a time-boxed paper window.
- **TA_FAIL must not veto** a live MAD SOUND path during that window.
- Structure-based TP paper can stay **off** if live TP remains the ROI rule only.

---

## 7. Orchestrator routines

Typical scheduled jobs on the orchestrator:

| Routine | Cadence | Purpose |
|---|---|---|
| Morning board | Daily morning (local TZ) | Read board/checkpoints; assign one owner per task; refresh STATUS |
| Nightly pass | Daily evening | ≤10 lines: shipped / stalled / needs operator |
| Operator email instructions | Every N minutes | Accept **signed** instructions only from the operator’s allowlisted From address |
| One-off event watches | Calendar | e.g. known macro/legislative dates |

---

## 8. Communication Agent

- Email the operator on: trade **open**, trade **close**, MA verdicts (if enabled), scheduled digests (e.g. weekly P&L, evening backtest).
- One email per distinct ask — no nag loops.
- Include venue tag when multi-venue (`venue=<name>`).

---

## 9. Decision log pattern

Each lock becomes `decisions/NNNN-short-slug.md` with:

- **Chose**
- **Why**
- **Rejected**
- **Unsure** (optional)

Examples of locks that tend to matter: size caps, close protocol, stop-loss, weekend filters, venue authority, signed API watch auth for Auto-review.

---

## 10. Auto-review / signed watches

Automation safety layers may **pause** close watches if signed position reads look unauthorized.

**Mitigation used here:** operator grants **standing auth** in orchestrator chat that Desk may:

1. Read HMAC credentials from a local workstation file  
2. Call signed position/account endpoints  
3. Auto-close on armed TP/SL prints under written rules  

Log that as a numbered decision so future child runs inherit trusted context.

---

## 11. Git backup (optional)

- Private → public only after a secret scrub.
- Exclude: `.env`, HMAC files, seeds, cookie DBs, raw fills with account ids if sensitive.
- Prefer profiles, routines, skills, ops markdown, and non-secret scan code.

---

## 12. Operator checklist to reproduce

1. Create agents with the roster above; put them in one sidebar section if helpful.  
2. Create Ops project; all agents join it.  
3. Seed `BOARD.md` / `ROADMAP.md` / `STATUS.md` / empty `TRADES.md` / `decisions/`.  
4. Wire Research scan → MAD vet → Orchestrator PLACE → Desk execute → Journal + Comms.  
5. Lock risk rules as decision notes **before** first live order.  
6. Create venue API key: trade+read, **no withdraw**, IP allowlist `<WORKSTATION_IP>`.  
7. Store secrets via secure capture / local file; prove signed `position` read **PASS**.  
8. Arm TP (+50% ROI) and SL (−30% ROI on new) watches on Desk.  
9. Turn on Communication emails and orchestrator email-instruction poll.  
10. Run one paper week before raising size.

---

## 13. Placeholders reference

| Placeholder | Meaning |
|---|---|
| `<OPERATOR>` | Human owner |
| `<OPERATOR_EMAIL>` | Notification + signed-instruction inbox |
| `<WORKSTATION_IP>` | Allowlisted IP for signed API |
| `<AUTOMATION_HOST_IP>` | Optional second allowlist entry |
| `<VENUE_A>` | Primary USDT‑M futures venue |
| `<VENUE_B>` | Optional second venue |

---

## 14. What this deliberately does *not* include

- Exchange API keys, seeds, or session cookies  
- Exact wallet balances or historical PnL  
- Home address, family details, or device serials  
- Unredacted email contents  

If publishing these notes, re-scan adjacent repo files for the same classes of data.
