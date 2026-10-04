"""
SkillSathi - Family Concern Extraction & Mapping Engine
Maps natural-language parent and learner inputs to structured concern categories with confidence & severity.
STRICT RULE: Do NOT present sentiment classification as psychological truth. Label as 'detected concern' or 'reported concern'.
"""
from typing import List, Dict, Any, Tuple
import re
from app.models.family import ConcernCategory


class ConcernEngine:
    """Extracts and standardizes family concerns from natural language."""

    KEYWORDS = {
        ConcernCategory.INCOME: [
            "salary", "money", "earn", "income", "paisa", "kamai", "remuneration", "low pay", "stipend", "wages"
        ],
        ConcernCategory.JOB_SECURITY: [
            "security", "permanent", "layoff", "contract", "stable", "stability", "recession", "loss of job"
        ],
        ConcernCategory.SOCIAL_STATUS: [
            "status", "respect", "relatives", "society", "izzat", "shame", "reputation", "prestige", "stigma", "white collar"
        ],
        ConcernCategory.SAFETY: [
            "safety", "safe", "hazard", "girls", "women", "night shift", "accident", "injury", "dangerous", "suraksha"
        ],
        ConcernCategory.CAREER_GROWTH: [
            "growth", "promotion", "future", "stuck", "career ladder", "dead end", "advancement", "taraqqi"
        ],
        ConcernCategory.FURTHER_EDUCATION: [
            "degree", "btech", "b.voc", "polytechnic", "higher studies", "college", "university", "padhai", "graduation"
        ],
        ConcernCategory.LOCATION: [
            "location", "far away", "travel", "commute", "hostel", "relocate", "migration", "distant", "local", "near home"
        ],
        ConcernCategory.AFFORDABILITY: [
            "fee", "cost", "expensive", "afford", "loan", "expenses", "kharcha", "tuition"
        ],
    }

    @classmethod
    def analyze_natural_language_concern(
        cls,
        text: str,
        user_role: str = "PARENT"
    ) -> List[Dict[str, Any]]:
        """
        Extracts mapped categories and estimates severity (1-10) and confidence.
        """
        if not text or not text.strip():
            return []

        cleaned_text = text.lower()
        extracted_concerns = []

        for category, keywords in cls.KEYWORDS.items():
            matched_words = [kw for kw in keywords if re.search(r'\b' + re.escape(kw) + r'\b', cleaned_text)]
            if matched_words:
                # Severity calculation based on intensity modifiers
                severity = 6
                if any(w in cleaned_text for w in ["very", "extremely", "deeply", "severe", "terrified", "bothered"]):
                    severity = 9
                elif any(w in cleaned_text for w in ["slightly", "minor", "wondering", "curious"]):
                    severity = 4

                confidence = min(0.95, 0.70 + (len(matched_words) * 0.10))

                extracted_concerns.append({
                    "category": category.value,
                    "concern_text": text.strip(),
                    "severity_level": severity,
                    "confidence_score": round(confidence, 2),
                    "concern_type": "detected concern",
                    "matched_indicators": matched_words,
                    "source_role": user_role
                })

        # If no explicit category matched, assign GENERAL / OTHER
        if not extracted_concerns:
            extracted_concerns.append({
                "category": ConcernCategory.OTHER.value,
                "concern_text": text.strip(),
                "severity_level": 5,
                "confidence_score": 0.60,
                "concern_type": "reported concern",
                "matched_indicators": [],
                "source_role": user_role
            })

        return extracted_concerns

    @classmethod
    def map_concerns_from_text(
        cls,
        text: str,
        source_role: str = "PARENT"
    ) -> List[Dict[str, Any]]:
        return cls.analyze_natural_language_concern(text=text, user_role=source_role)
