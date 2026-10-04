"""
SkillSathi - Trade, Category, and Training Provider Schemas
"""
from typing import Optional, List
from pydantic import Field
from app.schemas.common import BaseSchema, TimestampedSchema
from app.schemas.pathway import CareerPathwayRead


class LocationRead(TimestampedSchema):
    state: str
    district: str
    pincode: Optional[str] = None
    region_type: str = "URBAN"
    industrial_cluster_name: Optional[str] = None
    is_active: bool = True
    is_demo: bool = False


class TradeCategoryRead(TimestampedSchema):
    code: str
    name: str
    description: Optional[str] = None
    icon_name: str = "Compass"


class TradeBase(BaseSchema):
    code: str
    title: str
    sector: str
    nsqf_level: int = 4
    duration_months: int = 12
    min_qualification: str = "10th Standard"
    description: Optional[str] = None
    is_active: bool = True
    is_demo: bool = False


class TradeRead(TradeBase, TimestampedSchema):
    category_id: Optional[int] = None
    category: Optional[TradeCategoryRead] = None


class TrainingProviderBase(BaseSchema):
    name: str
    code: str
    provider_type: str = "GOVT_ITI"
    affiliation_body: str = "NCVET"
    website_url: Optional[str] = None
    is_verified: bool = True
    is_demo: bool = False


class TrainingProviderRead(TrainingProviderBase, TimestampedSchema):
    location_id: Optional[int] = None
    location: Optional[LocationRead] = None


class TradeDetailRead(TradeRead):
    career_pathways: List[CareerPathwayRead] = []
    providers: List[TrainingProviderRead] = []
