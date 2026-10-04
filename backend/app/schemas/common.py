"""
SkillSathi - Common Schemas
"""
from typing import Optional, Generic, TypeVar, Any, Dict
from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, Field

DataT = TypeVar("DataT")


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class TimestampedSchema(BaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime


class ApiResponse(BaseSchema, Generic[DataT]):
    success: bool = True
    message: str = "Success"
    data: Optional[DataT] = None
    error: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    meta: Optional[Dict[str, Any]] = None

