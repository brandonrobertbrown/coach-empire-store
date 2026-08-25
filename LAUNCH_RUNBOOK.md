# LAUNCH RUNBOOK — Coach's 60-Minute Path to First Dollar
**Print or keep open. Do top-to-bottom. Nothing here needs me — everything here feeds the machine I built you.**

## STEP 1 — Gumroad account + payout (15 min)
1. gumroad.com → Sign up (or log in) with your email
2. Settings → **Payouts** → connect bank
3. Enter USAA routing + account numbers (have them from your USAA app)
4. Choose **Direct deposit / ACH** — NOT PayPal (PayPal skims an extra 2%)
5. Done means: payout screen shows your bank ending in the last-4 you recognize

## STEP 2 — Publish product #1: AlphaBoostPack (10 min)
1. Gumroad → New product → Digital product
2. Name: `Alpha-Boost: 50 Elite AI Prompts + Goal-Chain Workflow`
3. Price: **$39**
4. Upload file: `C:\Users\brand\Empire\releases\AlphaBoostPack_v20260825.zip`
5. Cover image: `C:\Users\brand\Empire\products\AlphaBoostPack\hero.png`
6. Description: copy-paste from `C:\Users\brand\Empire\LISTINGS_AND_PROMO.md` (Product 1 section, "Description" line)
7. Publish → copy the product URL

## STEP 3 — Publish products #2 and #3 (15 min)
Same flow, twice:
| Product | Zip | Price | Hero image |
|---|---|---|---|
| Faceless Channel Launch Kit | `FacelessChannelKit_v20260825.zip` | $27 | `products\FacelessChannelKit\hero.png` |
| 90-Day AI Freelance Sprint | `AIFreelanceSprint_v20260825.zip` | $47 | `products\AIFreelanceSprint\hero.png` |

Descriptions for both are pre-written in `LISTINGS_AND_PROMO.md`.

## STEP 4 — Log your listings (2 min)
Open `C:\Users\brand\Empire\ledger\live_listings.json` and make it look like:
```json
{"listings": [
  {"product": "AlphaBoostPack", "platform": "Gumroad", "url": "<paste url>", "live_date": "2026-08-25"}
]}
```
(one entry per product). This flips my dashboard gate from RED to counting.

## STEP 5 — First promo volley (15 min)
Post promo #1 for each product from `LISTINGS_AND_PROMO.md`:
- Personal X/Twitter account
- Personal LinkedIn (the FreelanceSprint post is written for LinkedIn tone)
- One relevant subreddit/community where genuinely allowed — use the value-first angle noted per product

## STEP 6 — When sales land
Each sale → add a row to `C:\Users\brand\Empire\ledger\sales_log.csv`:
```
date,product,platform,amount_usd
2026-08-28,AlphaBoostPack,Gumroad,39.00
```
Then run (or ask me): `python C:\Users\brand\Empire\revenue_dashboard.py`

## What happens automatically after that
- Every morning 06:00: new sellable pack generated into `Empire/releases/` (cron job 3f235637d909)
- You upload the good ones (~10 min/product), I keep the catalog compounding toward Phase 2 targets

## Cash-flow reality (so nothing surprises you)
- First payout holds ~1–3 weeks while Gumroad reviews the account
- After review: money hits USAA via ACH on Fridays, 2–5 business days transit
- Net per sale after fees: $39→~$33 · $47→~$40 · $27→~$22.50

## If you want me to drive any step WITH you
Say "launch with me" and I'll walk the screens live via computer control — you stay on keyboard for anything touching your bank login.
