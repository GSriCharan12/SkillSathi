"""
SkillSathi - Data Normalizer
Transforms heterogeneous external records into unified SkillSathi canonical schemas.
"""
from typing import Dict, Any, List
from app.utils.logger import logger


class DataNormalizer:
    """Standardizes external government & sector schemas into SkillSathi formats."""

    @staticmethod
    def normalize_trade_record(raw: Dict[str, Any], source_agency: str) -> Dict[str, Any]:
        """Convert varied external schema keys into unified trade dictionary."""
        return {
            "trade_code": str(raw.get("code") or raw.get("qp_code") or raw.get("trade_id") or "UNKNOWN").strip().upper(),
            "title": str(raw.get("trade_name") or raw.get("title") or raw.get("job_role") or "Untitled Trade").strip(),
            "sector": str(raw.get("sector") or raw.get("sector_name") or "General Vocational").strip(),
            "nsqf_level": int(raw.get("nsqf_level") or raw.get("level") or 4),
            "duration_months": int(raw.get("duration_months") or raw.get("duration") or 12),
            "min_qualification": str(raw.get("min_qualification") or raw.get("eligibility") or "10th Standard").strip(),
            "overview": str(raw.get("description") or raw.get("overview") or "").strip(),
            "source_agency": source_agency
        }

    @staticmethod
    def normalize_evidence_record(raw: Dict[str, Any], source_agency: str) -> Dict[str, Any]:
        """Convert external outcome metrics into verified evidence format."""
        return {
            "source_agency": source_agency,
            "category": str(raw.get("category") or "SALARY").upper().strip(),
            "metric_title": str(raw.get("metric_name") or raw.get("title") or "Verified Metric").strip(),
            "evidence_value": str(raw.get("value") or raw.get("stat") or "N/A").strip(),
            "evidence_metadata": raw.get("metadata") or {},
            "source_url": raw.get("source_url") or "",
            "is_verified": 1
        }
