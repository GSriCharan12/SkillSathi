"""
SkillSathi - Pathway, Step, and Progression Option Schemas
"""
from typing import Optional, List
from app.schemas.common import BaseSchema, TimestampedSchema
from app.schemas.evidence import EvidenceSourceRead


class ProgressionOptionRead(TimestampedSchema):
    pathway_step_id: int
    destination_type: str
    title: str
    eligibility_criteria: Optional[str] = None
    recognizing_body: str = "AICTE/UGC"
    source_id: Optional[int] = None
    source: Optional[EvidenceSourceRead] = None


class CareerPathwayStepRead(TimestampedSchema):
    pathway_id: int
    step_order: int
    role_title: str
    experience_required_months: int = 0
    certifications_required: Optional[str] = None
    expected_monthly_inr_min: Optional[int] = None
    expected_monthly_inr_max: Optional[int] = None
    education_ladder_option: Optional[str] = None
    description: Optional[str] = None
    progression_options: List[ProgressionOptionRead] = []


class CareerPathwayRead(TimestampedSchema):
    trade_id: int
    title: str
    overview: Optional[str] = None
    entry_qualification: str
    total_progression_years: int
    is_demo: bool = False
    steps: List[CareerPathwayStepRead] = []
