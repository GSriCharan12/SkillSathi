"""
SkillSathi - Evidence Source Provenance & Sync Monitoring Models
Ensures every piece of outcome data retains full provenance and tracking.
"""
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime, Text, JSON, Boolean, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.models.base import TimeStampedBase


class EvidenceSource(TimeStampedBase):
    """
    Evidence source provenance entity.
    Stores publisher details, publication dates, verification status, and sync freshness.
    """
    __tablename__ = "evidence_sources"

    source_name = Column(String(128), unique=True, index=True, nullable=False)
    publisher = Column(String(128), nullable=False)
    url = Column(String(512), nullable=True)
    source_type = Column(String(64), default="GOVERNMENT_API", nullable=False, index=True)  # GOVERNMENT_API, OFFICIAL_REPORT, CENSUS_SURVEY, TRACER_STUDY, DEMO_SEED
    geographic_scope = Column(String(64), default="NATIONAL", nullable=False)                # NATIONAL, STATE, DISTRICT
    data_period = Column(String(64), nullable=True)                                          # e.g., "2023-2024", "Annual Tracer 2025"
    publication_date = Column(DateTime, nullable=True)
    retrieval_timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    verification_status = Column(String(64), default="OFFICIAL_VERIFIED", nullable=False, index=True)  # OFFICIAL_VERIFIED, PROVISIONALLY_VERIFIED, UNVERIFIED, REJECTED
    freshness_status = Column(String(64), default="FRESH", nullable=False, index=True)      # LIVE, FRESH, STALE, FAILED, MANUAL_REVIEW
    last_synced_at = Column(DateTime, nullable=True)
    next_recommended_sync = Column(DateTime, nullable=True)
    is_demo = Column(Boolean, default=False, nullable=False, index=True)

    # Relationships
    sync_runs = relationship("DataSyncRun", back_populates="source", cascade="all, delete-orphan")
    quality_checks = relationship("DataQualityCheck", back_populates="source", cascade="all, delete-orphan")
    outcomes = relationship("OutcomeData", back_populates="source")
    progression_options = relationship("ProgressionOption", back_populates="source")


class DataSyncRun(TimeStampedBase):
    """
    Tracks data sync executions for auditing, monitoring, and debugging data ingestion pipelines.
    """
    __tablename__ = "data_sync_runs"

    source_id = Column(Integer, ForeignKey("evidence_sources.id", ondelete="CASCADE"), nullable=False, index=True)
    start_time = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    end_time = Column(DateTime, nullable=True)
    records_found = Column(Integer, default=0, nullable=False)
    records_inserted = Column(Integer, default=0, nullable=False)
    records_updated = Column(Integer, default=0, nullable=False)
    records_rejected = Column(Integer, default=0, nullable=False)
    status = Column(String(32), default="RUNNING", nullable=False, index=True)  # RUNNING, COMPLETED, FAILED, PARTIAL
    error_log = Column(Text, nullable=True)
    triggered_by = Column(String(64), default="SYSTEM_CRON", nullable=False)

    # Relationships
    source = relationship("EvidenceSource", back_populates="sync_runs")
    quality_checks = relationship("DataQualityCheck", back_populates="sync_run")

    __table_args__ = (
        Index("idx_sync_source_status", "source_id", "status"),
    )


class DataQualityCheck(TimeStampedBase):
    """
    Tracks rejected, flagged, or anomalous records detected during validation.
    """
    __tablename__ = "data_quality_checks"

    source_id = Column(Integer, ForeignKey("evidence_sources.id", ondelete="SET NULL"), nullable=True, index=True)
    sync_run_id = Column(Integer, ForeignKey("data_sync_runs.id", ondelete="SET NULL"), nullable=True, index=True)
    entity_type = Column(String(64), nullable=False, index=True)  # OUTCOME, TRADE, PROVIDER, EARNINGS
    record_identifier = Column(String(128), nullable=True)
    issue_type = Column(String(64), nullable=False, index=True)   # INVALID_PERCENTAGE, NEGATIVE_EARNINGS, MISSING_SOURCE, INVALID_DATE, DUPLICATE_ENTRY, INCOMPATIBLE_GEO, UNSUPPORTED_COMBINATION
    raw_payload = Column(JSON, nullable=True)
    details = Column(Text, nullable=False)
    status = Column(String(32), default="REJECTED", nullable=False, index=True)  # FLAGGED, REJECTED, RESOLVED, IGNORED

    # Relationships
    source = relationship("EvidenceSource", back_populates="quality_checks")
    sync_run = relationship("DataSyncRun", back_populates="quality_checks")
