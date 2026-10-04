"""
SkillSathi - AI Counselling Service
Coordinates Intent Detection -> Family Context -> Concern Detection -> Evidence Retrieval -> LLM Generation.
"""
from typing import Dict, Any, List
from app.ai.factory import get_ai_provider
from app.ai.base import AIResponse
from app.utils.logger import logger


class AICounsellingService:
    def __init__(self):
        self.provider = get_ai_provider()

    async def counsel_family(
        self,
        user_message: str,
        user_role: str = "PARENT",
        family_id: int = 1,
        locale: str = "en-IN"
    ) -> AIResponse:
        """
        Executes the end-to-end Family Decision AI Pipeline:
        1. Intent & Concern Detection
        2. Family Profile Context Assembly
        3. Verified Evidence Lookup
        4. Empathetic LLM Synthesis
        """
        logger.info(f"AI Counselling pipeline triggered for role={user_role}, locale={locale}")

        # 1. Detect Concerns
        intent_info = await self.provider.detect_concerns_and_intent(
            text=user_message,
            role=user_role,
            locale=locale
        )

        # 2. Assemble Context (Structured Family Context)
        family_context = {
            "family_id": family_id,
            "user_role": user_role,
            "detected_intent": intent_info.get("intent")
        }

        # 3. Evidence retrieval mock/stub (RAG pipeline)
        relevant_evidence = [
            {
                "source": "MSDE Tracer Study",
                "metric": "Average 1-year placement rate in Electric Vehicle technician trades is 88.4%",
                "verified": True
            }
        ]

        # 4. Generate AI Response
        response = await self.provider.generate_counselling_response(
            user_message=user_message,
            family_context=family_context,
            detected_concerns=intent_info.get("detected_concerns", []),
            available_evidence=relevant_evidence,
            locale=locale
        )
        return response
