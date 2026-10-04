"""SkillSathi Consolidated Schemas Index."""
from app.schemas.common import BaseSchema, TimestampedSchema, ApiResponse
from app.schemas.health import HealthStatus, DatabaseHealthStatus, AppVersionInfo
from app.schemas.evidence import EvidenceSourceBase, EvidenceSourceRead, DataQualityCheckRead
from app.schemas.trade import (
    LocationRead, TradeCategoryRead, TradeBase, TradeRead,
    TrainingProviderBase, TrainingProviderRead, TradeDetailRead
)
from app.schemas.pathway import (
    CareerPathwayRead, CareerPathwayStepRead, ProgressionOptionRead
)
from app.schemas.outcome import (
    OutcomeDataRead, EmploymentDataRead, EarningsDataRead
)
from app.schemas.sync import (
    DataSyncRunRead, AdminMonitoringSummary
)
from app.schemas.family import (
    UserRegisterRequest, UserLoginRequest, UserRead, TokenResponse,
    LearnerOnboardingUpdate, LearnerRead,
    ParentOnboardingUpdate, ParentRead,
    FamilyConcernRead, FamilySnapshotResponse,
)
from app.schemas.counsellor_case import (
    CounsellorNoteCreate, CounsellorNoteOut,
    CounsellorCaseCreate, CounsellorCaseAssign,
    CounsellorCaseStatusUpdate, ResourceRecommendation,
    CounsellorCaseOut, CounsellorDashboardSummary,
)
from app.schemas.family_decision import (
    DecisionStateUpdate, ConcernResolutionRequest,
    SaveTradeRequest, FamilyDecisionRoomSnapshot,
)
from app.schemas.admin_analytics import (
    AdminOverviewMetrics, ConcernCategoryStat,
    FamilyResistanceIndexItem, GeographicConcernHotspot,
    TradeAnalyticsItem, CounsellingFunnelStage,
    ProgrammeAnalyticsResponse,
)

__all__ = [
    "BaseSchema", "TimestampedSchema", "ApiResponse",
    "HealthStatus", "DatabaseHealthStatus", "AppVersionInfo",
    "EvidenceSourceBase", "EvidenceSourceRead", "DataQualityCheckRead",
    "LocationRead", "TradeCategoryRead", "TradeBase", "TradeRead",
    "TrainingProviderBase", "TrainingProviderRead", "TradeDetailRead",
    "CareerPathwayRead", "CareerPathwayStepRead", "ProgressionOptionRead",
    "OutcomeDataRead", "EmploymentDataRead", "EarningsDataRead",
    "DataSyncRunRead", "AdminMonitoringSummary",
    "UserRegisterRequest", "UserLoginRequest", "UserRead", "TokenResponse",
    "LearnerOnboardingUpdate", "LearnerRead",
    "ParentOnboardingUpdate", "ParentRead",
    "FamilyConcernRead", "FamilySnapshotResponse",
    # Counsellor Cases & Notes
    "CounsellorNoteCreate", "CounsellorNoteOut",
    "CounsellorCaseCreate", "CounsellorCaseAssign",
    "CounsellorCaseStatusUpdate", "ResourceRecommendation",
    "CounsellorCaseOut", "CounsellorDashboardSummary",
    # Family Decision Room
    "DecisionStateUpdate", "ConcernResolutionRequest",
    "SaveTradeRequest", "FamilyDecisionRoomSnapshot",
    # Programme Analytics & Resistance Dashboard
    "AdminOverviewMetrics", "ConcernCategoryStat",
    "FamilyResistanceIndexItem", "GeographicConcernHotspot",
    "TradeAnalyticsItem", "CounsellingFunnelStage",
    "ProgrammeAnalyticsResponse",
]
