"""
SkillSathi - Google Gemini AI Provider
"""
import httpx
from typing import Dict, Any, List, Optional
from app.ai.base import BaseAIProvider, AIResponse
from app.utils.logger import logger


class GeminiAIProvider(BaseAIProvider):
    """Google Gemini AI Provider implementing structured family decision dialogue."""

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = "gemini-1.5-flash", **kwargs):
        super().__init__(api_key=api_key, model_name=model_name or "gemini-1.5-flash", **kwargs)
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"

    async def generate_counselling_response(
        self,
        user_message: str,
        family_context: Dict[str, Any],
        detected_concerns: List[Dict[str, Any]],
        available_evidence: List[Dict[str, Any]],
        locale: str = "en-IN"
    ) -> AIResponse:
        if not self.api_key:
            logger.warning("No Gemini API key supplied; returning fallback response.")
            return AIResponse(
                content="Please configure AI_API_KEY for live Gemini generation. SkillSathi is running in fallback mode.",
                provider_name="GeminiProvider",
                model_name=self.model_name
            )

        # In production, uses generative REST API or Google GenAI SDK
        prompt = (
            f"You are SkillSathi, an empathetic AI family counsellor for Indian vocational education decisions.\n"
            f"Family Context: {family_context}\n"
            f"Concerns: {detected_concerns}\n"
            f"Verified Evidence: {available_evidence}\n"
            f"User Query: {user_message}\n"
            f"Respond empathetically, addressing family concerns with verified facts."
        )

        try:
            model = self.model_name.replace("models/", "")
            url = f"{self.base_url}/models/{model}:generateContent?key={self.api_key}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}]
            }
            async with httpx.AsyncClient(timeout=30.0) as client:
                res = await client.post(url, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts:
                            text = parts[0].get("text", "")
                            return AIResponse(
                                content=text,
                                provider_name="GeminiProvider",
                                model_name=self.model_name,
                                raw_response=data
                            )
                else:
                    logger.error(f"Gemini API returned status {res.status_code}: {res.text}")
        except Exception as e:
            logger.error(f"Gemini API request failed: {e}")

        return AIResponse(
            content="We encountered a temporary network issue connecting to the AI counsellor. SkillSathi verified pathways remain accessible.",
            provider_name="GeminiProvider",
            model_name=self.model_name
        )

    async def detect_concerns_and_intent(
        self,
        text: str,
        role: str,
        locale: str = "en-IN"
    ) -> Dict[str, Any]:
        return {
            "intent": "VOCATIONAL_PATHWAY_INQUIRY",
            "detected_concerns": ["INCOME", "STATUS"],
            "severity_score": 6,
            "role": role
        }
