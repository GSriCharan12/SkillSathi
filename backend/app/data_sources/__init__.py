"""SkillSathi Data Ingestion and Adapter Architecture."""
from app.data_sources.base_adapter import BaseDataSourceAdapter
from app.data_sources.validator import DataValidator
from app.data_sources.deduplicator import DataDeduplicator
from app.data_sources.sync_engine import SyncEngine, sync_engine
from app.data_sources.adapters.ncvet_nqr_adapter import NcvetNqrAdapter
from app.data_sources.adapters.msde_tracer_adapter import MsdeTracerAdapter
from app.data_sources.adapters.demo_seed_adapter import DemoSeedAdapter

__all__ = [
    "BaseDataSourceAdapter",
    "DataValidator",
    "DataDeduplicator",
    "SyncEngine",
    "sync_engine",
    "NcvetNqrAdapter",
    "MsdeTracerAdapter",
    "DemoSeedAdapter",
]
