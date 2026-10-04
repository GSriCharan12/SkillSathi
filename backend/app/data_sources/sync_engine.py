"""
SkillSathi - Ingestion & Synchronization Engine
Coordinates multi-source data sync, audit tracking, error capture, and freshness monitoring.
"""
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.data_sources.base_adapter import BaseDataSourceAdapter
from app.data_sources.adapters.ncvet_nqr_adapter import NcvetNqrAdapter
from app.data_sources.adapters.msde_tracer_adapter import MsdeTracerAdapter
from app.data_sources.adapters.demo_seed_adapter import DemoSeedAdapter
from app.models.evidence_source import EvidenceSource, DataSyncRun, DataQualityCheck
from app.utils.logger import logger


class SyncEngine:
    def __init__(self):
        self.adapters: Dict[str, BaseDataSourceAdapter] = {
            "ncvet_nqr": NcvetNqrAdapter(),
            "msde_tracer": MsdeTracerAdapter(),
            "demo_seed": DemoSeedAdapter(),
        }

    def register_adapter(self, key: str, adapter: BaseDataSourceAdapter):
        self.adapters[key] = adapter

    def get_registered_adapters(self) -> List[Dict[str, Any]]:
        return [
            {
                "key": k,
                "source_name": a.source_name,
                "publisher": a.publisher,
                "source_type": a.source_type,
                "geographic_scope": a.geographic_scope,
                "is_demo": a.is_demo,
            }
            for k, a in self.adapters.items()
        ]

    async def sync_by_key(self, key: str, db: Session, triggered_by: str = "ADMIN_API") -> Dict[str, Any]:
        if key not in self.adapters:
            raise ValueError(f"Unknown data source adapter key: '{key}'. Available: {list(self.adapters.keys())}")
        adapter = self.adapters[key]
        return await adapter.sync(db, triggered_by=triggered_by)

    async def sync_by_source_id(self, source_id: int, db: Session, triggered_by: str = "ADMIN_API") -> Dict[str, Any]:
        source = db.query(EvidenceSource).filter(EvidenceSource.id == source_id).first()
        if not source:
            raise ValueError(f"EvidenceSource with ID {source_id} not found in database.")

        # Find matching adapter by source_name
        for key, adapter in self.adapters.items():
            if adapter.source_name == source.source_name:
                return await adapter.sync(db, triggered_by=triggered_by)

        raise ValueError(f"No active adapter registered for source: '{source.source_name}'")

    async def sync_all(self, db: Session, triggered_by: str = "SYSTEM_CRON") -> List[Dict[str, Any]]:
        results = []
        # Ensure qualifications are synced first before dependent tracer outcomes
        order = ["ncvet_nqr", "msde_tracer", "demo_seed"]
        for key in order:
            if key in self.adapters:
                try:
                    res = await self.adapters[key].sync(db, triggered_by=triggered_by)
                    results.append(res)
                except Exception as e:
                    logger.error(f"Sync error for adapter '{key}': {e}")
                    results.append({
                        "key": key,
                        "status": "FAILED",
                        "error": str(e)
                    })
        return results


sync_engine = SyncEngine()
