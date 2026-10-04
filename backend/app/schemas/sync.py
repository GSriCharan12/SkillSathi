"""
SkillSathi - Data Sync & Admin Monitoring Schemas
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.schemas.common import BaseSchema, TimestampedSchema
from app.schemas.evidence import EvidenceSourceRead, DataQualityCheckRead


class DataSyncRunRead(TimestampedSchema):
    source_id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    records_found: int = 0
    records_inserted: int = 0
    records_updated: int = 0
    records_rejected: int = 0
    status: str
    error_log: Optional[str] = None
    triggered_by: str
    source: Optional[EvidenceSourceRead] = None


class AdminMonitoringSummary(BaseSchema):
    total_sources: int
    total_trades: int
    total_providers: int
    total_outcomes: int
    total_sync_runs: int
    total_quality_checks: int
    sources_by_freshness: Dict[str, int]
    sources_by_verification: Dict[str, int]
    recent_sync_runs: List[DataSyncRunRead]
    recent_quality_alerts: List[DataQualityCheckRead]
