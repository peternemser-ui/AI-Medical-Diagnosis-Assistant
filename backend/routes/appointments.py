from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from datetime import datetime, date
from pydantic import BaseModel

from ..auth.dependencies import get_current_active_user
from ..auth.models import User

router = APIRouter(prefix="/api/appointments", tags=["appointments"])


class AppointmentCreate(BaseModel):
    title: str
    description: Optional[str] = None
    appointment_type: str = "in-person"
    specialty: Optional[str] = None
    scheduled_at: datetime
    duration_minutes: int = 30
    provider_id: Optional[str] = None
    location: Optional[str] = None


class AppointmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    status: Optional[str] = None


@router.get("")
async def list_appointments(
    status: Optional[str] = None,
    upcoming_only: bool = False,
    current_user: User = Depends(get_current_active_user)
):
    """List user's appointments."""
    return {"data": [], "count": 0}


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_appointment(
    appointment: AppointmentCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a new appointment."""
    return {"id": "new-appointment-id", **appointment.model_dump()}


@router.get("/{appointment_id}")
async def get_appointment(
    appointment_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get appointment details."""
    return {"id": appointment_id}


@router.put("/{appointment_id}")
async def update_appointment(
    appointment_id: str,
    data: AppointmentUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update an appointment."""
    return {"id": appointment_id, "updated": True}


@router.delete("/{appointment_id}")
async def cancel_appointment(
    appointment_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Cancel an appointment."""
    return {"id": appointment_id, "cancelled": True}


@router.get("/available-slots")
async def get_available_slots(
    provider_id: str,
    date: date,
    current_user: User = Depends(get_current_active_user)
):
    """Get available appointment slots for a provider."""
    return {"slots": [], "date": str(date)}


@router.post("/{appointment_id}/confirm")
async def confirm_appointment(
    appointment_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Confirm an appointment."""
    return {"id": appointment_id, "confirmed": True}


@router.post("/{appointment_id}/reschedule")
async def reschedule_appointment(
    appointment_id: str,
    new_time: datetime,
    current_user: User = Depends(get_current_active_user)
):
    """Reschedule an appointment."""
    return {"id": appointment_id, "rescheduled": True, "new_time": new_time}
