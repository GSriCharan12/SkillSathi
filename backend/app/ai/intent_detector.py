"""
SkillSathi - Intent Detector for Vocational Family Dialogue
Maps multi-lingual and colloquial family queries into standardized intent classes.
"""
from typing import Dict, Any, List
import re


class IntentDetector:
    INTENT_KEYWORD_MAP = {
        "COUNSELLOR_REQUEST": [
            "talk to counsellor", "human counsellor", "counselor call", "advisor",
            "expert se baat", "counsellor tho matladali", "human help", "escalate"
        ],
        "INCOME": [
            "salary", "starting wage", "income", "stipend", "earn", "paisa", "kamai",
            "jeetham", "jeetam", "paisalu", "money", "earnings", "package"
        ],
        "JOB_SECURITY": [
            "security", "permanent", "contract", "pf", "esi", "stability", "naukri",
            "secure", "layoff", "bhadhratha", "sthiratha"
        ],
        "CAREER_GROWTH": [
            "growth", "future", "promotion", "3 years", "5 years", "superintendent",
            "supervisor", "edugudala", "bhavishya", "ladder", "progression"
        ],
        "SOCIAL_PERCEPTION": [
            "respect", "izzat", "society", "status", "relatives", "prestige",
            "samajam", "paruvu", "shame", "dignity", "proud"
        ],
        "SAFETY": [
            "safety", "safe", "hazard", "girls", "women", "night shift", "accident",
            "suraksha", "bhadram", "protection"
        ],
        "FURTHER_EDUCATION": [
            "degree", "college", "bvoc", "b.voc", "btech", "b.tech", "diploma",
            "lateral entry", "chadhuvu", "higher studies", "university", "padhai"
        ],
        "LOCAL_OPPORTUNITIES": [
            "local", "warangal", "pune", "district", "near home", "cluster",
            "daggara", "santhaoor", "nearby", "location", "telangana", "proximity"
        ],
        "TRAINING_PROVIDER": [
            "iti", "nsti", "polytechnic", "college", "admission", "fees", "hostel",
            "intake", "seats", "institute", "centre"
        ],
        "COMPARISON": [
            "compare", "difference", "versus", "vs", "which is better", "rendu",
            "tulana", "solar or ev", "cnc or drone"
        ],
        "ELIGIBILITY": [
            "eligibility", "qualification", "10th pass", "12th pass", "criteria",
            "requirements", "marks", "age"
        ],
        "PATHWAY": [
            "pathway", "roadmap", "steps", "how to become", "process", "ladder",
            "stages", "step by step"
        ],
        "CAREER_INFORMATION": [
            "what is", "about trade", "details", "work", "job profile", "overview",
            "ev technician", "solar pv", "cnc machinist", "biomedical", "drone"
        ]
    }

    @classmethod
    def detect_intent(cls, text: str) -> Dict[str, Any]:
        if not text or not text.strip():
            return {
                "primary_intent": "GENERAL",
                "confidence": 0.5,
                "secondary_intents": []
            }

        cleaned = text.lower()
        matched_scores: Dict[str, int] = {}

        for intent, patterns in cls.INTENT_KEYWORD_MAP.items():
            count = 0
            for pattern in patterns:
                if pattern in cleaned:
                    count += 1
            if count > 0:
                matched_scores[intent] = count

        if not matched_scores:
            return {
                "primary_intent": "GENERAL",
                "confidence": 0.6,
                "secondary_intents": []
            }

        sorted_intents = sorted(matched_scores.items(), key=lambda x: x[1], reverse=True)
        primary = sorted_intents[0][0]
        secondary = [item[0] for item in sorted_intents[1:]]

        return {
            "primary_intent": primary,
            "confidence": min(0.95, 0.7 + (sorted_intents[0][1] * 0.1)),
            "secondary_intents": secondary
        }
