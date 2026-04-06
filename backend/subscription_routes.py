"""
Subscription API routes.

GET  /api/subscription/status  — current tier, usage, limits
POST /api/subscription/check   — check if user can perform action (feature or model)
GET  /api/subscription/tiers   — list all available tiers with pricing
POST /api/subscription/upgrade — upgrade tier (placeholder for Stripe)
"""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from auth import get_current_user, get_optional_user
from agents.subscription_agent import SubscriptionManager

logger = logging.getLogger(__name__)

subscription_router = APIRouter(prefix="/api/subscription", tags=["subscription"])

# Singleton manager instance
_manager = SubscriptionManager()


# ── Request / Response models ───────────────────────────────────────────

class FeatureCheckRequest(BaseModel):
    feature: Optional[str] = None
    model: Optional[str] = None


class UpgradeRequest(BaseModel):
    tier: str
    # Stripe fields — placeholder for real integration
    stripe_payment_method_id: Optional[str] = None


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

    In production this would create a Stripe checkout session / subscription.
    For now it directly sets the tier (placeholder).
    """
    user_id = user["id"]
    tier_key = body.tier

    try:
        _manager.set_user_tier(
            user_id,
            tier_key,
            stripe_customer_id=None,  # Placeholder
            stripe_subscription_id=None,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    logger.info("User %s upgraded to tier: %s", user_id, tier_key)

    return {
        "success": True,
        "message": f"Upgraded to {tier_key}",
        "tier": _manager.get_user_tier(user_id),
        "usage": _manager.check_usage(user_id),
    }
