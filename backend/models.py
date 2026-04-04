from pydantic import BaseModel, field_validator
from typing import Optional


class DiagnosisRequest(BaseModel):
    symptoms: str
    age: int = 30
    gender: str = "unknown"
    duration: str = "recent"
    severity: int = 5
    language: str = "en"  # UI language code: en, zh, es, fr, hi, de, pt, ja, ko, ar, ru, it
    image_base64: Optional[str] = None
    audio_base64: Optional[str] = None
    medical_history: Optional[str] = None
    current_medications: Optional[str] = None
    allergies: Optional[str] = None
    family_history: Optional[str] = None
    social_history: Optional[str] = None
    model_preference: str = "auto"  # "auto", "opus", "sonnet", "haiku"
    specialist_routing: Optional[list[str]] = None  # e.g. ["cardiology", "neurology"]

    @field_validator("age")
    @classmethod
    def age_must_be_reasonable(cls, v: int) -> int:
        if v < 0 or v > 150:
            raise ValueError("Age must be between 0 and 150")
        return v

    @field_validator("severity")
    @classmethod
    def severity_must_be_bounded(cls, v: int) -> int:
        return max(1, min(10, v))

    @field_validator("symptoms")
    @classmethod
    def symptoms_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Symptoms must not be empty")
        if len(v) > 10_000:
            raise ValueError("Symptoms text too long (max 10,000 characters)")
        return v.strip()


class FollowupRequest(BaseModel):
    question: str
    previous_messages: list = []
    original_symptoms: str = ""
    previous_diagnosis: Optional[dict] = None
    language: str = "en"

    @field_validator("question")
    @classmethod
    def question_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Question must not be empty")
        if len(v) > 5_000:
            raise ValueError("Question too long (max 5,000 characters)")
        return v.strip()


class InterviewRequest(BaseModel):
    """PA interview request — one round of the clinical interview."""
    conversation: list[dict] = []  # [{role: "user"|"assistant", content: "..."}]
    age: int = 0
    gender: str = "unknown"
    language: str = "en"
    model_preference: str = "auto"

    @field_validator("age")
    @classmethod
    def age_must_be_reasonable(cls, v: int) -> int:
        if v < 0 or v > 150:
            raise ValueError("Age must be between 0 and 150")
        return v


class QuestionGenerationRequest(BaseModel):
    symptoms: str = ""
    age: int = 30
    gender: str = "unknown"
    language: str = "en"
    conversation_history: list[str] = []
    previous_questions: list[str] = []
    questions_asked: int = 0
    total_ai_questions: int = 4
    mode: str = "followup"  # "followup" or "hpi_detail"
    context: Optional[str] = None  # Custom prompt override for question generation

    @field_validator("age")
    @classmethod
    def age_must_be_reasonable(cls, v: int) -> int:
        if v < 0 or v > 150:
            raise ValueError("Age must be between 0 and 150")
        return v
