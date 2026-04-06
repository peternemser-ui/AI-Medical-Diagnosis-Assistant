"""
Subscription API routes.

GET  /api/subscription/status  — current tier, usage, limits
POST /api/subscription/check   — check if user can perform action (feature or model)
GET  /api/subscription/tiers   — list all available tiers with pricing
POST /api/subscription/upgrade — create Stripe checkout session (or demo mode upgrade)
POST /api/subscription/webhook — Stripe webhook handler
POST /api/subscription/billing-portal — Stripe billing portal session
"""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from auth import get_current_user, get_optional_user
from agents.subscription_agent import SubscriptionManager
from stripe_service import StripeService
from email_service import EmailService

logger = logging.getLogger(__name__)

subscription_router = APIRouter(prefix="/api/subscription", tags=["subscription"])

# Singleton instances
_manager = SubscriptionManager()
_stripe = StripeService()
_email = EmailService()


# ── Request / Response models ───────────────────────────────────────────

class FeatureCheckRequest(BaseModel):
    feature: Optional[str] = None
    model: Optional[str] = None


class UpgradeRequest(BaseModel):
    tier: str
    billing: str = "monthly"
    success_url: Optional[str] = None
    cancel_url: Optional[str] = None


class BillingPortalRequest(BaseModel):
    return_url: Optional[str] = None


# ── Endpoints ───────────────────────────────────────────────────────────

@subscription_router.get("/status")
async def subscription_status(user: dict = Depends(get_current_user)):
    """Return the user's current subscription tier, usage, and limits."""
    user_id = user["id"]
    tier_info = _manager.get_user_tier(user_id)
    usage = _manager.check_usage(user_id)
    return {
        "tier": tier_info,
        "usage": usage,
    }


@subscription_router.post("/check")
async def subscription_check(body: FeatureCheckRequest, user: dict = Depends(get_current_user)):
    """Check if the user can use a specific feature or model."""
    user_id = user["id"]

    result = {"allowed": True, "upgrade_prompt": None}

    if body.feature:
        if not _manager.can_use_feature(user_id, body.feature):
            result["allowed"] = False
            result["upgrade_prompt"] = _manager.get_upgrade_prompt(user_id, body.feature)

    if body.model:
        if not _manager.can_use_model(user_id, body.model):
            result["allowed"] = False
            result["upgrade_prompt"] = _manager.get_upgrade_prompt(user_id, body.model)

    return result


@subscription_router.get("/tiers")
async def list_tiers():
    """Return all subscription tiers with pricing and features (public)."""
    return {"tiers": _manager.get_all_tiers()}


@subscription_router.post("/upgrade")
async def upgrade_tier(body: UpgradeRequest, user: dict = Depends(get_current_user)):
    """
    Upgrade user's subscription tier.

    Creates a Stripe Checkout session when Stripe is configured.
    Falls back to direct tier upgrade in demo mode.
    """
    user_id = user["id"]
    tier_key = body.tier

    # Validate tier exists
    all_tiers = _manager.get_all_tiers()
    valid_keys = [t["tier_key"] for t in all_tiers] if isinstance(all_tiers, list) else list(all_tiers.keys()) if isinstance(all_tiers, dict) else []
    if tier_key not in valid_keys and tier_key not in ("free", "plus", "pro", "family"):
        raise HTTPException(status_code=400, detail=f"Invalid tier: {tier_key}")

    result = _stripe.create_checkout_session(
        user_id=user_id,
        user_email=user.get("email", ""),
        tier=tier_key,
        billing=body.billing,
        success_url=body.success_url or "",
        cancel_url=body.cancel_url or "",
    )

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    logger.info("User %s upgrade to %s — demo=%s", user_id, tier_key, result.get("demo", False))

    # If demo mode (instant upgrade), send confirmation email
    if result.get("demo"):
        tier_prices = {"plus": 9.99, "pro": 29.99, "family": 49.99}
        price = tier_prices.get(tier_key, 0)
        _email.send_upgrade_confirmation(
            email=user.get("email", ""),
            name=user.get("name", "User"),
            tier=tier_key,
            price=price,
        )

    return {
        "success": True,
        "url": result.get("url", "/settings"),
        "demo": result.get("demo", False),
        "session_id": result.get("session_id"),
        "tier": _manager.get_user_tier(user_id),
        "usage": _manager.check_usage(user_id),
    }


@subscription_router.post("/webhook")
async def stripe_webhook(request: Request):
    """Handle Stripe webhook events (checkout complete, subscription cancelled, etc.)."""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")

    result = _stripe.handle_webhook(payload, sig_header)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result


@subscription_router.post("/billing-portal")
async def billing_portal(body: BillingPortalRequest, user: dict = Depends(get_current_user)):
    """Create a Stripe billing portal session for the user to manage their subscription."""
    tier_info = _manager.get_user_tier(user["id"])
    customer_id = tier_info.get("stripe_customer_id") if isinstance(tier_info, dict) else None

    if not customer_id and not _stripe.enabled:
        # Demo mode — just redirect to settings
        return {"url": body.return_url or "/settings", "demo": True}

    if not customer_id:
        raise HTTPException(status_code=400, detail="No Stripe customer found. Please upgrade first.")

    result = _stripe.create_billing_portal(
        customer_id=customer_id,
        return_url=body.return_url or "",
    )

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result
