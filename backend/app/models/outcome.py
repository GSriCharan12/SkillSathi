"""
SkillSathi - Verified Outcome, Employment, and Earnings Models
STRICT RULE: The AI must NEVER invent vocational outcome data. All stats link to EvidenceSource.
"""
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, Text, JSON, Boolean, Index
from sqlalchemy.orm import relationship
from app.models.base import TimeStampedBase


class OutcomeData(TimeStampedBase):
    """
    Primary verified outcome record linking trades to verified placement rates,
    stipends, earnings, and government sources.
    """
    __tablename__ = "outcome_data"

    trade_id = Column(Integer, ForeignKey("trades.id", ondelete="CASCADE"), nullable=False, index=True)
    provider_id = Column(Integer, ForeignKey("training_providers.id", ondelete="SET NULL"), nullable=True, index=True)
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="SET NULL"), nullable=True, index=True)
    placement_rate = Column(Float, nullable=False)                                          # 0.0 to 100.0%
    earnings_min = Column(Integer, nullable=False)                                          # INR
    earnings_max = Column(Integer, nullable=False)                                          # INR
    earnings_period = Column(String(32), default="MONTHLY", nullable=False)                # MONTHLY, ANNUAL, STIPEND
    employment_type = Column(String(64), default="REGULAR_WAGE", nullable=False)           # REGULAR_WAGE, APPRENTICE, SELF_EMPLOYED, CONTRACT
    data_year = Column(Integer, nullable=False, index=True)                                 # e.g., 2024
    sample_size = Column(Integer, nullable=True)
    source_id = Column(Integer, ForeignKey("evidence_sources.id", ondelete="RESTRICT"), nullable=False, index=True)
    verification_status = Column(String(64), default="OFFICIAL_VERIFIED", nullable=False, index=True)
    last_verified_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    last_synced_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    is_demo = Column(Boolean, default=False, nullable=False, index=True)

    # Relationships
    trade = relationship("Trade", back_populates="outcomes")
    provider = relationship("TrainingProvider", back_populates="outcomes")
    location = relationship("Location", back_populates="outcomes")
    source = relationship("EvidenceSource", back_populates="outcomes")
    employment_records = relationship("EmploymentData", back_populates="outcome", cascade="all, delete-orphan")
    earnings_records = relationship("EarningsData", back_populates="outcome", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_outcome_trade_loc_year", "trade_id", "location_id", "data_year"),
        Index("idx_outcome_source_status", "source_id", "verification_status"),
    )


class EmploymentData(TimeStampedBase):
    """
    Detailed employment distribution, top hiring sectors, retention, and formal contract data.
    """
    __tablename__ = "employment_data"

    outcome_id = Column(Integer, ForeignKey("outcome_data.id", ondelete="CASCADE"), nullable=True, index=True)
    trade_id = Column(Integer, ForeignKey("trades.id", ondelete="CASCADE"), nullable=False, index=True)
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="SET NULL"), nullable=True, index=True)
    top_hiring_sectors = Column(JSON, nullable=True)  # e.g., ["Automotive OEM", "Solar EPC", "Smart Metering"]
    top_employer_names = Column(JSON, nullable=True)  # e.g., ["Tata Motors", "Schneider Electric", "L&T"]
    retention_rate_1yr = Column(Float, nullable=True) # e.g., 82.5%
    formal_contract_pct = Column(Float, nullable=True) # e.g., 94.0%
    source_id = Column(Integer, ForeignKey("evidence_sources.id", ondelete="RESTRICT"), nullable=False, index=True)
    is_demo = Column(Boolean, default=False, nullable=False, index=True)

    # Relationships
    outcome = relationship("OutcomeData", back_populates="employment_records")
    trade = relationship("Trade", back_populates="employment_data")


class EarningsData(TimeStampedBase):
    """
    Granular salary percentiles, training stipends, and mid-career progression data.
    """
    __tablename__ = "earnings_data"

    outcome_id = Column(Integer, ForeignKey("outcome_data.id", ondelete="CASCADE"), nullable=True, index=True)
    trade_id = Column(Integer, ForeignKey("trades.id", ondelete="CASCADE"), nullable=False, index=True)
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="SET NULL"), nullable=True, index=True)
    median_starting_monthly_inr = Column(Integer, nullable=False)
    mid_career_monthly_inr = Column(Integer, nullable=True)
    p10_inr = Column(Integer, nullable=True)
    p90_inr = Column(Integer, nullable=True)
    stipend_during_training_inr = Column(Integer, default=0, nullable=False)
    source_id = Column(Integer, ForeignKey("evidence_sources.id", ondelete="RESTRICT"), nullable=False, index=True)
    is_demo = Column(Boolean, default=False, nullable=False, index=True)

    # Relationships
    outcome = relationship("OutcomeData", back_populates="earnings_records")
    trade = relationship("Trade", back_populates="earnings_data")
