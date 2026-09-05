# STATUS
Last updated: Sat 5 Sep 2026, 13:45 BST

## Today

TWO LIVE. No third (except locked 15 Sep LINKUSDT 25% cloture).

1) GIGGLEUSDT LONG 23.64 @ 43.95787, 20x CROSS — iOS (not Trading Desk). Three LIMIT BUY tickets:
   - 2393700114, 18.76 @ 44.32, 10:22:54 BST
   - 2394377543, 1.24 @ 42.70, 12:25:09 BST
   - 2394386276, 3.64 @ 42.52, 12:25:48 BST
   Open fees ~0.2543 USDT. Close ≥ 45.0568 (+50% ROI on 20x). Desk watch giggleusdt-long-50-roi-close-watch every 5m.

2) LINKUSDT LONG 28.42 @ 11.812, 20x CROSS — Trading Desk order 51915254711 at 13:40:01 BST. MAD SOUND on Research 1332 mid 11.7905. 5% second beside GIGGLE. Close ≥ 12.1073. Watch linkusdt-long-50-roi-close-watch every 5m. Not the 15 Sep 25% cloture clip.

PROCESS RULE (Operator 5 Sep ~13:45 BST, refines 13:43): FLAT = Research scan every **10 min** for a first. ONE live = Research may scan for SECOND-CANDIDATE only (MAD reviews; Desk monitors open). TWO live = only Trading Desk (close watches); Research/MAD/Verification PAUSED until Desk wakes them (flat or seat frees). Combined ~15%. Never withdraw.

USAGE: Many routines still hitting resource_exhausted; chat intermittently up.

Paper: TA/SMC secondary gate paper 7–14 days (cannot veto live). Sep-4 equity options book Ops PAPER-SEP-OPTIONS.md. Clarity Act cloture LINK 25% still 15 Sep only.

SPOT+FUTURES BOOKS: Research samples both; futures fail-closed primary; spot second sample. Execution fapi only. X unwired. Scan cadence when flat = 10m.

INTAKE: blocked (tracker / support / deps unwired). Checkout cluster parked.

ROADMAP: still empty. No invented product work.

## Owners (this thread)
- Binance orderbook scan: FLAT every 10 min (first); ONE live = SECOND-CANDIDATE only; TWO live = paused until Desk wakes; crypto and TradFi USDT-M; futures primary, spot second; TA below book/flow; CMC via official API (n/a on TradFi); SECOND-CANDIDATE while one live (ping HFM only) — Research Agent
- Verify Research Agent proposals (SOUND/SKIP/WEAK); tag DIRECTION_VETO on every SKIP; weekday 14:30 re-vet of still-green overnight SKIPs — Market Analysis Agent
- Execute SOUND first at ≤10% while flat; second at 5% while one is open (SKIP without direction veto, or SOUND second); TradFi second filter; 20x cross; no third (except locked LINK cloture); close +50% ROI unless HOLD — Trading desk
- Email open/close, 18:00 backtest, and Market Analysis Agent verdicts (always on) to operator@example.com; skip per-second approval asks when MA has cleared the second (Operator 08:25) — Communication Agent
- Executed trades + gains log (TRADES.md); weekly Friday 18:00 P&L email — Trading Journal
- Paper-mark Research Agent proposals (hypothetical +10% coin); 18:00 missed-trade backtest; post-trade learning to Hedge Fund Manager — Verification Agent
- Paper Sep-4 equity options marks/expiry; CLARITY Act cloture watch for LINK clip — Research Agent
- Stage 1 read/reproduce/common cause — Research Agent (checkout; parked)
- Stage 2 branch + PR + regression test — unowned
- Stage 3 review — Market Analysis Agent
- Stage 4 preview URL — Trading desk (after Market Analysis Agent AND Operator)
- Stage 5 decision note — Trading Journal

Exceptional hold (live as a rule, dormant until a real +50% ROI print): after +50% ROI, if Research Agent and Market Analysis Agent both call HOLD (long: bid notional > ask at 0.5% and 1%, 15m taker-buy share > 50%, 5m return still positive; short: invert), Trading desk holds. Close when any of those fails, still above +50% ROI. If they do not both agree, close at +50% ROI.

## Needs you
- The three checkout bug reports (not in Gmail, Drive, or GitHub)
- Vercel for Trading desk (preview only, still waits for you)
- Product roadmap items when you want non-trading work queued (ROADMAP.md is empty)

## Guardrails
No merge to main. No deploy without Operator. No scope change. All agents operate 24/7. Only Trading desk may place a futures order: first while flat is Market Analysis Agent-sound at ≤10%; a second while one is open is 5% (SKIP without direction veto, or SOUND second); TradFi/commodity second beside crypto first needs paper-green mid and not on local high; no third except locked 15 Sep LINKUSDT 25% cloture; always 20x cross; close at +50% ROI from entry unless Research Agent and Market Analysis Agent both call HOLD after +50% ROI (then close still above +50% ROI when the book breaks). Never touch withdrawals, under any circumstance. Current agent names only.
