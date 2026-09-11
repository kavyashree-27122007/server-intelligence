export interface IntentResult {
  name: string;
  intent_id: string;
  confidence: number;
  all_scores: Record<string, number>;
}

export interface EvidenceItem {
  customer_message: string;
  brand_response: string;
  conversation_id?: string;
  similarity: number;
  timestamp?: string;
  retrieval_method: string;
}

export interface AnalysisResult {
  message: string;
  intent: IntentResult;
  evidence: EvidenceItem[];
  draft_reply: string;
  decision: "AUTO_HANDLE" | "ESCALATE";
  decision_confidence: number;
  reason: string;
  risk_factors: string[];
  request_id: string;
  latency_ms: number;
}

export interface IntentInfo {
  intent_id: string;
  intent_name: string;
  description: string;
  inclusion_criteria: string;
  exclusion_criteria: string;
  examples: string[];
  precision?: number;
  recall?: number;
  f1?: number;
  support?: number;
}

export interface EvaluationMetrics {
  metrics: Record<string, {
    "Majority Baseline": number;
    "TF-IDF Baseline": number;
    "AI Agent": number;
  }>;
  per_intent: Array<{
    intent_name: string;
    precision: number;
    recall: number;
    f1: number;
    support: number;
  }>;
  escalation_details: {
    accuracy: number;
    precision: number;
    recall: number;
    f1: number;
  };
  judge_agreement: {
    validation_sample_size: number;
    pearson_correlation: number;
    spearman_correlation: number;
    score_agreement_pct_within_half_point: number;
    mean_absolute_error: number;
  };
  sample_size: number;
  brand: string;
}

export interface FailureMode {
  rank: number;
  category: string;
  example_message: string;
  expected_behavior: string;
  actual_behavior: string;
  why_failed: string;
  hypothesis: string;
  potential_fix: string;
}

export interface DecisionEntry {
  decision_id: string;
  title: string;
  decision: string;
  why: string;
  tradeoff: string;
}
