"""
Explicit Multi-Factor Escalation Engine for Support Intelligence.

Implements principled, explainable decision logic to decide between:
- AUTO_HANDLE: Safe, routine query with high intent confidence and strong historical evidence.
- ESCALATE: Query contains safety risks, account-specific ambiguity, low confidence,
  or weak historical retrieval evidence.

Formula:
  Risk Score = w_intent * (1 - intent_conf)
             + w_retrieval * (1 - max_similarity)
             + w_evidence * (1 - min(evidence_count, 3)/3)
             + w_risk_signals * (has_risk_keywords)
             + w_urgency * (urgency_sentiment_score)

Threshold:
  If Risk Score >= 0.45 or any Critical Risk Trigger -> ESCALATE
  Else -> AUTO_HANDLE
"""
import re
from typing import List, Tuple
from app.core.config import settings
from app.core.logging import logger
from app.models.schemas import EscalationResult, EvidenceItem


# Critical triggers that immediately mandate human escalation
CRITICAL_RISK_PATTERNS = [
    (r"\b(lawyer|attorney|legal action|sue|court|lawsuit)\b", "Legal dispute or litigation threat"),
    (r"\b(hack(ed|ing)?|compromised|unauthorized access|stolen account)\b", "Account security compromise"),
    (r"\b(fraud|fraudulent|identity theft|scam)\b", "Suspected fraud or financial crime"),
    (r"\b(suicide|self[- ]harm|harm myself|kill myself)\b", "Critical user safety concern"),
    (r"\b(chargeback|police report|attorney general)\b", "Formal dispute escalation"),
]

# Sensitive patterns that increase risk score
SENSITIVE_PATTERNS = [
    (r"\b(refund|overcharged|double charge|charged twice|unauthorized charge)\b", "Financial dispute requiring billing access"),
    (r"\b(cancel(lation)? subscription|close account|delete account)\b", "Irreversible account action"),
    (r"\b(furious|disgusted|unacceptable|horrible service|worst company|scammers)\b", "High-severity customer frustration"),
    (r"\b(password|security code|otp|pin|credentials)\b", "Credential / authentication sensitivity"),
]


class EscalationEngine:
    """
    Evaluates customer message, predicted intent, and historical evidence
    to make an auditable AUTO_HANDLE vs ESCALATE decision.
    """

    def __init__(
        self,
        intent_conf_threshold: float = 0.55,
        similarity_threshold: float = 0.45,
        risk_cutoff: float = 0.45,
    ):
        self.intent_conf_threshold = intent_conf_threshold
        self.similarity_threshold = similarity_threshold
        self.risk_cutoff = risk_cutoff

    def evaluate(
        self,
        message: str,
        intent_name: str,
        intent_confidence: float,
        evidence: List[EvidenceItem],
    ) -> EscalationResult:
        """
        Evaluate customer support interaction and return human-interpretable escalation decision.
        """
        risk_factors: List[str] = []
        message_lower = message.lower()

        # 1. Check Critical Risk Triggers (Hard Escalation)
        for pattern, reason in CRITICAL_RISK_PATTERNS:
            if re.search(pattern, message_lower):
                risk_factors.append(f"Critical trigger: {reason}")
                logger.info(f"Escalation triggered by critical pattern: {reason}")
                return EscalationResult(
                    decision="ESCALATE",
                    confidence=0.95,
                    reason=f"Mandatory human review required: {reason}.",
                    risk_factors=risk_factors,
                    risk_score=1.0,
                )

        # 2. Check Sensitive Patterns
        sensitive_score = 0.0
        for pattern, reason in SENSITIVE_PATTERNS:
            if re.search(pattern, message_lower):
                risk_factors.append(f"Sensitive domain: {reason}")
                sensitive_score += 0.25
        sensitive_score = min(sensitive_score, 0.60)

        # 3. Component scores (0.0 to 1.0 each)
        # Intent uncertainty
        intent_uncertainty = max(0.0, 1.0 - intent_confidence)
        if intent_confidence < self.intent_conf_threshold:
            risk_factors.append(
                f"Low intent confidence ({intent_confidence:.1%}, threshold {self.intent_conf_threshold:.1%})"
            )

        # Retrieval weakness
        max_sim = max([e.similarity for e in evidence], default=0.0)
        retrieval_weakness = max(0.0, 1.0 - max_sim)
        if max_sim < self.similarity_threshold:
            risk_factors.append(
                f"Weak historical evidence match ({max_sim:.1%}, threshold {self.similarity_threshold:.1%})"
            )

        # Evidence sparsity
        evidence_count = len(evidence)
        sparsity_penalty = max(0.0, 1.0 - (min(evidence_count, 3) / 3.0))
        if evidence_count < 2:
            risk_factors.append(f"Insufficient historical evidence ({evidence_count} examples retrieved)")

        # Message brevity / vagueness
        length_penalty = 0.0
        word_count = len(message.strip().split())
        if word_count <= 3:
            length_penalty = 0.35
            risk_factors.append(f"Underspecified query ({word_count} words)")

        # 4. Multi-Factor Risk Score Formulation
        # Weights sum to 1.0
        w_intent = 0.25
        w_retrieval = 0.25
        w_sparsity = 0.15
        w_sensitive = 0.25
        w_brevity = 0.10

        composite_risk = (
            w_intent * intent_uncertainty
            + w_retrieval * retrieval_weakness
            + w_sparsity * sparsity_penalty
            + w_sensitive * sensitive_score
            + w_brevity * length_penalty
        )
        composite_risk = min(1.0, max(0.0, composite_risk))

        # 5. Final Decision
        if composite_risk >= self.risk_cutoff or len(risk_factors) >= 2:
            decision = "ESCALATE"
            # Decision confidence is how sure we are about escalating
            decision_confidence = min(0.98, 0.50 + composite_risk * 0.5)
            # Stated human-readable reason
            primary_reason = risk_factors[0] if risk_factors else "Elevated risk score"
            reason_text = (
                f"Escalated to human support agent: {primary_reason}. "
                f"Composite risk score: {composite_risk:.2f}."
            )
        else:
            decision = "AUTO_HANDLE"
            decision_confidence = min(0.98, 0.50 + (1.0 - composite_risk) * 0.5)
            reason_text = (
                f"Safe to auto-handle: high intent clarity ({intent_confidence:.1%}) "
                f"and verified historical resolution match ({max_sim:.1%})."
            )

        return EscalationResult(
            decision=decision,
            confidence=round(decision_confidence, 3),
            reason=reason_text,
            risk_factors=risk_factors,
            risk_score=round(composite_risk, 3),
        )
