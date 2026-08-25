#!/usr/bin/env python3
"""Coach Empire — revenue ledger & proof-gate dashboard.

Reads Coach-entered sales events and computes progress toward targets.
Coach (or any marketplace export) appends rows to ledger/sales_log.csv:
    date,product,platform,amount_usd
Live listing URLs go in ledger/live_listings.json as:
    {"listings": [{"product": "...", "platform": "Gumroad", "url": "...", "live_date": "..."}]}

Usage: python revenue_dashboard.py            # full status report
       python revenue_dashboard.py --json     # machine-readable
"""
from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

EMPIRE = Path(__file__).resolve().parent
LEDGER = EMPIRE / "ledger"
SALES = LEDGER / "sales_log.csv"
LISTINGS = LEDGER / "live_listings.json"
TARGET_MONTHLY = 5000.0
TARGET_RAMP = 10000.0
RAMP_DEADLINE = "2026-10-31"

def main() -> int:
    now = datetime.now(timezone.utc)
    sales = []
    if SALES.exists():
        with SALES.open(newline="") as f:
            sales = [r for r in csv.DictReader(f) if r.get("amount_usd")]

    listings = []
    if LISTINGS.exists():
        listings = json.loads(LISTINGS.read_text()).get("listings", [])

    month = now.strftime("%Y-%m")
    mtd = sum(float(s["amount_usd"]) for s in sales if s["date"].startswith(month))
    all_time = sum(float(s["amount_usd"]) for s in sales)

    by_product: dict[str, float] = {}
    for s in sales:
        by_product[s["product"]] = by_product.get(s["product"], 0.0) + float(s["amount_usd"])

    days_left = max(0, (
        datetime.fromisoformat(RAMP_DEADLINE + "T23:59:59+00:00") - now
    ).days)

    if "--json" in sys.argv:
        print(json.dumps({
            "month_to_date_usd": round(mtd, 2),
            "all_time_usd": round(all_time, 2),
            "target_monthly_usd": TARGET_MONTHLY,
            "target_ramp_usd": TARGET_RAMP,
            "ramp_deadline": RAMP_DEADLINE,
            "days_remaining": days_left,
            "live_listings": len(listings),
            "sales_events": len(sales),
        }, indent=2))
        return 0

    W = 62
    def bar(pct: float) -> str:
        filled = int(min(1.0, pct) * 30)
        return "[" + "#" * filled + "-" * (30 - filled) + f"] {pct*100:.1f}%"

    print("=" * W)
    print("COACH EMPIRE — REVENUE DASHBOARD".center(W))
    print(f"generated: {now.isoformat(timespec='seconds')}Z".center(W))
    print("=" * W)
    print(f"Live listings:      {len(listings)}")
    print(f"Sales events:       {len(sales)}")
    print(f"Month-to-date:      ${mtd:,.2f}")
    print(f"All-time:           ${all_time:,.2f}")
    print("-" * W)
    pct5k = mtd / TARGET_MONTHLY if TARGET_MONTHLY else 0
    print(f"$5,000/mo goal:     {bar(pct5k)}")
    pct10k = mtd / TARGET_RAMP if TARGET_RAMP else 0
    print(f"$10k ramp goal:     {bar(pct10k)}   ({days_left} days to {RAMP_DEADLINE})")
    gap = max(0.0, TARGET_RAMP - mtd)
    need_per_day = gap / days_left if days_left else gap
    print(f"Ramp gap:           ${gap:,.2f}  → ${need_per_day:,.2f}/day required")
    print("-" * W)
    print("By product:")
    for p, amt in sorted(by_product.items(), key=lambda kv: -kv[1]):
        print(f"  {p:<28} ${amt:>9,.2f}")
    if not by_product:
        print("  (no sales logged yet — first sale unlocks the graph)")
    print("-" * W)

    gates = []
    if not listings:
        gates.append("[GATE] No live listings — upload releases/ zips to marketplaces.")
    if not sales:
        gates.append("[GATE] Zero sales logged — promo posts not yet driving traffic?")
    if mtd >= TARGET_MONTHLY:
        gates.append("[PROOF] $5k/mo target MET — shift focus to ramp retention.")
    if mtd >= TARGET_RAMP:
        gates.append("[PROOF] $10k ramp target MET ahead of deadline.")
    for g in gates:
        print(g)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
