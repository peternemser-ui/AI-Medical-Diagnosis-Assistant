"""
Referral Tracking -- Track when users click "Call Office" or "Get Directions"
on specialist cards.

Revenue: $5-25 per qualified referral.
"""

import json
import uuid
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter

REFERRALS_PATH = Path(__file__).parent / "referrals.json"

# Revenue per qualified referral by specialty
REFERRAL_RATES = {
    "default": 5,
    "Cardiology": 25,
    "Orthopedics": 20,
    "Dermatology": 15,
    "Neurology": 25,
    "Oncology": 25,
    "Gastroenterology": 20,
    "Psychiatry": 15,
    "Endocrinology": 20,
    "Pulmonology": 20,
    "Primary Care": 5,
    "Urgent Care": 10,
}


class ReferralTracker:
    def __init__(self):
        self.data = self._load()

    def _load(self) -> dict:
        if REFERRALS_PATH.exists():
            try:
                return json.loads(REFERRALS_PATH.read_text())
            except (json.JSONDecodeError, IOError):
                pass
        return {"clicks": []}

    def _save(self):
        REFERRALS_PATH.write_text(json.dumps(self.data, indent=2, default=str))

    def track_click(
        self,
        user_id: str,
        doctor_npi: str,
        doctor_name: str,
        specialty: str,
        action_type: str,
        location: str = "",
    ) -> dict:
        """Record a referral click. action_type: 'call', 'directions', 'website'."""
        click = {
            "id": uuid.uuid4().hex[:12],
            "user_id": user_id,
            "doctor_npi": doctor_npi,
            "doctor_name": doctor_name,
            "specialty": specialty,
            "action_type": action_type,
            "location": location,
            "timestamp": datetime.now().isoformat(),
        }
        self.data["clicks"].append(click)
        self._save()
        return click

    def get_stats(self, days: int = 30) -> dict:
        """Return referral stats for the last N days."""
        cutoff = datetime.now() - timedelta(days=days)
        recent = [
            c for c in self.data["clicks"]
            if datetime.fromisoformat(c["timestamp"]) > cutoff
        ]

        by_specialty = dict(Counter(c["specialty"] for c in recent))
        by_action = dict(Counter(c["action_type"] for c in recent))
        by_location = dict(Counter(c.get("location", "unknown") for c in recent))

        # Top referred doctors
        doctor_counts = Counter(
            (c["doctor_npi"], c["doctor_name"], c["specialty"]) for c in recent
        )
        top_doctors = [
            {"npi": npi, "name": name, "specialty": spec, "clicks": count}
            for (npi, name, spec), count in doctor_counts.most_common(10)
        ]

        return {
            "period_days": days,
            "total_clicks": len(recent),
            "by_specialty": by_specialty,
            "by_action": by_action,
            "by_location": by_location,
            "top_doctors": top_doctors,
        }

    def get_billable_referrals(self, days: int = 30) -> dict:
        """
        Return qualified referrals (unique user+doctor within a 24h window).
        A referral is qualified when a unique user interacts with a unique doctor
        at least once. Multiple clicks by the same user to the same doctor
        within 24h count as a single qualified referral.
        """
        cutoff = datetime.now() - timedelta(days=days)
        recent = [
            c for c in self.data["clicks"]
            if datetime.fromisoformat(c["timestamp"]) > cutoff
        ]

        # Group by (user, doctor, date) -- one qualified referral per day per pair
        seen = set()
        qualified = []
        for click in recent:
            ts = datetime.fromisoformat(click["timestamp"])
            day_key = (click["user_id"], click["doctor_npi"], ts.strftime("%Y-%m-%d"))
            if day_key not in seen:
                seen.add(day_key)
                qualified.append(click)

        # Estimate revenue
        total_revenue = 0.0
        for q in qualified:
            rate = REFERRAL_RATES.get(q["specialty"], REFERRAL_RATES["default"])
            total_revenue += rate

        return {
            "period_days": days,
            "total_clicks": len(recent),
            "qualified_referrals": len(qualified),
            "estimated_revenue": round(total_revenue, 2),
            "avg_revenue_per_referral": round(total_revenue / max(len(qualified), 1), 2),
            "referrals": qualified[:50],  # return the most recent 50
        }


# Singleton instance
referral_tracker = ReferralTracker()
