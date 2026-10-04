"""
SkillSathi - Consolidated API Router
Aggregates all domain routers under /api/v1 prefix.
"""
from fastapi import APIRouter
from app.routers.health import router as health_router
from app.routers.auth import router as auth_router
from app.routers.family import router as family_router
from app.routers.trades import router as trades_router
from app.routers.outcomes import router as outcomes_router
from app.routers.pathways import router as pathways_router
from app.routers.evidence import router as evidence_router
from app.routers.data_sync import router as data_sync_router
from app.routers.admin_monitoring import router as admin_monitoring_router
from app.routers.counselling import router as counselling_router
from app.routers.counsellor_cases import router as counsellor_cases_router
from app.routers.family_decisions import router as family_decisions_router
from app.routers.admin_analytics import router as admin_analytics_router

api_router = APIRouter()

# 1. Health & Diagnostics
api_router.include_router(health_router, prefix="")

# 2. Authentication & Access Control
api_router.include_router(auth_router, prefix="")

# 3. Family Decision Room & Onboarding
api_router.include_router(family_router, prefix="")

# 4. Trades & Training Providers
api_router.include_router(trades_router, prefix="")

# 5. Verified Outcomes & Tracer Evidence
api_router.include_router(outcomes_router, prefix="")

# 6. Career Pathways & Lateral Education Ladders
api_router.include_router(pathways_router, prefix="")

# 7. Evidence Sources & Provenance
api_router.include_router(evidence_router, prefix="")

# 8. Data Synchronization & Ingestion Engine
api_router.include_router(data_sync_router, prefix="")

# 9. Admin Data Monitoring & Quality Telemetry
api_router.include_router(admin_monitoring_router, prefix="")

# 10. AI Vocational Counselling Engine
api_router.include_router(counselling_router, prefix="")

# 11. Human Counsellor Cases & Real-Time Escalations
api_router.include_router(counsellor_cases_router, prefix="")

# 12. Family Decision Room & Consensus Matrix
api_router.include_router(family_decisions_router, prefix="")

# 13. Scheme Administrator & Programme Analytics
api_router.include_router(admin_analytics_router, prefix="")


