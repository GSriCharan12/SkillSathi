"""
SkillSathi - Pydantic Schemas for Counsellor Cases, Notes, and Escalations
Smart India Hackathon 2026 - Problem Statement 26241
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class CounsellorNoteCreate(BaseModel):
    note_text: str = Field(..., min_length=2)
    visibility: str = Field(default="COUNSELLOR_PRIVATE", description="'COUNSELLOR_PRIVATE' or 'FAMILY_SHARED'")
    is_action_item: bool = Field(default=False)


class CounsellorNoteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    case_id: int
    author_id: Optional[int] = None
    author_name: Optional[str] = None
    note_text: str
    visibility: str
    is_action_item: bool
    created_at: datetime
    updated_at: datetime


class CounsellorCaseCreate(BaseModel):
    family_id: int
    learner_id: Optional[int] = None
    trade_id: Optional[int] = None
    priority: str = Field(default="MEDIUM", description="'LOW', 'MEDIUM', 'HIGH', 'URGENT'")
    escalation_reason: str = Field(..., min_length=5)
    parent_concerns: Optional[List[str]] = None
    ai_summary: Optional[str] = None
    evidence_shown: Optional[List[Dict[str, Any]]] = None
    unresolved_questions: Optional[List[str]] = None
    preferred_contact_method: Optional[str] = Field(default="PHONE_CALL")
    contact_details: Optional[str] = None


class CounsellorCaseAssign(BaseModel):
    counsellor_id: int


class CounsellorCaseStatusUpdate(BaseModel):
    case_status: str = Field(..., description="'OPEN', 'ASSIGNED', 'IN_PROGRESS', 'RESOLVED', 'FOLLOW_UP_NEEDED'")
    resolution_summary: Optional[str] = None
    scheduled_at: Optional[datetime] = None


class ResourceRecommendation(BaseModel):
    resource_type: str = Field(..., description="'SCHEME', 'INSTITUTE', 'COUNSELLING_GUIDE', 'POLICY_DOC'")
    title: str
    description: str
    url: Optional[str] = None
    source_name: Optional[str] = None


class CounsellorCaseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    family_id: int
    family_code: Optional[str] = None
    family_name: Optional[str] = None
    location_label: Optional[str] = None
    learner_id: Optional[int] = None
    learner_name: Optional[str] = None
    trade_id: Optional[int] = None
    trade_title: Optional[str] = None
    assigned_counsellor_id: Optional[int] = None
    assigned_counsellor_name: Optional[str] = None
    priority: str
    case_status: str
    escalation_reason: str
    parent_concerns: Optional[List[str]] = None
    ai_summary: Optional[str] = None
    evidence_shown: Optional[List[Dict[str, Any]]] = None
    unresolved_questions: Optional[List[str]] = None
    recommended_resources: Optional[List[Dict[str, Any]]] = None
    resolution_summary: Optional[str] = None
    preferred_contact_method: str
    contact_details: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    notes_count: int = 0
    notes: Optional[List[CounsellorNoteOut]] = None


class CounsellorDashboardSummary(BaseModel):
    total_cases: int
    new_cases: int
    active_cases: int
    priority_cases: int
    resolved_cases: int
    recent_cases: List[CounsellorCaseOut]
