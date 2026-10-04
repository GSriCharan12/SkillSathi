"""
SkillSathi - Data Ingestion Validation Tests
Ensures strict rejection of invalid statistical data, negative earnings, and missing provenance.
"""
import pytest
from app.data_sources.validator import DataValidator


def test_validate_valid_outcome():
    valid_record = {
        "source_id": 1,
        "trade_code": "ELE/Q5901",
        "placement_rate": 85.5,
        "earnings_min": 18000,
        "earnings_max": 25000,
        "data_year": 2024
    }
    is_valid, errors, issue_type = DataValidator.validate_outcome_record(valid_record)
    assert is_valid is True
    assert len(errors) == 0
    assert issue_type == "NONE"


def test_reject_impossible_percentage():
    invalid_record = {
        "source_id": 1,
        "trade_code": "ELE/Q5901",
        "placement_rate": 145.0,  # > 100%
        "earnings_min": 18000,
        "earnings_max": 25000,
        "data_year": 2024
    }
    is_valid, errors, issue_type = DataValidator.validate_outcome_record(invalid_record)
    assert is_valid is False
    assert issue_type == "INVALID_PERCENTAGE"
    assert any("Impossible placement rate" in e for e in errors)


def test_reject_negative_earnings():
    invalid_record = {
        "source_id": 1,
        "trade_code": "ELE/Q5901",
        "placement_rate": 80.0,
        "earnings_min": -5000,  # Negative
        "earnings_max": 25000,
        "data_year": 2024
    }
    is_valid, errors, issue_type = DataValidator.validate_outcome_record(invalid_record)
    assert is_valid is False
    assert issue_type == "NEGATIVE_EARNINGS"
    assert any("Negative minimum earnings" in e for e in errors)


def test_reject_inverted_earnings_range():
    invalid_record = {
        "source_id": 1,
        "trade_code": "ELE/Q5901",
        "placement_rate": 80.0,
        "earnings_min": 30000,
        "earnings_max": 20000,  # min > max
        "data_year": 2024
    }
    is_valid, errors, issue_type = DataValidator.validate_outcome_record(invalid_record)
    assert is_valid is False
    assert issue_type == "NEGATIVE_EARNINGS"
    assert any("cannot exceed earnings_max" in e for e in errors)


def test_reject_missing_source():
    invalid_record = {
        "trade_code": "ELE/Q5901",
        "placement_rate": 80.0,
        "earnings_min": 15000,
        "earnings_max": 22000,
        "data_year": 2024
    }
    is_valid, errors, issue_type = DataValidator.validate_outcome_record(invalid_record)
    assert is_valid is False
    assert issue_type == "MISSING_SOURCE"


def test_reject_invalid_year():
    invalid_record = {
        "source_id": 1,
        "trade_code": "ELE/Q5901",
        "placement_rate": 80.0,
        "earnings_min": 15000,
        "earnings_max": 22000,
        "data_year": 1995  # Too old
    }
    is_valid, errors, issue_type = DataValidator.validate_outcome_record(invalid_record)
    assert is_valid is False
    assert issue_type == "INVALID_DATE"


def test_validate_trade_nsqf_level():
    valid_trade = {"code": "ELE/Q5901", "title": "Solar Tech", "nsqf_level": 4}
    is_valid, _, _ = DataValidator.validate_trade_record(valid_trade)
    assert is_valid is True

    invalid_trade = {"code": "ELE/Q5901", "title": "Solar Tech", "nsqf_level": 15}
    is_valid, errors, issue_type = DataValidator.validate_trade_record(invalid_trade)
    assert is_valid is False
    assert any("NSQF level must be between 1 and 10" in e for e in errors)
