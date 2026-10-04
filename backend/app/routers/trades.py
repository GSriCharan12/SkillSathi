"""
SkillSathi - Trades, Training Providers & Pathway Comparison API Router
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.common import ApiResponse
from app.schemas.trade import TradeRead, TradeDetailRead, TrainingProviderRead
from app.services.trade_service import TradeService
from app.utils.response import success_response, error_response

router = APIRouter(tags=["Trades & Vocational Qualifications"])


@router.get(
    "/trades",
    summary="List and search vocational trades with localization",
    description="Filter trades by sector, NSQF level, duration, and user location (state/district)."
)
async def list_trades(
    search: Optional[str] = Query(None, description="Search term for title, code, or sector"),
    sector: Optional[str] = Query(None, description="Filter by economic sector"),
    nsqf_level: Optional[int] = Query(None, ge=1, le=10, description="NSQF Qualification Level"),
    duration_months_max: Optional[int] = Query(None, description="Maximum course duration in months"),
    state: Optional[str] = Query(None, description="Family state for localized availability"),
    district: Optional[str] = Query(None, description="Family district for localized availability"),
    is_demo: Optional[bool] = Query(None, description="Filter demo vs official records"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db)
):
    trades = TradeService.list_trades(
        db=db,
        search=search,
        sector=sector,
        nsqf_level=nsqf_level,
        duration_months_max=duration_months_max,
        state=state,
        district=district,
        is_demo=is_demo,
        skip=skip,
        limit=limit
    )
    return success_response(
        data=trades,
        message=f"Retrieved {len(trades)} vocational trades.",
        meta={"total": len(trades), "skip": skip, "limit": limit, "state": state, "district": district}
    )


@router.get(
    "/trades/compare",
    summary="Compare two or more vocational pathways side-by-side",
    description="Side-by-side comparison of duration, eligibility, local availability, verified placement, earnings, and higher education avenues."
)
async def compare_trades(
    trade_ids: str = Query(..., description="Comma-separated trade IDs, e.g. '1,2,3'"),
    state: Optional[str] = Query(None, description="State for localized comparison"),
    district: Optional[str] = Query(None, description="District for localized comparison"),
    db: Session = Depends(get_db)
):
    try:
        parsed_ids = [int(tid.strip()) for tid in trade_ids.split(",") if tid.strip()]
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="trade_ids parameter must be comma-separated integers, e.g. '1,2,3'"
        )

    if not parsed_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one trade_id must be provided for comparison."
        )

    comparison_data = TradeService.compare_trades(
        db=db,
        trade_ids=parsed_ids,
        state=state,
        district=district
    )

    return success_response(
        data=comparison_data,
        message=f"Compared {comparison_data['comparison_count']} vocational pathways."
    )


@router.get(
    "/trades/{id}",
    summary="Get complete trade dossier and career pathways",
    description="Returns full curriculum, NSQF parameters, vertical progression ladders, and verified local outcome statistics."
)
async def get_trade_details(
    id: int,
    state: Optional[str] = Query(None, description="State for localized provider & outcome prioritization"),
    district: Optional[str] = Query(None, description="District for localized provider & outcome prioritization"),
    db: Session = Depends(get_db)
):
    trade = TradeService.get_trade_by_id(db=db, trade_id=id, state=state, district=district)
    if not trade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vocational trade with ID {id} not found."
        )
    return success_response(
        data=trade,
        message="Vocational trade details retrieved successfully."
    )


@router.get(
    "/providers",
    response_model=ApiResponse[List[TrainingProviderRead]],
    summary="List training providers (ITIs, Polytechnics, NSTIs)",
    description="Filter training providers by state, district, affiliation, and institution type."
)
async def list_providers(
    state: Optional[str] = Query(None, description="State name"),
    district: Optional[str] = Query(None, description="District name"),
    provider_type: Optional[str] = Query(None, description="GOVT_ITI, PRIVATE_ITI, NSTI, POLYTECHNIC"),
    search: Optional[str] = Query(None, description="Search provider name or code"),
    is_demo: Optional[bool] = Query(None, description="Filter demo vs official records"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db)
):
    providers = TradeService.list_providers(
        db=db, state=state, district=district, provider_type=provider_type, search=search, is_demo=is_demo, skip=skip, limit=limit
    )
    return success_response(
        data=[TrainingProviderRead.model_validate(p).model_dump() for p in providers],
        message=f"Retrieved {len(providers)} training providers.",
        meta={"total": len(providers), "skip": skip, "limit": limit}
    )
