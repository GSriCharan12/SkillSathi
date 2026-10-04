"""
SkillSathi - Consolidated SQLAlchemy Models Registry
All 26 entities required for Real Data Architecture.
"""
from app.models.base import TimeStampedBase
from app.models.evidence_source import EvidenceSource, DataSyncRun, DataQualityCheck
from app.models.location import Location
from app.models.trade import TradeCategory, Trade, TrainingProvider, ProviderTrade
from app.models.pathway import CareerPathway, CareerPathwayStep, ProgressionOption
from app.models.outcome import OutcomeData, EmploymentData, EarningsData
from app.models.family import (
    User,
    Family,
    Learner,
    ParentGuardian,
    FamilyConcern,
    LearnerPreference,
    FamilyDecision,
)
from app.models.counselling import (
    CounsellingSession,
    CounsellingMessage,
    CareerExploration,
    CounsellorCase,
    CounsellorNote,
    AdminEvent,
)

__all__ = [
    "TimeStampedBase",
    # Provenance & Quality
    "EvidenceSource",
    "DataSyncRun",
    "DataQualityCheck",
    # Locations
    "Location",
    # Trades & Providers
    "TradeCategory",
    "Trade",
    "TrainingProvider",
    "ProviderTrade",
    # Pathways & Ladders
    "CareerPathway",
    "CareerPathwayStep",
    "ProgressionOption",
    # Outcomes & Earnings
    "OutcomeData",
    "EmploymentData",
    "EarningsData",
    # Family Units & Users
    "User",
    "Family",
    "Learner",
    "ParentGuardian",
    "FamilyConcern",
    "LearnerPreference",
    "FamilyDecision",
    # Counselling & Audit
    "CounsellingSession",
    "CounsellingMessage",
    "CareerExploration",
    "CounsellorCase",
    "CounsellorNote",
    "AdminEvent",
]
