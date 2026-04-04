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
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from models import DiagnosisRequest, FollowupRequest, QuestionGenerationRequest, InterviewRequest
from agents import OrchestratorAgent
from config import OLLAMA_VERSION_URL, OLLAMA_TAGS_URL, OLLAMA_API_URL, OLLAMA_HEALTH_CHECK_TIMEOUT

# ── Setup ────────────────────────────────────────────────────────────
load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")
logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="AI Medical Diagnosis API",
    version="3.0.0",
    description="Multi-agent medical diagnosis powered by Claude AI",
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

_cors_origins = [o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3001,http://localhost:3002,http://localhost:3003").split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Anthropic-API-Key", "X-OpenAI-API-Key", "X-Google-API-Key"],
)

# ── Security headers middleware ──────────────────────────────
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    if os.getenv("ENFORCE_HTTPS", "").lower() == "true":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

from admin.router import admin_router, billing_router
app.include_router(admin_router)
app.include_router(billing_router)

from auth_routes import auth_router
app.include_router(auth_router)

from medication_routes import medication_router
app.include_router(medication_router)


# ── Helpers ──────────────────────────────────────────────────────────

def _get_api_key(header_key: Optional[str] = None) -> tuple[Optional[str], str]:
    """Resolve API key from header or env. Returns (key, provider).
    Supports Anthropic, OpenAI, Google, and Ollama (local).
    """
    key = header_key or os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY")
    # Check for Ollama — use it when no cloud key is available or explicitly requested
    if not key or key == "ollama":
        # Check if Ollama is running locally
        try:
            import httpx
            resp = httpx.get(OLLAMA_VERSION_URL, timeout=OLLAMA_HEALTH_CHECK_TIMEOUT)
            if resp.status_code == 200:
                return "ollama", "ollama"
        except Exception as e:
            logger.debug("Ollama not reachable: %s", e)
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


def _resolve_key_with_fallback(model_pref: str, all_keys: dict, fallback_key=None, exclude_providers: list = None) -> tuple[Optional[str], str]:
    """Resolve API key based on model preference with fallback to any available key.

    Priority order based on model_pref:
    - gpt-*    → openai > anthropic > google > ollama
    - gemini-* → google > anthropic > openai > ollama
    - opus/sonnet/haiku → anthropic > openai > google > ollama
    - auto     → anthropic > openai > google > ollama

    exclude_providers: list of providers that already failed (for retry logic)
    """
    exclude = set(exclude_providers or [])

    # Build priority order based on model preference
    if model_pref.startswith('gpt'):
        order = ['openai', 'anthropic', 'google']
    elif model_pref.startswith('gemini'):
        order = ['google', 'anthropic', 'openai']
    elif model_pref in ('opus', 'sonnet', 'haiku'):
        order = ['anthropic', 'openai', 'google']
    else:
        order = ['anthropic', 'openai', 'google']

    # Try each key in priority order, skipping excluded providers
    for vendor in order:
        if vendor in exclude:
            continue
        key = all_keys.get(vendor)
        if key:
            return key, vendor

    # Try Ollama as last resort (if not excluded)
    if "ollama" not in exclude:
        try:
            import httpx
            resp = httpx.get(OLLAMA_VERSION_URL, timeout=OLLAMA_HEALTH_CHECK_TIMEOUT)
            if resp.status_code == 200:
                return "ollama", "ollama"
        except Exception:
            pass

    return None, "none"


def _is_auth_or_key_error(error: Exception) -> bool:
    """Check if an error is an authentication/API key issue (worth retrying with different key)."""
    err_str = str(error).lower()
    return any(term in err_str for term in [
        'api_key', 'api key', 'authentication', 'unauthorized', '401',
        'invalid key', 'invalid_api_key', 'permission', '403', 'forbidden',
        'rate limit', '429', 'quota', 'billing', 'overloaded', '529', '503',
    ])


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
    # Check if Ollama is running locally
    ollama_available = False
    ollama_models = []
    try:
        import httpx
        resp = httpx.get(OLLAMA_TAGS_URL, timeout=OLLAMA_HEALTH_CHECK_TIMEOUT)
        if resp.status_code == 200:
            ollama_available = True
            ollama_models = [m["name"] for m in resp.json().get("models", [])]
    except Exception as e:
        logger.debug("Ollama health check unavailable: %s", e)
    return {
        "status": "healthy",
        "api_key_configured": has_key or ollama_available,
        "ollama_available": ollama_available,
        "ollama_models": ollama_models,
        "architecture": "multi-agent",
        "agents": ["triage", "diagnostician", "specialist", "treatment"],
        "cors": "enabled",
    }


@app.post("/api/validate-key")
@limiter.limit("10/minute")
async def validate_api_key(
    request: Request,
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
        except ImportError:
            results["anthropic"] = {"valid": False, "message": "anthropic package not installed on server"}
            anthropic_key = None
    if anthropic_key:
        try:
            from anthropic import AuthenticationError as AnthropicAuthError, RateLimitError as AnthropicRateLimit, PermissionDeniedError as AnthropicPermError
        except ImportError:
            results["anthropic"] = {"valid": False, "message": "anthropic package not installed on server"}
            anthropic_key = None

    if anthropic_key:
        try:
            client = AsyncAnthropic(api_key=anthropic_key)
            resp = await client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=10,
                messages=[{"role": "user", "content": "Hi"}],
            )
            results["anthropic"] = {"valid": True, "model": "claude-haiku-4-5", "message": "Key is valid"}
        except AnthropicAuthError:
            results["anthropic"] = {"valid": False, "message": "Invalid API key"}
        except AnthropicPermError:
            results["anthropic"] = {"valid": False, "message": "API key lacks permission for this model"}
        except AnthropicRateLimit:
            results["anthropic"] = {"valid": True, "message": "Key valid (rate limited)"}
        except Exception as e:
            err = str(e)
            etype = type(e).__name__
            if "401" in err:
                results["anthropic"] = {"valid": False, "message": "Invalid API key"}
            elif "overloaded" in err.lower() or "529" in err or "503" in err:
                results["anthropic"] = {"valid": True, "message": "Key valid (API temporarily overloaded)"}
            elif "timeout" in err.lower() or "timed out" in err.lower():
                results["anthropic"] = {"valid": True, "message": "Key likely valid (request timed out)"}
            elif "connect" in err.lower():
                results["anthropic"] = {"valid": False, "message": "Cannot reach Anthropic API — check network"}
            else:
                results["anthropic"] = {"valid": False, "message": f"{etype}: {err[:120]}"}
    else:
        results["anthropic"] = {"valid": False, "message": "No key provided"}

    # Test OpenAI
    openai_key = x_openai_api_key or os.getenv("OPENAI_API_KEY")
    if openai_key:
        try:
            from openai import AsyncOpenAI
        except ImportError:
            results["openai"] = {"valid": False, "message": "openai package not installed on server"}
            openai_key = None
    if openai_key:
        try:
            from openai import AuthenticationError as OpenAIAuthError, RateLimitError as OpenAIRateLimit
            client = AsyncOpenAI(api_key=openai_key)
            resp = await client.chat.completions.create(
                model="gpt-4o-mini",
                max_tokens=5,
                messages=[{"role": "user", "content": "Hi"}],
            )
            results["openai"] = {"valid": True, "model": "gpt-4o-mini", "message": "Key is valid"}
        except OpenAIAuthError:
            results["openai"] = {"valid": False, "message": "Invalid API key"}
        except OpenAIRateLimit:
            results["openai"] = {"valid": True, "message": "Key valid (rate limited)"}
        except Exception as e:
            err = str(e)
            etype = type(e).__name__
            if "401" in err:
                results["openai"] = {"valid": False, "message": "Invalid API key"}
            elif "timeout" in err.lower() or "timed out" in err.lower():
                results["openai"] = {"valid": True, "message": "Key likely valid (request timed out)"}
            else:
                results["openai"] = {"valid": False, "message": f"{etype}: {err[:120]}"}
    else:
        results["openai"] = {"valid": False, "message": "No key provided"}

    # Test Google
    google_key = x_google_api_key or os.getenv("GOOGLE_API_KEY")
    if google_key:
        try:
            from google import genai
        except ImportError:
            results["google"] = {"valid": False, "message": "google-genai package not installed on server"}
            google_key = None
        if google_key:
            try:
                client = genai.Client(api_key=google_key)
                resp = await client.aio.models.generate_content(
                    model="gemini-2.0-flash",
                    contents="Hi",
                )
                results["google"] = {"valid": True, "model": "gemini-2.0-flash", "message": "Key is valid"}
            except Exception as e:
                err = str(e)
                if "401" in err or "403" in err or "API_KEY_INVALID" in err:
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
@limiter.limit("20/hour")
async def diagnose_symptoms(
    diagnosis_request: DiagnosisRequest,
    request: Request,
    x_openai_api_key: Optional[str] = Header(None),
    x_anthropic_api_key: Optional[str] = Header(None),
):
    """
    Main diagnosis endpoint.

    Runs the full multi-agent pipeline:
    Triage → Diagnostician → Specialist → Treatment
    """
    model_pref = diagnosis_request.model_preference or 'auto'
    all_keys = _get_all_api_keys(request)
    failed_providers = []
    last_error = None

    # Retry loop: try each available provider until one works
    for attempt in range(3):
        try:
            api_key, provider = _resolve_key_with_fallback(model_pref, all_keys, exclude_providers=failed_providers)
            logger.info("Attempt %d: resolved provider=%s for model_pref=%s (excluded: %s, keys available: %s)",
                         attempt + 1, provider, model_pref, failed_providers, [k for k, v in all_keys.items() if v])

            if not api_key:
                logger.warning("No more API keys to try — returning fallback diagnosis")
                return _fallback_diagnosis(diagnosis_request)

            if provider == "openai":
                logger.info("OpenAI key detected — using OpenAI single-model diagnosis")
                return await _openai_diagnosis(api_key, diagnosis_request)

            # Ollama: use local model via multi-agent pipeline
            if provider == "ollama":
                logger.info("Ollama detected — using local model for multi-agent diagnosis")
                if not diagnosis_request.model_preference or diagnosis_request.model_preference == "auto":
                    diagnosis_request.model_preference = "llama3.1:8b"

            logger.info(
                "Starting multi-agent diagnosis for: %s (age=%d, gender=%s, provider=%s)",
                diagnosis_request.symptoms[:80],
                diagnosis_request.age,
                diagnosis_request.gender,
                provider,
            )

            orchestrator = OrchestratorAgent(
                api_key=api_key if provider != "ollama" else "ollama",
                openai_key=all_keys.get("openai"),
                google_key=all_keys.get("google"),
            )
            result = await orchestrator.run_diagnosis(
                symptoms=diagnosis_request.symptoms,
                age=diagnosis_request.age,
                gender=diagnosis_request.gender,
                duration=diagnosis_request.duration,
                severity=diagnosis_request.severity,
                language=diagnosis_request.language,
                image_base64=diagnosis_request.image_base64,
                medical_history=diagnosis_request.medical_history,
                current_medications=diagnosis_request.current_medications,
                allergies=diagnosis_request.allergies,
                family_history=diagnosis_request.family_history,
                social_history=diagnosis_request.social_history,
                model_preference=diagnosis_request.model_preference,
                specialist_routing=diagnosis_request.specialist_routing,
            )

            logger.info(
                "Multi-agent diagnosis complete in %.1fs (agents: %s, specialist: %s, provider: %s)",
                result.get("total_time", 0),
                ", ".join(result.get("agents_used", [])),
                diagnosis_request.specialist_routing or "generic",
                provider,
            )

            # Debug: dump result to file for inspection
            try:
                import pathlib
                debug_path = pathlib.Path(__file__).parent / "_debug_last_result.json"
                debug_path.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
            except Exception:
                pass

            return result

        except Exception as e:
            last_error = e
            logger.warning("Provider %s failed (attempt %d): %s", provider, attempt + 1, e)
            if _is_auth_or_key_error(e):
                failed_providers.append(provider)
                logger.info("Marking provider %s as failed, will try next available key", provider)
                continue
            else:
                # Non-auth error (network, server, etc.) — don't retry with different key
                logger.error("Diagnosis error (non-retryable): %s", e, exc_info=True)
                raise HTTPException(status_code=500, detail=f"Diagnosis failed: {str(e)}")

    # All providers exhausted
    logger.error("All providers failed. Last error: %s", last_error)
    raise HTTPException(status_code=500, detail=f"All API providers failed. Last error: {str(last_error)}")


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
    model_pref = diagnosis_request.model_preference or 'auto'
    all_keys = _get_all_api_keys(http_request)
    failed_providers = []

    # Try providers with automatic fallback on auth/key errors
    for attempt in range(3):
        try:
            api_key, provider = _resolve_key_with_fallback(model_pref, all_keys, exclude_providers=failed_providers)
            logger.info("Stream attempt %d: resolved provider=%s for model_pref=%s (excluded: %s, keys available: %s)",
                         attempt + 1, provider, model_pref, failed_providers, [k for k, v in all_keys.items() if v])

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

            # Ollama: use local model
            if provider == "ollama":
                if not diagnosis_request.model_preference or diagnosis_request.model_preference == "auto":
                    diagnosis_request.model_preference = "llama3.1:8b"

            logger.info(
                "Starting streaming multi-agent diagnosis for: %s (age=%d, gender=%s, provider=%s)",
                diagnosis_request.symptoms[:80],
                diagnosis_request.age,
                diagnosis_request.gender,
                provider,
            )

            event_queue: asyncio.Queue = asyncio.Queue()
            orchestrator = OrchestratorAgent(
                api_key=api_key if provider != "ollama" else "ollama",
                openai_key=all_keys.get("openai"),
                google_key=all_keys.get("google"),
            )

            # Spawn the streaming pipeline as a background task with error handling
            async def _run_streaming_pipeline():
                try:
                    await orchestrator.run_diagnosis_streaming(
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
                    )
                except Exception as exc:
                    logger.error("Streaming pipeline crashed: %s", exc, exc_info=True)
                    await event_queue.put({
                        "event": "complete",
                        "result": {
                            "answer": f"Diagnosis pipeline error: {exc}",
                            "causes": [],
                            "red_flags": [],
                            "recommended_tests": [],
                            "agent_timings": {},
                            "total_time": 0,
                            "multi_agent": True,
                            "agents_used": [],
                            "estimated_cost": 0,
                            "error": str(exc),
                        },
                    })

            asyncio.create_task(_run_streaming_pipeline())

            async def event_generator():
                yield {"data": json.dumps({"event": "started", "message": f"Pipeline started (provider: {provider})"})}
                while True:
                    try:
                        event = await asyncio.wait_for(event_queue.get(), timeout=10.0)
                        yield {"data": json.dumps(event)}
                        if event.get("event") == "complete":
                            break
                    except asyncio.TimeoutError:
                        yield {"comment": "keepalive"}

            from sse_starlette.sse import EventSourceResponse
            return EventSourceResponse(event_generator(), ping=5)

        except Exception as e:
            logger.warning("Stream provider %s failed (attempt %d): %s", provider, attempt + 1, e)
            if _is_auth_or_key_error(e):
                failed_providers.append(provider)
                logger.info("Stream: marking provider %s as failed, trying next key", provider)
                continue
            else:
                logger.error("Streaming diagnosis error (non-retryable): %s", e, exc_info=True)
                raise HTTPException(status_code=500, detail=f"Streaming diagnosis failed: {str(e)}")

    # All providers exhausted
    logger.error("Stream: all providers failed")
    raise HTTPException(status_code=500, detail="All API providers failed")


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

        # Build language instruction for non-English follow-ups
        fu_lang = getattr(followup_req, 'language', 'en') or 'en'
        FU_LANG_NAMES = {"en":"English","zh":"Chinese (Simplified)","es":"Spanish","fr":"French","hi":"Hindi","de":"German","pt":"Portuguese","ja":"Japanese","ko":"Korean","ar":"Arabic","ru":"Russian","it":"Italian"}
        fu_lang_suffix = ""
        if fu_lang != "en" and fu_lang in FU_LANG_NAMES:
            fu_lang_suffix = f"\nIMPORTANT: Respond entirely in {FU_LANG_NAMES[fu_lang]}."

        if provider == "openai":
            # Quick OpenAI follow-up
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            system_msg = "You are a medical AI assistant providing follow-up guidance."
            if fu_lang_suffix:
                system_msg += fu_lang_suffix
            resp = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_msg},
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
            language=fu_lang,
        )

        return {
            "answer": result["answer"],
            "agent": result.get("agent", "treatment"),
            "estimated_cost": 0.02,
        }

    except Exception as e:
        logger.error("Followup error: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=f"Followup failed: {str(e)}")


@app.post("/api/interview")
async def pa_interview(
    request_data: InterviewRequest,
    http_request: Request,
    x_openai_api_key: Optional[str] = Header(None),
    x_anthropic_api_key: Optional[str] = Header(None),
):
    """Run one round of the PA clinical interview."""
    try:
        all_keys = _get_all_api_keys(http_request)
        model_pref = request_data.model_preference or 'auto'
        api_key, provider = _resolve_key_with_fallback(model_pref, all_keys)

        if not api_key:
            # No API key — return scripted follow-up questions
            # The first user message is the chief complaint (already provided)
            exchange_count = len([m for m in request_data.conversation if m.get("role") == "user"])
            followup_questions = [
                # index 0 = already answered (chief complaint), so start from index 1
                "When did this start? Was it sudden or gradual?",
                "How severe would you rate this on a scale of 1-10?",
                "Have you noticed any other symptoms alongside this?",
                "Do you have any medical conditions or take any medications?",
                "Do you have any allergies to medications?",
                "Does anything make it better or worse?",
                "Is there any relevant family history of similar conditions?",
            ]
            # exchange_count starts at 1 (chief complaint already in conversation)
            q_index = exchange_count - 1  # offset since chief complaint is already exchange 0
            if q_index >= 0 and q_index < len(followup_questions):
                return {"action": "ask", "question": followup_questions[q_index], "exchange_count": exchange_count}
            else:
                # Enough questions asked — route to general medicine
                chief = ""
                for m in request_data.conversation:
                    if m.get("role") == "user":
                        chief = m.get("content", "")
                        break
                return {
                    "action": "route",
                    "routing": {
                        "specialties": ["general_medicine"],
                        "urgency": "routine",
                        "patient_summary": "Basic interview completed. See conversation for clinical details.",
                        "chief_complaint": chief
                    },
                    "exchange_count": exchange_count
                }

        # Determine model preference
        model_pref = request_data.model_preference
        if model_pref == "auto":
            model_pref = None
        if provider == "ollama":
            model_pref = "llama3.1:8b"

        # Create PA agent
        from agents.pa_agent import PAInterviewAgent
        from agents.message_bus import MessageBus
        from agents.llm_client import LLMClient

        bus = MessageBus()
        all_keys = _get_all_api_keys(http_request)
        llm_client = LLMClient(
            anthropic_key=api_key if provider == "anthropic" else None,
            openai_key=all_keys.get("openai"),
            google_key=all_keys.get("google"),
        )

        pa = PAInterviewAgent(
            api_key=api_key if provider != "ollama" else "ollama",
            bus=bus,
            llm_client=llm_client,
        )

        # Inject language instruction into the conversation context
        lang = getattr(request_data, 'language', 'en') or 'en'
        LANG_NAMES = {"en":"English","zh":"Chinese (Simplified)","es":"Spanish","fr":"French","hi":"Hindi","de":"German","pt":"Portuguese","ja":"Japanese","ko":"Korean","ar":"Arabic","ru":"Russian","it":"Italian"}
        lang_instruction = ""
        if lang != "en" and lang in LANG_NAMES:
            lang_instruction = f"\n[LANGUAGE: Respond in {LANG_NAMES[lang]}. Ask questions and provide all text in {LANG_NAMES[lang]}.]"

        result = await pa.interview(
            conversation=request_data.conversation,
            age=request_data.age,
            gender=request_data.gender,
            model_preference=model_pref,
            language_instruction=lang_instruction,
        )

        return result

    except Exception as e:
        logger.error("PA interview error: %s", e, exc_info=True)
        # On error, return a safe fallback
        return {
            "action": "ask",
            "question": "I apologize for the interruption. Could you tell me more about your symptoms?",
            "exchange_count": len([m for m in request_data.conversation if m.get("role") == "user"])
        }


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

        # Language instruction for non-English
        gen_lang = getattr(request_data, 'language', 'en') or 'en'
        GEN_LANG_NAMES = {"en":"English","zh":"Chinese (Simplified)","es":"Spanish","fr":"French","hi":"Hindi","de":"German","pt":"Portuguese","ja":"Japanese","ko":"Korean","ar":"Arabic","ru":"Russian","it":"Italian"}
        gen_lang_suffix = ""
        if gen_lang != "en" and gen_lang in GEN_LANG_NAMES:
            gen_lang_suffix = f" IMPORTANT: Write the question in {GEN_LANG_NAMES[gen_lang]}."

        # HPI detail mode: generate multiple context-aware questions at once
        if request_data.mode == "hpi_detail" and request_data.context:
            if provider == "openai" or provider == "ollama":
                from openai import OpenAI
                client_kwargs = {"api_key": api_key}
                model_name = "gpt-4o"
                if provider == "ollama":
                    client_kwargs = {"api_key": "ollama", "base_url": OLLAMA_API_URL}
                    model_name = "llama3.1:8b"
                client = OpenAI(**client_kwargs)
                resp = client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": request_data.context + gen_lang_suffix}],
                    max_tokens=500, temperature=0.5,
                )
                return {"question": resp.choices[0].message.content.strip(), "estimated_cost": 0.0}
            else:
                import anthropic
                client = anthropic.Anthropic(api_key=api_key)
                resp = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=500,
                    temperature=0.5,
                    messages=[{"role": "user", "content": request_data.context + gen_lang_suffix}],
                )
                return {"question": resp.content[0].text.strip(), "estimated_cost": 0.01}

        if provider == "openai" or provider == "ollama":
            from openai import OpenAI
            client_kwargs = {"api_key": api_key}
            model_name = "gpt-4o"
            if provider == "ollama":
                client_kwargs = {"api_key": "ollama", "base_url": OLLAMA_API_URL}
                model_name = "llama3.1:8b"
            client = OpenAI(**client_kwargs)
            prompt = (
                f"Generate ONE specific follow-up question for a {request_data.age}-year-old {request_data.gender} "
                f"with symptoms: {request_data.symptoms}. Question {request_data.questions_asked + 1} of {request_data.total_ai_questions}. "
                f"Previously asked: {request_data.previous_questions}. Return ONLY the question, no preamble.{gen_lang_suffix}"
            )
            resp = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150, temperature=0.7,
            )
            return {"question": resp.choices[0].message.content.strip().strip('"'), "estimated_cost": 0.0}

        orchestrator = OrchestratorAgent(api_key=api_key)
        question = await orchestrator.generate_question(
            symptoms=request_data.symptoms,
            age=request_data.age,
            gender=request_data.gender,
            conversation_history=request_data.conversation_history,
            previous_questions=request_data.previous_questions,
            questions_asked=request_data.questions_asked,
            total_ai_questions=request_data.total_ai_questions,
            language=gen_lang,
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


# Map app specialty names to NPI taxonomy search terms
_SPECIALTY_MAP = {
    "primary care": ["Family Medicine", "Internal Medicine", "General Practice"],
    "self-management": ["Family Medicine", "Internal Medicine"],
    "internal medicine": ["Internal Medicine"],
    "dermatology": ["Dermatology"],
    "dermatologist": ["Dermatology"],
    "allergy": ["Allergy & Immunology"],
    "cardiology": ["Cardiovascular Disease"],
    "gastroenterology": ["Gastroenterology"],
    "neurology": ["Neurology"],
    "psychiatry": ["Psychiatry"],
    "rheumatology": ["Rheumatology"],
    "orthopedic": ["Orthopaedic Surgery"],
    "pulmonology": ["Pulmonary Disease"],
    "endocrinology": ["Endocrinology, Diabetes & Metabolism"],
    "oncology": ["Hematology & Oncology"],
    "urology": ["Urology"],
    "ophthalmology": ["Ophthalmology"],
    "ent": ["Otolaryngology"],
    "pediatrics": ["Pediatrics"],
    "ob/gyn": ["Obstetrics & Gynecology"],
}


def _resolve_taxonomy_terms(specialty: str) -> list[str]:
    """Convert an app specialty label into NPI taxonomy search terms."""
    lower = specialty.lower().strip()
    # Direct match
    if lower in _SPECIALTY_MAP:
        return _SPECIALTY_MAP[lower]
    # Try each part of compound specialties like "Primary Care / Dermatology"
    terms = []
    for part in lower.replace("/", ",").replace(" - ", ",").split(","):
        part = part.strip()
        if part in _SPECIALTY_MAP:
            terms.extend(_SPECIALTY_MAP[part])
        elif part:
            # Use the part as-is (capitalize properly for NPI)
            terms.append(part.title())
    return terms if terms else [specialty]


async def _npi_search(client, taxonomy: str, postal_code: str = "", city: str = "", state: str = "", limit: int = 10):
    """Run a single NPI registry search and return parsed results."""
    params = {
        "version": "2.1",
        "enumeration_type": "NPI-1",
        "taxonomy_description": taxonomy,
        "limit": limit,
    }
    if postal_code:
        params["postal_code"] = postal_code
    if city:
        params["city"] = city
    if state:
        params["state"] = state

    resp = await client.get("https://npiregistry.cms.hhs.gov/api/", params=params)
    data = resp.json()
    return data.get("results", [])


def _parse_npi_results(raw_results: list, specialty_label: str) -> list[dict]:
    """Parse raw NPI API results into clean doctor records."""
    results = []
    seen_npis = set()
    for r in raw_results:
        npi = r.get("number", "")
        if npi in seen_npis:
            continue
        seen_npis.add(npi)

        basic = r.get("basic", {})
        addresses = r.get("addresses", [])
        addr = next(
            (a for a in addresses if a.get("address_purpose") == "LOCATION"),
            addresses[0] if addresses else {},
        )
        taxonomies = r.get("taxonomies", [])
        primary_tax = next((t for t in taxonomies if t.get("primary")), taxonomies[0] if taxonomies else {})

        name_parts = []
        if basic.get("first_name"):
            name_parts.append(basic["first_name"].title())
        if basic.get("last_name"):
            name_parts.append(basic["last_name"].title())
        credential = basic.get("credential", "")

        full_name = " ".join(name_parts)
        if credential:
            full_name += f", {credential}"

        address_lines = []
        if addr.get("address_1"):
            address_lines.append(addr["address_1"].title())
        if addr.get("address_2"):
            address_lines.append(addr["address_2"].title())
        city_state = []
        if addr.get("city"):
            city_state.append(addr["city"].title())
        if addr.get("state"):
            city_state.append(addr["state"])
        if addr.get("postal_code"):
            city_state.append(addr["postal_code"][:5])
        if city_state:
            address_lines.append(", ".join(city_state))

        results.append({
            "npi": npi,
            "name": full_name,
            "specialty": primary_tax.get("desc", specialty_label),
            "address": "\n".join(address_lines),
            "phone": addr.get("telephone_number", ""),
            "accepting_patients": primary_tax.get("state", "") != "N",
        })
    return results


@app.get("/api/find-doctors")
async def find_doctors(
    specialty: str = "Primary Care",
    location: str = "",
    limit: int = 10,
):
    """
    Search the NPI Registry (free, no API key) for healthcare providers
    by specialty and location (zip code, city, or state).
    Handles compound specialty names and broadens search if needed.
    """
    import httpx

    # Parse location
    loc = location.strip()
    postal_code = ""
    city = ""
    state = ""
    if loc:
        if loc.isdigit() and len(loc) == 5:
            postal_code = loc
        elif "," in loc:
            parts = [p.strip() for p in loc.split(",")]
            city = parts[0]
            if len(parts) > 1 and len(parts[1]) <= 2:
                state = parts[1].upper()
        elif len(loc) == 2:
            state = loc.upper()
        else:
            city = loc

    taxonomy_terms = _resolve_taxonomy_terms(specialty)
    target_limit = min(limit, 20)

    try:
        all_raw = []
        async with httpx.AsyncClient(timeout=15.0) as client:
            # Search each taxonomy term
            for term in taxonomy_terms:
                raw = await _npi_search(client, term, postal_code=postal_code, city=city, state=state, limit=target_limit)
                all_raw.extend(raw)
                if len(all_raw) >= target_limit:
                    break

            # If zip code search returned too few, broaden to zip prefix (e.g., 816*)
            if len(all_raw) < 3 and postal_code and len(postal_code) == 5:
                for term in taxonomy_terms:
                    raw = await _npi_search(client, term, postal_code=postal_code[:3] + "*", limit=target_limit)
                    all_raw.extend(raw)
                    if len(all_raw) >= target_limit:
                        break

        results = _parse_npi_results(all_raw, specialty)[:target_limit]
        return {"results": results, "count": len(results)}

    except Exception as e:
        logger.error(f"NPI Registry search failed: {e}")
        return {"results": [], "count": 0, "error": str(e)}


@app.options("/{full_path:path}")
async def options_handler():
    return {"message": "CORS preflight OK"}


