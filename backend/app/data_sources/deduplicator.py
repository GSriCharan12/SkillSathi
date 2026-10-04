"""
SkillSathi - Data Deduplicator
Identifies duplicate records in ingestion streams using canonical composite hash keys.
"""
from typing import List, Dict, Any, Tuple, Set
import hashlib


class DataDeduplicator:
    """Detects and partitions duplicate records from batch ingestion payloads."""

    @staticmethod
    def generate_record_key(record: Dict[str, Any]) -> str:
        # 1. If it's a trade definition
        if "code" in record and "title" in record:
            trade_code = str(record["code"]).strip().upper()
            return f"TRADE|{trade_code}"

        # 2. If it's a provider definition
        if "provider_code" in record and "provider_name" in record and "placement_rate" not in record:
            provider_code = str(record["provider_code"]).strip().upper()
            return f"PROVIDER|{provider_code}"

        # 3. If it's an outcome record
        trade_id = str(record.get("trade_id") or record.get("trade_code") or "").strip().upper()
        provider_id = str(record.get("provider_id") or record.get("provider_code") or "NONE").strip().upper()
        location_id = str(record.get("location_id") or f"{record.get('state', '')}_{record.get('district', '')}").strip().upper()
        year = str(record.get("data_year") or "").strip()
        source_id = str(record.get("source_id") or record.get("source_name") or "").strip().upper()

        raw_str = f"OUTCOME|{trade_id}|{provider_id}|{location_id}|{year}|{source_id}"
        return hashlib.sha256(raw_str.encode("utf-8")).hexdigest()

    @classmethod
    def deduplicate_records(cls, records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Partitions records into unique stream and duplicate rejects.
        Returns: (unique_records, duplicate_records)
        """
        seen_keys: Set[str] = set()
        unique_records = []
        duplicate_records = []

        for record in records:
            key = cls.generate_record_key(record)
            if key in seen_keys:
                duplicate_records.append(record)
            else:
                seen_keys.add(key)
                unique_records.append(record)

        return (unique_records, duplicate_records)
