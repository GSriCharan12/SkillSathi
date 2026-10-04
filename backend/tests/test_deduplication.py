"""
SkillSathi - Data Deduplication Tests
"""
from app.data_sources.deduplicator import DataDeduplicator


def test_deduplication_partitions_duplicates():
    records = [
        {
            "trade_id": "ELE/Q5901",
            "provider_id": "ITI_PUNE_01",
            "state": "Maharashtra",
            "district": "Pune",
            "data_year": 2024,
            "source_id": "MSDE_TRACER",
            "placement_rate": 84.5
        },
        {
            "trade_id": "ELE/Q5901",
            "provider_id": "ITI_PUNE_01",
            "state": "Maharashtra",
            "district": "Pune",
            "data_year": 2024,
            "source_id": "MSDE_TRACER",
            "placement_rate": 84.5  # Exact duplicate
        },
        {
            "trade_id": "ASC/Q1427",
            "provider_id": "ITI_TN_02",
            "state": "Tamil Nadu",
            "district": "Kanchipuram",
            "data_year": 2024,
            "source_id": "MSDE_TRACER",
            "placement_rate": 89.2  # Unique
        }
    ]

    unique_recs, duplicates = DataDeduplicator.deduplicate_records(records)
    assert len(unique_recs) == 2
    assert len(duplicates) == 1
    assert duplicates[0]["trade_id"] == "ELE/Q5901"
