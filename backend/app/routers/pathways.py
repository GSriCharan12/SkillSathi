"""
SkillSathi - Pathways & Progression Ladders API Router
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.common import ApiResponse
from app.schemas.pathway import CareerPathwayRead
from app.services.pathway_service import PathwayService
from app.utils.response import success_response

router = APIRouter(tags=["Career Pathways & Mobility"])


@router.get(
    "/pathways",
    response_model=ApiResponse[List[CareerPathwayRead]],
    summary="List career pathways and vertical mobility ladders",
    description="Retrieve NSQF progression steps, lateral entry degree avenues (B.Voc, Polytechnic Diploma, B.Tech), and salary ladders."
)
async def list_pathways(
    trade_id: Optional[int] = Query(None, description="Filter by Trade ID"),
    is_demo: Optional[bool] = Query(None, description="Filter demo pathways"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db)
):
    pathways = PathwayService.list_pathways(
        db=db, trade_id=trade_id, is_demo=is_demo, skip=skip, limit=limit
    )
    return success_response(
        data=[CareerPathwayRead.model_validate(p).model_dump() for p in pathways],
        message=f"Retrieved {len(pathways)} career pathways.",
        meta={"total": len(pathways), "skip": skip, "limit": limit}
    )
