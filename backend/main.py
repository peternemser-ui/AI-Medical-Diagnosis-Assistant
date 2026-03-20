"""
AI Medical Diagnosis Assistant – FastAPI Backend

Multi-agent architecture powered by Claude (Anthropic SDK).
Agents: Triage → Diagnostician → Specialist → Treatment
Coordinated by the Orchestrator agent.
"""

import os
import json
import asyncio
import logging
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from models import DiagnosisRequest, FollowupRequest, QuestionGenerationRequest
from agents import OrchestratorAgent

# ── Setup ────────────────────────────────────────────────────────────
load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Medical Diagnosis API",
    version="3.0.0",
    description="Multi-agent medical diagnosis powered by Claude AI",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Helpers ──────────────────────────────────────────────────────────

def _get_api_key(header_key: Optional[str] = None) -> tuple[Optional[str], str]:
    """Resolve API key from header or env. Returns (key, provider)."""
    key = header_key or os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not key:
        return None, "none"
    if key.startswith("sk-ant-"):
        return key, "anthropic"
    if key.startswith("AIza"):
        return key, "google"
    return key, "openai"


def _get_all_api_keys(request: Request) -> dict[str, Optional[str]]:
    """Extract all vendor API keys from headers and env."""
    return {
        "anthropic": request.headers.get("x-anthropic-api-key") or os.getenv("ANTHROPIC_API_KEY"),
        "openai": request.headers.get("x-openai-api-key") or os.getenv("OPENAI_API_KEY"),
        "google": request.headers.get("x-google-api-key") or os.getenv("GOOGLE_API_KEY"),
    }


def _fallback_diagnosis(req: DiagnosisRequest) -> dict:
    """Basic keyword-based response when no AI key is available."""
    symptoms_lower = req.symptoms.lower()
    conditions = []

    if any(w in symptoms_lower for w in ["fever", "temperature", "hot", "chills"]):
        conditions.append("Viral or bacterial infection")
    if any(w in symptoms_lower for w in ["cough", "throat", "sore throat"]):
        conditions.append("Upper respiratory infection")
    if any(w in symptoms_lower for w in ["headache", "head pain", "migraine"]):
        conditions.append("Headache disorder")
    if any(w in symptoms_lower for w in ["stomach", "nausea", "vomit", "diarrhea"]):
        conditions.append("Gastrointestinal issue")
    if any(w in symptoms_lower for w in ["pain", "ache", "hurt", "sore"]):
        conditions.append("Musculoskeletal condition")
    if not conditions:
        conditions.append("General medical condition")

    lines = [
        "AI Medical Assessment (Fallback Mode)",
        "--------------------------------------",
        f"Age: {req.age} | Gender: {req.gender}",
        f"Symptoms: {req.symptoms}",
        "",
        "Preliminary conditions to consider:",
    ]
    for c in conditions[:3]:
        lines.append(f"  - {c}")
    lines += [
        "",
        "Recommendations:",
        "  1. Monitor symptoms and note changes",
        "  2. Stay hydrated",
        "  3. Get adequate rest",
        "  4. Consult a healthcare provider for proper evaluation",
        "",
        "Note: Set your Anthropic API key for full multi-agent analysis.",
        "Disclaimer: Not a substitute for professional medical care.",
    ]

    return {
        "answer": "\n".join(lines),
        "confidence_scores": {"high": 0.6, "medium": 0.3, "low": 0.1},
        "causes": [{"cause": c, "value": 50, "explanation": "", "urgency": "routine", "specialty": "Primary Care"} for c in conditions[:3]],
        "red_flags": [],
        "additional_questions": [],
        "recommended_tests": [],
        "multi_agent": False,
        "estimated_cost": 0.0,
    }


async def _openai_diagnosis(api_key: str, req: DiagnosisRequest) -> dict:
    """Fallback: use OpenAI GPT-4o for diagnosis when no Anthropic key is available."""
    import time
    from openai import OpenAI

    start = time.time()
    client = OpenAI(api_key=api_key)

    prompt = f"""You are an expert medical AI. Analyze these symptoms and provide a comprehensive differential diagnosis.

Patient: {req.age}-year-old {req.gender}
Symptoms: {req.symptoms}
Duration: {req.duration}
Severity: {req.severity}/10

Respond in valid JSON with this structure:
{{
  "diagnoses": [
    {{"condition": "Name", "confidence": 85, "explanation": "Clinical reasoning", "urgency": "routine|soon|urgent", "specialty": "Primary Care|Specialist"}}
  ],
  "red_flags": ["list of warning signs"],
  "additional_questions": ["follow-up questions"],
  "recommended_tests": ["diagnostic tests"],
  "patient_summary": "Plain language summary for the patient",
  "action_checklist": ["numbered action items"],
  "warning_signs": ["when to seek immediate care"],
  "safety_notes": "any safety concerns"
}}

Provide at least 3 differential diagnoses ranked by likelihood. Include clinical reasoning for each."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert medical AI. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4000,
            temperature=0.2,
        )
        content = response.choices[0].message.content.strip()

        import re
        # Parse JSON from response
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            match = re.search(r'\{.*\}', content, re.DOTALL)
            data = json.loads(match.group(0)) if match else {"diagnoses": []}

        causes = [
            {
                "cause": d.get("condition", "Unknown"),
                "value": d.get("confidence", 50),
                "explanation": d.get("explanation", ""),
                "urgency": d.get("urgency", "routine"),
                "specialty": d.get("specialty", "Primary Care"),
            }
            for d in data.get("diagnoses", [])
        ]

        total_time = round(time.time() - start, 2)

        return {
            "answer": f"AI Medical Assessment (OpenAI GPT-4o)\n{'=' * 40}\nAge: {req.age} | Gender: {req.gender}\n\n"
                      + "\n".join(f"{i+1}. {c['cause']} — {c['value']}% confidence\n   {c['explanation']}" for i, c in enumerate(causes)),
            "confidence_scores": {"high": 0.6, "medium": 0.3, "low": 0.1},
            "causes": causes,
            "red_flags": data.get("red_flags", []),
            "additional_questions": data.get("additional_questions", []),
            "recommended_tests": data.get("recommended_tests", []),
            "patient_summary": data.get("patient_summary", ""),
            "action_checklist": data.get("action_checklist", []),
            "safety_status": "REVIEWED",
            "safety_warnings": [data.get("safety_notes", "")] if data.get("safety_notes") else [],
            "medications": [],
            "lifestyle_recommendations": [],
            "warning_signs": data.get("warning_signs", []),
            "follow_up_timeline": "",
            "agent_details": {},
            "agent_timings": {"openai_gpt4o": total_time},
            "total_time": total_time,
            "agent_communication_log": [],
            "multi_agent": False,
            "agents_used": ["openai_gpt4o"],
            "estimated_cost": 0.05,
        }
    except Exception as e:
        logger.error("OpenAI diagnosis failed: %s", e)
        raise


# ── Endpoints ────────────────────────────────────────────────────────

@app.get("/")
async def root():
    return {
        "message": "AI Medical Diagnosis API is running!",
        "status": "ok",
        "version": "3.0.0",
        "architecture": "multi-agent (Triage → Diagnostician → Specialist → Treatment)",
        "powered_by": "Claude AI (Anthropic)",
        "endpoints": ["GET /", "GET /health", "POST /api/diagnose", "POST /api/followup", "POST /api/generate-question"],
    }


@app.get("/health")
async def health_check():
    has_key = bool(os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY"))
    return {
        "status": "healthy",
        "api_key_configured": has_key,
        "architecture": "multi-agent",
        "agents": ["triage", "diagnostician", "specialist", "treatment"],
        "cors": "enabled",
    }


@app.post("/api/validate-key")
async def validate_api_key(
    http_request: Request,
    x_openai_api_key: Optional[str] = Header(None),
    x_anthropic_api_key: Optional[str] = Header(None),
    x_google_api_key: Optional[str] = Header(None),
):
    """Validate an API key by making a minimal test call to the provider."""
    results = {}

    # Test Anthropic
    anthropic_key = x_anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
    if anthropic_key:
        try:
            from anthropic import AsyncAnthropic
            client = AsyncAnthropic(api_key=anthropic_key)
            resp = await client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=10,
                messages=[{"role": "user", "content": "Hi"}],
            )
            results["anthropic"] = {"valid": True, "model": "claude-haiku-4-5", "message": "Key is valid"}
        except Exception as e:
            err = str(e)
            if "401" in err or "auth" in err.lower() or "invalid" in err.lower():
                results["anthropic"] = {"valid": False, "message": "Invalid API key"}
            elif "429" in err or "rate" in err.lower():
                results["anthropic"] = {"valid": True, "message": "Key valid (rate limited)"}
            else:
                results["anthropic"] = {"valid": False, "message": f"Error: {err[:100]}"}
    else:
        results["anthropic"] = {"valid": False, "message": "No key provided"}

    # Test OpenAI
    openai_key = x_openai_api_key or os.getenv("OPENAI_API_KEY")
    if openai_key:
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=openai_key)
            resp = await client.chat.completions.create(
                model="gpt-4o-mini",
                max_tokens=5,
                messages=[{"role": "user", "content": "Hi"}],
            )
            results["openai"] = {"valid": True, "model": "gpt-4o-mini", "message": "Key is valid"}
        except Exception as e:
            err = str(e)
            if "401" in err or "auth" in err.lower() or "invalid" in err.lower():
                results["openai"] = {"valid": False, "message": "Invalid API key"}
            elif "429" in err or "rate" in err.lower():
                results["openai"] = {"valid": True, "message": "Key valid (rate limited)"}
            else:
                results["openai"] = {"valid": False, "message": f"Error: {err[:100]}"}
    else:
        results["openai"] = {"valid": False, "message": "No key provided"}

    # Test Google
    google_key = x_google_api_key or os.getenv("GOOGLE_API_KEY")
    if google_key:
        try:
            from google import genai
            client = genai.Client(api_key=google_key)
            resp = await client.aio.models.generate_content(
                model="gemini-2.0-flash",
                contents="Hi",
            )
            results["google"] = {"valid": True, "model": "gemini-2.0-flash", "message": "Key is valid"}
        except Exception as e:
            err = str(e)
            if "401" in err or "403" in err or "auth" in err.lower() or "invalid" in err.lower():
                results["google"] = {"valid": False, "message": "Invalid API key"}
            elif "429" in err or "rate" in err.lower():
                results["google"] = {"valid": True, "message": "Key valid (rate limited)"}
            else:
                results["google"] = {"valid": False, "message": f"Error: {err[:100]}"}
    else:
        results["google"] = {"valid": False, "message": "No key provided"}

    any_valid = any(r.get("valid") for r in results.values())
    return {"results": results, "any_valid": any_valid}


@app.post("/api/diagnose")
async def diagnose_symptoms(
    diagnosis_request: DiagnosisRequest,
    http_request: Request,
    x_openai_api_key: Optional[str] = Header(None),
    x_anthropic_api_key: Optional[str] = Header(None),
):
    """
    Main diagnosis endpoint.

    Runs the full multi-agent pipeline:
    Triage → Diagnostician → Specialist → Treatment
    """
    try:
        api_key, provider = _get_api_key(x_anthropic_api_key or x_openai_api_key)

        if not api_key:
            logger.warning("No API key — returning fallback diagnosis")
            return _fallback_diagnosis(diagnosis_request)

        if provider == "openai":
            logger.info("OpenAI key detected — using OpenAI single-model diagnosis")
            return await _openai_diagnosis(api_key, diagnosis_request)

        logger.info(
            "Starting multi-agent diagnosis for: %s (age=%d, gender=%s)",
            diagnosis_request.symptoms[:80],
            diagnosis_request.age,
            diagnosis_request.gender,
        )

        all_keys = _get_all_api_keys(http_request)
        orchestrator = OrchestratorAgent(
            api_key=api_key,
            openai_key=all_keys.get("openai"),
            google_key=all_keys.get("google"),
        )
        result = await orchestrator.run_diagnosis(
            symptoms=diagnosis_request.symptoms,
            age=diagnosis_request.age,
            gender=diagnosis_request.gender,
            duration=diagnosis_request.duration,
            severity=diagnosis_request.severity,
            image_base64=diagnosis_request.image_base64,
            medical_history=diagnosis_request.medical_history,
            current_medications=diagnosis_request.current_medications,
            allergies=diagnosis_request.allergies,
            family_history=diagnosis_request.family_history,
            social_history=diagnosis_request.social_history,
            model_preference=diagnosis_request.model_preference,
        )

        logger.info(
            "Multi-agent diagnosis complete in %.1fs (agents: %s)",
            result.get("total_time", 0),
            ", ".join(result.get("agents_used", [])),
        )

        return result

    except Exception as e:
        logger.error("Diagnosis error: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=f"Diagnosis failed: {str(e)}")


@app.post("/api/diagnose/stream")
async def diagnose_symptoms_stream(
    diagnosis_request: DiagnosisRequest,
    http_request: Request,
    x_openai_api_key: Optional[str] = Header(None),
    x_anthropic_api_key: Optional[str] = Header(None),
):
    """
    Streaming diagnosis endpoint using Server-Sent Events.

    Each agent's result is streamed as it completes:
      data: {"event": "agent_complete", "agent": "triage", ...}\n\n

    Final event:
      data: {"event": "complete", "result": { ... }}\n\n
    """
    try:
        api_key, provider = _get_api_key(x_anthropic_api_key or x_openai_api_key)

        if not api_key:
            logger.warning("No API key — returning fallback diagnosis via SSE")
            fallback = _fallback_diagnosis(diagnosis_request)

            async def fallback_generator():
                yield f"data: {json.dumps({'event': 'complete', 'result': fallback})}\n\n"

            return StreamingResponse(fallback_generator(), media_type="text/event-stream")

        if provider == "openai":
            logger.info("OpenAI key detected — returning single SSE event")
            result = await _openai_diagnosis(api_key, diagnosis_request)

            async def openai_generator():
                yield f"data: {json.dumps({'event': 'complete', 'result': result})}\n\n"

            return StreamingResponse(openai_generator(), media_type="text/event-stream")

        logger.info(
            "Starting streaming multi-agent diagnosis for: %s (age=%d, gender=%s)",
            diagnosis_request.symptoms[:80],
            diagnosis_request.age,
            diagnosis_request.gender,
        )

        event_queue: asyncio.Queue = asyncio.Queue()
        all_keys = _get_all_api_keys(http_request)
        orchestrator = OrchestratorAgent(
            api_key=api_key,
            openai_key=all_keys.get("openai"),
            google_key=all_keys.get("google"),
        )

        # Spawn the streaming pipeline as a background task
        asyncio.create_task(orchestrator.run_diagnosis_streaming(
            event_queue=event_queue,
            symptoms=diagnosis_request.symptoms,
            age=diagnosis_request.age,
            gender=diagnosis_request.gender,
            duration=diagnosis_request.duration,
            severity=diagnosis_request.severity,
            image_base64=getattr(diagnosis_request, 'image_base64', None),
            medical_history=diagnosis_request.medical_history,
            current_medications=diagnosis_request.current_medications,
            allergies=diagnosis_request.allergies,
            family_history=diagnosis_request.family_history,
            social_history=diagnosis_request.social_history,
            model_preference=diagnosis_request.model_preference,
        ))

        async def event_generator():
            while True:
                event = await event_queue.get()
                yield f"data: {json.dumps(event)}\n\n"
                if event.get("event") == "complete":
                    break

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    except Exception as e:
        logger.error("Streaming diagnosis error: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=f"Streaming diagnosis failed: {str(e)}")


@app.post("/api/followup")
async def followup_question(
    followup_req: FollowupRequest,
    http_request: Request,
    x_openai_api_key: Optional[str] = Header(None),
    x_anthropic_api_key: Optional[str] = Header(None),
):
    """Handle follow-up questions using the treatment agent."""
    try:
        api_key, provider = _get_api_key(x_anthropic_api_key or x_openai_api_key)

        if not api_key:
            return {
                "answer": "Please configure an API key for AI-powered follow-up responses.",
                "estimated_cost": 0.0,
            }

        if provider == "openai":
            # Quick OpenAI follow-up
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            resp = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a medical AI assistant providing follow-up guidance."},
                    {"role": "user", "content": f"Patient follow-up question: {followup_req.question}\nOriginal symptoms: {followup_req.original_symptoms}"}
                ],
                max_tokens=1500,
                temperature=0.3,
            )
            return {"answer": resp.choices[0].message.content, "estimated_cost": 0.02}

        orchestrator = OrchestratorAgent(api_key=api_key)
        result = await orchestrator.run_followup(
            question=followup_req.question,
            previous_diagnosis=followup_req.previous_diagnosis,
            original_symptoms=followup_req.original_symptoms,
        )

        return {
            "answer": result["answer"],
            "agent": result.get("agent", "treatment"),
            "estimated_cost": 0.02,
        }

    except Exception as e:
        logger.error("Followup error: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=f"Followup failed: {str(e)}")


@app.post("/api/generate-question")
async def generate_question(
    request_data: QuestionGenerationRequest,
    http_request: Request,
    x_openai_api_key: Optional[str] = Header(None),
    x_anthropic_api_key: Optional[str] = Header(None),
):
    """Generate a follow-up question using the diagnostician agent."""
    try:
        api_key, provider = _get_api_key(x_anthropic_api_key or x_openai_api_key)

        if not api_key:
            return {
                "question": "What is the severity of your symptoms on a scale of 1-10?",
                "estimated_cost": 0.0,
            }

        if provider == "openai":
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            prompt = (
                f"Generate ONE specific follow-up question for a {request_data.age}-year-old {request_data.gender} "
                f"with symptoms: {request_data.symptoms}. Question {request_data.questions_asked + 1} of {request_data.total_ai_questions}. "
                f"Previously asked: {request_data.previous_questions}. Return ONLY the question."
            )
            resp = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150, temperature=0.7,
            )
            return {"question": resp.choices[0].message.content.strip().strip('"'), "estimated_cost": 0.01}

        orchestrator = OrchestratorAgent(api_key=api_key)
        question = await orchestrator.generate_question(
            symptoms=request_data.symptoms,
            age=request_data.age,
            gender=request_data.gender,
            conversation_history=request_data.conversation_history,
            previous_questions=request_data.previous_questions,
            questions_asked=request_data.questions_asked,
            total_ai_questions=request_data.total_ai_questions,
        )

        return {"question": question, "estimated_cost": 0.01}

    except Exception as e:
        logger.error("Question generation error: %s", e, exc_info=True)
        return {
            "question": "Can you tell me more about when these symptoms started and if anything makes them better or worse?",
            "estimated_cost": 0.0,
        }


@app.get("/api/agents")
async def list_agents():
    """Return information about the multi-agent system."""
    return {
        "architecture": "Multi-Agent Medical Diagnosis Pipeline",
        "agents": [
            {"name": "triage", "role": "Emergency triage (ESI 5-level)", "model": "claude-sonnet-4-6", "step": 1},
            {"name": "diagnostician", "role": "Differential diagnosis (VINDICATE + Bayesian)", "model": "claude-opus-4-6", "step": 2},
            {"name": "research", "role": "Evidence-based medical research (GRADE)", "model": "claude-sonnet-4-6", "step": 2},
            {"name": "specialist", "role": "Domain-specific deep analysis (30+ scoring systems)", "model": "claude-sonnet-4-6", "step": 3},
            {"name": "treatment", "role": "Treatment planning & medication safety", "model": "claude-sonnet-4-6", "step": 4},
            {"name": "safety", "role": "Patient safety review (Beers, STOPP/START)", "model": "claude-sonnet-4-6", "step": 5},
            {"name": "empathy", "role": "Patient-friendly communication", "model": "claude-sonnet-4-6", "step": 6},
        ],
        "pipeline": "Triage → Diagnostician+Research (parallel) → Specialist → Treatment → Safety → Empathy",
        "communication": "Agents communicate via async MessageBus",
        "model": "Claude Sonnet 4.6 (Opus 4.6 for diagnostician)",
    }


@app.get("/debug")
async def debug_info():
    return {
        "message": "Debug endpoint working",
        "version": "3.0.0",
        "architecture": "multi-agent",
        "routes_available": [
            "GET /",
            "GET /health",
            "POST /api/diagnose",
            "POST /api/followup",
            "POST /api/generate-question",
            "GET /api/agents",
            "GET /debug",
            "GET /docs",
        ],
        "cors_enabled": True,
    }


@app.options("/{full_path:path}")
async def options_handler():
    return {"message": "CORS preflight OK"}
