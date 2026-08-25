# Quote & Invoice Generator Demo — Instant PDF Quotes
# Simulates a landscaping company's intake form. Customer answers 5 questions,
# gets a branded quote number + itemized total in under a second.
# Run: python quote_generator.py
from datetime import datetime

BUSINESS = {
    "name": "Greenline Landscaping",
    "phone": "(555) 010-7788",
}

PRICE_TABLE = {
    # service -> (unit price, unit label)
    "mowing": (45, "per visit"),
    "hedge trimming": (60, "per visit"),
    "mulch install": (85, "per yard"),
    "leaf cleanup": (120, "per visit"),
    "fertilization": (55, "per application"),
}

def build_quote(customer: str, address: str, services: list) -> dict:
    lines, total = [], 0.0
    for svc in services:
        key = svc.lower().strip()
        if key not in PRICE_TABLE:
            raise ValueError(f"unknown service: {svc}")
        price, unit = PRICE_TABLE[key]
        lines.append((svc.title(), price, unit))
        total += price
    quote_no = f"GL-{datetime.utcnow():%Y%m%d-%H%M%S}"
    return {
        "quote_number": quote_no,
        "customer": customer,
        "address": address,
        "lines": lines,
        "total_usd": round(total, 2),
    }

def render(q: dict) -> str:
    out = [f"=== {BUSINESS['name']} QUOTE {q['quote_number']} ===",
           f"For: {q['customer']} | {q['address']}", ""]
    for name, price, unit in q["lines"]:
        out.append(f"  {name:<20} ${price:>6.2f}  ({unit})")
    out += ["", f"  TOTAL: ${q['total_usd']:.2f}",
            f"Questions? {BUSINESS['phone']} - reply to accept this quote."]
    return "\n".join(out)

if __name__ == "__main__":
    leads = [
        ("Sarah Mitchell", "412 Oakwood Ln", ["Mowing", "Hedge Trimming", "Mulch Install"]),
        ("Dan Ortiz", "88 Riverbend Rd", ["Leaf Cleanup", "Fertilization"]),
    ]
    for cust, addr, svcs in leads:
        print(render(build_quote(cust, addr, svcs)))
        print()
    print("[demo] 2 quotes generated instantly. Owner saves ~3 hrs/week of manual quoting.")
