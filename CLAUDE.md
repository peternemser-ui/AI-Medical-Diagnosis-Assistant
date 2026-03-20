# AI Medical Diagnosis Assistant

## Project Overview
Multi-agent medical diagnosis system powered by Claude AI (Anthropic SDK). A Vue.js 3 frontend communicates with a FastAPI backend that runs 4 autonomous AI agents in a diagnostic pipeline.

## Architecture

### Multi-Agent Pipeline (7 Agents)
```
Patient Input → Triage → Diagnostician + Research (parallel) → Specialist → Treatment → Safety → Empathy → Unified Response
```

All agents communicate via an async MessageBus and can request consultations from each other.

### Agents (backend/agents/)
1. **Triage Agent** (`triage.py`) — Urgency assessment, red flag detection, domain classification
2. **Diagnostician Agent** (`diagnostician.py`) — Differential diagnosis, Bayesian clinical reasoning, pattern matching
3. **Research Agent** (`research.py`) — Evidence-based literature, clinical guidelines, drug interactions, disease prevalence
4. **Specialist Agent** (`specialist.py`) — Domain-specific deep analysis, diagnostic criteria (HEART, Wells, CURB-65, PHQ-9)
5. **Treatment Agent** (`treatment.py`) — Treatment plans, medication safety checks, lifestyle recommendations
6. **Safety Agent** (`safety.py`) — Contraindication checks, dosage safety, allergy risk, dangerous combination detection
7. **Empathy Agent** (`empathy.py`) — Patient-friendly language translation, plain-language summaries, action checklists

### Infrastructure
- **Orchestrator** (`orchestrator.py`) — Coordinates the 7-agent pipeline, runs Diagnostician+Research in parallel
- **Base Agent** (`base.py`) — Abstract base class with Claude tool-use loop
- **Message Bus** (`message_bus.py`) — Async inter-agent communication system

### Tech Stack
- **Frontend:** Vue.js 3 + Vite + Tailwind CSS
- **Backend:** FastAPI + Anthropic SDK (Claude)
- **AI Model:** Claude Sonnet (via Anthropic API)
- **Legacy Support:** OpenAI GPT-4o (fallback)

## Running the Project

```bash
# Backend
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Frontend
cd frontend
npm install
npm run dev
```

## Environment Variables
- `ANTHROPIC_API_KEY` — Required for multi-agent mode (recommended)
- `OPENAI_API_KEY` — Legacy fallback

## Key Files
- `backend/main.py` — FastAPI endpoints (v3.0.0)
- `backend/agents/` — All agent code
- `backend/models.py` — Pydantic request/response models
- `frontend/src/views/VoiceDiagnosis.vue` — Main chat interface
- `frontend/src/components/ChatArea.vue` — Message rendering + DiagnosisCard
- `frontend/src/components/AgentPipelineIndicator.vue` — Live agent status visualization
- `frontend/src/components/DiagnosisCard.vue` — Structured diagnosis result cards
- `frontend/src/services/api.js` — API client (supports both Anthropic + OpenAI keys)

## API Endpoints
- `POST /api/diagnose` — Runs full multi-agent pipeline
- `POST /api/followup` — Follow-up questions via treatment agent
- `POST /api/generate-question` — AI-generated follow-up questions via diagnostician
- `GET /api/agents` — Multi-agent system info
- `GET /health` — Health check

## Conventions
- Backend agents return structured JSON with `causes`, `red_flags`, `recommended_tests`, `agent_timings`
- Frontend stores API keys in localStorage (`anthropic_api_key` or `openai_api_key`)
- All agents use Claude Sonnet with temperature 0.2-0.3 for clinical accuracy
- The frontend simulates agent pipeline progress during the API call, then snaps to real timings
