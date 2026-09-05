---
name: Binance proposal check
description: >-
  use this when verifying a Binance USDT-M futures trade proposal for viability
  and soundness before treating it as a candidate
---
---
name: Binance proposal check
description: >-
  use this when verifying a Binance USDT-M futures trade proposal for viability
  and soundness before treating it as a candidate
---
# Binance USDT-M proposal check

Proposals only. Never place, cancel, or size a live order. Never touch withdrawals. Never use API keys or exchange session cookies.

## Inputs needed
- Symbol, side (long/short), mid
- Why the proposer likes it (book imbalance, flow)
- Stated failure reason
- Spot book fields if attached (imb, spread, aligned-or-against futures)

Treat prior snapshots as stale. Re-check live public data.

## Data (public unsigned REST only)
Use `https://www.binance.com/fapi` from this computer for futures. Do not use `fapi.binance.com` (HTTP 451). Do not wait on a Mac approval card. Independent live re-check is mandatory. Fail-closed only on real futures book data, not on a blocked pull.

- `GET https://www.binance.com/fapi/v1/depth?symbol=...&limit=500`
- `GET https://www.binance.com/fapi/v1/klines?symbol=...&interval=1m&limit=60`
- `GET https://www.binance.com/fapi/v1/ticker/24hr?symbol=...`
- `GET https://www.binance.com/fapi/v1/premiumIndex?symbol=...`
- `GET https://www.binance.com/fapi/v1/ticker/bookTicker?symbol=...`

Spot (second sample, not fail-closed): `GET https://www.binance.com/api/v3/depth?symbol=...&limit=500` when a USDT spot pair exists. If no spot pair (many TradFi perps), mark `spot: n/a`. If the spot pull fails, mark `spot: unavailable` and continue on futures.

## Checks (fail closed on futures)
1. **Liquid futures book** — real 24h quote volume; skip thin books.
2. **Not a spoofable wall** — size that can vanish; wall not resting near mid or not replenishing.
3. **Not squeeze-exhaust** — skip if parabolic 24h move AND deeply negative funding AND 15–60m rolling over.
4. **Spread tradable** — bid-ask not eating the edge.
5. **Imbalance actually near mid** — 0.5% and 1% futures depth, not a wall far from mid.
6. **Downside if the wall pulls** — what happens if that size disappears.

## Spot (extra, Operator 31 Aug 2026)
Re-check spot 0.5%/1% imb and spread when a pair exists. Never SOUND on spot alone. Spot against a merely-ok futures book is extra skip caution. Spot aligned is a plus, not a size-up. A large spot-futures mid gap is caution, not a chase.

Weight: futures book, then futures flow, then spot book, then TA, then CMC.

Do not invent a better trade unless the original is unsound and you can say why.

## Verdict
One of `sound` / `weak` / `skip`, plus one reason. No padding.
