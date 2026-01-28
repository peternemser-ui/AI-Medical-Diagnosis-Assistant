import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def mock_openai():
    """Mock OpenAI API responses."""
    with patch('ai_engine.openai') as mock:
        mock.ChatCompletion.create.return_value = Mock(
            choices=[
                Mock(message=Mock(content='{"diagnoses": [{"condition": "Test", "confidence": 80}]}'))
            ]
        )
        yield mock


@pytest.fixture
def mock_azure_speech():
    """Mock Azure Speech Services."""
    with patch('ai_engine.speechsdk') as mock:
        yield mock


@pytest.fixture
def sample_symptoms():
    """Sample symptom data for testing."""
    return {
        "symptoms": "severe headache with nausea and sensitivity to light",
        "duration": "3 days",
        "severity": 7
    }


@pytest.fixture
def sample_diagnosis():
    """Sample diagnosis response."""
    return {
        "diagnoses": [
            {
                "condition": "Migraine",
                "confidence": 85,
                "description": "A neurological condition causing severe headaches",
                "urgency": "soon",
                "symptoms": ["headache", "nausea", "light sensitivity"],
                "recommendations": ["Rest in dark room", "Stay hydrated", "OTC pain relievers"]
            },
            {
                "condition": "Tension Headache",
                "confidence": 60,
                "description": "Common headache from muscle tension",
                "urgency": "routine",
                "symptoms": ["headache", "neck tension"],
                "recommendations": ["Rest", "Stress management"]
            }
        ],
        "red_flags": [],
        "follow_up_questions": ["Have you experienced migraines before?"]
    }


@pytest.fixture
def sample_drug_search():
    """Sample drug search results."""
    return {
        "drugs": [
            {"rxcui": "5640", "name": "Ibuprofen", "strength": "200mg"},
            {"rxcui": "5641", "name": "Ibuprofen", "strength": "400mg"}
        ]
    }


@pytest.fixture
def sample_user():
    """Sample user data."""
    return {
        "id": "user_123",
        "email": "test@example.com",
        "name": "Test User"
    }


@pytest.fixture
def auth_headers(sample_user):
    """Generate authentication headers."""
    return {
        "Authorization": "Bearer test_token_123",
        "Content-Type": "application/json"
    }
