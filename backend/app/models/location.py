"""
SkillSathi - Geographic & Location Models
Stores standard Indian administrative divisions, industrial clusters, and region types.
"""
from sqlalchemy import Column, String, Integer, Boolean, Index
from sqlalchemy.orm import relationship
from app.models.base import TimeStampedBase


class Location(TimeStampedBase):
    __tablename__ = "locations"

    state = Column(String(64), nullable=False, index=True)
    district = Column(String(64), nullable=False, index=True)
    pincode = Column(String(10), nullable=True, index=True)
    region_type = Column(String(32), default="URBAN", nullable=False)  # RURAL, URBAN, SEMI_URBAN
    industrial_cluster_name = Column(String(128), nullable=True, index=True)  # e.g., "Pimpri-Chinchwad Auto Belt", "Sriperumbudur Electronics"
    is_active = Column(Boolean, default=True, nullable=False)
    is_demo = Column(Boolean, default=False, nullable=False, index=True)

    # Relationships
    providers = relationship("TrainingProvider", back_populates="location")
    outcomes = relationship("OutcomeData", back_populates="location")
    families = relationship("Family", back_populates="location")

    __table_args__ = (
        Index("idx_location_state_district", "state", "district"),
    )
