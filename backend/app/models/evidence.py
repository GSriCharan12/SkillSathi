"""
SkillSathi - Verified Evidence Database Model
Stores verified government/industry metrics (MSDE, NSDC, NAPS, state data) to resolve family concerns.
"""
from sqlalchemy import Column, String, Integer, ForeignKey, Text, JSON, Boolean, Index
from sqlalchemy.orm import relationship
from app.models.base import TimeStampedBase


class VerifiedEvidence(TimeStampedBase):
    __tablename__ = "verified_evidences"

    trade_id = Column(Integer, ForeignKey("vocational_trades.id", ondelete="CASCADE"), nullable=True, index=True)
    source_agency = Column(String(64), nullable=False, index=True)  # e.g., "MSDE", "NSDC", "NAPS", "State Survey"
    category = Column(String(64), nullable=False, index=True)       # e.g., "SALARY", "PLACEMENT", "SAFETY", "MOBILITY"
    metric_title = Column(String(128), nullable=False)
    evidence_value = Column(String(255), nullable=False)
    evidence_metadata = Column(JSON, nullable=True)                 # Geo tags, sample size, year, etc.
    source_url = Column(String(512), nullable=True)
    is_verified = Column(Integer, default=1, nullable=False)

    # Relationships
    trade = relationship("VocationalTrade", back_populates="evidence_records")

    __table_args__ = (
        Index("idx_evidence_source_cat", "source_agency", "category"),
    )
