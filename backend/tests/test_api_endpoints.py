"""
Integration tests for the main FastAPI endpoints:

  GET  /health
  POST /api/diagnose  (valid payload, empty symptoms)
  GET  /api/agents
  POST /api/followup

All AI calls (Anthropic / OpenAI / Ollama) are mocked so the tests run
without any real API keys.
"""

from __future__ import annotations

import sys
import os
import json
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Make the backend package importable
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def client():
    """Create a FastAPI TestClient with all external calls mocked out."""
    from fastapi.testclient import TestClient

    # Patch Ollama check so the server doesn't try to reach a local daemon
    with patch("httpx.get", side_effect=Exception("Ollama not available in tests")):
        # Patch email service so signup tests don't fail on missing SMTP config
        with patch("email_service.EmailService.send_welcome", return_value=None), \
             patch("email_service.EmailService.send_diagnosis_complete", return_value=None), \
             patch("email_service.EmailService.send_usage_warning", return_value=None):
            from main import app
            with TestClient(app, raise_server_exceptions=False) as c:
                yield c


# ---------------------------------------------------------------------------
# Minimal mock diagnosis result matching what the orchestrator returns
# ---------------------------------------------------------------------------

_MOCK_DIAGNOSIS = {
    "answer": "Mock medical assessment for tests.",
    "confidence_scores": {"high": 0.7, "medium": 0.2, "low": 0.1},
    "causes": [
        {
            "cause": "Viral upper respiratory infection",
            "value": 75,
            "explanation": "Most common cause of sore throat + runny nose.",
            "urgency": "routine",
            "specialty": "Primary Care",
        }
    ],
    "red_flags": [],
    "additional_questions": ["How long have you had these symptoms?"],
    "recommended_tests": ["Rapid strep test"],
    "patient_summary": "Likely a common cold. Rest and fluids recommended.",
    "action_checklist": ["Rest", "Stay hydrated"],
    "safety_status": "SAFE",
    "safety_warnings": [],
    "medications": [],
    "lifestyle_recommendations": ["Rest", "Hydrate"],
    "warning_signs": ["High fever", "Difficulty breathing"],
    "follow_up_timeline": "7 days",
    "agent_details": {},
    "agent_timings": {"triage": 0.5, "diagnostician": 1.2},
    "total_time": 3.1,
    "agent_communication_log": [],
    "multi_agent": True,
    "agents_used": ["triage", "diagnostician", "specialist", "treatment", "safety", "empathy"],
    "estimated_cost": 0.002,
    "token_usage": {"total_input_tokens": 500, "total_output_tokens": 300},
    "provider": "anthropic",
    "model_used": "claude-sonnet-4-6",
    "provider_display": "Claude (Anthropic)",
}


# ---------------------------------------------------------------------------
# GET /health
# ---------------------------------------------------------------------------

class TestHealthEndpoint:

    def test_health_returns_200(self, client):
        """GET /health must return HTTP 200."""
        resp = client.get("/health")
        assert resp.status_code == 200

    def test_health_response_structure(self, client):
        """GET /health response must include status and architecture keys."""
        resp = client.get("/health")
        data = resp.json()
        assert "status" in data
        assert data["status"] == "healthy"
        assert "architecture" in data

    def test_health_lists_agents(self, client):
        """GET /health response includes the 4 pipeline agents."""
        resp = client.get("/health")
        data = resp.json()
        assert "agents" in data
        assert isinstance(data["agents"], list)
        assert len(data["agents"]) >= 4


# ---------------------------------------------------------------------------
# GET /api/agents
# ---------------------------------------------------------------------------

class TestAgentsEndpoint:

    def test_agents_returns_200(self, client):
        """GET /api/agents must return HTTP 200."""
        resp = client.get("/api/agents")
        assert resp.status_code == 200

    def test_agents_response_has_agents_list(self, client):
        """GET /api/agents returns a list with the 7 pipeline agents."""
        resp = client.get("/api/agents")
        data = resp.json()
        assert "agents" in data
        agents = data["agents"]
        assert isinstance(agents, list)
        assert len(agents) == 7

    def test_agents_names_are_correct(self, client):
        """GET /api/agents — agent names match the pipeline definition."""
        resp = client.get("/api/agents")
        names = {a["name"] for a in resp.json()["agents"]}
        expected = {"triage", "diagnostician", "research", "specialist", "treatment", "safety", "empathy"}
        assert names == expected

    def test_agents_pipeline_string_present(self, client):
        """GET /api/agents includes the pipeline description string."""
        resp = client.get("/api/agents")
        data = resp.json()
        assert "pipeline" in data
        assert "Triage" in data["pipeline"]


# ---------------------------------------------------------------------------
# POST /api/diagnose
# ---------------------------------------------------------------------------

class TestDiagnoseEndpoint:

    def test_diagnose_empty_symptoms_returns_422(self, client):
        """POST /api/diagnose with empty symptoms must return 422 (validation error)."""
        payload = {"symptoms": "", "age": 30, "gender": "female"}
        resp = client.post("/api/diagnose", json=payload)
        assert resp.status_code == 422

    def test_diagnose_missing_symptoms_returns_422(self, client):
        """POST /api/diagnose with no symptoms field returns 422."""
        resp = client.post("/api/diagnose", json={"age": 25, "gender": "male"})
        assert resp.status_code == 422

    def test_diagnose_whitespace_only_symptoms_returns_422(self, client):
        """POST /api/diagnose with whitespace-only symptoms returns 422 (validator strips)."""
        payload = {"symptoms": "   ", "age": 30, "gender": "male"}
        resp = client.post("/api/diagnose", json=payload)
        assert resp.status_code == 422

    def test_diagnose_invalid_age_returns_422(self, client):
        """POST /api/diagnose with out-of-range age returns 422."""
        payload = {"symptoms": "headache", "age": 200, "gender": "male"}
        resp = client.post("/api/diagnose", json=payload)
        assert resp.status_code == 422

    def test_diagnose_valid_payload_with_mocked_ai_returns_200(self, client):
        """POST /api/diagnose with a valid payload returns 200 when AI is mocked."""
        payload = {
            "symptoms": "headache and mild fever for two days",
            "age": 30,
            "gender": "female",
            "duration": "2 days",
            "severity": 4,
        }

        # Mock the OrchestratorAgent so no real Anthropic call happens
        with patch("main.OrchestratorAgent") as MockOrchestrator:
            mock_instance = MagicMock()
            mock_instance.run_diagnosis = AsyncMock(return_value=_MOCK_DIAGNOSIS)
            MockOrchestrator.return_value = mock_instance

            # Provide a fake Anthropic key header so the code picks "anthropic" provider
            resp = client.post(
                "/api/diagnose",
                json=payload,
                headers={"x-anthropic-api-key": "sk-ant-fake-key-for-testing"},
            )

        assert resp.status_code == 200

    def test_diagnose_valid_payload_response_has_causes(self, client):
        """POST /api/diagnose valid response includes a causes list."""
        payload = {
            "symptoms": "sore throat and runny nose",
            "age": 25,
            "gender": "male",
        }

        with patch("main.OrchestratorAgent") as MockOrchestrator:
            mock_instance = MagicMock()
            mock_instance.run_diagnosis = AsyncMock(return_value=_MOCK_DIAGNOSIS)
            MockOrchestrator.return_value = mock_instance

            resp = client.post(
                "/api/diagnose",
                json=payload,
                headers={"x-anthropic-api-key": "sk-ant-fake-key-for-testing"},
            )

        assert resp.status_code == 200
        data = resp.json()
        assert "causes" in data
        assert isinstance(data["causes"], list)
        assert len(data["causes"]) > 0

    def test_diagnose_no_api_key_returns_fallback(self, client):
        """POST /api/diagnose with no key returns a fallback response (not 500)."""
        payload = {"symptoms": "headache", "age": 35, "gender": "unknown"}
        # Patch Ollama check to fail — no key at all → fallback mode
        with patch("httpx.get", side_effect=Exception("no ollama")):
            resp = client.post("/api/diagnose", json=payload)
        # Fallback should return 200 with a basic answer, not 500
        assert resp.status_code in (200, 402, 422)


# ---------------------------------------------------------------------------
# POST /api/followup
# ---------------------------------------------------------------------------

class TestFollowupEndpoint:

    def test_followup_returns_200_with_mocked_ai(self, client):
        """POST /api/followup with a valid payload returns 200 when AI is mocked."""
        payload = {
            "question": "Should I take ibuprofen?",
            "original_symptoms": "headache and mild fever",
            "previous_messages": [],
            "previous_diagnosis": None,
        }

        mock_result = {"answer": "Ibuprofen can help with fever and headache. Consult your doctor.", "agent": "treatment"}

        with patch("main.OrchestratorAgent") as MockOrchestrator:
            mock_instance = MagicMock()
            mock_instance.run_followup = AsyncMock(return_value=mock_result)
            MockOrchestrator.return_value = mock_instance

            resp = client.post(
                "/api/followup",
                json=payload,
                headers={"x-anthropic-api-key": "sk-ant-fake-key-for-testing"},
            )

        assert resp.status_code == 200

    def test_followup_response_has_answer_key(self, client):
        """POST /api/followup response body includes an 'answer' key."""
        payload = {
            "question": "Is this serious?",
            "original_symptoms": "chest tightness",
            "previous_messages": [],
        }

        mock_result = {"answer": "Chest tightness should be evaluated promptly.", "agent": "treatment"}

        with patch("main.OrchestratorAgent") as MockOrchestrator:
            mock_instance = MagicMock()
            mock_instance.run_followup = AsyncMock(return_value=mock_result)
            MockOrchestrator.return_value = mock_instance

            resp = client.post(
                "/api/followup",
                json=payload,
                headers={"x-anthropic-api-key": "sk-ant-fake-key-for-testing"},
            )

        data = resp.json()
        assert "answer" in data
        assert len(data["answer"]) > 0

    def test_followup_empty_question_returns_422(self, client):
        """POST /api/followup with empty question returns 422."""
        payload = {"question": "", "original_symptoms": "headache"}
        resp = client.post("/api/followup", json=payload)
        assert resp.status_code == 422

    def test_followup_no_api_key_returns_fallback_message(self, client):
        """POST /api/followup with no key returns a safe default message."""
        payload = {
            "question": "What should I do?",
            "original_symptoms": "runny nose",
            "previous_messages": [],
        }
        with patch("httpx.get", side_effect=Exception("no ollama")):
            resp = client.post("/api/followup", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert "answer" in data
