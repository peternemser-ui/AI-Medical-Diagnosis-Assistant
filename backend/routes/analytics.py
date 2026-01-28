from fastapi import APIRouter, Depends, Query
from typing import Optional
from datetime import datetime, timedelta

from ..auth.dependencies import get_admin_user
from ..auth.models import User
from ..services.analytics_service import AnalyticsService

router = APIRouter(prefix="/api/analytics", tags=["analytics"])
analytics_service = AnalyticsService()


@router.get("/dashboard")
async def get_dashboard_stats(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    admin: User = Depends(get_admin_user)
):
    """Get dashboard statistics."""
    stats = await analytics_service.get_dashboard_stats(start_date, end_date)
    return stats


@router.get("/trends/diagnoses")
async def get_diagnosis_trends(
    days: int = Query(30, ge=1, le=365),
    granularity: str = Query("day", regex="^(hour|day|week|month)$"),
    admin: User = Depends(get_admin_user)
):
    """Get diagnosis count trends over time."""
    trends = await analytics_service.get_diagnosis_trends(days, granularity)
    return {"trends": trends}


@router.get("/conditions")
async def get_condition_statistics(admin: User = Depends(get_admin_user)):
    """Get statistics about diagnosed conditions."""
    stats = await analytics_service.get_condition_statistics()
    return {"conditions": stats}


@router.get("/health")
async def get_system_health_metrics(admin: User = Depends(get_admin_user)):
    """Get system health metrics."""
    metrics = await analytics_service.get_system_health_metrics()
    return metrics


@router.get("/user/{user_id}/activity")
async def get_user_activity(
    user_id: str,
    limit: int = Query(50, ge=1, le=200),
    admin: User = Depends(get_admin_user)
):
    """Get activity history for a specific user."""
    activity = await analytics_service.get_user_activity(user_id, limit)
    return {"activity": activity}


@router.get("/export")
async def export_analytics_data(
    start_date: datetime,
    end_date: datetime,
    event_types: Optional[str] = None,
    admin: User = Depends(get_admin_user)
):
    """Export analytics data for a date range."""
    types = event_types.split(",") if event_types else None
    data = await analytics_service.export_data(start_date, end_date, types)
    return {"data": data, "count": len(data)}


@router.post("/track")
async def track_event(
    event_name: str,
    properties: Optional[dict] = None,
    current_user: Optional[User] = None
):
    """Track an analytics event."""
    user_id = current_user.id if current_user else None
    await analytics_service.track_event(event_name, user_id, properties)
    return {"tracked": True}
