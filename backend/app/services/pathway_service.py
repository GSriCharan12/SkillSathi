"""
SkillSathi - Pathway Service
"""
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.pathway import CareerPathway, CareerPathwayStep, ProgressionOption


class PathwayService:
    @staticmethod
    def list_pathways(
        db: Session,
        trade_id: Optional[int] = None,
        is_demo: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[CareerPathway]:
        query = db.query(CareerPathway).options(
            joinedload(CareerPathway.steps).joinedload(CareerPathwayStep.progression_options)
        )

        if is_demo is not None:
            query = query.filter(CareerPathway.is_demo == is_demo)
        if trade_id:
            query = query.filter(CareerPathway.trade_id == trade_id)

        return query.offset(skip).limit(limit).all()
