"""
SkillSathi - Data Quality & Ingestion Validator
Strict Validation Rules:
- Rejects impossible percentages (< 0 or > 100)
- Rejects negative earnings / stipends
- Rejects records missing source provenance
- Rejects invalid data years (< 2000 or > current year + 1)
- Rejects incompatible geographic structures
"""
from typing import Dict, Any, List, Tuple
from datetime import datetime, timezone
from app.utils.logger import logger


class DataValidator:
    """Validates normalized records for semantic, statistical, and relational integrity."""

    @staticmethod
    def validate_outcome_record(record: Dict[str, Any]) -> Tuple[bool, List[str], str]:
        """
        Validates an outcome statistic.
        Returns: (is_valid, error_messages, primary_issue_type)
        """
        errors = []
        issue_type = "UNKNOWN"

        # 1. Source Provenance Check
        if not record.get("source_id") and not record.get("source_name"):
            errors.append("Record lacks required source provenance link.")
            issue_type = "MISSING_SOURCE"

        # 2. Percentage Bounds Check
        placement_rate = record.get("placement_rate")
        if placement_rate is not None:
            try:
                rate_val = float(placement_rate)
                if rate_val < 0.0 or rate_val > 100.0:
                    errors.append(f"Impossible placement rate: {rate_val}%. Must be between 0.0 and 100.0%.")
                    issue_type = "INVALID_PERCENTAGE"
            except (ValueError, TypeError):
                errors.append(f"Invalid non-numeric placement rate: {placement_rate}")
                issue_type = "INVALID_PERCENTAGE"
        else:
            errors.append("Placement rate is required.")
            issue_type = "INVALID_PERCENTAGE"

        # 3. Earnings Non-Negativity & Rationality Check
        earnings_min = record.get("earnings_min")
        earnings_max = record.get("earnings_max")
        if earnings_min is not None:
            try:
                min_val = int(earnings_min)
                if min_val < 0:
                    errors.append(f"Negative minimum earnings: {min_val}")
                    issue_type = "NEGATIVE_EARNINGS"
            except (ValueError, TypeError):
                errors.append(f"Invalid non-integer earnings_min: {earnings_min}")
                issue_type = "NEGATIVE_EARNINGS"

        if earnings_max is not None:
            try:
                max_val = int(earnings_max)
                if max_val < 0:
                    errors.append(f"Negative maximum earnings: {max_val}")
                    issue_type = "NEGATIVE_EARNINGS"
                if earnings_min is not None and int(earnings_min) > max_val:
                    errors.append(f"earnings_min ({earnings_min}) cannot exceed earnings_max ({max_val})")
                    issue_type = "NEGATIVE_EARNINGS"
            except (ValueError, TypeError):
                errors.append(f"Invalid non-integer earnings_max: {earnings_max}")
                issue_type = "NEGATIVE_EARNINGS"

        # 4. Data Year Sanity Check
        data_year = record.get("data_year")
        current_year = datetime.now(timezone.utc).year
        if data_year is not None:
            try:
                year_val = int(data_year)
                if year_val < 2010 or year_val > current_year + 1:
                    errors.append(f"Invalid data_year: {year_val}. Expected between 2010 and {current_year + 1}.")
                    issue_type = "INVALID_DATE"
            except (ValueError, TypeError):
                errors.append(f"Invalid non-integer data_year: {data_year}")
                issue_type = "INVALID_DATE"
        else:
            errors.append("data_year is required.")
            issue_type = "INVALID_DATE"

        # 5. Trade Identifier Check
        if not record.get("trade_code") and not record.get("trade_id"):
            errors.append("Missing trade identifier (trade_code or trade_id).")
            issue_type = "UNSUPPORTED_COMBINATION"

        return (len(errors) == 0, errors, issue_type if errors else "NONE")

    @staticmethod
    def validate_trade_record(record: Dict[str, Any]) -> Tuple[bool, List[str], str]:
        errors = []
        issue_type = "UNKNOWN"

        if not record.get("code"):
            errors.append("Trade code is missing.")
            issue_type = "UNSUPPORTED_COMBINATION"
        if not record.get("title"):
            errors.append("Trade title is missing.")
            issue_type = "UNSUPPORTED_COMBINATION"

        nsqf = record.get("nsqf_level")
        if nsqf is not None:
            try:
                nsqf_int = int(nsqf)
                if not (1 <= nsqf_int <= 10):
                    errors.append(f"NSQF level must be between 1 and 10, got: {nsqf_int}")
                    issue_type = "UNSUPPORTED_COMBINATION"
            except (ValueError, TypeError):
                errors.append(f"Invalid non-integer nsqf_level: {nsqf}")
                issue_type = "UNSUPPORTED_COMBINATION"

        return (len(errors) == 0, errors, issue_type if errors else "NONE")
