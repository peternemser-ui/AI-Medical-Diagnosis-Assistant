from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum
import uuid


class UrgencyLevel(str, Enum):
    ROUTINE = "routine"
    SOON = "soon"
    URGENT = "urgent"
    EMERGENCY = "emergency"


class DiagnosisStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    REVIEWED = "reviewed"
    ARCHIVED = "archived"


class UserModel(BaseModel):
    """Database model for users."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: str
    name: str
    hashed_password: str
    role: str = "patient"
    email_verified: bool = False
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Profile fields
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

    # Medical profile
    blood_type: Optional[str] = None
    allergies: Optional[List[str]] = []
    medications: Optional[List[str]] = []
    conditions: Optional[List[str]] = []
    emergency_contact: Optional[str] = None


class DiagnosisModel(BaseModel):
    """Database model for diagnoses."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    session_id: Optional[str] = None

    # Input
    symptoms: List[str]
    symptom_description: str
    duration: Optional[str] = None
    severity: Optional[int] = None
    body_location: Optional[str] = None
    image_url: Optional[str] = None

    # AI Response
    conditions: List[dict] = []  # [{name, confidence, description}]
    recommendations: List[str] = []
    urgency: UrgencyLevel = UrgencyLevel.ROUTINE
    red_flags: List[str] = []
    follow_up_questions: List[str] = []

    # Metadata
    status: DiagnosisStatus = DiagnosisStatus.PENDING
    ai_model: str = "gpt-4o"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Review
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    review_notes: Optional[str] = None


class SessionModel(BaseModel):
    """Database model for user sessions."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    token: str
    device_info: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime
    last_activity: datetime = Field(default_factory=datetime.utcnow)


class MedicalHistoryModel(BaseModel):
    """Database model for medical history entries."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    diagnosis_id: Optional[str] = None

    entry_type: str  # symptom, diagnosis, medication, procedure, test
    title: str
    description: Optional[str] = None
    date: datetime
    provider: Optional[str] = None
    notes: Optional[str] = None

    # Attachments
    attachments: List[str] = []

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ConversationModel(BaseModel):
    """Database model for conversation history."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    diagnosis_id: Optional[str] = None

    messages: List[dict] = []  # [{role, content, timestamp}]

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class DrugInteractionModel(BaseModel):
    """Database model for tracked drug interactions."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str

    drugs: List[str]
    severity: str  # minor, moderate, major
    description: str
    recommendations: List[str] = []

    checked_at: datetime = Field(default_factory=datetime.utcnow)


class AppointmentModel(BaseModel):
    """Database model for appointments."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    provider_id: Optional[str] = None

    title: str
    description: Optional[str] = None
    appointment_type: str  # in-person, telemedicine
    specialty: Optional[str] = None

    scheduled_at: datetime
    duration_minutes: int = 30
    status: str = "scheduled"  # scheduled, confirmed, completed, cancelled

    location: Optional[str] = None
    video_link: Optional[str] = None
    notes: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
