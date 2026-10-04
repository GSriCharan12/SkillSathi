"""
SkillSathi - Evidence Source & Provenance Schemas
"""
from typing import Optional, List
from datetime import datetime
from pydantic import Field
from app.schemas.common import BaseSchema, TimestampedSchema


class EvidenceSourceBase(BaseSchema):
    source_name: str
    publisher: str
    url: Optional[str] = None
    source_type: str = "GOVERNMENT_API"
    geographic_scope: str = "NATIONAL"
    data_period: Optional[str] = None
    publication_date: Optional[datetime] = None
    verification_status: str = "OFFICIAL_VERIFIED"
    freshness_status: str = "FRESH"
    is_demo: bool = False


class EvidenceSourceRead(EvidenceSourceBase, TimestampedSchema):
    retrieval_timestamp: datetime
    last_synced_at: Optional[datetime] = None
    next_recommended_sync: Optional[datetime] = None


class DataQualityCheckRead(TimestampedSchema):
    source_id: Optional[int] = None
    sync_run_id: Optional[int] = None
    entity_type: str
    record_identifier: Optional[str] = None
    issue_type: str
    details: str
    status: str
