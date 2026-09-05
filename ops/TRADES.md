# TRADES

Append-only log of executed fills and realized gains. Owned by Trading Journal.

Default venue: Binance USDT-M. Do not invent fills. Do not place orders. Do not touch withdrawals.

## Book status
Proposals-only as of 31 Aug 2026, 10:29 BST. Zero logged fills.
Ship-only execution as of 31 Aug 2026, 10:37 BST. Still zero logged fills. Max 10% of futures-account funds committed at a time.
Exit rule as of 31 Aug 2026, 10:43 BST: Ship closes a fill once it is up 10%; at most one trade open. Log those closes and the gain. Still zero executions.
24/7 as of 31 Aug 2026, 11:13 BST: log fills and closes whenever Ship reports them, not only at 21:15. Still zero executions.
Hold-after-+10% exception as of 31 Aug 2026, 11:33 BST: Ship may hold past +10% only if Scout and Critic both agree HOLD. Close still must be above +10% when HOLD breaks. Default +10% close otherwise. Still zero executions.
Names as of 31 Aug 2026, 11:36 BST: fills come only from Trading desk. Trading Journal owns this log. Still zero executions.
Next-SOUND open as of 31 Aug 2026, 12:55 BST: Trading desk to open the next Market Analysis Agent SOUND on a Research Agent proposal (close +10% unless 0011 HOLD). No backfill of CYS skip or SUI weak. Still no sanctioned order path. Still zero executions.
20x cross locked as of 31 Aug 2026, 14:35 BST (0019): every Trading desk open is 20x and cross. Isolated and other leverages banned. Size cap, one-open, +10% close, HOLD, withdrawal ban unchanged. Still zero executions.
Size cap as of 31 Aug 2026, 14:38 BST (0020): 10% stays ~12.87 USDT at 20x, not 20x margin (~257 notional). Still zero executions.
Scan as of 31 Aug 2026, 14:46 BST (0021): Research Agent every 3 minutes, 24/7. Still zero executions.
Second live as of 31 Aug 2026, 14:46 BST (0022): default one open; second only with Operator approval; combined 10% cap unless that approval says otherwise. 0022 supersedes 0007. Still zero executions.
Combined cap locked as of 31 Aug 2026, 14:49 BST (0023): an approved second still shares ~12.87 USDT with the first. Cap lifts only if that specific approval says so. Still zero executions.
First logged close as of 1 Sep 2026, 01:56:14 BST: CBRSUSDT LONG 3.49 closed via iOS reduce-only MARKET SELL (Trading desk reported, did not place). Not the +100% ROI print (193.0918). Account flat. Net incl. fees −0.8339 USDT.
Open as of 1 Sep 2026, 17:18:56 BST: BCHUSDT SHORT 1.018 @ 246.67278, 20x CROSS, margin ~12.56 USDT (≤10%), notional ~251.11, open fees ~0.1257. Trading desk placed (order 39783114819). MA SOUND on Research 1709 (mid 247.485). No exchange TP. Close ≤ 245.4394 (+10% ROI) unless Research+MA HOLD (0011). One live; second needs Operator (0022).
Close target as of 1 Sep 2026, 17:42 BST: live BCHUSDT SHORT close mark/last ≤ 240.5060 (+50% ROI on 20x; was 245.4394). Standing for all future fills: +50% ROI unless HOLD after that print. No duplicate open row.
Half-size SKIP path as of 1 Sep 2026, ~18:03 BST (0028): while FLAT, Research one-pick + MA SKIP without direction veto → 5% of funds, 20x, +50% ROI close. SOUND remains ≤10%. Dormant while BCH is one-open. Not a fill.
Half-size superseded as of 1 Sep 2026, 18:05 BST (0029): 5% only as a SECOND while one is open (Research one-pick + MA SKIP without direction veto, or SOUND second also 5%). First while flat = SOUND ≤10% only. 0028 while-FLAT path is out. Not a fill. Live BCH remains one-open.
Weekday 14:30 BST re-vet as of 1 Sep 2026, ~18:46 BST (0034): overnight SKIP/WEAK one-picks still paper-green are a fresh one-pick on a new mid. Do not auto-open SKIP. 0029 unchanged. Not a fill.
Combined cap as of 1 Sep 2026, ~19:38 BST (0035): 15% of USDT-M funds (10% first + 5% second). No third. 0023 superseded. APT Research 1926 not a fill.
APTUSDT SHORT instructed as of 1 Sep 2026, ~19:40 BST: 5% second while BCH is live. Trading desk to place. Not a fill until desk reports an execution. No duplicate open row.
Open as of 1 Sep 2026, 19:40:20 BST: APTUSDT SHORT 228.8 @ 0.5486, 20x CROSS, margin 6.276 USDT (5%), fees 0.0628, order 20561639910. Close ≤ 0.534885 (+50% ROI). Instructed 5% second beside live BCH. Combined under 15%. No third. Trading desk placed.
Both lives closed as of 1 Sep 2026, 20:28 BST: BCHUSDT SHORT 1.018 iOS reduce-only BUY at 20:28:26 (exit 247.33, net −0.92050). APTUSDT SHORT 228.8 iOS reduce-only BUY at 20:28:32 (exit 0.5613, net −3.03273). Trading desk reported, did not place. Not +50% ROI prints. Account flat. Desk-reported wallet [WALLET_REDACTED].
HFM confirm 1 Sep 2026 ~20:32 BST: same two iOS closes, no duplicate fill rows. Combined net about −3.95 USDT. Wallet [WALLET_REDACTED]. Book FLAT. Never withdraw.
Open as of 1 Sep 2026, 21:48:25 BST: CRCLUSDT LONG 1.36 @ 89.17, 20x CROSS, margin 6.0636 USDT (5% of wallet, Operator veto override while FLAT), fees 0.0485, order 1099123376. Close ≥ 91.39925 (+50% ROI). One live; no second. Desk-reported wallet after [WALLET_REDACTED]. Trading desk placed.
HFM confirm 1 Sep 2026 ~21:49 BST: same CRCLUSDT LONG open, no duplicate fill row. Desk fill, not SOUND. Available 115.6171 USDT. Close mark/last ≥ 91.39925. Never withdraw.
Open as of 1 Sep 2026, 22:10:46 BST: XAUUSDT LONG 0.028 @ 4335.80, 20x CROSS, margin 6.0701 USDT (5%), fees 0.0486, order 13906003826. Close ≥ 4444.195 (+50% ROI). 5% second beside live CRCL. Combined under 15%. No third. CRCL not touched. Desk-reported wallet after 121.6328 USDT. Trading desk placed.
HFM confirm 1 Sep 2026 ~22:11 BST: same XAUUSDT LONG second, no duplicate fill row. Available 109.4904 USDT. Close mark/last ≥ 4444.195. Two live (CRCL + XAU). No third. Never withdraw.
XAUUSDT LONG closed as of 2 Sep 2026, 07:22:27 BST: 0.028 iOS reduce-only MARKET SELL (order 13988364455, clientOrderId ios_vVR806bSJnZbQnaHvl1E). Entry 4335.80, exit 4326.48, realized −0.26096, net incl. fees −0.35798. Trading desk reported, did not place. Not +50% ROI print (4444.195). Do not re-open this XAU fill. CRCLUSDT LONG still the one live. No third. Never withdraw.
CRCLUSDT LONG add as of 2 Sep 2026, 15:27:16 BST: iOS BUY 6.44 @ 89.2479658 (order 1106435272, clientOrderId ios_usdt_aAKoRBxKdKWvy9jWarSg). Trading desk reported, did not place. Combined size 7.80 with desk open 1.36 @ 89.17. Not a new name. No third.
CRCLUSDT LONG closed as of 2 Sep 2026, 21:16:06 BST: iOS reduce-only MARKET SELL 7.80 @ 88.91 (order 1108535431, clientOrderId ios_hjnMUhRCkJTPvR3gZkL4). Realized −2.53010, open fees 0.27841, close fees 0.27740, net −3.08591. Trading desk reported, did not place. Not +50% ROI print (91.39925). Account FLAT on CRCL. Do not re-open. Never withdraw.
Desk-discovered live as of 5 Sep 2026, ~13:36 BST: GIGGLEUSDT LONG 23.64 @ 43.95787, 20x CROSS. Open order id and fill time unknown to HFM (likely Operator iOS while agents were resource_exhausted). Book was wrongly treated FLAT until this find. Close +50% ROI ≥ 45.0568 pending exact fill time/order from Trading desk. Never invent. Never withdraw.
GIGGLEUSDT LONG enriched as of 5 Sep 2026, ~13:40 BST: three Operator iOS opens (not desk) — 18.76 @ 44.32 (10:22:54, order 2393700114), 1.24 @ 42.70 (12:25:09, order 2394377543), 3.64 @ 42.52 (12:25:48, order 2394386276); avg 43.95787; open fees ~0.2543; close ≥ 45.0568. Book not FLAT.
Desk exact GIGGLE confirm 5 Sep ~13:41 BST: same three LIMIT BUY iOS opens from signed userTrades/allOrders. No duplicate fill rows. Never withdraw.
Open as of 5 Sep 2026, 13:40:01 BST: LINKUSDT LONG 28.42 @ 11.812, 20x CROSS, margin ~16.785 USDT (5% second beside GIGGLE), fees 0.16784852, order 51915254711. Close ≥ 12.1073 (+50% ROI). Not 15 Sep 25% cloture. Combined under 15%. No third. Trading desk placed.
HFM confirm 5 Sep 2026 ~13:41 BST: same LINKUSDT LONG second, no duplicate fill row. MAD SOUND Research 1332. Close mark/last ≥ 12.1073. Beside GIGGLEUSDT LONG 23.64 @ 43.95787. Not 15 Sep 25% cloture. Never withdraw.
Live-book process as of 5 Sep 2026, ~13:43 BST (0039 / Operator): while any USDT-M is open, only Trading Desk process runs. Research 10-min scan only when FLAT. Trading Journal still logs opens/closes when Desk reports (event-driven, not a scan loop). Never invent. Never withdraw.

## Skipped (not fills)
| Time (BST) | Symbol | Side | Note |
| --- | --- | --- | --- |
| 31 Aug 2026, 10:37 | CYSUSDT | short | skipped, not a fill |

## Fills
| Time (BST) | Venue | Symbol | Side | Size | Entry | Exit or mark | Realized P&L | Fees | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 Sep 2026, 01:56:14 | Binance USDT-M | CBRSUSDT | LONG close | 3.49 | 183.8969 | 183.8051 | −0.3206 USDT (net incl. fees −0.8339) | open 0.2567 + close 0.2566 | iOS reduce-only MARKET SELL order 439587412 (clientOrderId ios_NQSmtEkCBW98PKamldCD); Trading desk reported, did not place; not +100% ROI print |
| 1 Sep 2026, 17:18:56 | Binance USDT-M | BCHUSDT | SHORT open | 1.018 | 246.67278 | live; +50% ROI ≤ 240.5060 | — | ~0.1257 | Trading desk placed, order 39783114819; 20x CROSS; notional ~251.11; margin ~12.56; no exchange TP; MA SOUND Research 1709 (mid 247.485); close was 245.4394 |
| 1 Sep 2026, 19:40:20 | Binance USDT-M | APTUSDT | SHORT open (second) | 228.8 | 0.5486 | live; +50% ROI ≤ 0.534885 | — | 0.0628 | Trading desk placed, order 20561639910; 20x CROSS; margin 6.276 (5%); beside BCH; combined under 15% |
| 1 Sep 2026, 20:28:26 | Binance USDT-M | BCHUSDT | SHORT close | 1.018 | 246.67278 | 247.33 | −0.66905 USDT (net incl. fees −0.92050) | open 0.12556 + close 0.12589 | iOS reduce-only MARKET BUY order 39784334487 (clientOrderId ios_9pkWNFiEgjxOXoeyzhGD); Trading desk reported, did not place; not +50% ROI print |
| 1 Sep 2026, 20:28:32 | Binance USDT-M | APTUSDT | SHORT close | 228.8 | 0.5486 | 0.5613 | −2.90576 USDT (net incl. fees −3.03273) | open 0.06276 + close 0.06421 | iOS reduce-only MARKET BUY order 20561915983 (clientOrderId ios_smqklcCCkAoi1Zlq17wr); Trading desk reported, did not place; not +50% ROI print |
| 1 Sep 2026, 21:48:25 | Binance USDT-M | CRCLUSDT | LONG open | 1.36 | 89.17 | live; +50% ROI ≥ 91.39925 | — | 0.0485 | Trading desk placed, order 1099123376; 20x CROSS; margin 6.0636 (5%, Operator veto override while FLAT); no second |
| 1 Sep 2026, 22:10:46 | Binance USDT-M | XAUUSDT | LONG open (second) | 0.028 | 4335.80 | live; +50% ROI ≥ 4444.195 | — | 0.0486 | Trading desk placed, order 13906003826; 20x CROSS; margin 6.0701 (5%); beside CRCL; combined under 15%; no third; CRCL not touched |
| 2 Sep 2026, 07:22:27 | Binance USDT-M | XAUUSDT | LONG close | 0.028 | 4335.80 | 4326.48 | −0.26096 USDT (net incl. fees −0.35798) | open 0.04856096 + close 0.04845657 | iOS reduce-only MARKET SELL order 13988364455 (clientOrderId ios_vVR806bSJnZbQnaHvl1E); Trading desk reported, did not place; not +50% ROI print; do not re-open |
| 2 Sep 2026, 15:27:16 | Binance USDT-M | CRCLUSDT | LONG add | 6.44 | 89.2479658 | added to live 1.36 @ 89.17; combined 7.80 | — | part of combined open 0.27841 | iOS BUY order 1106435272 (clientOrderId ios_usdt_aAKoRBxKdKWvy9jWarSg); Trading desk reported, did not place |
| 2 Sep 2026, 21:16:06 | Binance USDT-M | CRCLUSDT | LONG close | 7.80 | 89.17 desk 1.36 + iOS 6.44 @ 89.2479658 | 88.91 | −2.53010 USDT (net incl. fees −3.08591) | open 0.27841 + close 0.27740 | iOS reduce-only MARKET SELL order 1108535431 (clientOrderId ios_hjnMUhRCkJTPvR3gZkL4); Trading desk reported, did not place; not +50% ROI print; do not re-open; account FLAT |
| 5 Sep 2026, 10:22:54 | Binance USDT-M | GIGGLEUSDT | LONG open | 18.76 | 44.32 | live; avg position 43.95787; +50% ROI ≥ 45.0568 | — | part of ~0.2543 | iOS LIMIT BUY order 2393700114 (clientOrderId ios_usdt_mAMa0PSeLS0yLK8XoxRb); Trading desk reported, did not place; from signed userTrades |
| 5 Sep 2026, 12:25:09 | Binance USDT-M | GIGGLEUSDT | LONG add | 1.24 | 42.70 | live; avg position 43.95787; +50% ROI ≥ 45.0568 | — | part of ~0.2543 | iOS LIMIT BUY order 2394377543 (clientOrderId ios_usdt_spZK2FjodKeKWNuRSiAx); Trading desk reported, did not place; from signed userTrades |
| 5 Sep 2026, 12:25:48 | Binance USDT-M | GIGGLEUSDT | LONG add | 3.64 | 42.52 | live; combined 23.64 avg 43.95787; +50% ROI ≥ 45.0568 | — | part of ~0.2543 | iOS LIMIT BUY order 2394386276 (clientOrderId ios_usdt_LXEineCIAAXOCfVQIiFj); Trading desk reported, did not place; from signed userTrades |
| 5 Sep 2026, 13:40:01 | Binance USDT-M | LINKUSDT | LONG open (second) | 28.42 | 11.812 | live; +50% ROI ≥ 12.1073 | — | 0.16784852 | Trading desk placed, order 51915254711 (clientOrderId MhpKmnyx7FmooMLvrkaQYB); 20x CROSS; margin ~16.785 (5% second beside GIGGLE); MAD SOUND Research 1332; not 15 Sep 25% cloture; combined under 15%; no third |

