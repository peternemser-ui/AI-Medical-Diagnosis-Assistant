"""
Stripe Payment Integration

Handles:
- Checkout session creation
- Subscription management
- Webhook processing
- Billing portal
"""
import os
import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# Stripe price IDs (set these in .env or here as defaults)
STRIPE_PRICES = {
    "plus_monthly": os.getenv("STRIPE_PRICE_PLUS_MONTHLY", "price_plus_monthly"),
    "plus_annual": os.getenv("STRIPE_PRICE_PLUS_ANNUAL", "price_plus_annual"),
    "pro_monthly": os.getenv("STRIPE_PRICE_PRO_MONTHLY", "price_pro_monthly"),
    "pro_annual": os.getenv("STRIPE_PRICE_PRO_ANNUAL", "price_pro_annual"),
    "family_monthly": os.getenv("STRIPE_PRICE_FAMILY_MONTHLY", "price_family_monthly"),
    "family_annual": os.getenv("STRIPE_PRICE_FAMILY_ANNUAL", "price_family_annual"),
}

class StripeService:
    def __init__(self):
        self.api_key = os.getenv("STRIPE_SECRET_KEY", "")
        self.webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET", "")
        self.enabled = bool(self.api_key and self.api_key.startswith("sk_"))

    def create_checkout_session(self, user_id, user_email, tier, billing="monthly", success_url="", cancel_url=""):
        """Create a Stripe Checkout session. Returns session URL."""
        if not self.enabled:
            # Demo mode — simulate successful checkout
            logger.info("Stripe not configured — using demo mode for %s -> %s", user_email, tier)
            from agents.subscription_agent import SubscriptionManager
            sub = SubscriptionManager()
            sub.set_user_tier(user_id, tier)
            return {"url": success_url or "/settings", "demo": True, "tier": tier}

        try:
            import stripe
            stripe.api_key = self.api_key
            price_key = f"{tier}_{billing}"
            price_id = STRIPE_PRICES.get(price_key)
            if not price_id:
                return {"error": f"No price configured for {price_key}"}

            session = stripe.checkout.Session.create(
                customer_email=user_email,
                payment_method_types=["card"],
                line_items=[{"price": price_id, "quantity": 1}],
                mode="subscription",
                success_url=success_url or "http://localhost:3000/settings?upgraded=true",
                cancel_url=cancel_url or "http://localhost:3000/pricing",
                metadata={"user_id": user_id, "tier": tier},
            )
            return {"url": session.url, "session_id": session.id}
        except ImportError:
            logger.warning("stripe package not installed — using demo mode")
            from agents.subscription_agent import SubscriptionManager
            sub = SubscriptionManager()
            sub.set_user_tier(user_id, tier)
            return {"url": success_url or "/settings", "demo": True, "tier": tier}
        except Exception as e:
            logger.error("Stripe error: %s", e)
            return {"error": str(e)}

    def create_billing_portal(self, customer_id, return_url=""):
        """Create a Stripe billing portal session."""
        if not self.enabled:
            return {"url": "/settings", "demo": True}
        try:
            import stripe
            stripe.api_key = self.api_key
            session = stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=return_url or "http://localhost:3000/settings",
            )
            return {"url": session.url}
        except Exception as e:
            return {"error": str(e)}

    def handle_webhook(self, payload, sig_header):
        """Process Stripe webhook events."""
        if not self.enabled:
            return {"status": "demo_mode"}
        try:
            import stripe
            stripe.api_key = self.api_key
            event = stripe.Webhook.construct_event(payload, sig_header, self.webhook_secret)

            if event["type"] == "checkout.session.completed":
                session = event["data"]["object"]
                user_id = session["metadata"].get("user_id")
                tier = session["metadata"].get("tier")
                if user_id and tier:
                    from agents.subscription_agent import SubscriptionManager
                    sub = SubscriptionManager()
                    sub.set_user_tier(user_id, tier)
                    logger.info("Stripe: upgraded user %s to %s", user_id, tier)

            elif event["type"] == "customer.subscription.deleted":
                # Downgrade to free
                session = event["data"]["object"]
                user_id = session["metadata"].get("user_id", "")
                if user_id:
                    from agents.subscription_agent import SubscriptionManager
                    sub = SubscriptionManager()
                    sub.set_user_tier(user_id, "free")

            return {"status": "ok", "type": event["type"]}
        except Exception as e:
            logger.error("Webhook error: %s", e)
            return {"error": str(e)}
