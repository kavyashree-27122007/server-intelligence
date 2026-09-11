"""
Pipeline Orchestration Service for Support Intelligence.

Coordinates:
1. Input validation & sanitization
2. Intent Classification (with confidence scoring)
3. Historical Evidence Retrieval (dense semantic + lexical fallback)
4. Evidence-Grounded Reply Generation (via LLMProvider)
5. Multi-Factor Escalation Decision (with human-readable audit reason)
6. Latency & audit logging
"""
import time
import uuid
from typing import Optional

from app.core.config import settings
from app.core.logging import logger
from app.models.schemas import (
    AnalysisResult,
    AnalyzeRequest,
    EscalationResult,
    EvidenceItem,
    IntentResult,
)
from app.classification.classifier import TfidfIntentClassifier
from app.retrieval.retriever import HybridSupportRetriever
from app.generation.generator import get_llm_provider
from app.escalation.engine import EscalationEngine


class SupportIntelligencePipeline:
    """
    End-to-end evidence-grounded customer support pipeline.
    """

    def __init__(self):
        self.brand = settings.brand
        self.classifier = TfidfIntentClassifier()
        self.retriever = HybridSupportRetriever()
        self.escalation_engine = EscalationEngine(
            intent_conf_threshold=settings.escalation.low_confidence_threshold,
            similarity_threshold=settings.escalation.low_similarity_threshold,
        )
        self.llm_provider = get_llm_provider()
        self.is_ready = False

    def load_artifacts(self):
        """Load trained models and vector indices from disk."""
        model_path = settings.project_root / "data" / "index" / "classifier.joblib"
        index_dir = settings.project_root / "data" / "index"

        if model_path.exists():
            self.classifier.load(model_path)
            logger.info(f"Loaded classifier from {model_path}")
        else:
            logger.warning(f"Classifier artifact not found at {model_path}")

        if (index_dir / "lexical_index.pkl").exists() or (index_dir / "semantic_index.pkl").exists():
            self.retriever.load(index_dir)
            logger.info(f"Loaded retriever indices from {index_dir}")
        else:
            logger.warning(f"Retrieval indices not found at {index_dir}")

        self.is_ready = True

    def analyze(self, request: AnalyzeRequest) -> AnalysisResult:
        start_time = time.time()
        request_id = str(uuid.uuid4())
        message = request.message.strip()

        logger.info(f"[{request_id}] Analyzing incoming message: \"{message[:60]}...\"")

        # 1. Intent Classification
        try:
            intent: IntentResult = self.classifier.predict(message)
        except Exception as e:
            logger.error(f"Classification failed: {e}. Falling back to default.")
            intent = IntentResult(
                name="General Inquiries",
                intent_id="general_inquiries",
                confidence=0.35,
                all_scores={"General Inquiries": 0.35},
            )

        # 2. Historical Evidence Retrieval
        try:
            evidence = self.retriever.retrieve_similar_messages(
                query=message,
                brand=self.brand,
                intent=intent.name,
                top_k=settings.retrieval.top_k,
                similarity_threshold=settings.retrieval.similarity_threshold,
            )
        except Exception as e:
            logger.error(f"Retrieval failed: {e}. Empty evidence returned.")
            evidence = []

        # 3. Grounded Reply Generation
        try:
            draft_reply, reply_confidence, is_grounded = self.llm_provider.generate(
                customer_message=message,
                intent_name=intent.name,
                intent_confidence=intent.confidence,
                evidence=evidence,
                brand=self.brand,
            )
        except Exception as e:
            logger.error(f"LLM Generation failed: {e}. Using fallback guidance.")
            draft_reply = (
                f"Thank you for reaching out to {self.brand} Support. We are reviewing your request "
                f"and will get back to you shortly. Please send us a private message with your account details."
            )
            reply_confidence = 0.40
            is_grounded = False

        # 4. Human Escalation Decision
        escalation: EscalationResult = self.escalation_engine.evaluate(
            message=message,
            intent_name=intent.name,
            intent_confidence=intent.confidence,
            evidence=evidence,
        )

        latency_ms = round((time.time() - start_time) * 1000, 2)
        logger.info(
            f"[{request_id}] Decision: {escalation.decision} (conf={escalation.confidence:.2f}), "
            f"Intent: {intent.name} ({intent.confidence:.2f}), Latency: {latency_ms}ms"
        )

        return AnalysisResult(
            message=message,
            intent=intent,
            evidence=evidence,
            draft_reply=draft_reply,
            decision=escalation.decision,
            decision_confidence=escalation.confidence,
            reason=escalation.reason,
            risk_factors=escalation.risk_factors,
            request_id=request_id,
            latency_ms=latency_ms,
        )


# Global singleton pipeline instance
pipeline = SupportIntelligencePipeline()
