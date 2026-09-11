# Golden Evaluation Dataset Documentation

## Overview
- **Total Examples:** 200
- **Target Brand:** `SpotifyCares`
- **Source:** Historical TWCS support interactions & representative customer inquiries
- **Format:** `data/golden_set.csv`
- **Data Leakage Safeguard:** Strictly excluded from the retrieval train index. Evaluated in zero-shot fashion.

---

## Class Distribution Across Discovered Intents

| Discovered Intent | Count | Percentage |
| :--- | :--- | :--- |
| Audio & Playback Issues | 35 | 17.5% |
| Subscription & Billing | 30 | 15.0% |
| Account Access & Login | 22 | 11.0% |
| Playlist & Library Management | 22 | 11.0% |
| General Inquiries & Feedback | 20 | 10.0% |
| Device & Connectivity Integration | 19 | 9.5% |
| Family & Duo Administration | 18 | 9.0% |
| Offline Listening & Downloads | 17 | 8.5% |
| Catalog & Content Inquiries | 17 | 8.5% |

---

## Action & Escalation Distribution

| Action | Count | Percentage | Description |
| :--- | :--- | :--- | :--- |
| **AUTO_HANDLE** | 161 | 80.5% | Routine technical guidance, self-service FAQs, or standard procedures. |
| **ESCALATE** | 39 | 19.5% | Financial refunds, security breaches, legal threats, or high ambiguity. |

---

## Difficulty Breakdown

| Difficulty | Count | Percentage | Characteristics |
| :--- | :--- | :--- | :--- |
| **Easy** | 106 | 53.0% | Clear intent keywords, unambiguous phrasing, standard resolution. |
| **Medium** | 59 | 29.5% | Multi-clause inquiries, subtle hardware/platform conditions. |
| **Hard** | 35 | 17.5% | Extreme brevity ("help"), hostile sentiment, security/safety emergencies. |

---

## Annotation Methodology & Rubric
1. **Intent Grounding:** Each example is mapped to one of the 9 taxonomy intents defined in `intent_taxonomy.json`.
2. **Escalation Grounding:** An interaction MUST be marked `ESCALATE` if:
   - It demands monetary refunds or compensation.
   - It alleges account security compromises (hacking, stolen credentials).
   - It involves legal, safety, or regulatory threats.
   - The customer message is severely underspecified (e.g. "yo", "help") such that guessing risks hallucination.
3. **Guidance Specifications:** Concise, authoritative instructions detailing how a human support specialist would resolve the issue.
