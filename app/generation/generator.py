"""
Response Generation System with Pluggable LLM Providers.

Supported Providers:
1. GeminiProvider (Google Gemini API via google-genai or google-generativeai)
2. OpenAIProvider (OpenAI API via official SDK)
3. LocalModelProvider / Fallback Grounded Synthesizer
4. MockProvider (ONLY used in isolated unit tests)
"""
import os
import re
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Any

from app.core.config import settings
from app.core.logging import logger
from app.models.schemas import EvidenceItem


SUPPORT_SYSTEM_PROMPT = """You are a professional customer support representative for {brand}.
Your task is to draft an empathetic, concise, and accurate response to the customer's inquiry.

CRITICAL INSTRUCTIONS:
1. BASE YOUR RESPONSE DIRECTLY ON THE PROVIDED HISTORICAL RESOLUTION EXAMPLES.
2. Tone: Helpful, calm, professional, concise (typical for Twitter/chat customer care).
3. Under no circumstances should you fabricate policies, account status, refund amounts, or unverified timelines.
4. Do NOT say an action has been taken (e.g., "I have refunded your account") unless explicitly directed.
5. If the historical evidence does not provide clear instructions, politely inform the customer that their issue requires specialized review and ask for necessary non-sensitive verification details or direct them to support DM.
6. Never mention "retrieval", "vector database", "database", or "AI" to the customer.
7. Keep the response to 1-3 clear sentences.
"""

USER_PROMPT_TEMPLATE = """Brand: {brand}
Customer Message: "{customer_message}"
Predicted Intent: {intent_name} (Confidence: {intent_confidence:.1%})

HISTORICAL EVIDENCE & PRECEDENTS:
{evidence_block}

Draft the optimal support response strictly grounded in the historical precedents above:"""


def build_evidence_block(evidence: List[EvidenceItem]) -> str:
    if not evidence:
        return "No closely matching historical precedents found. Advise routing to human support."
    lines = []
    for i, e in enumerate(evidence[:3], 1):
        lines.append(f"[Precedent {i}] (Similarity: {e.similarity:.2f})")
        lines.append(f"  Customer asked: \"{e.customer_message}\"")
        lines.append(f"  Brand resolved: \"{e.brand_response}\"")
    return "\n".join(lines)


class LLMProvider(ABC):
    @abstractmethod
    def generate(
        self,
        customer_message: str,
        intent_name: str,
        intent_confidence: float,
        evidence: List[EvidenceItem],
        brand: str,
    ) -> Tuple[str, float, bool]:
        """
        Returns: (draft_reply, confidence, is_grounded)
        """
        pass


class GeminiProvider(LLMProvider):
    """Google Gemini API Provider."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-1.5-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_name = model
        self._client = None

        if self.api_key:
            try:
                from google import genai
                self._client = genai.Client(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Could not initialize google.genai: {e}")

    def generate(
        self,
        customer_message: str,
        intent_name: str,
        intent_confidence: float,
        evidence: List[EvidenceItem],
        brand: str,
    ) -> Tuple[str, float, bool]:
        if not self.api_key or self._client is None:
            raise RuntimeError(
                "Gemini API key is not configured. Set GEMINI_API_KEY in your .env file."
            )

        evidence_block = build_evidence_block(evidence)
        system_instruction = SUPPORT_SYSTEM_PROMPT.format(brand=brand)
        user_prompt = USER_PROMPT_TEMPLATE.format(
            brand=brand,
            customer_message=customer_message,
            intent_name=intent_name,
            intent_confidence=intent_confidence,
            evidence_block=evidence_block,
        )

        try:
            response = self._client.models.generate_content(
                model=self.model_name,
                contents=user_prompt,
                config={
                    "system_instruction": system_instruction,
                    "temperature": 0.2,
                    "max_output_tokens": 250,
                },
            )
            draft = response.text.strip()
            # Clean quotes if wrapped
            if draft.startswith('"') and draft.endswith('"'):
                draft = draft[1:-1].strip()

            is_grounded = bool(evidence and evidence[0].similarity >= 0.40)
            confidence = min(0.95, round(0.5 + (0.5 * (evidence[0].similarity if evidence else 0.3)), 2))
            return draft, confidence, is_grounded
        except Exception as e:
            logger.error(f"Gemini generation error: {e}")
            raise RuntimeError(f"Gemini API error: {str(e)}")


class OpenAIProvider(LLMProvider):
    """OpenAI API Provider."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model_name = model
        self._client = None
        if self.api_key:
            try:
                from openai import OpenAI
                self._client = OpenAI(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Could not initialize OpenAI: {e}")

    def generate(
        self,
        customer_message: str,
        intent_name: str,
        intent_confidence: float,
        evidence: List[EvidenceItem],
        brand: str,
    ) -> Tuple[str, float, bool]:
        if not self.api_key or self._client is None:
            raise RuntimeError(
                "OpenAI API key is not configured. Set OPENAI_API_KEY in your .env file."
            )

        evidence_block = build_evidence_block(evidence)
        system_instruction = SUPPORT_SYSTEM_PROMPT.format(brand=brand)
        user_prompt = USER_PROMPT_TEMPLATE.format(
            brand=brand,
            customer_message=customer_message,
            intent_name=intent_name,
            intent_confidence=intent_confidence,
            evidence_block=evidence_block,
        )

        try:
            response = self._client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,
                max_tokens=250,
            )
            draft = response.choices[0].message.content.strip()
            if draft.startswith('"') and draft.endswith('"'):
                draft = draft[1:-1].strip()

            is_grounded = bool(evidence and evidence[0].similarity >= 0.40)
            confidence = min(0.95, round(0.5 + (0.5 * (evidence[0].similarity if evidence else 0.3)), 2))
            return draft, confidence, is_grounded
        except Exception as e:
            logger.error(f"OpenAI generation error: {e}")
            raise RuntimeError(f"OpenAI API error: {str(e)}")


class EvidenceSynthesisProvider(LLMProvider):
    """
    Evidence-Grounded Local Synthesizer:
    Used when external API keys are unavailable or for baseline comparison.
    Synthesizes historical resolutions directly from the retrieved corpus
    without hallucination.
    """

    def generate(
        self,
        customer_message: str,
        intent_name: str,
        intent_confidence: float,
        evidence: List[EvidenceItem],
        brand: str,
    ) -> Tuple[str, float, bool]:
        if not evidence or evidence[0].similarity < 0.20:
            return (
                f"Hi there, thanks for reaching out to {brand}. To assist you with this issue safely, "
                f"please send us a DM with your account details and we will investigate promptly.",
                0.50,
                False,
            )

        best = evidence[0]
        # Clean brand response signature / handle references
        resp = best.brand_response
        resp = re.sub(r"^@\w+\s*", "", resp)
        # Remove trailing staff signatures like ^AA, /BM
        resp = re.sub(r"\s*(\^|/)[A-Z]{1,3}\s*$", "", resp).strip()

        return resp, min(0.92, round(best.similarity, 2)), True


class MockProvider(LLMProvider):
    """Deterministic Mock Provider for unit testing."""

    def generate(
        self,
        customer_message: str,
        intent_name: str,
        intent_confidence: float,
        evidence: List[EvidenceItem],
        brand: str,
    ) -> Tuple[str, float, bool]:
        return (
            f"Mock response for {brand} addressing {intent_name}.",
            0.90,
            True,
        )


def get_llm_provider() -> LLMProvider:
    provider_name = os.getenv("LLM_PROVIDER", settings.llm.provider).lower()
    gemini_key = os.getenv("GEMINI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if provider_name == "mock":
        return MockProvider()
    elif provider_name == "openai" and openai_key:
        return OpenAIProvider(api_key=openai_key)
    elif provider_name == "gemini" and gemini_key:
        return GeminiProvider(api_key=gemini_key)
    elif gemini_key:
        return GeminiProvider(api_key=gemini_key)
    elif openai_key:
        return OpenAIProvider(api_key=openai_key)
    else:
        logger.info("No external LLM API key detected. Using EvidenceSynthesisProvider.")
        return EvidenceSynthesisProvider()
