# SkillSathi

> **Tagline:** *"Explore a future your whole family believes in."*  
> **Repository:** [https://github.com/GSriCharan12/SkillSathi](https://github.com/GSriCharan12/SkillSathi)  
> **Platform:** AI-Enabled Career Counselling and Family Decision-Support Platform for Vocational Education.

---

## 1. Executive Summary & Problem Context
In India, vocational education pathways (ITI certificates, Polytechnic diplomas, B.Voc degrees, and NAPS apprenticeship ladders) are frequently vetoed or abandoned not because students lack capability, but because **parents and family decision-makers harbor deep-seated anxieties** regarding:
- **Income & Financial Stability** (entry wage disparity, stipend security during training)
- **Social Status & Prestige (*Izzat*)** (stigma vs traditional degree paths)
- **Workplace Safety & Conditions** (safe industrial clusters, commute accessibility)
- **Long-term Career Mobility** (fear of dead-end careers; lack of awareness regarding lateral B.Tech / B.Voc entry).

Existing career guidance platforms are single-user and learner-centric. **SkillSathi treats the entire FAMILY as the fundamental decision unit**, mediating generational perspectives with verified, localized government tracer data (MSDE, NCVET, DGT, Labour Bureau, AICTE).

---

## 2. Platform Capabilities

1. **Dedicated Role-Based Portals**: Strict, role-isolated portals for **Students / Learners**, **Parents / Guardians**, **Certified Counsellors**, and **Scheme Administrators**.
2. **Joint Family Decision Room**: Real-time perspective alignment matching learner ambitions with parent security priorities.
3. **Anti-Hallucination Vocational AI**: 8-stage dialogue engine strictly grounded in official tracer statistics (no invented metrics or dead-end assumptions).
4. **Universal English Interface & Voice Guidance**: Natural, accessible career advisory with real-time speech input.
5. **Source Provenance & Freshness Hierarchy**: Transparent citations categorized into `LIVE`, `FRESH`, `STALE`, and `DEMO`.
6. **Certified Counsellor Workstation**: Escalation ecosystem for edge cases, state hostel subsidy circulars, and case notes.
7. **Scheme Administrator Telemetry**: Heatmaps and district resistance analytics mapping where and why parental hesitation is concentrated.


---

## 3. Documentation Index

Detailed technical specifications are available in the [`docs/`](./docs) directory:
- [System Architecture & Data Flows](./docs/architecture.md)
- [Database Schema & Provenance Model](./docs/database.md)
- [Official Data Sources & Ingestion Pipeline](./docs/data-sources.md)
- [AI Engine & Anti-Hallucination Guardrails](./docs/ai.md)
- [Security, RBAC & Privacy Standards](./docs/security.md)
- [Platform Demonstration Guide](./docs/demo.md)

---

## 4. Technology Stack

| Component | Technology | Description |
|---|---|---|
| **Frontend** | Next.js 16.3.8 (App Router), React 19, TypeScript | Server-side rendering, responsive touch layout |
| **Design System** | Future Garden Tokens, Tailwind CSS | Warm Ivory, Deep Navy, Teal, Emerald, and Coral |
| **Motion** | Framer Motion | Accessible motion engine respecting `prefers-reduced-motion` |
| **Backend** | FastAPI (Python 3.13), Pydantic v2 | High-throughput asynchronous REST & WebSocket API |
| **ORM & Database** | SQLAlchemy 2.0+, Alembic, MySQL 8.0+ | Relational schema with ACID compliance |
| **AI Provider Abstraction** | Gemini 1.5 Flash / OpenAI / Ollama / Mock | Provider-agnostic RAG dialogue pipeline |

---

## 5. Getting Started & Local Setup

### Prerequisites
- Node.js `v20+` (tested on `v22.14.0`)
- Python `3.11+` (tested on `3.13.2`)
- MySQL Server 8.0+ (Optional for SQLite test / mock mode)

### 1. Environment Configuration
Copy the template environment files:
```bash
cp .env.example .env
cp frontend/.env.example frontend/.env.local
```

Key environment parameters in `.env`:
```ini
# Application Mode
APP_ENV=development
SECRET_KEY=skillsathi_production_super_secret_jwt_signing_key_2026

# Database Connection (MySQL or SQLite)
DATABASE_URL=sqlite:///./skillsathi.db
# DATABASE_URL=mysql+pymysql://skillsathi_user:skillsathi_password@localhost:3306/skillsathi_db

# AI Provider Configuration (mock, gemini, openai, ollama)
AI_PROVIDER=mock
GEMINI_API_KEY=your_gemini_api_key_here
```

### 2. Backend Setup & Run
```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
- **API Base**: `http://localhost:8000`
- **Interactive OpenAPI Docs**: `http://localhost:8000/docs`
- **Health Probe**: `http://localhost:8000/api/v1/health`

### 3. Frontend Setup & Run
```bash
cd frontend
npm install
npm run dev
```
- Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 6. Testing & Quality Verification

Run the full automated test suite (45/45 unit, integration, and E2E tests):
```bash
# Run backend pytest suite
python -m pytest backend/tests

# Run frontend production build & TypeScript check
cd frontend
npm run build
```

---

## 7. Data Synchronization & Ingestion Pipeline

To trigger manual or scheduled synchronization of official government data feeds:
```bash
# Sync all registered adapters (NCVET, DGT, Labour Bureau)
python -m backend.app.data_sources.sync_coordinator
```

---

## 8. Production Deployment

### Containerized Deployment (Docker)
```bash
# Build and start services via Docker Compose
docker compose up -d --build
```

### Production Build Validation
- Frontend: `npm run build` outputs optimized static and SSR assets.
- Backend: Run via `uvicorn app.main:app --workers 4 --host 0.0.0.0 --port 8000`.
