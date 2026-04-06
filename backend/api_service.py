"""
API-as-a-Service -- Let other apps use the 7-agent pipeline.

Pricing:
- Starter: 1,000 calls/month ($49/mo)
- Growth: 10,000 calls/month ($299/mo)
- Enterprise: 100,000 calls/month ($1,999/mo)
- Pay-as-you-go: $1.50 per call
"""

import json
import uuid
from pathlib import Path
from datetime import datetime

API_KEYS_PATH = Path(__file__).parent / "api_keys.json"

PLANS = {
    "starter": {"limit": 1_000, "price": 49},
    "growth": {"limit": 10_000, "price": 299},
    "enterprise": {"limit": 100_000, "price": 1_999},
    "payg": {"limit": None, "price_per_call": 1.50},
}


class ApiKeyManager:
    def __init__(self):
        self.data = self._load()

    def _load(self):
        if API_KEYS_PATH.exists():
            return json.loads(API_KEYS_PATH.read_text())
        return {"keys": {}, "usage": {}}

    def _save(self):
        API_KEYS_PATH.write_text(json.dumps(self.data, indent=2, default=str))

    def create_key(self, developer_name: str, email: str, plan: str = "starter") -> str:
        key_id = f"mda_{uuid.uuid4().hex[:24]}"
        self.data["keys"][key_id] = {
            "developer": developer_name,
            "email": email,
            "plan": plan,
            "created": datetime.now().isoformat(),
            "active": True,
            "calls_this_month": 0,
            "total_calls": 0,
        }
        self._save()
        return key_id

    def validate_key(self, key: str):
        info = self.data["keys"].get(key)
        if not info or not info["active"]:
            return None
        return info

    def track_usage(self, key: str):
        if key in self.data["keys"]:
            self.data["keys"][key]["calls_this_month"] += 1
            self.data["keys"][key]["total_calls"] += 1

            # Track daily usage
            today = datetime.now().strftime("%Y-%m-%d")
            if "usage" not in self.data:
                self.data["usage"] = {}
            if key not in self.data["usage"]:
                self.data["usage"][key] = {}
            self.data["usage"][key][today] = self.data["usage"][key].get(today, 0) + 1

            self._save()

    def check_limit(self, key: str) -> bool:
        """Return True if the key is within its plan limit (or is pay-as-you-go)."""
        info = self.data["keys"].get(key)
        if not info or not info["active"]:
            return False
        plan = PLANS.get(info["plan"], PLANS["starter"])
        if plan.get("limit") is None:
            return True  # pay-as-you-go has no cap
        return info["calls_this_month"] < plan["limit"]

    def revoke_key(self, key: str) -> bool:
        if key in self.data["keys"]:
            self.data["keys"][key]["active"] = False
            self._save()
            return True
        return False

    def get_all_keys(self) -> dict:
        return self.data["keys"]

    def get_usage(self, key: str = None) -> dict:
        """Return daily usage data. If key is provided, filter to that key."""
        usage = self.data.get("usage", {})
        if key:
            return usage.get(key, {})
        return usage

    def get_usage_stats(self) -> dict:
        """Aggregate usage statistics across all keys."""
        keys = self.data["keys"]
        total_calls = sum(k.get("total_calls", 0) for k in keys.values())
        active_keys = sum(1 for k in keys.values() if k.get("active"))
        inactive_keys = sum(1 for k in keys.values() if not k.get("active"))

        # Revenue estimate
        revenue = 0.0
        for info in keys.values():
            plan = PLANS.get(info.get("plan", "starter"), PLANS["starter"])
            if "price" in plan:
                revenue += plan["price"]
            elif "price_per_call" in plan:
                revenue += info.get("calls_this_month", 0) * plan["price_per_call"]

        return {
            "total_keys": len(keys),
            "active_keys": active_keys,
            "inactive_keys": inactive_keys,
            "total_calls": total_calls,
            "estimated_monthly_revenue": round(revenue, 2),
            "plans": PLANS,
        }


# Singleton instance
api_key_manager = ApiKeyManager()
