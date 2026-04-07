"""
Subscription & Billing Agent

Manages user subscription tiers, usage limits, and feature gating.
Tiers: free, plus ($9.99/mo), pro ($29.99/mo), family ($49.99/mo)

Usage data is persisted in a JSON file (backend/subscription_data.json).
"""

import json
import os
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# ── Tier definitions ────────────────────────────────────────────────────

TIERS = {
    "free": {
        "name": "Free",
        "price": 0,
        "diagnoses_per_month": 2,
        "models": ["ollama"],
        "features": ["basic_report", "body_map"],
        "max_photos": 1,
        "pdf_export": False,
        "specialist_routing": False,
        "family_members": 0,
    },
    "plus": {
        "name": "Plus",
        "price": 9.99,
        "diagnoses_per_month": 20,
        "models": ["ollama", "claude-haiku-4-5", "claude-sonnet-4-6", "gpt-4o-mini"],
        "features": ["basic_report", "body_map", "pdf_export", "photo_analysis", "history"],
        "max_photos": 5,
        "pdf_export": True,
        "specialist_routing": True,
        "family_members": 0,
    },
    "pro": {
        "name": "Pro",
        "price": 29.99,
        "diagnoses_per_month": -1,  # unlimited
        "models": ["ollama", "claude-haiku-4-5", "claude-sonnet-4-6", "claude-opus-4-6", "gpt-4o", "gpt-4o-mini"],
        "features": [
            "basic_report", "body_map", "pdf_export", "photo_analysis",
            "history", "specialist_routing", "priority_support", "api_access",
        ],
        "max_photos": -1,
        "pdf_export": True,
        "specialist_routing": True,
        "family_members": 0,
    },
    "family": {
        "name": "Family",
        "price": 49.99,
        "diagnoses_per_month": -1,
        "models": ["ollama", "claude-haiku-4-5", "claude-sonnet-4-6", "claude-opus-4-6", "gpt-4o"],
        "features": [
            "basic_report", "body_map", "pdf_export", "photo_analysis",
            "history", "specialist_routing", "family_profiles", "pediatric_mode",
        ],
        "max_photos": -1,
        "pdf_export": True,
        "specialist_routing": True,
        "family_members": 5,
    },
}

# Feature display names for upgrade prompts
FEATURE_LABELS = {
    "basic_report": "Basic Reports",
    "body_map": "Body Map",
    "pdf_export": "PDF Export",
    "photo_analysis": "Photo Analysis",
    "history": "Diagnosis History",
    "specialist_routing": "Specialist Routing",
    "priority_support": "Priority Support",
    "api_access": "API Access",
    "family_profiles": "Family Profiles",
    "pediatric_mode": "Pediatric Mode",
}

# ── Data file path ──────────────────────────────────────────────────────

_DATA_DIR = Path(__file__).resolve().parent.parent
_DATA_FILE = _DATA_DIR / "subscription_data.json"


class SubscriptionManager:
    """Manages subscription tiers, usage tracking, and feature gating."""

    def __init__(self):
        self._data = self._load()

    # ── Persistence ─────────────────────────────────────────────────────

    def _load(self) -> dict:
        """Load subscription data from JSON file."""
        if _DATA_FILE.exists():
            try:
                with open(_DATA_FILE, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                logger.warning("Failed to load subscription data: %s", e)
        return {"users": {}}

    def _save(self):
        """Persist subscription data to JSON file."""
        try:
            with open(_DATA_FILE, "w") as f:
                json.dump(self._data, f, indent=2, default=str)
        except IOError as e:
            logger.error("Failed to save subscription data: %s", e)

    def _ensure_user(self, user_id: str) -> dict:
        """Ensure user entry exists with default free tier."""
        if user_id not in self._data["users"]:
            self._data["users"][user_id] = {
                "tier": "free",
                "usage": [],
                "upgraded_at": None,
                "stripe_customer_id": None,
                "stripe_subscription_id": None,
            }
            self._save()
        return self._data["users"][user_id]

    # ── Current month key ───────────────────────────────────────────────

    @staticmethod
    def _month_key() -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m")

    # ── Public API ──────────────────────────────────────────────────────

    def get_user_tier(self, user_id: str) -> dict:
        """Return the user's current tier info including all limits."""
        user = self._ensure_user(user_id)
        tier_key = user["tier"]
        tier = TIERS.get(tier_key, TIERS["free"]).copy()
        tier["tier_key"] = tier_key
        tier["stripe_customer_id"] = user.get("stripe_customer_id")
        tier["stripe_subscription_id"] = user.get("stripe_subscription_id")
        tier["upgraded_at"] = user.get("upgraded_at")
        return tier

    def check_usage(self, user_id: str) -> dict:
        """Return usage status: used, limit, remaining, can_diagnose."""
        user = self._ensure_user(user_id)
        tier_key = user["tier"]
        tier = TIERS.get(tier_key, TIERS["free"])
        limit = tier["diagnoses_per_month"]

        month = self._month_key()
        used = sum(1 for u in user.get("usage", []) if u.get("month") == month)

        if limit == -1:
            # unlimited
            return {
                "tier": tier_key,
                "tier_name": tier["name"],
                "used": used,
                "limit": -1,
                "remaining": -1,
                "can_diagnose": True,
                "month": month,
            }

        remaining = max(0, limit - used)
        return {
            "tier": tier_key,
            "tier_name": tier["name"],
            "used": used,
            "limit": limit,
            "remaining": remaining,
            "can_diagnose": remaining > 0,
            "month": month,
        }

    def increment_usage(self, user_id: str):
        """Record a diagnosis use for the current month."""
        user = self._ensure_user(user_id)
        if "usage" not in user:
            user["usage"] = []
        user["usage"].append({
            "month": self._month_key(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        self._save()

    def can_use_feature(self, user_id: str, feature: str) -> bool:
        """Check if the user's tier includes a given feature."""
        user = self._ensure_user(user_id)
        tier_key = user["tier"]
        tier = TIERS.get(tier_key, TIERS["free"])
        return feature in tier["features"]

    def can_use_model(self, user_id: str, model: str) -> bool:
        """Check if the user's tier allows a given AI model."""
        user = self._ensure_user(user_id)
        tier_key = user["tier"]
        tier = TIERS.get(tier_key, TIERS["free"])
        return model in tier["models"]

    def get_upgrade_prompt(self, user_id: str, blocked_feature: Optional[str] = None) -> dict:
        """Return upgrade message when the user hits a limit or requests a gated feature."""
        user = self._ensure_user(user_id)
        current_key = user["tier"]
        current = TIERS.get(current_key, TIERS["free"])

        # Find the cheapest tier that unlocks the feature
        suggested_tier_key = None
        if blocked_feature:
            for key in ["plus", "pro", "family"]:
                t = TIERS[key]
                if blocked_feature in t["features"] or blocked_feature in t["models"]:
                    suggested_tier_key = key
                    break

        if not suggested_tier_key:
            # Default: suggest one tier up
            tier_order = ["free", "plus", "pro", "family"]
            idx = tier_order.index(current_key) if current_key in tier_order else 0
            suggested_tier_key = tier_order[min(idx + 1, len(tier_order) - 1)]

        suggested = TIERS[suggested_tier_key]
        feature_label = FEATURE_LABELS.get(blocked_feature, blocked_feature or "this feature")

        return {
            "message": f"Upgrade to {suggested['name']} to unlock {feature_label}.",
            "current_tier": current_key,
            "current_tier_name": current["name"],
            "suggested_tier": suggested_tier_key,
            "suggested_tier_name": suggested["name"],
            "suggested_price": suggested["price"],
            "upgrade_url": "/pricing",
        }

    def set_user_tier(self, user_id: str, tier_key: str, stripe_customer_id: Optional[str] = None,
                      stripe_subscription_id: Optional[str] = None):
        """Upgrade/downgrade a user's tier (called after Stripe webhook or manually)."""
        if tier_key not in TIERS:
            raise ValueError(f"Unknown tier: {tier_key}")
        user = self._ensure_user(user_id)
        user["tier"] = tier_key
        user["upgraded_at"] = datetime.now(timezone.utc).isoformat()
        if stripe_customer_id:
            user["stripe_customer_id"] = stripe_customer_id
        if stripe_subscription_id:
            user["stripe_subscription_id"] = stripe_subscription_id
        self._save()

    def track_cost(self, user_id: str, cost: float):
        """Add a cost entry to the user's monthly running total."""
        if cost <= 0:
            return
        user = self._ensure_user(user_id)
        if "costs" not in user:
            user["costs"] = []
        user["costs"].append({
            "month": self._month_key(),
            "amount": round(cost, 4),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        self._save()

    def get_monthly_cost(self, user_id: str) -> dict:
        """Return total cost spent this month."""
        user = self._ensure_user(user_id)
        month = self._month_key()
        costs = user.get("costs", [])
        total = sum(c["amount"] for c in costs if c.get("month") == month)
        count = sum(1 for c in costs if c.get("month") == month)
        return {
            "month": month,
            "total_cost": round(total, 4),
            "diagnosis_count": count,
        }

    def get_all_tiers(self) -> list[dict]:
        """Return all tiers with their details for the pricing page."""
        result = []
        for key, tier in TIERS.items():
            entry = tier.copy()
            entry["tier_key"] = key
            result.append(entry)
        return result
