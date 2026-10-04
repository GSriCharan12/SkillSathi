"""
SkillSathi - Evidence Sources & Provenance API Router
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.common import ApiResponse
from app.schemas.evidence import EvidenceSourceRead, DataQualityCheckRead
from app.services.evidence_service import EvidenceService
from app.services.evidence_retrieval_service import EvidenceRetrievalService
from app.utils.response import success_response

router = APIRouter(tags=["Evidence Sources & Provenance"])


@router.get(
    "/evidence",
    response_model=ApiResponse[List[EvidenceSourceRead]],
    summary="List official evidence sources and data freshness status",
    description="Retrieve provenance metadata for MSDE, NCVET, NSDC, and state datasets powering SkillSathi."
)
async def list_evidence_sources(
    source_type: Optional[str] = Query(None, description="GOVERNMENT_API, OFFICIAL_REPORT, TRACER_STUDY, DEMO_SEED"),
    verification_status: Optional[str] = Query(None, description="OFFICIAL_VERIFIED, PROVISIONALLY_VERIFIED"),
    freshness_status: Optional[str] = Query(None, description="LIVE, FRESH, STALE, FAILED, MANUAL_REVIEW"),
    is_demo: Optional[bool] = Query(None, description="Filter demo sources"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db)
):
    sources = EvidenceService.list_sources(
        db=db,
        source_type=source_type,
        verification_status=verification_status,
        freshness_status=freshness_status,
        is_demo=is_demo,
        skip=skip,
        limit=limit
    )
    return success_response(
        data=[EvidenceSourceRead.model_validate(s).model_dump() for s in sources],
        message=f"Retrieved {len(sources)} evidence sources.",
        meta={"total": len(sources), "skip": skip, "limit": limit}
    )


@router.get(
    "/evidence/retrieve",
    summary="Retrieve ranked evidence with anti-hallucination guarantees",
    description="Search verified evidence items ranked by geographic proximity, trade relevance, and freshness."
)
async def retrieve_evidence(
    trade_id: Optional[int] = Query(None, description="Trade ID"),
    trade_code: Optional[str] = Query(None, description="Trade Code, e.g. ELE/Q5901"),
    state: Optional[str] = Query(None, description="Family state e.g. Telangana"),
    district: Optional[str] = Query(None, description="Family district e.g. Warangal"),
    concern_type: Optional[str] = Query(None, description="Concern category: INCOME, PLACEMENT, SAFETY, etc."),
    query: Optional[str] = Query(None, description="Specific user question or keyword"),
    limit: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db)
):
    result = EvidenceRetrievalService.retrieve_ranked_evidence(
        db=db,
        trade_id=trade_id,
        trade_code=trade_code,
        state=state,
        district=district,
        concern_type=concern_type,
        query=query,
        limit=limit
    )
    return success_response(
        data=result,
        message="Ranked evidence retrieved successfully." if result["is_available"] else "Verified information for this question is currently unavailable."
    )


@router.get(
    "/evidence/{id}",
    response_model=ApiResponse[EvidenceSourceRead],
    summary="Get single evidence source provenance details",
    description="Returns source publisher, citation URL, data period, and verification tier."
)
async def get_evidence_source_details(
    id: int,
    db: Session = Depends(get_db)
):
    source = EvidenceService.get_source_by_id(db=db, source_id=id)
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evidence source with ID {id} not found."
        )
    return success_response(
        data=EvidenceSourceRead.model_validate(source).model_dump(),
        message="Evidence source retrieved successfully."
    )


@router.get(
    "/evidence/quality-checks/recent",
    response_model=ApiResponse[List[DataQualityCheckRead]],
    summary="List data quality alerts and validation rejections",
    description="Audit log of rejected records, anomalous statistics, and duplicate ingestions."
)
async def list_quality_checks(
    source_id: Optional[int] = Query(None, description="Filter by Source ID"),
    issue_type: Optional[str] = Query(None, description="INVALID_PERCENTAGE, NEGATIVE_EARNINGS, DUPLICATE_ENTRY"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    checks = EvidenceService.list_quality_checks(
        db=db, source_id=source_id, issue_type=issue_type, skip=skip, limit=limit
    )
    return success_response(
        data=[DataQualityCheckRead.model_validate(c).model_dump() for c in checks],
        message=f"Retrieved {len(checks)} data quality alerts.",
        meta={"total": len(checks)}
    )
