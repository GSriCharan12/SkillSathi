"""
SkillSathi - Outcome & Evidence Service
Strict Outcome Retrieval Engine: Never returns fabricated statistics.
"""
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.outcome import OutcomeData, EmploymentData, EarningsData
from app.models.trade import Trade
from app.models.location import Location


class OutcomeService:
    @staticmethod
    def list_outcomes(
        db: Session,
        trade_id: Optional[int] = None,
        provider_id: Optional[int] = None,
        state: Optional[str] = None,
        district: Optional[str] = None,
        year: Optional[int] = None,
        verification_status: Optional[str] = None,
        is_demo: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[OutcomeData]:
        query = db.query(OutcomeData).options(
            joinedload(OutcomeData.trade),
            joinedload(OutcomeData.provider),
            joinedload(OutcomeData.location),
            joinedload(OutcomeData.source),
            joinedload(OutcomeData.employment_records),
            joinedload(OutcomeData.earnings_records)
        )

        if is_demo is not None:
            query = query.filter(OutcomeData.is_demo == is_demo)
        if trade_id:
            query = query.filter(OutcomeData.trade_id == trade_id)
        if provider_id:
            query = query.filter(OutcomeData.provider_id == provider_id)
        if year:
            query = query.filter(OutcomeData.data_year == year)
        if verification_status:
            query = query.filter(OutcomeData.verification_status == verification_status)
        if state or district:
            query = query.join(Location, OutcomeData.location_id == Location.id)
            if state:
                query = query.filter(Location.state.ilike(f"%{state}%"))
            if district:
                query = query.filter(Location.district.ilike(f"%{district}%"))

        return query.order_by(OutcomeData.placement_rate.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_outcome_by_id(db: Session, outcome_id: int) -> Optional[OutcomeData]:
        return db.query(OutcomeData).options(
            joinedload(OutcomeData.trade),
            joinedload(OutcomeData.provider),
            joinedload(OutcomeData.location),
            joinedload(OutcomeData.source),
            joinedload(OutcomeData.employment_records),
            joinedload(OutcomeData.earnings_records)
        ).filter(OutcomeData.id == outcome_id).first()
