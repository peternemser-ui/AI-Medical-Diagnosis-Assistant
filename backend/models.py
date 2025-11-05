from pydantic import BaseModel
from typing import Optional

class DiagnosisRequest(BaseModel):
    age: int
    gender: str
    symptoms: str
    image_base64: Optional[str] = None
    audio_base64: Optional[str] = None
