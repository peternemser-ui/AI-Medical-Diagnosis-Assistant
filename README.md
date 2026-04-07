# MedDiagnose AI

> AI-powered medical diagnosis platform with 7 specialized agents, real-time streaming, and enterprise-grade features.

<!-- Screenshot placeholders -->
<!-- ![Landing Page](docs/screenshots/landing.png) -->
<!-- ![Consultation](docs/screenshots/consultation.png) -->
<!-- ![Admin Dashboard](docs/screenshots/admin.png) -->

---

## Features

### For Patients

- **Conversational AI consultation** with animated avatar (Dr. Hopps) featuring eye tracking and expression changes
- **Photo upload with annotation tools** -- circle, arrow, freehand draw, text labels
- **Interactive body map** for point-and-click symptom input
- **Voice input** with Web Speech API recognition and synthesis
- **Multi-language support** across 12 languages (English, Spanish, French, German, Italian, Portuguese, Chinese, Japanese, Korean, Hindi, Arabic, Russian)
- **PDF clinical reports** with medical disclaimers and structured findings
- **Appointment booking** with NPI-based doctor search
- **Symptom autocomplete** with medical terminology suggestions

### For Clinicians

- **7-agent diagnostic pipeline** (Triage, Diagnostician, Research, Specialist, Treatment, Safety, Empathy)
- **5 specialist sub-agents** (Cardiology, Neurology, Dermatology, Gastroenterology, Psychiatry)
- **Clinical reasoning transparency** -- expandable evidence sections per diagnosis
- **ESI triage urgency system** with red-flag detection
- **Drug interaction checking** via dedicated agent
- **Safety review** with 50+ contraindication rules
- **Scoring systems**: HEART, Wells, CURB-65, PHQ-9 and more

### For Operators

- **Admin dashboard** with 16 operational pages (Overview, Agents, Analytics, Billing, Cases, Config, Developer Portal, Improve, Logs, Model Compare, Referrals, Reports, Reviews, SEO, System Insights)
- **Self-learning Quality Auditor** that identifies systematic weaknesses
- **Agent health monitoring** with derived status indicators
- **Real-time SSE streaming** for diagnosis progress
- **Feature flags system** for controlled rollouts
- **Rate limiting** via SlowAPI

### For Business

- **Freemium subscription tiers** (Free / Plus / Pro / Family)
- **Stripe payment integration** with subscription management
- **API-as-a-Service** for external developers (Developer Portal)
- **White-label theming** for B2B clinic deployments
- **Specialist referral tracking** with revenue attribution
- **Analytics funnel tracking** across the patient journey

---

## Architecture

### Multi-Agent Pipeline

```
Patient Input
    |
    v
  Triage -----> urgency level, red flags, domain classification
    |
    v
  Diagnostician + Research  (parallel execution)
    |
    v
  Specialist -----> domain-specific deep analysis (Cardiology, Neuro, Derm, GI, Psych)
    |
    v
  Treatment -----> medication plans, lifestyle recommendations
    |
    v
  Safety -----> contraindication checks, dosage validation, allergy risk
    |
    v
  Empathy -----> patient-friendly language, plain-English summaries, action checklists
    |
    v
  Unified Report
```

All agents communicate via an **async MessageBus** and can request consultations from each other. The Orchestrator coordinates the pipeline and runs Diagnostician + Research in parallel for speed.

### Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Vue.js 3 + Vite + Tailwind CSS |
| **Backend** | FastAPI + Python 3.11+ |
| **AI Models** | Anthropic Claude (Sonnet/Haiku/Opus), OpenAI GPT-4o, Google Gemini, Ollama (local) |
| **Auth** | JWT + bcrypt + Fernet encryption |
| **Database** | PostgreSQL 16 (Docker), SQLite (local dev) |
| **Cache** | Redis 7 (sessions, rate limiting, pub/sub) |
| **Deployment** | Docker Compose (3 services + PostgreSQL + Redis) |
| **PWA** | Service worker + offline mode |

### Key Agents

| Agent | File | Purpose |
|-------|------|---------|
| Triage | `triage.py` | Urgency assessment, red-flag detection, domain routing |
| Diagnostician | `diagnostician.py` | Differential diagnosis, Bayesian reasoning, pattern matching |
| Research | `research.py` | Evidence-based literature, clinical guidelines, prevalence data |
| Specialist | `specialist.py` | Domain-specific analysis via 5 sub-specialists |
| Treatment | `treatment.py` | Treatment plans, medication safety, lifestyle guidance |
| Safety | `safety.py` | Contraindications, dosage checks, dangerous combinations |
| Empathy | `empathy.py` | Patient-friendly translation, plain-language summaries |
| Quality Auditor | `quality_auditor.py` | Self-learning review of diagnostic accuracy |
| Drug Interaction | `drug_interaction_agent.py` | Dedicated drug-drug interaction analysis |
| Image | `image_agent.py` | Medical image analysis and annotation |

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- An Anthropic API key (recommended) or OpenAI API key

### Backend

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Docker (Full Stack)

```bash
docker-compose up --build
```

This starts five services: PostgreSQL, Redis, the FastAPI backend, and the Vite dev frontend. Access the app at `http://localhost:3000`.

### Access Points

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Recommended | Claude AI models (Sonnet, Haiku, Opus) |
| `OPENAI_API_KEY` | Optional | GPT-4o fallback |
| `GOOGLE_API_KEY` | Optional | Gemini models |
| `STRIPE_SECRET_KEY` | Optional | Payment processing |
| `SMTP_HOST` | Optional | Email notifications |
| `FRONTEND_URL` | Optional | Base URL for email links |
| `JWT_SECRET` | Optional | JWT signing key |
| `ENCRYPTION_KEY` | Optional | Fernet encryption key for PHI |
| `POSTGRES_PASSWORD` | Optional | Database password (Docker) |
| `REDIS_PASSWORD` | Optional | Redis password (Docker) |
| `ENFORCE_HTTPS` | Optional | Enable HSTS header |

API keys can also be configured via the in-app setup screen. Keys are stored in the browser's `localStorage` and sent via request headers -- never stored on the server.

---

## API Endpoints

### Core Diagnosis

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/diagnose` | Run full 7-agent diagnostic pipeline |
| `POST` | `/api/diagnose-stream` | SSE streaming version of diagnose |
| `POST` | `/api/followup` | Follow-up questions via treatment agent |
| `POST` | `/api/generate-question` | AI-generated follow-up questions |
| `GET` | `/api/agents` | Multi-agent system info |
| `GET` | `/health` | Health check |

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/auth/register` | Create account |
| `POST` | `/auth/login` | Login, receive JWT |
| `POST` | `/auth/refresh` | Refresh JWT token |

### Admin

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/admin/metrics` | System metrics and KPIs |
| `GET` | `/admin/agents` | Agent health and status |
| `GET` | `/admin/cases` | Case review queue |

### Subscriptions & Billing

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/subscription/checkout` | Create Stripe checkout session |
| `GET` | `/subscription/status` | Current plan details |

---

## Testing

```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd frontend
npm run test
```

---

## Project Structure

```
AI Medical Diagnosis Assistant/
|-- backend/
|   |-- main.py                  # FastAPI app, routes, middleware
|   |-- agents/
|   |   |-- orchestrator.py      # Pipeline coordinator
|   |   |-- base.py              # Abstract agent base class
|   |   |-- message_bus.py       # Async inter-agent communication
|   |   |-- triage.py            # Urgency & red-flag assessment
|   |   |-- diagnostician.py     # Differential diagnosis
|   |   |-- research.py          # Evidence-based literature
|   |   |-- specialist.py        # Domain-specific analysis
|   |   |-- treatment.py         # Treatment recommendations
|   |   |-- safety.py            # Contraindication checks
|   |   |-- empathy.py           # Patient-friendly language
|   |   |-- quality_auditor.py   # Self-learning QA
|   |   |-- specialists/         # Sub-specialist modules
|   |   |   |-- cardiology.py
|   |   |   |-- neurology.py
|   |   |   |-- dermatology.py
|   |   |   |-- gastroenterology.py
|   |   |   |-- psychiatry.py
|   |   |   +-- registry.py
|   |   +-- ...                  # 10+ utility agents
|   |-- admin/                   # Admin dashboard backend
|   |-- auth.py                  # JWT + bcrypt authentication
|   |-- config.py                # Environment configuration
|   |-- database.py              # Database connections
|   |-- models.py                # Pydantic request/response models
|   +-- tests/                   # Backend test suite
|-- frontend/
|   |-- src/
|   |   |-- views/
|   |   |   |-- HomeView.vue           # Landing page
|   |   |   |-- VoiceDiagnosis.vue     # Main consultation interface
|   |   |   |-- PricingView.vue        # Subscription plans
|   |   |   |-- AuthLogin.vue          # Login
|   |   |   |-- AuthSignup.vue         # Registration
|   |   |   +-- admin/                 # 16 admin dashboard pages
|   |   |-- components/
|   |   |   |-- ChatArea.vue           # Message rendering
|   |   |   |-- DiagnosisCard.vue      # Structured diagnosis cards
|   |   |   |-- DoctorAvatar.vue       # Animated Dr. Hopps
|   |   |   |-- BodyDiagram.vue        # Interactive body map
|   |   |   |-- CameraCapture.vue      # Photo capture
|   |   |   |-- AgentPipelineIndicator.vue  # Live pipeline progress
|   |   |   +-- ...                    # 40+ components
|   |   |-- i18n/translations.js       # 12-language support
|   |   +-- services/                  # API clients
|   +-- vite.config.js
+-- docker-compose.yml                 # Full-stack deployment
```

---

## Security & Privacy

- **JWT authentication** with bcrypt password hashing
- **Fernet encryption** for sensitive patient data at rest
- **Security headers**: X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, Referrer-Policy, Permissions-Policy
- **HSTS** support when HTTPS is enforced
- **Rate limiting** on all endpoints via SlowAPI
- **CORS** whitelisting with configurable origins
- **API keys** transmitted via headers, never logged or stored server-side
- **Input sanitization** and Pydantic validation on all inputs

---

## Medical Disclaimer

This is an AI-powered tool for **informational purposes only**. It does not constitute medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals for medical concerns. Never disregard professional medical advice or delay seeking it because of something generated by this application.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Material Icons are distributed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0).
