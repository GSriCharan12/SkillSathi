"""
SkillSathi - Verified Outcomes & Tracer Data API Router
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.common import ApiResponse
from app.schemas.outcome import OutcomeDataRead
from app.services.outcome_service import OutcomeService
from app.utils.response import success_response, error_response

router = APIRouter(tags=["Verified Outcomes & Evidence"])


@router.get(
    "/outcomes",
    response_model=ApiResponse[List[OutcomeDataRead]],
    summary="List verified vocational outcomes and employment metrics",
    description="Retrieve verified placement rates, salary bands, and training stipends sourced from MSDE and NSDC tracer studies."
)
async def list_outcomes(
    trade_id: Optional[int] = Query(None, description="Filter by Trade ID"),
    provider_id: Optional[int] = Query(None, description="Filter by Training Provider ID"),
    state: Optional[str] = Query(None, description="Filter by State"),
    district: Optional[str] = Query(None, description="Filter by District"),
    year: Optional[int] = Query(None, description="Filter by Data Year"),
    verification_status: Optional[str] = Query(None, description="OFFICIAL_VERIFIED, PROVISIONALLY_VERIFIED"),
    is_demo: Optional[bool] = Query(None, description="Filter demo records"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db)
):
    outcomes = OutcomeService.list_outcomes(
        db=db,
        trade_id=trade_id,
        provider_id=provider_id,
        state=state,
        district=district,
        year=year,
        verification_status=verification_status,
        is_demo=is_demo,
        skip=skip,
        limit=limit
    )
    return success_response(
        data=[OutcomeDataRead.model_validate(o).model_dump() for o in outcomes],
        message=f"Retrieved {len(outcomes)} verified outcome records.",
        meta={"total": len(outcomes), "skip": skip, "limit": limit}
    )


@router.get(
    "/outcomes/{id}",
    response_model=ApiResponse[OutcomeDataRead],
    summary="Get single outcome record with full provenance",
    description="Returns verified placement, salary percentiles, top hiring employers, and source attribution."
)
async def get_outcome_details(
    id: int,
    db: Session = Depends(get_db)
):
    outcome = OutcomeService.get_outcome_by_id(db=db, outcome_id=id)
    if not outcome:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Outcome record with ID {id} not found."
        )
    return success_response(
        data=OutcomeDataRead.model_validate(outcome).model_dump(),
        message="Outcome record retrieved successfully."
    )
