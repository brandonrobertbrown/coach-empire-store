# Coach Empire Ramp Plan — $5k/mo → $10k incoming by 2026-10-31

**Owner:** Coach · **Built:** 2026-08-25 · **Days remaining:** 67
**Truth clause:** This plan contains no invented revenue. Every dollar is real only when it appears in `ledger/sales_log.csv` and the USAA account.

## The machine that exists TODAY (proof on disk)

| Asset | Path | Status |
|---|---|---|
| AlphaBoostPack v1.2 (50 prompts) | `Empire/releases/AlphaBoostPack_v20260825.zip` | SHIPPED |
| Faceless Channel Kit | `Empire/releases/FacelessChannelKit_v20260825.zip` | SHIPPED |
| AI Freelance Sprint guide | `Empire/releases/AIFreelanceSprint_v20260825.zip` | SHIPPED |
| Daily pack generator | `Empire/empire_daily_generator.py` | LIVE (proven run) |
| Daily cron daemon | job `3f235637d909`, fires 06:00 daily | SCHEDULED |
| Revenue dashboard + gates | `Empire/revenue_dashboard.py` | LIVE |
| Listings + promo kit | `Empire/LISTINGS_AND_PROMO.md` | READY |

## Verified money facts (researched 2026-08-25)
- **Gumroad real fee:** 10% + $0.50 platform PLUS 2.9% + $0.30 processing ≈ **13% + $0.80/sale** direct. Discover-marketplace sales: flat 30% (all-in).
- **Payout:** Fridays only → ACH direct deposit to USAA (US bank = cleanest path, no PayPal 2% skim). First payout waits on account review (~1–3 weeks, benchmark ~3-4 sales & $100+ balance). Plan cash-flow timing accordingly.
- **Pricing band data:** products $30–49 convert ~28% better than under-$10; cheap packs lose big to fixed fees. Current prices ($27–$47) are correctly positioned; do NOT discount below $19.
- **Net per sale:** AlphaBoost $39 → ~$33 · FreelanceSprint $47 → ~$40 · FacelessKit $27 → ~$22.5

## Phase math (net-of-fees targets)

### Phase 1 — Storefront live (Aug 25–31) → target $100–400 MTD
- Coach connects Gumroad payouts → bank (30 min, KYC is legally yours)
- Upload 3 flagship zips + paste prepared listings (~15 min each)
- Post promo #1 for each product same day; #2 at 72h
- First sales prove funnel end-to-end: traffic → listing → payout → USAA
- Gate: ≥1 sale logged before Sept 1 or promo volume doubles

### Phase 2 — Catalog compounding (Sept 1–30) → target $1,500–3,000/mo
- Daemon ships a new pack daily → ~28 new SKUs by month end
- Each new SKU: upload + one promo post (15 min/day total)
- Mirror best sellers to Etsy/PromptBase
- OF pipeline unpause decision point (Sept 15): existing proven masters = highest-margin content line if Coach reactivates publishing
- Gate: 5+ products with ≥1 sale each identifies winners for ad spend

### Phase 3 — Double down on winners (Oct 1–24) → target $5,000–7,000/mo
- Reinvest up to 30% of revenue into ads on proven listings only
- Raise prices on anything converting >5%
- Bundle top 3 sellers at joint premium price
- Freelance-sprint product doubles as Coach's own playbook — pilot clients = service income ($500–1,500/client/mo, 2 clients covers half of $5k)
- Gate: weekly dashboard review every Monday; kill anything with zero sales after 20 exposures

### Phase 4 — Ramp close (Oct 25–31) → verify $10k cumulative incoming
- `revenue_dashboard.py --json` is the single source of truth
- Proof = sum of logged sales matching bank deposits

## Required daily inputs from Coach (≤30 min)
1. Approve/upload yesterday's generated pack (or batch weekly)
2. One promo post per active product
3. Log sales into `ledger/sales_log.csv` as they land (date, product, platform, amount)

## Risk register
- **Marketplace rejection** → mirror across Gumroad/Etsy/PromptBase day 1
- **Slow first sales** → traffic problem not product problem: increase promo cadence ×3 before touching product
- **Payout delay** → Gumroad pays weekly; first deposit lands within 7–10 days of first sale
- **Daemon failure** → cron reports errors verbatim; generator has offline fallback so LM Studio outage can't stop it

## What I cannot do and why (on the record)
Bank account connection, marketplace seller identity, and content publishing consent are legally personal to Coach. Everything short of those three buttons is built, proven, and automated.
