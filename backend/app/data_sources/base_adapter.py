"""
SkillSathi - Base Data Source Adapter Interface
Defines the standard lifecycle contract for all external data source ingesters:
fetch -> parse -> normalize -> validate -> deduplicate -> sync
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.evidence_source import EvidenceSource, DataSyncRun, DataQualityCheck
from app.data_sources.validator import DataValidator
from app.data_sources.deduplicator import DataDeduplicator
from app.utils.logger import logger


class BaseDataSourceAdapter(ABC):
    """
    Extensible interface for all educational, vocational, and governmental data sources.
    Ensures every ingested record is validated and attributed to an EvidenceSource.
    """

    def __init__(
        self,
        source_name: str,
        publisher: str,
        url: str,
        source_type: str = "GOVERNMENT_API",
        geographic_scope: str = "NATIONAL",
        data_period: str = "2024-2025",
        is_demo: bool = False
    ):
        self.source_name = source_name
        self.publisher = publisher
        self.url = url
        self.source_type = source_type
        self.geographic_scope = geographic_scope
        self.data_period = data_period
        self.is_demo = is_demo

    @abstractmethod
    async def fetch(self, filter_params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Fetch raw unparsed records from external API, file, or feed."""
        pass

    @abstractmethod
    def parse(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract structured record dictionaries from raw payload."""
        pass

    @abstractmethod
    def normalize(self, parsed_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Map heterogeneous schema attributes to SkillSathi canonical schema."""
        pass

    def validate(self, normalized_data: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Validate records against statistical and relational constraints.
        Returns: (valid_records, rejected_records_with_reasons)
        """
        valid = []
        rejected = []
        for rec in normalized_data:
            is_valid, errors, issue_type = DataValidator.validate_outcome_record(rec)
            if is_valid:
                valid.append(rec)
            else:
                rec_copy = dict(rec)
                rec_copy["_validation_errors"] = errors
                rec_copy["_issue_type"] = issue_type
                rejected.append(rec_copy)
        return (valid, rejected)

    def get_or_create_source_record(self, db: Session) -> EvidenceSource:
        """Ensures the source entity exists in MySQL with updated metadata."""
        src = db.query(EvidenceSource).filter(EvidenceSource.source_name == self.source_name).first()
        now = datetime.now(timezone.utc)
        if not src:
            src = EvidenceSource(
                source_name=self.source_name,
                publisher=self.publisher,
                url=self.url,
                source_type=self.source_type,
                geographic_scope=self.geographic_scope,
                data_period=self.data_period,
                publication_date=now,
                retrieval_timestamp=now,
                verification_status="OFFICIAL_VERIFIED" if not self.is_demo else "UNVERIFIED",
                freshness_status="FRESH" if not self.is_demo else "MANUAL_REVIEW",
                is_demo=self.is_demo
            )
            db.add(src)
            db.commit()
            db.refresh(src)
        return src

    async def sync(self, db: Session, triggered_by: str = "SYSTEM_SYNC") -> Dict[str, Any]:
        """
        Orchestrates full ingestion pipeline with audit logging and sync run tracking.
        """
        start_time = datetime.now(timezone.utc)
        source = self.get_or_create_source_record(db)

        # Create Sync Run Entry
        sync_run = DataSyncRun(
            source_id=source.id,
            start_time=start_time,
            status="RUNNING",
            triggered_by=triggered_by
        )
        db.add(sync_run)
        db.commit()
        db.refresh(sync_run)

        records_found = 0
        records_inserted = 0
        records_updated = 0
        records_rejected = 0
        errors_list = []

        try:
            # 1. Fetch
            raw_items = await self.fetch()
            records_found = len(raw_items)

            # 2. Parse
            parsed_items = self.parse(raw_items)

            # 3. Normalize
            normalized_items = self.normalize(parsed_items)
            for item in normalized_items:
                item["source_id"] = source.id
                item["is_demo"] = self.is_demo

            # 4. Validate
            valid_items, rejected_items = self.validate(normalized_items)

            # 5. Deduplicate Valid Items
            unique_valid, duplicate_rejects = DataDeduplicator.deduplicate_records(valid_items)
            for dup in duplicate_rejects:
                dup["_validation_errors"] = ["Duplicate record in sync stream."]
                dup["_issue_type"] = "DUPLICATE_ENTRY"
                rejected_items.append(dup)

            # Record Rejected Quality Checks
            records_rejected = len(rejected_items)
            for rej in rejected_items:
                qc = DataQualityCheck(
                    source_id=source.id,
                    sync_run_id=sync_run.id,
                    entity_type="OUTCOME_DATA",
                    record_identifier=str(rej.get("trade_code") or rej.get("trade_id") or "UNKNOWN"),
                    issue_type=rej.get("_issue_type", "UNKNOWN"),
                    raw_payload=rej,
                    details="; ".join(rej.get("_validation_errors", ["Validation failed"])),
                    status="REJECTED"
                )
                db.add(qc)

            # 6. Database Persistence (Insert/Update)
            inserted, updated = await self._persist_records(db, unique_valid, source.id)
            records_inserted = inserted
            records_updated = updated

            # Finalize Source & Sync Run
            end_time = datetime.now(timezone.utc)
            sync_run.end_time = end_time
            sync_run.records_found = records_found
            sync_run.records_inserted = records_inserted
            sync_run.records_updated = records_updated
            sync_run.records_rejected = records_rejected
            sync_run.status = "COMPLETED" if records_rejected == 0 else "PARTIAL"

            source.last_synced_at = end_time
            source.freshness_status = "FRESH" if not self.is_demo else "LIVE"
            db.commit()

        except Exception as exc:
            db.rollback()
            logger.error(f"Sync failed for source '{self.source_name}': {exc}", exc_info=True)
            end_time = datetime.now(timezone.utc)
            sync_run.end_time = end_time
            sync_run.status = "FAILED"
            sync_run.error_log = str(exc)
            source.freshness_status = "FAILED"
            db.commit()
            raise exc

        return {
            "source_id": source.id,
            "source_name": self.source_name,
            "sync_run_id": sync_run.id,
            "status": sync_run.status,
            "records_found": records_found,
            "records_inserted": records_inserted,
            "records_updated": records_updated,
            "records_rejected": records_rejected,
            "duration_seconds": round((end_time - start_time).total_seconds(), 2)
        }

    @abstractmethod
    async def _persist_records(self, db: Session, records: List[Dict[str, Any]], source_id: int) -> Tuple[int, int]:
        """Custom persistence handler for the adapter entity type. Returns (inserted_count, updated_count)."""
        pass
