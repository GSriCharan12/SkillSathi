"""
SkillSathi - AI Provider Factory
Provides a dynamic, pluggable architecture to switch LLM backends via environment variables.
"""
from app.config import get_settings
from app.ai.base import BaseAIProvider
from app.ai.mock_provider import MockAIProvider
from app.ai.gemini_provider import GeminiAIProvider
from app.ai.openai_provider import OpenAIProvider
from app.utils.logger import logger


class AIProviderFactory:
    @staticmethod
    def get_provider() -> BaseAIProvider:
        return get_ai_provider()


def get_ai_provider() -> BaseAIProvider:
    """Instantiate the configured AI provider instance."""
    settings = get_settings()
    provider_name = (settings.AI_PROVIDER or "mock").lower().strip()

    if provider_name == "gemini":
        logger.info(f"Initializing Gemini AI Provider (model: {settings.AI_MODEL})")
        return GeminiAIProvider(api_key=settings.AI_API_KEY, model_name=settings.AI_MODEL)
    elif provider_name in ("openai", "chatgpt"):
        logger.info(f"Initializing OpenAI Provider (model: {settings.AI_MODEL})")
        return OpenAIProvider(api_key=settings.AI_API_KEY, model_name=settings.AI_MODEL)
    else:
        logger.info(f"Initializing Mock AI Provider (provider: {provider_name})")
        return MockAIProvider(api_key=settings.AI_API_KEY, model_name=settings.AI_MODEL)

