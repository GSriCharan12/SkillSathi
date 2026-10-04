"""
SkillSathi - Health & Version Schemas
"""
from typing import Optional, List
from pydantic import Field
from app.schemas.common import BaseSchema


class HealthStatus(BaseSchema):
    status: str = Field(..., json_schema_extra={"example": "healthy"})
    app_name: str = Field(..., json_schema_extra={"example": "SkillSathi"})
    tagline: str = Field(..., json_schema_extra={"example": "Explore a future your whole family believes in."})
    version: str = Field(..., json_schema_extra={"example": "0.1.0"})
    environment: str = Field(..., json_schema_extra={"example": "development"})
    uptime_seconds: float = Field(..., json_schema_extra={"example": 120.5})
    timestamp: str


class DatabaseHealthStatus(BaseSchema):
    status: str = Field(..., json_schema_extra={"example": "healthy"})
    connected: bool = Field(..., json_schema_extra={"example": True})
    latency_ms: float = Field(..., json_schema_extra={"example": 2.4})
    database_engine: str = Field(..., json_schema_extra={"example": "MySQL"})
    database_version: Optional[str] = Field(None, json_schema_extra={"example": "8.0.36"})
    host: Optional[str] = None
    database: Optional[str] = None
    error: Optional[str] = None


class AppVersionInfo(BaseSchema):
    app_name: str
    version: str
    api_version: str = "v1"
    problem_statement: str = "AI-Enabled Career Counselling and Family Decision-Support Platform for Vocational Education"
    ai_provider: str
    ai_model: str
    build_time: str
    supported_locales: List[str]
