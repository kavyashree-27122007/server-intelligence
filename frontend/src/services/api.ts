import { AnalysisResult, EvaluationMetrics, IntentInfo, FailureMode, DecisionEntry } from '../types';

const API_BASE = typeof window !== 'undefined' && window.location.port === '5173'
  ? 'http://localhost:8000/api'
  : '/api';

export const api = {
  async analyze(message: string): Promise<AnalysisResult> {
    const res = await fetch(`${API_BASE}/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Analysis failed' }));
      throw new Error(err.detail || 'Failed to analyze message');
    }
    return res.json();
  },

  async getMetrics(): Promise<EvaluationMetrics> {
    const res = await fetch(`${API_BASE}/metrics`);
    if (!res.ok) throw new Error('Failed to fetch evaluation metrics');
    return res.json();
  },

  async getIntents(): Promise<{ brand: string; num_intents: number; intents: IntentInfo[] }> {
    const res = await fetch(`${API_BASE}/intents`);
    if (!res.ok) throw new Error('Failed to fetch intents');
    return res.json();
  },

  async getFailures(): Promise<FailureMode[]> {
    const res = await fetch(`${API_BASE}/failures`);
    if (!res.ok) throw new Error('Failed to fetch failure modes');
    return res.json();
  },

  async getDecisions(): Promise<DecisionEntry[]> {
    const res = await fetch(`${API_BASE}/decisions`);
    if (!res.ok) throw new Error('Failed to fetch decisions');
    return res.json();
  },

  async retrieve(query: string, top_k: number = 5) {
    const res = await fetch(`${API_BASE}/retrieve`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, top_k }),
    });
    if (!res.ok) throw new Error('Failed to retrieve evidence');
    return res.json();
  },

  async checkHealth() {
    const res = await fetch(`${API_BASE}/health`);
    return res.json();
  }
};
