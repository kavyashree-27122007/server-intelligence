"""
Pydantic models / schemas for the Support Intelligence API.
"""
from __future__ import annotations
from typing import List, Optional, Literal
from pydantic import BaseModel, Field


# ── Request Models ──────────────────────────────────────────────────────────

class AnalyzeRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000, description="Customer support message")
    context: Optional[str] = Field(None, max_length=2000, description="Optional prior conversation context")


class ClassifyRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)


class RetrieveRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    intent: Optional[str] = None
    top_k: int = Field(5, ge=1, le=20)


class GenerateRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    intent: str
    intent_confidence: float
    evidence: List["EvidenceItem"]


class EscalationRequest(BaseModel):
    message: str
    intent: str
    intent_confidence: float
    retrieval_similarity: float
    evidence_count: int


# ── Response Models ──────────────────────────────────────────────────────────

class IntentResult(BaseModel):
    name: str
    intent_id: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    all_scores: dict[str, float] = Field(default_factory=dict)


class EvidenceItem(BaseModel):
    customer_message: str
    brand_response: str
    conversation_id: Optional[str] = None
    similarity: float = Field(..., ge=0.0, le=1.0)
    timestamp: Optional[str] = None
    retrieval_method: str = "semantic"  # semantic | lexical


class EscalationResult(BaseModel):
    decision: Literal["AUTO_HANDLE", "ESCALATE"]
    confidence: float = Field(..., ge=0.0, le=1.0)
    reason: str
    risk_factors: List[str] = Field(default_factory=list)
    risk_score: float = Field(..., ge=0.0, le=1.0)


class AnalysisResult(BaseModel):
    message: str
    intent: IntentResult
    evidence: List[EvidenceItem]
    draft_reply: str
    decision: Literal["AUTO_HANDLE", "ESCALATE"]
    decision_confidence: float
    reason: str
    risk_factors: List[str]
    request_id: str
    latency_ms: float


class IntentInfo(BaseModel):
    intent_id: str
    intent_name: str
    description: str
    examples: List[str]
    example_count: int
    precision: Optional[float] = None
    recall: Optional[float] = None
    f1: Optional[float] = None


class MetricsResponse(BaseModel):
    brand: str
    dataset_total_rows: int
    brand_sample_size: int
    num_intents: int
    intent_macro_f1: Optional[float] = None
    escalation_f1: Optional[float] = None
    retrieval_recall_at_5: Optional[float] = None
    response_grounding: Optional[float] = None
    response_helpfulness: Optional[float] = None
    hallucination_rate: Optional[float] = None
    evaluation_status: str = "pending"


class FailureMode(BaseModel):
    rank: int
    category: str
    example_message: str
    expected_behavior: str
    actual_behavior: str
    why_failed: str
    hypothesis: str
    potential_fix: str


class DecisionEntry(BaseModel):
    decision_id: str
    title: str
    decision: str
    why: str
    tradeoff: str


class HealthResponse(BaseModel):
    status: str
    brand: str
    retrieval_ready: bool
    classifier_ready: bool
    llm_provider: str
    llm_available: bool
