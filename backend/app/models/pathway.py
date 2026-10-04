"""
SkillSathi - Career Pathways, Pathway Steps, and Progression Options
Tracks vertical educational ladders (Lateral Polytechnic, B.Voc, B.Tech) and career milestones.
"""
from sqlalchemy import Column, String, Integer, ForeignKey, Text, Boolean, Index
from sqlalchemy.orm import relationship
from app.models.base import TimeStampedBase


class CareerPathway(TimeStampedBase):
    __tablename__ = "career_pathways"

    trade_id = Column(Integer, ForeignKey("trades.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(128), nullable=False, index=True)
    overview = Column(Text, nullable=True)
    entry_qualification = Column(String(64), default="10th Standard Pass", nullable=False)
    total_progression_years = Column(Integer, default=5, nullable=False)
    is_demo = Column(Boolean, default=False, nullable=False, index=True)

    # Relationships
    trade = relationship("Trade", back_populates="career_pathways")
    steps = relationship("CareerPathwayStep", back_populates="pathway", cascade="all, delete-orphan")


class CareerPathwayStep(TimeStampedBase):
    __tablename__ = "career_pathway_steps"

    pathway_id = Column(Integer, ForeignKey("career_pathways.id", ondelete="CASCADE"), nullable=False, index=True)
    step_order = Column(Integer, default=1, nullable=False)
    role_title = Column(String(128), nullable=False)
    experience_required_months = Column(Integer, default=0, nullable=False)
    certifications_required = Column(String(256), nullable=True)
    expected_monthly_inr_min = Column(Integer, nullable=True)
    expected_monthly_inr_max = Column(Integer, nullable=True)
    education_ladder_option = Column(String(256), nullable=True)  # e.g., "Lateral entry to 2nd-year Diploma / B.Voc"
    description = Column(Text, nullable=True)

    # Relationships
    pathway = relationship("CareerPathway", back_populates="steps")
    progression_options = relationship("ProgressionOption", back_populates="pathway_step", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_pathway_step_order", "pathway_id", "step_order"),
    )


class ProgressionOption(TimeStampedBase):
    __tablename__ = "progression_options"

    pathway_step_id = Column(Integer, ForeignKey("career_pathway_steps.id", ondelete="CASCADE"), nullable=False, index=True)
    destination_type = Column(String(64), default="HIGHER_EDUCATION", nullable=False, index=True)  # HIGHER_EDUCATION, LATERAL_DIPLOMA, APPRENTICESHIP, DIRECT_EMPLOYMENT, ENTREPRENEURSHIP
    title = Column(String(128), nullable=False)
    eligibility_criteria = Column(String(256), nullable=True)
    recognizing_body = Column(String(64), default="AICTE/UGC", nullable=False)  # AICTE, UGC, NCVET, DGT
    source_id = Column(Integer, ForeignKey("evidence_sources.id", ondelete="SET NULL"), nullable=True, index=True)

    # Relationships
    pathway_step = relationship("CareerPathwayStep", back_populates="progression_options")
    source = relationship("EvidenceSource", back_populates="progression_options")
