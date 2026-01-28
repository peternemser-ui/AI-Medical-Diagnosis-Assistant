from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from datetime import datetime

from ..auth.dependencies import get_admin_user
from ..auth.models import User

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/users")
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    role: Optional[str] = None,
    search: Optional[str] = None,
    admin: User = Depends(get_admin_user)
):
    """List all users with pagination and filters."""
    return {
        "data": [],
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": 0,
            "total_pages": 0
        }
    }


@router.get("/users/{user_id}")
async def get_user(user_id: str, admin: User = Depends(get_admin_user)):
    """Get user details."""
    return {"id": user_id, "name": "User", "email": "user@example.com"}


@router.put("/users/{user_id}")
async def update_user(user_id: str, data: dict, admin: User = Depends(get_admin_user)):
    """Update user information."""
    return {"id": user_id, "updated": True}


@router.delete("/users/{user_id}")
async def delete_user(user_id: str, admin: User = Depends(get_admin_user)):
    """Delete a user."""
    return {"deleted": True}


@router.post("/users/{user_id}/disable")
async def disable_user(user_id: str, admin: User = Depends(get_admin_user)):
    """Disable a user account."""
    return {"id": user_id, "disabled": True}


@router.post("/users/{user_id}/enable")
async def enable_user(user_id: str, admin: User = Depends(get_admin_user)):
    """Enable a user account."""
    return {"id": user_id, "enabled": True}


@router.get("/diagnoses")
async def list_diagnoses(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    urgency: Optional[str] = None,
    admin: User = Depends(get_admin_user)
):
    """List all diagnoses with filters."""
    return {"data": [], "pagination": {"page": page, "total": 0}}


@router.get("/diagnoses/{diagnosis_id}")
async def get_diagnosis(diagnosis_id: str, admin: User = Depends(get_admin_user)):
    """Get diagnosis details."""
    return {"id": diagnosis_id}


@router.post("/diagnoses/{diagnosis_id}/review")
async def review_diagnosis(
    diagnosis_id: str,
    notes: str,
    admin: User = Depends(get_admin_user)
):
    """Mark diagnosis as reviewed."""
    return {"id": diagnosis_id, "reviewed": True, "reviewed_by": admin.id}


@router.get("/stats")
async def get_admin_stats(admin: User = Depends(get_admin_user)):
    """Get admin dashboard statistics."""
    return {
        "total_users": 0,
        "total_diagnoses": 0,
        "active_sessions": 0,
        "urgent_cases": 0
    }


@router.get("/settings")
async def get_settings(admin: User = Depends(get_admin_user)):
    """Get system settings."""
    return {"ai_model": "gpt-4o", "rate_limit": 20}


@router.put("/settings")
async def update_settings(settings: dict, admin: User = Depends(get_admin_user)):
    """Update system settings."""
    return {"updated": True}
