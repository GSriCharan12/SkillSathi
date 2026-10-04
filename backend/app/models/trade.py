"""
SkillSathi - Trade, Category, and Training Provider Models
Maps NSQF vocational qualifications, ITIs, Polytechnics, and PMKK training centers.
"""
from sqlalchemy import Column, String, Integer, ForeignKey, Text, Boolean, Index
from sqlalchemy.orm import relationship
from app.models.base import TimeStampedBase


class TradeCategory(TimeStampedBase):
    __tablename__ = "trade_categories"

    code = Column(String(32), unique=True, index=True, nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    icon_name = Column(String(64), default="Compass", nullable=False)

    # Relationships
    trades = relationship("Trade", back_populates="category")


class Trade(TimeStampedBase):
    __tablename__ = "trades"

    category_id = Column(Integer, ForeignKey("trade_categories.id", ondelete="SET NULL"), nullable=True, index=True)
    code = Column(String(64), unique=True, index=True, nullable=False)  # QP/NOS Code or CTS Code
    title = Column(String(128), nullable=False, index=True)
    sector = Column(String(64), nullable=False, index=True)            # Automotive, Electronics, Green Energy, Healthcare
    nsqf_level = Column(Integer, default=4, nullable=False, index=True)
    duration_months = Column(Integer, default=12, nullable=False)
    min_qualification = Column(String(64), default="10th Standard", nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_demo = Column(Boolean, default=False, nullable=False, index=True)

    # Relationships
    category = relationship("TradeCategory", back_populates="trades")
    provider_trades = relationship("ProviderTrade", back_populates="trade", cascade="all, delete-orphan")
    career_pathways = relationship("CareerPathway", back_populates="trade", cascade="all, delete-orphan")
    outcomes = relationship("OutcomeData", back_populates="trade", cascade="all, delete-orphan")
    employment_data = relationship("EmploymentData", back_populates="trade", cascade="all, delete-orphan")
    earnings_data = relationship("EarningsData", back_populates="trade", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_trade_sector_level", "sector", "nsqf_level"),
    )


class TrainingProvider(TimeStampedBase):
    __tablename__ = "training_providers"

    name = Column(String(192), nullable=False, index=True)
    code = Column(String(64), unique=True, index=True, nullable=False)  # DGT MIS / NCVET / AICTE Institute code
    provider_type = Column(String(64), default="GOVT_ITI", nullable=False, index=True)  # GOVT_ITI, PRIVATE_ITI, NSTI, POLYTECHNIC, PMKK, DGT_AFFILIATED
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="SET NULL"), nullable=True, index=True)
    affiliation_body = Column(String(64), default="NCVET", nullable=False)               # NCVET, DGT, AICTE, NSDC
    website_url = Column(String(512), nullable=True)
    is_verified = Column(Boolean, default=True, nullable=False, index=True)
    is_demo = Column(Boolean, default=False, nullable=False, index=True)

    # Relationships
    location = relationship("Location", back_populates="providers")
    provider_trades = relationship("ProviderTrade", back_populates="provider", cascade="all, delete-orphan")
    outcomes = relationship("OutcomeData", back_populates="provider")


class ProviderTrade(TimeStampedBase):
    __tablename__ = "provider_trades"

    provider_id = Column(Integer, ForeignKey("training_providers.id", ondelete="CASCADE"), nullable=False, index=True)
    trade_id = Column(Integer, ForeignKey("trades.id", ondelete="CASCADE"), nullable=False, index=True)
    annual_intake_seats = Column(Integer, default=40, nullable=False)
    course_fee_inr = Column(Integer, default=0, nullable=False)
    is_hostel_available = Column(Boolean, default=False, nullable=False)
    has_placement_cell = Column(Boolean, default=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    provider = relationship("TrainingProvider", back_populates="provider_trades")
    trade = relationship("Trade", back_populates="provider_trades")

    __table_args__ = (
        Index("idx_provider_trade_unique", "provider_id", "trade_id", unique=True),
    )
