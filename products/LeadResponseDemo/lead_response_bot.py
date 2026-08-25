# Lead-Response Bot Demo — Instant Reply Engine
# Simulates a local business's website contact form. When a lead comes in,
# replies in <1 second with a personalized SMS/email + booking link.
# Run: python lead_response_bot.py
import json
import time
from datetime import datetime

BUSINESS = {
    "name": "Summit Peak Dental",
    "owner": "Dr. Reyes",
    "booking_link": "https://summitpeakdental.example.com/book",
    "hours": "Mon-Fri 8am-5pm",
}

REPLY_TEMPLATE = (
    "Hi {first_name}, thanks for contacting {business}! "
    "This is our instant assistant - you're in the queue for {service}. "
    "Grab a time that works you: {booking_link} "
    "(We're open {hours}.)"
)

def handle_lead(lead: dict) -> dict:
    """Process an inbound lead and return the outbound reply payload."""
    reply = REPLY_TEMPLATE.format(
        first_name=lead["name"].split()[0],
        business=BUSINESS["name"],
        service=lead.get("service", "your visit"),
        booking_link=BUSINESS["booking_link"],
        hours=BUSINESS["hours"],
    )
    return {
        "to": lead["contact"],
        "message": reply,
        "response_time_seconds": 0.8,
        "logged_at": datetime.utcnow().isoformat() + "Z",
    }

if __name__ == "__main__":
    # Simulated inbound leads hitting the form
    leads = [
        {"name": "Maria Lopez", "contact": "+1-555-0142", "service": "teeth cleaning"},
        {"name": "James Carter", "contact": "jcarter@example.com", "service": "whitening consult"},
        {"name": "Priya Patel", "contact": "+1-555-0199", "service": "chipped tooth"},
    ]
    print(f"[demo] {BUSINESS['name']} lead-response bot\n")
    for lead in leads:
        t0 = time.perf_counter()
        out = handle_lead(lead)
        elapsed = time.perf_counter() - t0
        print(f"LEAD IN : {lead['name']} ({lead['contact']}) -> {lead['service']}")
        print(f"REPLY   : {out['message']}")
        print(f"SENT TO : {out['to']} | processed in {elapsed*1000:.1f}ms\n")
        time.sleep(0.3)
    print("[demo] 3 leads captured, 3 instant replies sent. Zero leads went cold.")
