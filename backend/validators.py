"""
Request Validation Utilities
"""
from pydantic import BaseModel, validator, Field
from typing import Optional, List
import re


class DiagnosisRequest(BaseModel):
    """Enhanced diagnosis request validation"""
    age: int = Field(..., ge=0, le=150, description="Patient age (0-150)")
    gender: str = Field(..., min_length=1, max_length=50, description="Patient gender")
    symptoms: str = Field(..., min_length=5, max_length=10000, description="Symptoms description")
    duration: Optional[str] = Field(None, max_length=500, description="Symptom duration")
    severity: Optional[int] = Field(None, ge=1, le=10, description="Severity rating (1-10)")
    medical_history: Optional[str] = Field(None, max_length=5000, description="Medical history")
    medications: Optional[List[str]] = Field(default=[], description="Current medications")
    allergies: Optional[List[str]] = Field(default=[], description="Known allergies")
    body_areas: Optional[List[str]] = Field(default=[], description="Affected body areas")

    @validator('gender')
    def validate_gender(cls, v):
        """Validate gender field"""
        if not v or not v.strip():
            raise ValueError('Gender cannot be empty')

        # Normalize gender
        v = v.strip().lower()
        valid_genders = ['male', 'female', 'man', 'woman', 'non-binary', 'nonbinary', 'other', 'prefer not to say']

        # Allow any gender input, but warn if unusual
        if not any(gender in v for gender in valid_genders):
            # Just pass through, don't reject
            pass

        return v

    @validator('symptoms')
    def validate_symptoms(cls, v):
        """Validate symptoms field"""
        if not v or not v.strip():
            raise ValueError('Symptoms cannot be empty')

        # Check for minimum meaningful content
        v = v.strip()
        if len(v) < 5:
            raise ValueError('Symptoms description must be at least 5 characters')

        # Check for gibberish
        if re.match(r'^(.)\1+$', v):
            raise ValueError('Please provide a meaningful symptom description')

        return v

    @validator('medical_history', 'duration')
    def validate_text_fields(cls, v):
        """Validate optional text fields"""
        if v:
            v = v.strip()
            # Remove null bytes
            v = v.replace('\x00', '')
        return v

    @validator('medications', 'allergies', 'body_areas', pre=True)
    def validate_lists(cls, v):
        """Validate list fields"""
        if v is None:
            return []

        if not isinstance(v, list):
            return []

        # Filter out empty strings
        return [item.strip() for item in v if item and item.strip()]


class FollowupRequest(BaseModel):
    """Followup question request validation"""
    question: str = Field(..., min_length=1, max_length=1000, description="Followup question")
    context: Optional[str] = Field(None, max_length=10000, description="Conversation context")
    diagnosis_id: Optional[str] = Field(None, description="Associated diagnosis ID")

    @validator('question')
    def validate_question(cls, v):
        """Validate question field"""
        if not v or not v.strip():
            raise ValueError('Question cannot be empty')

        v = v.strip()
        return v


class GenerateQuestionRequest(BaseModel):
    """AI question generation request validation"""
    context: str = Field(..., min_length=5, max_length=10000, description="Current context")
    symptoms: Optional[str] = Field(None, max_length=5000, description="Current symptoms")
    previous_questions: Optional[List[str]] = Field(default=[], description="Previously asked questions")

    @validator('context')
    def validate_context(cls, v):
        """Validate context field"""
        if not v or not v.strip():
            raise ValueError('Context cannot be empty')

        return v.strip()

    @validator('previous_questions', pre=True)
    def validate_previous_questions(cls, v):
        """Validate previous questions"""
        if v is None:
            return []

        if not isinstance(v, list):
            return []

        return [q.strip() for q in v if q and q.strip()]


class ImageAnalysisRequest(BaseModel):
    """Image analysis request validation"""
    image_data: str = Field(..., description="Base64 encoded image data")
    image_type: str = Field(..., description="Image MIME type")
    description: Optional[str] = Field(None, max_length=1000, description="Image description")

    @validator('image_type')
    def validate_image_type(cls, v):
        """Validate image MIME type"""
        valid_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/gif']

        if v.lower() not in valid_types:
            raise ValueError(f'Invalid image type. Allowed: {", ".join(valid_types)}')

        return v.lower()

    @validator('image_data')
    def validate_image_data(cls, v):
        """Validate base64 image data"""
        if not v or not v.strip():
            raise ValueError('Image data cannot be empty')

        # Check if it's base64 format
        if not re.match(r'^[A-Za-z0-9+/]+=*$', v):
            raise ValueError('Invalid base64 image data')

        # Check size (rough estimate: 10MB max)
        if len(v) > 14000000:  # ~10MB in base64
            raise ValueError('Image too large (max 10MB)')

        return v


class DrugSearchRequest(BaseModel):
    """Drug search request validation"""
    query: str = Field(..., min_length=2, max_length=200, description="Drug name or query")
    limit: Optional[int] = Field(10, ge=1, le=50, description="Maximum results")

    @validator('query')
    def validate_query(cls, v):
        """Validate search query"""
        if not v or not v.strip():
            raise ValueError('Search query cannot be empty')

        v = v.strip()

        # Remove special characters that might cause issues
        v = re.sub(r'[<>"\']', '', v)

        return v


class DrugInteractionRequest(BaseModel):
    """Drug interaction check request validation"""
    drug_ids: List[str] = Field(..., min_items=2, max_items=10, description="Drug RxCUI IDs")

    @validator('drug_ids')
    def validate_drug_ids(cls, v):
        """Validate drug IDs"""
        if not v or len(v) < 2:
            raise ValueError('At least 2 drugs are required for interaction check')

        if len(v) > 10:
            raise ValueError('Maximum 10 drugs allowed for interaction check')

        # Validate each ID is numeric
        for drug_id in v:
            if not drug_id.strip().isdigit():
                raise ValueError(f'Invalid drug ID: {drug_id}')

        return [drug_id.strip() for drug_id in v]
