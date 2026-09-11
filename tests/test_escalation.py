"""
Unit tests for escalation engine: critical triggers, sensitive queries, and auto-handling.
"""
import pytest
from app.escalation.engine import EscalationEngine
from app.models.schemas import EvidenceItem


@pytest.fixture
def engine():
    return EscalationEngine()


def test_critical_trigger_legal(engine):
    evidence = [EvidenceItem(customer_message="test", brand_response="test", similarity=0.9)]
    res = engine.evaluate(
        message="I will get my lawyer and sue you in court for unauthorized charges",
        intent_name="Subscription & Billing",
        intent_confidence=0.95,
        evidence=evidence,
    )
    assert res.decision == "ESCALATE"
    assert "Legal dispute" in res.reason
    assert res.risk_score == 1.0


def test_critical_trigger_security(engine):
    evidence = [EvidenceItem(customer_message="test", brand_response="test", similarity=0.9)]
    res = engine.evaluate(
        message="Someone hacked my account and took unauthorized access",
        intent_name="Account Access & Login",
        intent_confidence=0.90,
        evidence=evidence,
    )
    assert res.decision == "ESCALATE"
    assert "security" in res.reason.lower()


def test_routine_auto_handle(engine):
    evidence = [
        EvidenceItem(customer_message="How to turn off shuffle", brand_response="Tap the green shuffle icon", similarity=0.85),
        EvidenceItem(customer_message="Turn off shuffle mode", brand_response="Toggle shuffle button", similarity=0.80),
    ]
    res = engine.evaluate(
        message="How do I turn off shuffle on my playlist?",
        intent_name="Playlist & Library Management",
        intent_confidence=0.92,
        evidence=evidence,
    )
    assert res.decision == "AUTO_HANDLE"
    assert res.confidence >= 0.50
    assert len(res.risk_factors) == 0


def test_escalate_on_sparse_or_weak_evidence(engine):
    # High confidence in intent but no retrieval evidence
    res = engine.evaluate(
        message="I am having a strange obscure glitch on an unsupported smartwatch OS",
        intent_name="Audio & Playback Issues",
        intent_confidence=0.80,
        evidence=[],
    )
    assert res.decision == "ESCALATE"
    assert any("evidence" in rf.lower() for rf in res.risk_factors)
