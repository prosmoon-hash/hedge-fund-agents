# 0030 — Weekday 14:25 BST re-vet of overnight SKIP/WEAK one-picks

Date: 2026-09-01
Related: [0029](./0029-half-size-second-only.md), [0027](./0027-post-trade-learning.md)
Supersedes: —

## Chose
Weekdays at 14:25 BST, Verification Desk sends Market Analysis and Hedge Fund Manager the overnight SKIP/WEAK Research one-picks that are still paper-green vs original mid (symbol, side, original mid, scan_id, current mark, paper %). Paper-red is dropped. Market Analysis re-vets at 14:30 BST as fresh one-picks on live fapi. Not auto-open of the stale SKIP. First while FLAT remains SOUND-only (0029). Paper +10% coin and live +50% ROI close unchanged. Not fills. No orders. Never withdraw.

## Why
Hedge Fund Manager relayed a Operator lock ~18:46 BST 1 Sep 2026. Market Analysis confirmed they will ask at 14:30 BST.

## Rejected
- Auto-opening overnight SKIP while FLAT (0028)
- Sending paper-red names
- Verification Desk placing the re-vet trade

## Unsure
- Exact cutoff for “overnight” vs same-morning scans just before 14:25 (chose: any SKIP/WEAK one-pick from the prior close through 14:25 that is still unfilled and paper-green)
