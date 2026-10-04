"""
SkillSathi - Standardized API Response Utilities
"""
from typing import Any, Optional, Dict
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class StandardResponse(BaseModel):
    """Unified API response wrapper for consistency across all endpoints."""
    success: bool = True
    message: str = "Operation successful"
    data: Optional[Any] = None
    error: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    meta: Optional[Dict[str, Any]] = None


def success_response(
    data: Any = None,
    message: str = "Operation successful",
    meta: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    return {
        "success": True,
        "message": message,
        "data": data,
        "error": None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "meta": meta or {}
    }


def error_response(
    message: str = "An error occurred",
    error: Optional[str] = None,
    meta: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    return {
        "success": False,
        "message": message,
        "data": None,
        "error": error or message,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "meta": meta or {}
    }
