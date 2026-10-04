"""
SkillSathi - Pydantic Schemas for Administrator and Programme Analytics System
Smart India Hackathon 2026 - Problem Statement 26241:
"A dashboard for scheme administrators showing where and why family resistance is concentrated."
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class AdminOverviewMetrics(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    families_counselled: int = 0
    active_sessions: int = 0
    high_concern_cases: int = 0
    counsellor_escalations: int = 0
    resolved_sessions: int = 0
    unresolved_cases: int = 0
    average_family_alignment: float = 0.0
    total_trades_cataloged: int = 0
    total_providers_mapped: int = 0


class ConcernCategoryStat(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    category: str
    count: int = 0
    percentage: float = 0.0
    avg_severity: float = 0.0
    unresolved_count: int = 0
    top_associated_trades: List[str] = []
    top_districts: List[str] = []


class FamilyResistanceIndexItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    family_id: int
    family_code: str
    district: Optional[str] = None
    state: Optional[str] = None
    concern_score: float  # 0 to 100
    unresolved_concerns: int
    decision_state: str
    counsellor_requested: bool
    primary_concern: Optional[str] = None
    resistance_level: str  # "LOW", "MODERATE", "HIGH", "ACUTE"


class GeographicConcernHotspot(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    state: str
    district: str
    total_families: int = 0
    total_concerns: int = 0
    avg_resistance_score: float = 0.0
    primary_concern_category: str = "INCOME"
    top_explored_trade: Optional[str] = None
    escalation_rate: float = 0.0


class TradeAnalyticsItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    trade_id: int
    trade_title: str
    sector: str
    nsqf_level: int
    exploration_count: int = 0
    comparison_count: int = 0
    top_concern_category: Optional[str] = None
    escalations_count: int = 0
    average_alignment: float = 0.0


class CounsellingFunnelStage(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    stage_key: str
    stage_label: str
    count: int = 0
    conversion_pct: float = 0.0
    drop_off_pct: float = 0.0


class ProgrammeAnalyticsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    overview: AdminOverviewMetrics
    concerns_breakdown: List[ConcernCategoryStat] = []
    resistance_index: List[FamilyResistanceIndexItem] = []
    resistance_methodology: str
    geographic_hotspots: List[GeographicConcernHotspot] = []
    trade_analytics: List[TradeAnalyticsItem] = []
    counselling_funnel: List[CounsellingFunnelStage] = []
    filter_context: Dict[str, Any] = {}
    generated_at: str
