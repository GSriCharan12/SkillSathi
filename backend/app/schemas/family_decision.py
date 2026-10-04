"""
SkillSathi - Pydantic Schemas for Family Decision Room & Alignment
Smart India Hackathon 2026 - Problem Statement 26241
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class DecisionStateUpdate(BaseModel):
    decision_status: str = Field(
        ...,
        description="One of: 'EXPLORING', 'DISCUSSING', 'COMPARING', 'NEEDS_COUNSELLING', 'INFORMED', 'DECISION_MADE'"
    )
    selected_trade_id: Optional[int] = None
    selected_pathway_id: Optional[int] = None
    learner_agreed: Optional[bool] = None
    parent_agreed: Optional[bool] = None
    alignment_notes: Optional[str] = None


class ConcernResolutionRequest(BaseModel):
    concern_id: int
    resolution_notes: Optional[str] = None
    addressed_evidence_id: Optional[int] = None


class SaveTradeRequest(BaseModel):
    trade_id: int
    bookmarked: bool = True
    notes: Optional[str] = None


class FamilyDecisionRoomSnapshot(BaseModel):
    family_id: int
    family_code: str
    family_name: Optional[str] = None
    location_label: Optional[str] = None
    alignment_score: float
    decision_status: str  # EXPLORING, DISCUSSING, COMPARING, NEEDS_COUNSELLING, INFORMED, DECISION_MADE
    
    # Perspectives
    learner_perspective: Dict[str, Any]
    parent_perspective: Dict[str, Any]
    shared_priorities: List[str]
    discussion_topics: List[str]
    
    # Concerns
    reported_concerns: List[Dict[str, Any]]
    resolved_concerns_count: int
    open_concerns_count: int
    
    # Active & Saved Options
    selected_trade: Optional[Dict[str, Any]] = None
    saved_trades: List[Dict[str, Any]] = []
    
    # Relevant Evidence & Cases
    evidence_citations: List[Dict[str, Any]] = []
    active_counsellor_case: Optional[Dict[str, Any]] = None
    shared_counsellor_notes: List[Dict[str, Any]] = []
    
    learner_agreed: bool = False
    parent_agreed: bool = False
    updated_at: datetime
