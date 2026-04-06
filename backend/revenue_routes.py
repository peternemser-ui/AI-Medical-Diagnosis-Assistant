"""
Revenue feature routes: API-as-a-Service, White-Label, and Referral Tracking.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from api_service import api_key_manager, PLANS
from whitelabel import get_whitelabel_config, update_whitelabel_config
from referral_tracker import referral_tracker

revenue_router = APIRouter(tags=["revenue"])


# ── API-as-a-Service ────────────────────────────────────────────────


class CreateKeyRequest(BaseModel):
    developer_name: str
    email: str
    plan: str = "starter"


@revenue_router.post("/api/developer/keys")
async def create_api_key(req: CreateKeyRequest):
    """Create a new developer API key (admin only)."""
    if req.plan not in PLANS:
        raise HTTPException(status_code=400, detail=f"Invalid plan. Choose from: {list(PLANS.keys())}")
    key = api_key_manager.create_key(req.developer_name, req.email, req.plan)
    return {"key": key, "plan": req.plan, "message": "API key created successfully"}


@revenue_router.get("/api/developer/keys")
async def list_api_keys():
    """List all developer API keys (admin only)."""
    keys = api_key_manager.get_all_keys()
    items = []
    for key_id, info in keys.items():
        items.append({
            "key": key_id,
            "developer": info["developer"],
            "email": info["email"],
            "plan": info["plan"],
            "active": info["active"],
            "calls_this_month": info["calls_this_month"],
            "total_calls": info["total_calls"],
            "created": info["created"],
        })
    return {"keys": items, "total": len(items)}


@revenue_router.delete("/api/developer/keys/{key}")
async def revoke_api_key(key: str):
    """Revoke a developer API key (admin only)."""
    success = api_key_manager.revoke_key(key)
    if not success:
        raise HTTPException(status_code=404, detail="API key not found")
    return {"message": "API key revoked", "key": key}


@revenue_router.get("/api/developer/usage")
async def get_developer_usage():
    """Get aggregate developer API usage stats (admin only)."""
    stats = api_key_manager.get_usage_stats()
    daily_usage = api_key_manager.get_usage()
    return {**stats, "daily_usage": daily_usage}


# ── White-Label ─────────────────────────────────────────────────────


class WhiteLabelUpdateRequest(BaseModel):
    brand_name: Optional[str] = None
    tagline: Optional[str] = None
    logo_url: Optional[str] = None
    primary_color: Optional[str] = None
    accent_color: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    disclaimer: Optional[str] = None
    powered_by: Optional[bool] = None


@revenue_router.get("/api/whitelabel/config")
async def get_whitelabel():
    """Get current white-label configuration."""
    return get_whitelabel_config()


@revenue_router.post("/api/whitelabel/config")
async def update_whitelabel(req: WhiteLabelUpdateRequest):
    """Update white-label configuration (admin only)."""
    updates = {k: v for k, v in req.dict().items() if v is not None}
    config = update_whitelabel_config(updates)
    return config


# ── Referral Tracking ───────────────────────────────────────────────


class TrackReferralRequest(BaseModel):
    user_id: str = "anonymous"
    doctor_npi: str
    doctor_name: str
    specialty: str = ""
    action_type: str  # "call", "directions", "website"
    location: str = ""


@revenue_router.post("/api/referrals/track")
async def track_referral(req: TrackReferralRequest):
    """Track a referral click (called from frontend)."""
    if req.action_type not in ("call", "directions", "website"):
        raise HTTPException(status_code=400, detail="action_type must be 'call', 'directions', or 'website'")
    click = referral_tracker.track_click(
        user_id=req.user_id,
        doctor_npi=req.doctor_npi,
        doctor_name=req.doctor_name,
        specialty=req.specialty,
        action_type=req.action_type,
        location=req.location,
    )
    return {"tracked": True, "click_id": click["id"]}


@revenue_router.get("/api/admin/referrals/stats")
async def get_referral_stats(days: int = 30):
    """Referral analytics (admin only)."""
    stats = referral_tracker.get_stats(days)
    billable = referral_tracker.get_billable_referrals(days)
    return {
        **stats,
        "qualified_referrals": billable["qualified_referrals"],
        "estimated_revenue": billable["estimated_revenue"],
        "avg_revenue_per_referral": billable["avg_revenue_per_referral"],
    }
