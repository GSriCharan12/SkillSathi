"""
SkillSathi - AI Provider Base Interface
Defines the contract for all AI model providers (Gemini, OpenAI, Ollama, Mock, etc.).
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel


class AIResponse(BaseModel):
    content: str
    detected_concerns: List[str] = []
    recommended_evidence_ids: List[int] = []
    family_alignment_score: Optional[float] = None
    suggested_questions: List[str] = []
    raw_response: Optional[Dict[str, Any]] = None
    provider_name: str
    model_name: str


class BaseAIProvider(ABC):
    """Abstract Base Class for AI engines to ensure zero vendor lock-in."""

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None, **kwargs):
        self.api_key = api_key
        self.model_name = model_name
        self.extra_kwargs = kwargs

    @abstractmethod
    async def generate_counselling_response(
        self,
        user_message: str,
        family_context: Dict[str, Any],
        detected_concerns: List[Dict[str, Any]],
        available_evidence: List[Dict[str, Any]],
        locale: str = "en-IN"
    ) -> AIResponse:
        """
        Processes a family or learner query and produces a family-informed,
        evidence-backed counselling response.
        """
        pass

    @abstractmethod
    async def detect_concerns_and_intent(
        self,
        text: str,
        role: str,
        locale: str = "en-IN"
    ) -> Dict[str, Any]:
        """
        Analyzes dialogue to extract underlying root concerns (income, social stigma, safety, etc.).
        """
        pass
