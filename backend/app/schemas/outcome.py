"""
SkillSathi - Outcome, Employment, and Earnings Schemas
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import Field
from app.schemas.common import BaseSchema, TimestampedSchema
from app.schemas.evidence import EvidenceSourceRead
from app.schemas.trade import TradeRead, TrainingProviderRead, LocationRead


class EmploymentDataRead(TimestampedSchema):
    outcome_id: Optional[int] = None
    trade_id: int
    location_id: Optional[int] = None
    top_hiring_sectors: Optional[List[str]] = None
    top_employer_names: Optional[List[str]] = None
    retention_rate_1yr: Optional[float] = None
    formal_contract_pct: Optional[float] = None
    source_id: int
    is_demo: bool = False


class EarningsDataRead(TimestampedSchema):
    outcome_id: Optional[int] = None
    trade_id: int
    location_id: Optional[int] = None
    median_starting_monthly_inr: int
    mid_career_monthly_inr: Optional[int] = None
    p10_inr: Optional[int] = None
    p90_inr: Optional[int] = None
    stipend_during_training_inr: int = 0
    source_id: int
    is_demo: bool = False


class OutcomeDataRead(TimestampedSchema):
    trade_id: int
    provider_id: Optional[int] = None
    location_id: Optional[int] = None
    placement_rate: float
    earnings_min: int
    earnings_max: int
    earnings_period: str
    employment_type: str
    data_year: int
    sample_size: Optional[int] = None
    source_id: int
    verification_status: str
    last_verified_at: datetime
    last_synced_at: datetime
    is_demo: bool = False

    trade: Optional[TradeRead] = None
    provider: Optional[TrainingProviderRead] = None
    location: Optional[LocationRead] = None
    source: Optional[EvidenceSourceRead] = None
    employment_records: List[EmploymentDataRead] = []
    earnings_records: List[EarningsDataRead] = []
