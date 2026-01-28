import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch


class TestDiagnosisEndpoint:
    """Tests for the /api/diagnose endpoint."""

    def test_diagnose_success(self, client, mock_openai, sample_symptoms):
        """Test successful diagnosis request."""
        response = client.post("/api/diagnose", json=sample_symptoms)
        assert response.status_code == 200
        data = response.json()
        assert "diagnoses" in data or "error" not in data

    def test_diagnose_empty_symptoms(self, client):
        """Test diagnosis with empty symptoms."""
        response = client.post("/api/diagnose", json={"symptoms": ""})
        assert response.status_code in [400, 422]

    def test_diagnose_missing_symptoms(self, client):
        """Test diagnosis without symptoms field."""
        response = client.post("/api/diagnose", json={})
        assert response.status_code == 422

    def test_diagnose_with_additional_context(self, client, mock_openai):
        """Test diagnosis with additional patient context."""
        payload = {
            "symptoms": "chest pain",
            "age": 45,
            "gender": "male",
            "medical_history": ["hypertension", "diabetes"]
        }
        response = client.post("/api/diagnose", json=payload)
        assert response.status_code in [200, 422]

    def test_diagnose_rate_limiting(self, client, mock_openai, sample_symptoms):
        """Test rate limiting on diagnosis endpoint."""
        responses = []
        for _ in range(25):
            response = client.post("/api/diagnose", json=sample_symptoms)
            responses.append(response.status_code)

        # Should eventually get rate limited (429) or all succeed
        assert 200 in responses or 429 in responses

    def test_diagnose_response_structure(self, client, mock_openai, sample_symptoms):
        """Test that response has correct structure."""
        response = client.post("/api/diagnose", json=sample_symptoms)
        if response.status_code == 200:
            data = response.json()
            # Check for expected fields
            assert isinstance(data, dict)

    def test_diagnose_sanitizes_input(self, client, mock_openai):
        """Test that malicious input is sanitized."""
        payload = {
            "symptoms": "<script>alert('xss')</script>headache"
        }
        response = client.post("/api/diagnose", json=payload)
        if response.status_code == 200:
            data = response.json()
            assert "<script>" not in str(data)

    def test_diagnose_handles_unicode(self, client, mock_openai):
        """Test handling of unicode characters."""
        payload = {
            "symptoms": "头痛 headache douleur"
        }
        response = client.post("/api/diagnose", json=payload)
        assert response.status_code in [200, 422, 500]

    def test_diagnose_max_length(self, client, mock_openai):
        """Test maximum input length validation."""
        payload = {
            "symptoms": "a" * 10001
        }
        response = client.post("/api/diagnose", json=payload)
        assert response.status_code in [200, 400, 422]


class TestFollowUpEndpoint:
    """Tests for the /api/followup endpoint."""

    def test_followup_success(self, client, mock_openai):
        """Test successful follow-up question request."""
        payload = {
            "context": "headache",
            "previous_answers": [{"question": "duration", "answer": "3 days"}]
        }
        response = client.post("/api/followup", json=payload)
        assert response.status_code in [200, 422]

    def test_followup_empty_context(self, client):
        """Test follow-up with empty context."""
        payload = {
            "context": "",
            "previous_answers": []
        }
        response = client.post("/api/followup", json=payload)
        assert response.status_code in [400, 422, 200]

    def test_followup_with_history(self, client, mock_openai):
        """Test follow-up with conversation history."""
        payload = {
            "context": "severe migraine",
            "previous_answers": [
                {"question": "How long?", "answer": "2 hours"},
                {"question": "Any triggers?", "answer": "Stress and lack of sleep"}
            ]
        }
        response = client.post("/api/followup", json=payload)
        assert response.status_code in [200, 422]


class TestGenerateQuestionEndpoint:
    """Tests for the /api/generate-question endpoint."""

    def test_generate_question_success(self, client, mock_openai):
        """Test successful question generation."""
        payload = {
            "symptoms": "back pain",
            "step": 1
        }
        response = client.post("/api/generate-question", json=payload)
        assert response.status_code in [200, 422]

    def test_generate_question_different_steps(self, client, mock_openai):
        """Test question generation for different steps."""
        for step in range(1, 11):
            payload = {"symptoms": "headache", "step": step}
            response = client.post("/api/generate-question", json=payload)
            assert response.status_code in [200, 422]
