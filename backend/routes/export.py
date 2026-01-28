from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from typing import Optional
from datetime import datetime

from ..auth.dependencies import get_current_active_user
from ..auth.models import User
from ..services.export_service import ExportService, ExportFormat

router = APIRouter(prefix="/api/export", tags=["export"])
export_service = ExportService()


@router.get("/diagnosis/{diagnosis_id}")
async def export_diagnosis(
    diagnosis_id: str,
    format: str = Query("json", regex="^(json|csv|html|pdf)$"),
    current_user: User = Depends(get_current_active_user)
):
    """Export a diagnosis in the specified format."""
    diagnosis = {"id": diagnosis_id, "symptoms": [], "conditions": [], "urgency": "routine"}

    export_format = ExportFormat(format)
    content = await export_service.export_diagnosis(diagnosis, export_format)

    content_types = {
        "json": "application/json",
        "csv": "text/csv",
        "html": "text/html",
        "pdf": "application/pdf"
    }

    return Response(
        content=content,
        media_type=content_types.get(format, "application/octet-stream"),
        headers={"Content-Disposition": f"attachment; filename=diagnosis_{diagnosis_id}.{format}"}
    )


@router.get("/user-data")
async def export_user_data(
    include_diagnoses: bool = True,
    include_history: bool = True,
    include_conversations: bool = False,
    current_user: User = Depends(get_current_active_user)
):
    """Export all user data (GDPR compliance)."""
    content = await export_service.export_user_data(
        current_user.id,
        include_diagnoses=include_diagnoses,
        include_history=include_history,
        include_conversations=include_conversations
    )

    return Response(
        content=content,
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename=user_data_{current_user.id}.json"}
    )


@router.get("/diagnoses")
async def export_diagnoses(
    format: str = Query("json", regex="^(json|csv)$"),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_active_user)
):
    """Export multiple diagnoses."""
    diagnoses = []  # Would fetch from database

    export_format = ExportFormat(format)
    content = await export_service.export_diagnoses(diagnoses, export_format)

    content_types = {"json": "application/json", "csv": "text/csv"}

    return Response(
        content=content,
        media_type=content_types.get(format),
        headers={"Content-Disposition": f"attachment; filename=diagnoses.{format}"}
    )


@router.get("/history")
async def export_medical_history(
    format: str = Query("json", regex="^(json|csv)$"),
    current_user: User = Depends(get_current_active_user)
):
    """Export medical history."""
    return {"message": "Medical history export", "format": format}
