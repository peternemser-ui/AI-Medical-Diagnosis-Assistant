"""Stripe Billing Agent — manages usage tracking, subscription tiers, and billing."""

import random
import uuid
from datetime import datetime, timezone, timedelta
from collections import defaultdict


TIERS = {
    "free": {"diagnoses_per_month": 3, "price": 0, "name": "Free", "features": ["3 diagnoses/month", "Basic reports", "Email support"]},
    "starter": {"diagnoses_per_month": 50, "price": 29, "name": "Starter", "features": ["50 diagnoses/month", "PDF reports", "Priority support", "History export"]},
    "pro": {"diagnoses_per_month": 500, "price": 99, "name": "Professional", "features": ["500 diagnoses/month", "Advanced analytics", "API access", "Phone support", "Custom branding"]},
    "enterprise": {"diagnoses_per_month": -1, "price": 499, "name": "Enterprise", "features": ["Unlimited diagnoses", "Dedicated account manager", "SLA guarantee", "SSO integration", "Custom agents", "On-premise option"]},
}


class BillingAgent:
    """Manages usage tracking, subscription tiers, and Stripe billing."""

    def __init__(self):
        # In-memory storage (mock)
        self._usage: dict[str, list[dict]] = defaultdict(list)
        self._subscriptions: dict[str, dict] = {}
        self._invoices: list[dict] = []
        self._webhook_log: list[dict] = []

        # Seed demo data
        self._seed_demo_data()

    def _seed_demo_data(self):
        """Seed realistic demo data for the admin dashboard."""
        now = datetime.now(timezone.utc)

        # Demo users with various tiers
        demo_users = [
            ("user-001", "free"), ("user-002", "starter"), ("user-003", "pro"),
            ("user-004", "enterprise"), ("user-005", "starter"), ("user-006", "pro"),
            ("user-007", "free"), ("user-008", "free"), ("user-009", "starter"),
            ("user-010", "pro"), ("user-011", "free"), ("user-012", "starter"),
            ("user-013", "enterprise"), ("user-014", "free"), ("user-015", "starter"),
            ("user-016", "pro"), ("user-017", "free"), ("user-018", "free"),
            ("user-019", "starter"), ("user-020", "free"),
        ]

        for user_id, tier in demo_users:
            started = now - timedelta(days=random.randint(10, 180))
            self._subscriptions[user_id] = {
                "user_id": user_id,
                "tier": tier,
                "status": "active",
                "started_at": started.isoformat(),
                "current_period_start": (now - timedelta(days=now.day - 1)).isoformat(),
                "current_period_end": (now + timedelta(days=30 - now.day + 1)).isoformat(),
                "stripe_customer_id": f"cus_{uuid.uuid4().hex[:14]}",
                "stripe_subscription_id": f"sub_{uuid.uuid4().hex[:14]}" if tier != "free" else None,
            }

        # Seed usage records over the past 30 days
        models = ["claude-sonnet", "claude-sonnet", "claude-sonnet", "gpt-4o"]
        for user_id, tier in demo_users:
            tier_info = TIERS[tier]
            max_uses = tier_info["diagnoses_per_month"] if tier_info["diagnoses_per_month"] > 0 else 200
            num_uses = random.randint(1, min(max_uses, 30))
            for _ in range(num_uses):
                days_ago = random.randint(0, 29)
                ts = now - timedelta(days=days_ago, hours=random.randint(0, 23), minutes=random.randint(0, 59))
                model = random.choice(models)
                cost = 0.03 if "claude" in model else 0.05
                self._usage[user_id].append({
                    "diagnosis_id": f"diag-{uuid.uuid4().hex[:8]}",
                    "timestamp": ts.isoformat(),
                    "model_used": model,
                    "cost": round(cost + random.uniform(-0.01, 0.02), 4),
                    "tokens_used": random.randint(1500, 8000),
                })

        # Seed invoices
        for user_id, tier in demo_users:
            if tier == "free":
                continue
            price = TIERS[tier]["price"]
            for month_offset in range(3):
                inv_date = now - timedelta(days=30 * month_offset)
                self._invoices.append({
                    "invoice_id": f"inv_{uuid.uuid4().hex[:12]}",
                    "user_id": user_id,
                    "amount": price,
                    "currency": "usd",
                    "status": "paid" if month_offset > 0 else random.choice(["paid", "paid", "pending"]),
                    "tier": tier,
                    "created_at": inv_date.isoformat(),
                    "paid_at": inv_date.isoformat() if month_offset > 0 else None,
                })

    def check_usage(self, user_id: str) -> dict:
        """Return current usage, remaining quota, and tier info for a user."""
        sub = self._subscriptions.get(user_id)
        if not sub:
            # Default to free tier
            sub = {"user_id": user_id, "tier": "free", "status": "active"}

        tier = sub["tier"]
        tier_info = TIERS[tier]
        limit = tier_info["diagnoses_per_month"]

        # Count this month's usage
        now = datetime.now(timezone.utc)
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        month_usage = [
            u for u in self._usage.get(user_id, [])
            if u["timestamp"] >= month_start.isoformat()
        ]
        used = len(month_usage)
        remaining = max(0, limit - used) if limit > 0 else -1  # -1 = unlimited

        return {
            "user_id": user_id,
            "tier": tier,
            "tier_name": tier_info["name"],
            "price": tier_info["price"],
            "limit": limit,
            "used": used,
            "remaining": remaining,
            "unlimited": limit == -1,
            "usage_percent": round((used / limit) * 100, 1) if limit > 0 else 0,
            "period_start": sub.get("current_period_start"),
            "period_end": sub.get("current_period_end"),
        }

    def record_diagnosis(self, user_id: str, diagnosis_id: str, model_used: str, cost: float) -> dict:
        """Log a diagnosis usage event."""
        record = {
            "diagnosis_id": diagnosis_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "model_used": model_used,
            "cost": round(cost, 4),
            "tokens_used": random.randint(2000, 6000),
        }
        self._usage[user_id].append(record)
        return {"status": "recorded", "record": record}

    def get_billing_summary(self, user_id: str) -> dict:
        """Monthly breakdown, costs, and invoices for a user."""
        sub = self._subscriptions.get(user_id, {"tier": "free"})
        usage_records = self._usage.get(user_id, [])
        user_invoices = [inv for inv in self._invoices if inv["user_id"] == user_id]

        # Group usage by month
        monthly = defaultdict(lambda: {"count": 0, "cost": 0.0, "tokens": 0})
        for u in usage_records:
            month_key = u["timestamp"][:7]  # YYYY-MM
            monthly[month_key]["count"] += 1
            monthly[month_key]["cost"] += u.get("cost", 0)
            monthly[month_key]["tokens"] += u.get("tokens_used", 0)

        monthly_breakdown = [
            {"month": k, "diagnoses": v["count"], "api_cost": round(v["cost"], 2), "tokens": v["tokens"]}
            for k, v in sorted(monthly.items(), reverse=True)
        ]

        return {
            "user_id": user_id,
            "tier": sub["tier"],
            "monthly_breakdown": monthly_breakdown[:6],
            "total_diagnoses": len(usage_records),
            "total_cost": round(sum(u.get("cost", 0) for u in usage_records), 2),
            "invoices": sorted(user_invoices, key=lambda x: x["created_at"], reverse=True)[:10],
        }

    def create_checkout_session(self, user_id: str, tier: str) -> dict:
        """Create a mock Stripe checkout session URL."""
        if tier not in TIERS:
            return {"error": f"Invalid tier: {tier}"}
        if tier == "free":
            return {"error": "Cannot create checkout for free tier"}

        session_id = f"cs_{uuid.uuid4().hex[:24]}"
        return {
            "session_id": session_id,
            "url": f"https://checkout.stripe.com/pay/{session_id}",
            "tier": tier,
            "price": TIERS[tier]["price"],
            "currency": "usd",
            "mode": "subscription",
            "expires_at": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat(),
        }

    def handle_webhook(self, event: dict) -> dict:
        """Process a mock Stripe webhook event."""
        event_type = event.get("type", "unknown")
        data = event.get("data", {})
        self._webhook_log.append({
            "event_id": f"evt_{uuid.uuid4().hex[:14]}",
            "type": event_type,
            "processed_at": datetime.now(timezone.utc).isoformat(),
            "data": data,
        })

        if event_type == "checkout.session.completed":
            user_id = data.get("user_id")
            tier = data.get("tier")
            if user_id and tier:
                now = datetime.now(timezone.utc)
                self._subscriptions[user_id] = {
                    "user_id": user_id,
                    "tier": tier,
                    "status": "active",
                    "started_at": now.isoformat(),
                    "current_period_start": now.isoformat(),
                    "current_period_end": (now + timedelta(days=30)).isoformat(),
                    "stripe_customer_id": f"cus_{uuid.uuid4().hex[:14]}",
                    "stripe_subscription_id": f"sub_{uuid.uuid4().hex[:14]}",
                }

        return {"status": "processed", "event_type": event_type}

    def get_revenue_metrics(self) -> dict:
        """MRR, churn, ARPU, and other admin revenue metrics."""
        now = datetime.now(timezone.utc)
        subs = self._subscriptions

        # Tier distribution
        tier_counts = defaultdict(int)
        for s in subs.values():
            tier_counts[s["tier"]] += 1

        total_users = len(subs)
        paid_users = sum(1 for s in subs.values() if s["tier"] != "free")

        # MRR calculation
        mrr = sum(TIERS[s["tier"]]["price"] for s in subs.values())

        # ARPU (average revenue per user, paid only)
        arpu = round(mrr / paid_users, 2) if paid_users > 0 else 0

        # Usage stats across platform
        total_diagnoses_this_month = 0
        total_diagnoses_all = 0
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        daily_usage = defaultdict(int)

        for user_id, records in self._usage.items():
            total_diagnoses_all += len(records)
            for r in records:
                if r["timestamp"] >= month_start.isoformat():
                    total_diagnoses_this_month += 1
                # Build daily usage for chart (last 30 days)
                day_key = r["timestamp"][:10]
                day_dt = datetime.fromisoformat(r["timestamp"].replace("Z", "+00:00"))
                if (now - day_dt).days <= 30:
                    daily_usage[day_key] += 1

        # Build daily chart data (last 14 days)
        daily_chart = []
        for i in range(14, -1, -1):
            day = (now - timedelta(days=i)).strftime("%Y-%m-%d")
            daily_chart.append({"date": day, "diagnoses": daily_usage.get(day, 0)})

        # Recent transactions
        recent_transactions = sorted(self._invoices, key=lambda x: x["created_at"], reverse=True)[:15]

        # Churn rate (mock — 2-5%)
        churn_rate = round(random.uniform(2.0, 5.0), 1)

        return {
            "mrr": mrr,
            "arr": mrr * 12,
            "total_users": total_users,
            "paid_users": paid_users,
            "free_users": total_users - paid_users,
            "arpu": arpu,
            "churn_rate": churn_rate,
            "tier_distribution": dict(tier_counts),
            "total_diagnoses_this_month": total_diagnoses_this_month,
            "total_diagnoses_all_time": total_diagnoses_all,
            "daily_usage": daily_chart,
            "recent_transactions": recent_transactions,
            "growth_rate": round(random.uniform(5.0, 15.0), 1),
        }

    def get_platform_usage(self) -> dict:
        """Platform-wide usage statistics for admin."""
        now = datetime.now(timezone.utc)
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        total_calls = sum(len(records) for records in self._usage.values())
        month_calls = 0
        model_counts = defaultdict(int)
        total_cost = 0.0

        for records in self._usage.values():
            for r in records:
                total_cost += r.get("cost", 0)
                model_counts[r.get("model_used", "unknown")] += 1
                if r["timestamp"] >= month_start.isoformat():
                    month_calls += 1

        return {
            "total_api_calls": total_calls,
            "calls_this_month": month_calls,
            "total_cost": round(total_cost, 2),
            "models_used": dict(model_counts),
            "active_users": len(self._usage),
            "avg_calls_per_user": round(total_calls / max(len(self._usage), 1), 1),
        }

    def get_plans(self) -> list:
        """Return all available subscription plans."""
        plans = []
        for tier_id, info in TIERS.items():
            plans.append({
                "id": tier_id,
                "name": info["name"],
                "price": info["price"],
                "diagnoses_per_month": info["diagnoses_per_month"],
                "unlimited": info["diagnoses_per_month"] == -1,
                "features": info["features"],
                "popular": tier_id == "pro",
            })
        return plans


# Singleton
_billing_agent = None


def get_billing_agent() -> BillingAgent:
    global _billing_agent
    if _billing_agent is None:
        _billing_agent = BillingAgent()
    return _billing_agent
