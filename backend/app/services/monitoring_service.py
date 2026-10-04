"""
SkillSathi - Admin Data Monitoring Service
Aggregates source health, sync history, data freshness, failed syncs, and verification metrics.
"""
from typing import Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.evidence_source import EvidenceSource, DataSyncRun, DataQualityCheck
from app.models.trade import Trade, TrainingProvider
from app.models.outcome import OutcomeData
from app.schemas.sync import AdminMonitoringSummary


class MonitoringService:
    @staticmethod
    def get_admin_summary(db: Session) -> Dict[str, Any]:
        total_sources = db.query(EvidenceSource).count()
        total_trades = db.query(Trade).count()
        total_providers = db.query(TrainingProvider).count()
        total_outcomes = db.query(OutcomeData).count()
        total_sync_runs = db.query(DataSyncRun).count()
        total_quality_checks = db.query(DataQualityCheck).count()

        # Group by freshness
        freshness_rows = db.query(
            EvidenceSource.freshness_status, func.count(EvidenceSource.id)
        ).group_by(EvidenceSource.freshness_status).all()
        freshness_map = {status: count for status, count in freshness_rows}

        # Group by verification
        verification_rows = db.query(
            EvidenceSource.verification_status, func.count(EvidenceSource.id)
        ).group_by(EvidenceSource.verification_status).all()
        verification_map = {status: count for status, count in verification_rows}

        # Recent sync runs
        recent_sync_runs = db.query(DataSyncRun).order_by(DataSyncRun.start_time.desc()).limit(10).all()

        # Recent quality checks
        recent_qc = db.query(DataQualityCheck).order_by(DataQualityCheck.created_at.desc()).limit(10).all()

        return {
            "total_sources": total_sources,
            "total_trades": total_trades,
            "total_providers": total_providers,
            "total_outcomes": total_outcomes,
            "total_sync_runs": total_sync_runs,
            "total_quality_checks": total_quality_checks,
            "sources_by_freshness": freshness_map,
            "sources_by_verification": verification_map,
            "recent_sync_runs": recent_sync_runs,
            "recent_quality_alerts": recent_qc,
        }
