"""
SkillSathi - OpenAI-Compatible AI Provider
"""
import httpx
from typing import Dict, Any, List, Optional
from app.ai.base import BaseAIProvider, AIResponse
from app.utils.logger import logger


class OpenAIProvider(BaseAIProvider):
    """OpenAI / Compatible API Provider (works with OpenAI, Azure, LocalAI, vLLM)."""

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = "gpt-4o-mini", **kwargs):
        super().__init__(api_key=api_key, model_name=model_name or "gpt-4o-mini", **kwargs)
        self.base_url = kwargs.get("base_url", "https://api.openai.com/v1")

    async def generate_counselling_response(
        self,
        user_message: str,
        family_context: Dict[str, Any],
        detected_concerns: List[Dict[str, Any]],
        available_evidence: List[Dict[str, Any]],
        locale: str = "en-IN"
    ) -> AIResponse:
        if not self.api_key:
            return AIResponse(
                content="OpenAI API Key not configured. Using fallback response mode.",
                provider_name="OpenAIProvider",
                model_name=self.model_name
            )

        messages = [
            {"role": "system", "content": "You are SkillSathi, a specialized career counsellor helping Indian families align on vocational education."},
            {"role": "user", "content": f"Family: {family_context}\nConcerns: {detected_concerns}\nEvidence: {available_evidence}\nQuery: {user_message}"}
        ]

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                res = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={"model": self.model_name, "messages": messages, "temperature": 0.2}
                )
                if res.status_code == 200:
                    data = res.json()
                    content = data["choices"][0]["message"]["content"]
                    return AIResponse(
                        content=content,
                        provider_name="OpenAIProvider",
                        model_name=self.model_name,
                        raw_response=data
                    )
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")

        return AIResponse(
            content="Service temporarily unavailable. SkillSathi offline evidence remains active.",
            provider_name="OpenAIProvider",
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
            "severity_score": 5,
            "role": role
        }
