# Board
Last updated: Wed 2 Sep 2026, 08:15 BST

Every task has exactly one owner. Priorities come from ROADMAP.md, not whatever is loudest. Checkout cluster remains parked. All agents operate 24/7, no sleep. Old names (Chief, Scout, Critic, Ship, Ledger, Forge) are sunsetted.

## Standing
| Task | Owner | Notes |
| --- | --- | --- |
| Board, STATUS.md, today's assignments | Hedge Fund Manager | 24/7. No merge, deploy, or scope change. Morning board 8:03 and evening pass 18:03 every day. |
| Weekday morning intake | Research Agent | INTAKE.md at 8:00. Report only. |
| Binance USDT-M 3-min orderbook scan | Research Agent | 24/7. Crypto and TradFi perps. One proposal. Futures fail-closed primary; spot second. Book then flow then TA then CMC (n/a on TradFi, not a skip). Official CMC API. No site scrape. Never place an order. X unwired. While one live, flag seconds as SECOND-CANDIDATE; ping HFM only (do not auto-open). |
| Email on trade open/close, approval asks, MA verdicts, 18:00 backtest | Communication Agent | Standing: real open/close, any Operator approval ask (one email per distinct ask, no nag), Market Analysis Agent verdicts (SOUND/SKIP/WEAK, always on), and the 18:00 Verification Agent missed-trade backtest (paper, not a fill). No PRs. |
| PR review before Operator | Market Analysis Agent | Security and edge cases first. Never edit/approve/merge. |
| Verify Research Agent trade proposals | Market Analysis Agent | Viable and sound. Tag DIRECTION_VETO on every SKIP. Weigh TA below book/flow; weigh CMC. 24/7. No orders. Weekday 14:30 BST re-vet of still-green overnight SKIP/WEAK one-picks. |
| Preview after merge/sign-off | Trading desk | Preview only. Never prod, DNS, or env. |
| Execute Binance USDT-M trades | Trading desk | Sole executor. 24/7. First while flat: Market Analysis SOUND only at ≤10%. While one is open, a second may open at 5% (Research one-pick + MA SKIP with DIRECTION_VETO=no, or SOUND second also 5%). TradFi/commodity second beside a crypto first: must still be paper-green vs fresh mark and not on the local high, else skip/delay. No third (except locked 15 Sep LINKUSDT cloture clip). Always 20x, always cross. Close at +50% ROI on 20x (2.5% price) unless Research Agent and Market Analysis Agent both call HOLD after that print; then close still above +50% when the book breaks. Never withdraw. |
| Decision notes | Trading Journal | Ops decisions/. Write when a thread closes. |
| Executed trades + gains | Trading Journal | Ops TRADES.md. Every fill, any hour. Never invent. Never withdraw. Friday 18:00 weekly P&L email. |
| Paper-mark Research Agent proposals | Verification Agent | Mark to market 24/7. Not fills. No orders. Report only when paper P&L would have hit +10% coin from proposed mid. |
| 18:00 missed-trade backtest | Verification Agent | Daily 18:00 Europe/London, all 7 days. Untaken Research Agent proposals: would they have been profitable. Send report to Communication Agent. Not fills. |
| Post-trade learning | Verification Agent | After fills and when paper paths would have paid, propose one concrete strategy improvement to Hedge Fund Manager. Does not change live rules, place orders, or withdraw. |
| Paper Sep-4 equity options marks/expiry | Research Agent | PAPER-SEP-OPTIONS.md. Not Binance. Expiry Fri 4 Sep ~21:00 BST. |
| CLARITY Act cloture watch (15 Sep) | Research Agent | Confirm cloture success via The Block, CoinDesk, Cointelegraph, or Bloomberg only; then HFM sends Trading desk for locked LINKUSDT LONG 25% / 20x CROSS / close ×1.025. Not a fill today. |

## Today
| Stage | Task | Owner | Status |
| --- | --- | --- | --- |
| — | Scan Binance futures books every 3 min; propose one trade | Research Agent | Cron */3. Last scan ~08:08 BST (0804): SILENCE. ONE-LIVE CRCLUSDT LONG @ 89.17 mark~89.68 ROI20x~+11.4% close≥91.39925. XAU flat. 5% second seat free. Overnight continues. |
| — | Log every executed trade and gains | Trading Journal | TRADES.md: XAU close 07:22 (net −0.35798); CRCL LONG still open. Overnight BCH/APT closes already logged. |
| — | Verify Research Agent trade proposals (viable/sound) | Market Analysis Agent | LITUSDT LONG 0756 SKIP DIRECTION_VETO=yes (~08:03). ZHIPU 0750 TradFi second filtered FLAG_ONLY. 14:30 re-vet later today. 24/7. |
| — | Execute sound proposals, 20x cross, first SOUND ≤10% while flat, second 5% while one is open, close +50% ROI unless HOLD | Trading desk | Watching CRCLUSDT LONG 1.36 @ 89.17 (order 1099123376). Close ≥ 91.39925. Signed watches resumed. MA-cleared seconds auto-approved by HFM (Operator 08:25); LIT stays FLAG_ONLY (veto). No second open. Never withdraw. |
| — | Email operator@example.com on each open and close, approval ask, MA verdict, and 18:00 backtest | Communication Agent | XAU close emailed ~07:22 BST. MA verdict emails always on. Tonight’s 18:00 backtest still due. 24/7. |
| — | Paper-mark Research Agent proposals vs +10% coin | Verification Agent | No first-time +10% overnight. FLAG notes: ENA/DOT/ZHIPU. Closest unalerted UAIUSDT ~+9.2%. Not fills. Cron 24/7. |
| — | 18:00 missed-trade backtest to Communication Agent | Verification Agent | Due tonight 18:00. |
| — | Post-trade learning to Hedge Fund Manager | Verification Agent | XAU lesson sent ~07:30 (TradFi second filter). Operator locked it. |
| — | Paper Sep-4 options marks | Research Agent | Ten weeklies live on paper (~$372 debit). Expiry Fri 4 Sep. |
| 1 | Read/reproduce 3 checkout bug reports; common cause | Research Agent | Done as source gap. Zero of three found. Parked. |
| 2 | Fix on a branch + PR with regression test | — | Unowned. Communication Agent no longer implements. |
| 3 | Review PR (security, edge cases) | Market Analysis Agent | Queued |
| 4 | Preview deploy of the branch, post URL | Trading desk | Queued. Also needs repo + Vercel. |
| 5 | Decision note when this closes | Trading Journal | Queued on close |

## Next
_(roadmap still empty)_

## Blocked
| Task | Owner | Waiting on |
| --- | --- | --- |
| Checkout bug reports | Research Agent | Operator. Gmail/Drive empty of those reports. |
| Research Agent intake sources | Research Agent | Issue tracker / support queue |
| Trading desk preview | Trading desk | Product repo + Vercel + Market Analysis Agent sign-off + Operator |
| Merge to main / any deploy | — | Operator. Nobody else. |
| Any withdrawal | — | Never. Hard ban. |

## Done
| Task | Owner | When |
| --- | --- | --- |
| Stand up BOARD.md, ROADMAP.md, STATUS.md | Hedge Fund Manager | 29 Aug |
| Morning 8:03 / nightly 18:03 weekday passes | Hedge Fund Manager | 29 Aug; expanded to 7 days 31 Aug |
| Team roles confirmed | Hedge Fund Manager | 29 Aug; names sunsetted 31 Aug |
| Private GitHub `prosmoon-hash/scout-agent` (recipe only) | Hedge Fund Manager | 31 Aug |
| CoinMarketCap as research input (official API only) | Research Agent | 31 Aug 12:45 BST |
| TA as scan consideration (below book/flow) | Research Agent | 31 Aug 12:48 BST |
| HMAC order path live | Trading desk | 31 Aug 13:32 BST |
| TradFi USDT-M in the scan | Research Agent | 31 Aug 13:48 BST |
| Every open 20x cross | Trading desk | 31 Aug 14:35 BST |
| Scan cadence every 3 minutes | Research Agent | 31 Aug 14:46 BST |
| Approval emails (one per distinct ask) | Communication Agent | 31 Aug 14:58 BST |
| CBRS +100% ROI close exception (this trade only) | Trading desk | 31 Aug 17:50 BST; cleared on iOS close 1 Sep 01:56 |
| First 18:00 missed-trade backtest | Verification Agent | 31 Aug 18:14 BST |
| Dual-book scan (futures primary, spot second) | Research Agent | 31 Aug 21:16 BST |
| First TRADES.md close: CBRSUSDT LONG 3.49 | Trading Journal | 1 Sep 01:56 BST |
| First SOUND desk fill: BCHUSDT SHORT 1.018 | Trading desk | 1 Sep 17:18 BST |
| Standing live close +50% ROI on 20x | Hedge Fund Manager | 1 Sep 17:41 BST |
| MA verdict emails always on (cutover cancelled) | Communication Agent | 1 Sep ~17:22 BST |
| Verification post-trade learning | Verification Agent | 1 Sep ~17:59 BST |
| Half-size 5% is a second only (0029 supersedes 0028) | Hedge Fund Manager | 1 Sep 18:05 BST |
| Combined cap 15% (10% first + 5% second) | Hedge Fund Manager | 1 Sep ~19:39 BST |
| Paper 10 Sep-4 equity options | Research Agent | 1 Sep ~20:14 BST |
| CRCLUSDT LONG open (Operator veto override while flat) | Trading desk | 1 Sep 21:48 BST |
| XAUUSDT LONG second open then iOS close | Trading desk / Operator | Open 1 Sep 22:10; close 2 Sep 07:22 |
| Signed Binance position-read cards approved | Operator / Trading desk | 2 Sep ~06:27 BST |
| TradFi/commodity second filter locked | Hedge Fund Manager | 2 Sep (paper-green + not on local high) |
| LINKUSDT 25% cloture clip locked for 15 Sep | Hedge Fund Manager | 2 Sep |
