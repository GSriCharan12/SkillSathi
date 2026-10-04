"""
SkillSathi - Language & Regional Dialect Detector
Detects English, Telugu, Hindi, and transliterated Hinglish/Telenglish phrasing.
"""
import re
from typing import Dict, Any


class LanguageDetector:
    TELUGU_UNICODE_PATTERN = re.compile(r'[\u0C00-\u0C7F]')
    DEVANAGARI_UNICODE_PATTERN = re.compile(r'[\u0900-\u097F]')

    TELUGU_TRANSLITERATED_KEYWORDS = {
        "ela", "undhi", "untundi", "untundha", "cheppandi", "chadhavali",
        "jeetham", "jeetam", "paisalu", "bavuntunda", "edugudala", "chadhuvu",
        "diploma", "degree", "samacharam", "enti", "eppudu", "ekkada", "telugu",
        "kaavali", "vuntundha", "koduku", "kuthuru", "biddalu", "pellam"
    }

    HINDI_TRANSLITERATED_KEYWORDS = {
        "kya", "kaise", "hoga", "milega", "paisa", "kamai", "nokri", "naukri",
        "bataiye", "padhai", "aage", "bhavi", "bhavishya", "kitna", "chahiye",
        "karenge", "beti", "beta", "mata", "pita", "izzat", "samaj", "suraksha"
    }

    @classmethod
    def detect_language(cls, text: str) -> Dict[str, Any]:
        """
        Detects primary language and dialect (en, te, hi, hinglish, telenglish).
        """
        if not text or not text.strip():
            return {"primary_language": "en", "dialect": "standard", "confidence": 1.0}

        cleaned = text.strip()
        words = set(re.findall(r'\b[a-zA-Z]+\b', cleaned.lower()))

        # 1. Check Native Scripts
        if cls.TELUGU_UNICODE_PATTERN.search(cleaned):
            return {
                "primary_language": "te",
                "dialect": "telugu_script",
                "confidence": 0.98,
                "locale": "te-IN"
            }

        if cls.DEVANAGARI_UNICODE_PATTERN.search(cleaned):
            return {
                "primary_language": "hi",
                "dialect": "devanagari_script",
                "confidence": 0.98,
                "locale": "hi-IN"
            }

        # 2. Check Telugu Transliterated (Telenglish)
        telugu_matches = words.intersection(cls.TELUGU_TRANSLITERATED_KEYWORDS)
        if len(telugu_matches) >= 1 or any(k in cleaned.lower() for k in ["future ela", "salary entha", "degree osthada"]):
            return {
                "primary_language": "te",
                "dialect": "telenglish",
                "confidence": 0.90,
                "locale": "te-IN"
            }

        # 3. Check Hindi Transliterated (Hinglish)
        hindi_matches = words.intersection(cls.HINDI_TRANSLITERATED_KEYWORDS)
        if len(hindi_matches) >= 1 or any(k in cleaned.lower() for k in ["future kaisa", "salary kitna", "degree milegi"]):
            return {
                "primary_language": "hi",
                "dialect": "hinglish",
                "confidence": 0.90,
                "locale": "hi-IN"
            }

        return {
            "primary_language": "en",
            "dialect": "standard",
            "confidence": 0.95,
            "locale": "en-IN"
        }
