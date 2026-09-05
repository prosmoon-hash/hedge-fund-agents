# 0015 — CoinMarketCap into research

Date: 2026-08-31
Related: [0012](./0012-current-names-only.md), [0005](./0005-trades-log-proposals-only.md), [0006](./0006-ship-only-execution-cysusdt-not-a-fill.md)
Supersedes: —

## Chose
As of 12:43 BST 31 Aug 2026, Operator directed CoinMarketCap into research. Owner is Research Agent. There is no agent named Market Research Agent. Research Agent uses the official CMC API only: no site scrape, no Safari cookies. Market Analysis Agent weighs CMC fields in its verdict. The book stays fail-closed (proposals are not fills). Trading rules unchanged (0006, 0007, 0011). 0001–0014 not rewritten. No fill to log.

## Why
Hedge Fund Manager relayed Operator's direction. CMC is extra research input, not a new execution path and not a reason to open the book.

## Rejected
- Scraping coinmarketcap.com or reading Safari cookies for CMC
- Treating CMC data as a fill or as an order
- Assigning CMC to an agent named Market Research Agent
- Changing exit, size, or executor rules

## Unsure
- Which CMC fields Market Analysis Agent must weigh, and whether a missing CMC field fail-closes a proposal
