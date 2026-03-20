from pydantic import BaseModel
from typing import Optional


class DiagnosisRequest(BaseModel):
    symptoms: str
    age: int = 30
    gender: str = "unknown"
    duration: str = "recent"
    severity: int = 5
    image_base64: Optional[str] = None
    audio_base64: Optional[str] = None
    # Rich clinical data (optional, enhances diagnosis quality)
    medical_history: Optional[str] = None
    current_medications: Optional[str] = None
    allergies: Optional[str] = None
    family_history: Optional[str] = None
    social_history: Optional[str] = None
    # Model selection
    model_preference: str = "auto"  # "auto", "opus", "sonnet", "haiku"


class FollowupRequest(BaseModel):
    question: str
    previous_messages: list = []
    original_symptoms: str = ""
    previous_diagnosis: Optional[dict] = None


class QuestionGenerationRequest(BaseModel):
    symptoms: str = ""
    age: int = 30
    gender: str = "unknown"
    conversation_history: list[str] = []
    previous_questions: list[str] = []
    questions_asked: int = 0
    total_ai_questions: int = 4
