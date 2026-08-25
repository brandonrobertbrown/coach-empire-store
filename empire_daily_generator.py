#!/usr/bin/env python3
"""Coach Empire — daily product generator.

Generates one new sellable digital pack per run (prompt library expansion,
niche guide, checklist kit, template bundle) and packages it into releases/.
Runs fully offline: deterministic templates + optional LM Studio polish at
http://127.0.0.1:1234/v1 when available.

Usage:
    python empire_daily_generator.py            # generate today's pack
    python empire_daily_generator.py --list     # show generation themes
"""
from __future__ import annotations

import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

EMPIRE = Path(__file__).resolve().parent
OUT_ROOT = EMPIRE / "products" / "daily_packs"
STATE = EMPIRE / "ledger" / "generator_state.json"
LM_URL = "http://127.0.0.1:1234/v1/chat/completions"

THEMES = [
    {"id": "prompt_pack", "title": "Prompt Expansion Pack", "price": 19,
     "spec": "20 new prompts on {theme} with [BRACKETED] variables, grouped in 4 categories."},
    {"id": "checklist_kit", "title": "Operations Checklist Kit", "price": 17,
     "spec": "10 operational checklists for {theme}: launch, weekly ops, audit, recovery."},
    {"id": "template_bundle", "title": "Template Bundle", "price": 21,
     "spec": "8 fill-in-the-blank business document templates for {theme} with usage notes."},
    {"id": "niche_guide", "title": "Niche Playbook", "price": 24,
     "spec": "A 30-day playbook for launching a digital side-business in {theme}: steps, tools, math."},
]

ROTATION_TOPICS = [
    "real estate agents", "fitness coaches", "restaurant owners", "Etsy sellers",
    "local contractors", "wedding planners", "tutoring services", "barbershops",
    "dog trainers", "photographers", "food trucks", "cleaning services",
]


def lm_polish(prompt: str) -> str | None:
    """Optional polish pass via local LM Studio; silently skipped if down."""
    try:
        req = urllib.request.Request(
            LM_URL,
            data=json.dumps({
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 2000, "temperature": 0.7,
            }).encode(),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=90) as r:
            data = json.loads(r.read())
        content = data["choices"][0]["message"]["content"]
        return content if content and content.strip() else None
    except Exception:
        return None


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {"run_count": 0, "topic_index": 0}


def save_state(s: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(s, indent=2))


def build_pack(theme: dict, topic: str) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    slug = f"{theme['id']}_{topic.replace(' ', '_')}_{stamp}"
    pdir = OUT_ROOT / slug
    pdir.mkdir(parents=True, exist_ok=True)

    spec = theme["spec"].format(theme=topic)
    body = lm_polish(
        f"You write premium digital products sold to small-business owners and creators. "
        f"{spec} Be concrete, no filler, every item actionable. Markdown format."
    ) or _fallback_body(theme, topic)

    listing = (
        f"# {theme['title']}: {topic.title()} Edition\n\n"
        f"**${theme['price']}** - instant download.\n\n"
        f"Purpose-built for {topic}. No generic advice - every line written for this "
        f"exact business type. Lifetime updates included.\n"
    )
    (pdir / "content.md").write_text(body)
    (pdir / "LISTING_COPY.md").write_text(listing)
    (pdir / "manifest.json").write_text(json.dumps({
        "slug": slug, "theme_id": theme["id"], "topic": topic,
        "price_usd": theme["price"], "built_utc": datetime.now(timezone.utc).isoformat(),
    }, indent=2))
    return pdir


def _fallback_body(theme: dict, topic: str) -> str:
    """Full-quality offline generation — no LM needed."""
    T = topic.title()
    bodies = {
        "prompt_pack": (
            f"# Prompt Expansion Pack: {T} Edition\n\n"
            f"20 plug-and-play AI prompts written specifically for {topic}. "
            f"Replace [BRACKETS], paste into any LLM.\n\n"
            f"## Marketing & Growth\n"
            f"1. Write a Google Business Profile post announcing [OFFER] for {topic}, under 200 words with local keywords.\n"
            f"2. Draft 10 Instagram captions for [PHOTO CONTEXT] that end with soft CTAs appropriate for {topic}.\n"
            f"3. Create a referral-request message that doesn't feel pushy, for a satisfied {topic[:-1]} client.\n"
            f"4. Write 5 Google Ads headlines (30 chars max) for [SERVICE] targeting [CITY].\n"
            f"5. Turn this customer review into 3 social proof snippets: [REVIEW].\n\n"
            f"## Sales & Client Communication\n"
            f"6. Script a price-objection response for {topic}: acknowledge, reframe value, offer tier-down.\n"
            f"7. Write an inquiry-response template that answers, proves credibility, and books a call in under 120 words.\n"
            f"8. Draft a follow-up sequence (3 touches, 7 days) for a lead who went quiet after [EVENT].\n"
            f"9. Create a service-package comparison my customers instantly understand: [PACKAGES].\n"
            f"10. Write a win-back email for clients inactive 6+ months, warm not desperate.\n\n"
            f"## Operations\n"
            f"11. Design a daily open/close checklist for a one-person {topic} operation.\n"
            f"12. Convert this messy process description into a numbered SOP: [PROCESS].\n"
            f"13. Create a weekly metrics dashboard spec: 5 numbers that predict next month's revenue for {topic}.\n"
            f"14. Write vendor-negotiation talking points for reducing my monthly [EXPENSE] by 10-15%.\n"
            f"15. Build a seasonal-demand prep plan for [SEASON]: inventory, staffing, marketing timeline.\n\n"
            f"## Strategy\n"
            f"16. Analyze my top competitor [NAME/URL]: what they signal, what they miss, one wedge I take this month.\n"
            f"17. Stress-test my current pricing against inflation + my capacity ceiling; propose new tiers.\n"
            f"18. Map 3 adjacent revenue streams a trusted {topic[:-1]} business could add within 60 days.\n"
            f"19. Given goal [GOAL], write a 30-day action plan with weekly checkpoints and kill criteria.\n"
            f"20. Run a pre-mortem on opening [NEW LOCATION/OFFER]: top 5 failure causes, prevention for each.\n",
        ),
        "checklist_kit": (
            f"# Operations Checklist Kit: {T} Edition\n\n"
            f"10 field-tested checklists that keep a {topic} business running without chaos.\n\n"
            f"## 1. Daily Open (15 min)\n- Review yesterday's revenue vs plan\n- Check messages/inquiries from overnight\n- Confirm today's appointments/jobs\n- Cash float / payment systems verified\n- One marketing touch posted\n\n"
            f"## 2. Daily Close (15 min)\n- Reconcile payments received\n- Tomorrow confirmed with each client\n- Log any leads needing follow-up\n- Note one thing that worked today\n\n"
            f"## 3. Weekly Ops (45 min)\n- Revenue vs weekly target\n- Lead funnel review: inquiries → booked → completed\n- Follow-up every stale lead >7 days\n- Restock/supply order if below par\n- Schedule social posts for coming week\n\n"
            f"## 4. Weekly Marketing (60 min)\n- Request 2 reviews from recent happy clients\n- Post 3x minimum (1 promo, 1 proof, 1 personality)\n- Update GBP/listing photos monthly rotation\n- Outreach: 10 past clients with seasonal offer\n\n"
            f"## 5. Monthly Financial (90 min)\n- P&L simple version: revenue, COGS, fixed, net\n- Compare trailing 3 months; flag trend breaks\n- Tax set-aside transfer (% of net)\n- Subscription audit: cancel unused\n- Price check: costs risen >5% anywhere?\n\n"
            f"## 6. Monthly Growth (60 min)\n- Pick ONE growth experiment for next month\n- Review last experiment: keep/kill decision documented\n- Ask 3 clients the same question: 'What almost stopped you from hiring me?'\n- Update service page with newest proof/testimonial\n\n"
            f"## 7. Quarterly Audit (half day)\n- Full pricing review vs market\n- Competitor sweep: offerings, reviews, gaps\n- Equipment/tool maintenance or replacement plan\n- Goal reset: next quarter's ONE number\n\n"
            f"## 8. New Client Onboarding\n- Signed scope/quote returned\n- Deposit received & logged\n- Welcome message with expectations + timeline\n- Intake questions answered\n- Calendar slot protected + reminder scheduled\n\n"
            f"## 9. Job/Service Completion\n- Quality check against original request\n- Final invoice same-day\n- Review request sent at peak satisfaction moment\n- Photo of result saved to portfolio folder\n- Upsell/cross-sell note logged if spotted\n\n"
            f"## 10. Emergency Recovery (bad week protocol)\n- Identify the ONE broken thing causing most damage\n- Communicate proactively to affected clients\n- Fix root cause before adding new work\n- Write the checklist item that would have prevented it\n- Book recovery time before re-accepting full load\n",
        ),
        "template_bundle": (
            f"# Template Bundle: {T} Edition\n\n"
            f"8 fill-in-the-blank documents every {topic} business needs. Copy, replace brackets, send.\n\n"
            f"## 1. Service Quote Template\n"
            f"'Hi [NAME], thanks for reaching out about [NEED]. Based on what you described ([SUMMARY]), here's my quote: [SCOPE ITEMS]. Total: $[AMOUNT], which includes [INCLUSIONS]. Valid for 14 days. To book, reply approved and I'll send the deposit invoice ($[DEPOSIT]).'\n\n"
            f"## 2. Booking Confirmation\n"
            f"'Confirmed: [SERVICE] on [DATE] at [TIME], [LOCATION]. You'll get a reminder 24h before. Total due: $[AMOUNT] ([PAYMENT TERMS]). Need to change anything? Reply here at least 24h ahead.'\n\n"
            f"## 3. Review Request\n"
            f"'[NAME], it was great [WHAT YOU DID] for you! If you have 60 seconds, a quick review helps my small business more than any ad: [REVIEW LINK]. Either way, thanks for choosing [BUSINESS].'\n\n"
            f"## 4. Late Payment Nudge (friendly → firm ladder)\n"
            f"- Day 7: 'Quick heads-up that invoice #[N] shows unpaid — likely just slipped through. Resending here.'\n"
            f"- Day 14: '[NAME], invoice #[N] ($[AMOUNT]) is now a week past due. Please send payment by [DATE] to avoid late fee.'\n"
            f"- Day 21: 'Per our terms, work pauses on outstanding accounts. Happy to resolve today: [PAYMENT LINK].'\n\n"
            f"## 5. Referral Ask\n"
            f"'[NAME], people like you are exactly who I love working with. Know anyone else who needs [SERVICE]? If someone books from your intro, [REFERRAL REWARD].'\n\n"
            f"## 6. Price Increase Notice\n"
            f"'[NAME], starting [DATE], rates for [SERVICE] move to [NEW PRICE] (+[X]%). Current clients keep existing rates until [GRACE DATE]. This covers [REASON: materials/insurance/capability]. Locked-in rate available via [RETAINER/PREPAY OPTION]. Thank you for [X years] of trust.'\n\n"
            f"## 7. Scope Change Quote\n"
            f"'Happy to add [NEW REQUEST]. That's outside our original agreement ([ORIGINAL SCOPE]), so here's an add-on quote: $[AMOUNT], adds [TIME] to timeline. Reply approved and I'll fold it in.'\n\n"
            f"## 8. Testimonial Consent Form\n"
            f"'May we feature your feedback publicly? Yes/No. Name as you'd like it shown: ___. Business/social handle (optional): ___. Approved quote: ___.'\n",
        ),
        "niche_guide": (
            f"# Niche Playbook: {T}\n\n"
            f"A 30-day plan to launch a digital side-income stream serving {topic}.\n\n"
            f"## Why {topic.title()} Is a Buyer Niche\nThey spend money on: visibility, bookings, retention, and admin relief. Every product below maps to one of those four pains.\n\n"
            f"## Week 1 — Validate (Days 1–7)\n- Join 3 communities where {topic} gather (FB groups, subreddits, forums)\n- Log the 10 most-repeated complaints verbatim\n- Post one genuinely helpful answer daily (no selling)\n- Day 7: pick the complaint you can package against\n\n"
            f"## Week 2 — Build the Product (Days 8–14)\n- Format options ranked by speed: checklist pack (fastest) → template bundle → mini-guide → video course (slowest)\n- Build v1 in 3 sessions max — ugly and useful beats pretty and unfinished\n- Price anchor: $17–29 for packs, $39–59 for guides\n- Include one bonus nobody expects\n\n"
            f"## Week 3 — Set Up Shop (Days 15–21)\n- Marketplace listing: title formula = [Outcome] + [For Whom] + [Format]\n- Description: pain → contents → proof → guarantee\n- Screenshots/mockups: 4 images minimum\n- Launch price 30% under target for first 20 buyers ('founding price')\n\n"
            f"## Week 4 — First Sales Push (Days 22–30)\n- Return to communities: share results of your earlier helpful answers, mention the pack once\n- DM everyone who thanked/upvoted you: 'built the full version, founding price ends Sunday'\n- Collect every buyer reaction as social proof\n- Day 30 review: units × price = revenue; decide iterate/pivot/kill\n\n"
            f"## The Math to $1k/mo\nAt $27 average: 37 sales/month = ~1.2/day. That's traffic math, not luck: pick platforms where {topic} already gather and show up daily.\n\n"
            f"## Scaling After First $500\n- Raise price to full\n- Add order-bump (+$9 companion checklist)\n- Second product targeting the #2 complaint\n- Bundle both at 25% off joint price\n",
        ),
    }
    val = bodies.get(theme["id"])
    if isinstance(val, tuple):
        val = val[0]
    return val or f"# {theme['title']}: {T} Edition\n\nGenerated content pending."


def main() -> int:
    args = sys.argv[1:]
    if "--list" in args:
        for t in THEMES:
            print(f"{t['id']}: {t['title']} (${t['price']})")
        print(f"\nRotation topics ({len(ROTATION_TOPICS)}): " + ", ".join(ROTATION_TOPICS))
        return 0

    state = load_state()
    theme = THEMES[state["run_count"] % len(THEMES)]
    topic = ROTATION_TOPICS[state["topic_index"] % len(ROTATION_TOPICS)]
    pdir = build_pack(theme, topic)

    state["run_count"] += 1
    state["topic_index"] += 1
    state["last_run_utc"] = datetime.now(timezone.utc).isoformat()
    state["last_pack"] = str(pdir)
    save_state(state)

    # auto-package the new pack into releases/
    import zipfile
    zout = EMPIRE / "releases" / f"{pdir.name}.zip"
    with zipfile.ZipFile(zout, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(pdir.rglob("*")):
            if f.is_file():
                zf.write(f, arcname=str(f.relative_to(pdir)))
    print(f"[ok] pack built: {pdir}")
    print(f"[ok] release zip: {zout} ({zout.stat().st_size:,} bytes)")
    print(f"[next] upload to marketplace, log URL in ledger/live_listings.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
