"""
SkillSathi - Demo Seed Adapter
Provides synthetic, illustrative records for local unit testing and offline development.
STRICT RULE: All records from this adapter MUST have is_demo = True.
"""
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.data_sources.base_adapter import BaseDataSourceAdapter
from app.models.location import Location
from app.models.trade import Trade, TradeCategory, TrainingProvider, ProviderTrade
from app.models.outcome import OutcomeData
from app.utils.logger import logger


class DemoSeedAdapter(BaseDataSourceAdapter):
    def __init__(self):
        super().__init__(
            source_name="SkillSathi Development Demo Dataset",
            publisher="SkillSathi Sandbox Mock Factory",
            url="https://demo.skillsathi.internal/sandbox",
            source_type="DEMO_SEED",
            geographic_scope="STATE",
            data_period="2024-DEMO",
            is_demo=True
        )

    async def fetch(self, filter_params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        return [
            {
                "trade_code": "DEMO/AGRI/Q01",
                "trade_title": "[DEMO] Drone Agriculture Survey Technician",
                "category_code": "DEMO_AGRI",
                "category_name": "Demo Agriculture Technology",
                "sector": "Agriculture & Drone Tech",
                "nsqf_level": 4,
                "duration_months": 6,
                "min_qualification": "10th Standard Pass",
                "description": "[DEMO DATASET] Illustrative trade for testing non-production workflows.",
                "state": "Haryana",
                "district": "Karnal",
                "provider_code": "DEMO_INST_01",
                "provider_name": "[DEMO] Northern Agro-Skill Academy",
                "placement_rate": 78.0,
                "earnings_min": 14000,
                "earnings_max": 20000,
                "earnings_period": "MONTHLY",
                "employment_type": "CONTRACT",
                "data_year": 2024,
                "sample_size": 30
            }
        ]

    def parse(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return raw_data

    def normalize(self, parsed_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        normalized = []
        for item in parsed_data:
            normalized.append({
                "trade_code": item["trade_code"],
                "trade_title": item["trade_title"],
                "category_code": item["category_code"],
                "category_name": item["category_name"],
                "sector": item["sector"],
                "nsqf_level": item["nsqf_level"],
                "duration_months": item["duration_months"],
                "min_qualification": item["min_qualification"],
                "description": item["description"],
                "state": item["state"],
                "district": item["district"],
                "provider_code": item["provider_code"],
                "provider_name": item["provider_name"],
                "placement_rate": item["placement_rate"],
                "earnings_min": item["earnings_min"],
                "earnings_max": item["earnings_max"],
                "earnings_period": item["earnings_period"],
                "employment_type": item["employment_type"],
                "data_year": item["data_year"],
                "sample_size": item["sample_size"]
            })
        return normalized

    async def _persist_records(self, db: Session, records: List[Dict[str, Any]], source_id: int) -> Tuple[int, int]:
        inserted = 0
        updated = 0

        for rec in records:
            # 1. Location (is_demo=True)
            loc = db.query(Location).filter(Location.state == rec["state"], Location.district == rec["district"]).first()
            if not loc:
                loc = Location(state=rec["state"], district=rec["district"], region_type="RURAL", is_demo=True)
                db.add(loc)
                db.flush()

            # 2. Trade Category & Trade (is_demo=True)
            cat = db.query(TradeCategory).filter(TradeCategory.code == rec["category_code"]).first()
            if not cat:
                cat = TradeCategory(code=rec["category_code"], name=rec["category_name"])
                db.add(cat)
                db.flush()

            trade = db.query(Trade).filter(Trade.code == rec["trade_code"]).first()
            if not trade:
                trade = Trade(
                    category_id=cat.id,
                    code=rec["trade_code"],
                    title=rec["trade_title"],
                    sector=rec["sector"],
                    nsqf_level=rec["nsqf_level"],
                    duration_months=rec["duration_months"],
                    min_qualification=rec["min_qualification"],
                    description=rec["description"],
                    is_active=True,
                    is_demo=True
                )
                db.add(trade)
                db.flush()
                inserted += 1

            # 3. Provider (is_demo=True)
            provider = db.query(TrainingProvider).filter(TrainingProvider.code == rec["provider_code"]).first()
            if not provider:
                provider = TrainingProvider(
                    name=rec["provider_name"],
                    code=rec["provider_code"],
                    provider_type="PMKK",
                    location_id=loc.id,
                    is_verified=False,
                    is_demo=True
                )
                db.add(provider)
                db.flush()

            # 4. Outcome (is_demo=True)
            outcome = db.query(OutcomeData).filter(
                OutcomeData.trade_id == trade.id,
                OutcomeData.provider_id == provider.id,
                OutcomeData.source_id == source_id
            ).first()

            now = datetime.now(timezone.utc)
            if not outcome:
                outcome = OutcomeData(
                    trade_id=trade.id,
                    provider_id=provider.id,
                    location_id=loc.id,
                    placement_rate=rec["placement_rate"],
                    earnings_min=rec["earnings_min"],
                    earnings_max=rec["earnings_max"],
                    earnings_period=rec["earnings_period"],
                    employment_type=rec["employment_type"],
                    data_year=rec["data_year"],
                    sample_size=rec["sample_size"],
                    source_id=source_id,
                    verification_status="UNVERIFIED",
                    last_verified_at=now,
                    last_synced_at=now,
                    is_demo=True
                )
                db.add(outcome)
                inserted += 1

        db.commit()
        return (inserted, updated)
