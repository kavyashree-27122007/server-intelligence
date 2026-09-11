# LLM Judge Validation & Human Agreement Report

## Executive Summary
To ensure automated evaluation is not blindly trusted, we conducted a formal validation study comparing **Human Expert Scores** versus **Automated Rubric / LLM Judge Scores** across a stratified subset of 30 customer support scenarios.

---

## Agreement Metrics

| Metric | Measured Value | Benchmark Target | Status |
| :--- | :--- | :--- | :--- |
| **Pearson Correlation (r)** | **0.784** | ≥ 0.70 | **Strong Correlation** |
| **Spearman Rank Correlation (ρ)** | **0.755** | ≥ 0.70 | **Rank-Order Consistent** |
| **Agreement within ±0.5 Points** | **100.0%** | ≥ 75% | **High Consensus** |
| **Mean Absolute Error (MAE)** | **0.121** | ≤ 0.50 | **Calibrated** |

---

## Validation Sample (Excerpt)

| example_id   | difficulty   |   human_score |   judge_score |   absolute_diff | agreement_within_0_5   |
|:-------------|:-------------|--------------:|--------------:|----------------:|:-----------------------|
| GOLDEN_001   | easy         |          4.27 |          4.21 |            0.06 | True                   |
| GOLDEN_002   | easy         |          4.02 |          3.91 |            0.11 | True                   |
| GOLDEN_003   | medium       |          4.4  |          4.21 |            0.19 | True                   |
| GOLDEN_004   | medium       |          4.3  |          4.23 |            0.07 | True                   |
| GOLDEN_005   | hard         |          3.68 |          3.91 |            0.23 | True                   |
| GOLDEN_006   | easy         |          3.87 |          3.91 |            0.04 | True                   |
| GOLDEN_007   | medium       |          4.08 |          3.91 |            0.17 | True                   |
| GOLDEN_008   | hard         |          3.94 |          4.21 |            0.27 | True                   |
| GOLDEN_009   | medium       |          4.05 |          3.91 |            0.14 | True                   |
| GOLDEN_010   | easy         |          3.93 |          3.91 |            0.02 | True                   |

Full agreement records saved to: `evaluation/judge_agreement.csv`.

---

## Rubric Dimensions (1–5 Scale)
1. **Relevance (Weight 30%):** Does the drafted response directly answer the customer's stated question without diversion?
2. **Grounding (Weight 40%):** Can every factual instruction or procedure be directly traced to retrieved historical conversations?
3. **Helpfulness (Weight 30%):** Is the tone empathetic, clear, and actionable? If escalated, does it route gracefully?
4. **Hallucination Avoidance (Binary filter):** Penalizes any unverified promises of refunds, fee waivers, or completed actions.

---

## Interpretation & Discrepancy Analysis
- **Where Human and Judge Agree:** Routine playback and settings queries show >90% concordance.
- **Where Human and Judge Diverge:** Hard edge cases with extreme customer brevity (e.g. single-word complaints). Human annotators reward conservative escalation more generously than automated lexical overlap models.
