"""
SkillSathi - Data Synchronization API Router
"""
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.common import ApiResponse
from app.data_sources.sync_engine import sync_engine
from app.utils.response import success_response, error_response

router = APIRouter(prefix="/data-sync", tags=["Data Sync & Ingestion Engine"])


@router.get(
    "/adapters",
    response_model=ApiResponse[List[Dict[str, Any]]],
    summary="List registered data source adapters",
    description="Returns available external adapters and their ingestion policies."
)
async def list_adapters():
    adapters = sync_engine.get_registered_adapters()
    return success_response(
        data=adapters,
        message=f"Found {len(adapters)} registered data source adapters."
    )


@router.post(
    "/trigger-all",
    response_model=ApiResponse[List[Dict[str, Any]]],
    summary="Trigger full synchronization for all registered sources",
    description="Executes NCVET qualification register and MSDE tracer studies ingestion."
)
async def trigger_all_sync(
    db: Session = Depends(get_db)
):
    try:
        results = await sync_engine.sync_all(db=db, triggered_by="ADMIN_API_TRIGGER_ALL")
        return success_response(
            data=results,
            message="Data synchronization completed across all registered sources."
        )
    except Exception as e:
        return error_response(
            message="Sync execution encountered an error.",
            error=str(e)
        )


@router.post(
    "/{source_id}",
    response_model=ApiResponse[Dict[str, Any]],
    summary="Trigger synchronization for specific evidence source ID",
    description="Runs validation, deduplication, and persistence for the selected source ID."
)
async def trigger_source_sync(
    source_id: int,
    db: Session = Depends(get_db)
):
    try:
        result = await sync_engine.sync_by_source_id(source_id=source_id, db=db, triggered_by="ADMIN_API")
        return success_response(
            data=result,
            message=f"Source {source_id} synchronized successfully."
        )
    except ValueError as val_err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(val_err)
        )
    except Exception as e:
        return error_response(
            message=f"Sync execution failed for source ID {source_id}.",
            error=str(e)
        )
