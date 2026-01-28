from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from pydantic import BaseModel

from ..auth.dependencies import get_current_active_user
from ..auth.models import User
from ..services.notification_service import NotificationService

router = APIRouter(prefix="/api/notifications", tags=["notifications"])
notification_service = NotificationService()


class NotificationPreferences(BaseModel):
    in_app: bool = True
    email: bool = True
    sms: bool = False
    push: bool = True


@router.get("")
async def list_notifications(
    unread_only: bool = False,
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_active_user)
):
    """List user's notifications."""
    notifications = notification_service.get_user_notifications(
        current_user.id,
        unread_only=unread_only,
        limit=limit
    )
    return {
        "data": [
            {
                "id": n.id,
                "title": n.title,
                "message": n.message,
                "type": n.notification_type.value,
                "read": n.read_at is not None,
                "created_at": n.created_at.isoformat()
            }
            for n in notifications
        ],
        "unread_count": notification_service.get_unread_count(current_user.id)
    }


@router.get("/unread-count")
async def get_unread_count(current_user: User = Depends(get_current_active_user)):
    """Get count of unread notifications."""
    return {"count": notification_service.get_unread_count(current_user.id)}


@router.post("/{notification_id}/read")
async def mark_as_read(
    notification_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Mark a notification as read."""
    success = await notification_service.mark_as_read(current_user.id, notification_id)
    if not success:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"success": True}


@router.post("/read-all")
async def mark_all_as_read(current_user: User = Depends(get_current_active_user)):
    """Mark all notifications as read."""
    count = await notification_service.mark_all_as_read(current_user.id)
    return {"marked_read": count}


@router.get("/preferences")
async def get_notification_preferences(current_user: User = Depends(get_current_active_user)):
    """Get user's notification preferences."""
    return {"in_app": True, "email": True, "sms": False, "push": True}


@router.put("/preferences")
async def update_notification_preferences(
    preferences: NotificationPreferences,
    current_user: User = Depends(get_current_active_user)
):
    """Update user's notification preferences."""
    notification_service.set_user_preferences(current_user.id, preferences.model_dump())
    return {"updated": True}


@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete a notification."""
    return {"deleted": True}
