"""
SkillSathi - Evidence Source & Provenance Service
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.evidence_source import EvidenceSource, DataQualityCheck


class EvidenceService:
    @staticmethod
    def list_sources(
        db: Session,
        source_type: Optional[str] = None,
        verification_status: Optional[str] = None,
        freshness_status: Optional[str] = None,
        is_demo: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[EvidenceSource]:
        query = db.query(EvidenceSource)

        if is_demo is not None:
            query = query.filter(EvidenceSource.is_demo == is_demo)
        if source_type:
            query = query.filter(EvidenceSource.source_type == source_type)
        if verification_status:
            query = query.filter(EvidenceSource.verification_status == verification_status)
        if freshness_status:
            query = query.filter(EvidenceSource.freshness_status == freshness_status)

        return query.order_by(EvidenceSource.source_name.asc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_source_by_id(db: Session, source_id: int) -> Optional[EvidenceSource]:
        return db.query(EvidenceSource).filter(EvidenceSource.id == source_id).first()

    @staticmethod
    def list_quality_checks(
        db: Session,
        source_id: Optional[int] = None,
        issue_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 50
    ) -> List[DataQualityCheck]:
        query = db.query(DataQualityCheck)
        if source_id:
            query = query.filter(DataQualityCheck.source_id == source_id)
        if issue_type:
            query = query.filter(DataQualityCheck.issue_type == issue_type)
        return query.order_by(DataQualityCheck.created_at.desc()).offset(skip).limit(limit).all()
