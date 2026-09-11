# Engineering Decision Log: Support Intelligence Platform

A chronological, transparent record of 12 critical technical and architectural decisions made during the design, development, and evaluation of the **Support Intelligence** system.

---

### Decision 01 — Brand Selection (`SpotifyCares`)
- **Decision:** Selected `SpotifyCares` from among 108 brands in the Kaggle TWCS dataset, prioritizing actionable resolution density over raw volume alone.
- **Why:** While `AmazonHelp` had higher total volume (169k tweets), >85% of Amazon's tweets were repetitive redirects (*"Please contact us at amazon.com/help"*). In contrast, `SpotifyCares` (43,265 brand tweets) actively troubleshoots in-channel, providing technical steps (*"clear app cache"*, *"toggle hardware acceleration"*, *"re-pair bluetooth"*), making it far more suitable for evidence-grounded retrieval.
- **Trade-off:** Slightly lower total training examples (43k vs 169k), but drastically higher informational value per interaction.

---

### Decision 02 — Data-Derived 9-Intent Taxonomy (Avoiding Banking77)
- **Decision:** Created a tailored 9-intent taxonomy discovered empirically from Spotify's support stream rather than adopting existing generic taxonomies like Banking77.
- **Why:** Music streaming support involves domain-specific issues: local device caching, DRM licensing, offline device limits, and Bluetooth codecs. Generic banking or retail taxonomies cannot capture these mechanics.
- **Trade-off:** Required manual taxonomy design and inclusion/exclusion boundary definition rather than using off-the-shelf pre-annotated classification datasets.

---

### Decision 03 — Strict Train-Only Retrieval Indexing (Zero Contamination)
- **Decision:** The vector and lexical retrieval indices are built **exclusively on the 80% train split** (6,400 pairs). The 200 Golden evaluation examples are strictly held out.
- **Why:** In retrieval-augmented generation, indexing evaluation queries creates artificial 100% similarity hits (data leakage), completely invalidating groundedness evaluations.
- **Trade-off:** Retrieval recall on the test set reflects true generalization rather than memorization, resulting in honest ~97% Recall@5.

---

### Decision 04 — Dual-Pass Chunked Streaming for Conversation Reconstruction
- **Decision:** Implemented a two-pass streaming parser over the 492.6 MB raw CSV using chunks of 100,000 rows.
- **Why:** Loading 2.8 million multi-turn tweets into memory at once causes RAM spikes and crashed smaller developer environments. Pass 1 collects target brand outbound tweets; Pass 2 targets matching inbound IDs.
- **Trade-off:** Takes ~20 seconds to run, but keeps memory usage below 250 MB throughout preprocessing.

---

### Decision 05 — Normalization of Float-Parsed Tweet Identifiers
- **Decision:** Converted all `tweet_id` and `in_response_to_tweet_id` references via `str(int(float(x)))`.
- **Why:** Pandas interprets integer columns with `NaN` values as `float64`, converting ID `119239` into string `"119239.0"`, causing a silent 100% lookup mismatch when matching parent tweets.
- **Trade-off:** Slight parsing overhead during dataset cleaning, but eliminated silent thread dissociation bugs.

---

### Decision 06 — Hybrid Retrieval Architecture (Dense Semantic + Lexical Fallback)
- **Decision:** Built a two-stage hybrid retriever: primary dense normalized semantic embeddings + fallback TF-IDF lexical matching with brand and intent filtering.
- **Why:** Pure dense search occasionally misses exact technical error codes (e.g. `"Error code: 17"`), whereas pure keyword search fails on semantic paraphrases (*"song cuts off"* vs *"playback pauses"*).
- **Trade-off:** Requires maintaining both indices in memory, adding ~15 MB storage footprint.

---

### Decision 07 — Multi-Factor Linear Risk Model for Escalation
- **Decision:** Formulated escalation risk as a weighted sum of intent uncertainty (25%), retrieval weakness (25%), evidence sparsity (15%), sensitive domain triggers (25%), and message brevity (10%), backed by mandatory critical veto rules.
- **Why:** Binary classification or single-threshold confidence models fail when a customer is confident but legally threatening, or calm but reporting a double billing debit.
- **Trade-off:** Requires tuning 5 hyperparameter weights rather than a single cutoff score.

---

### Decision 08 — Critical Hard Escalation Triggers (Zero LLM Discretion)
- **Decision:** Implemented deterministic regex hard-triggers for litigation threats, account breaches, and self-harm that bypass LLM generation and force immediate `ESCALATE`.
- **Why:** LLMs frequently attempt to placate angry users or give generic advice during legal threats, creating brand liability. Critical risks require deterministic human escalation.
- **Trade-off:** Zero tolerance for nuance on trigger words (e.g., mentioning "lawyer" in a joke still triggers escalation), but ensures absolute compliance safety.

---

### Decision 09 — Stratified 200-Example Golden Benchmark
- **Decision:** Hand-curated exactly 200 golden test cases stratified across all 9 intents, with 3 calibrated difficulty levels (40% Easy, 35% Medium, 25% Hard) and 35% escalation cases.
- **Why:** Random sampling from Twitter produces >50% trivial greetings ("hey", "thanks"), resulting in inflated, uninformative evaluation scores.
- **Trade-off:** Manual curation requires substantial domain research and annotator time, but produces a trustworthy benchmark.

---

### Decision 10 — Provider Abstraction with Offline Fallback
- **Decision:** Implemented `LLMProvider` with Gemini, OpenAI, and a deterministic `EvidenceSynthesisProvider` fallback.
- **Why:** Prevents the entire evaluation harness or API server from failing if an external API key is missing or rate-limited.
- **Trade-off:** Requires writing and maintaining synthesis templates for zero-API execution.

---

### Decision 11 — Validation of LLM-as-Judge via Human Agreement
- **Decision:** Conducted a formal human-vs-judge agreement study on 30 validation interactions, calculating Pearson correlation ($r=0.72$), Spearman rank ($\rho=0.71$), and absolute MAE.
- **Why:** Blindly reporting LLM-as-judge scores without human calibration is circular and scientifically ungrounded.
- **Trade-off:** Human evaluation required additional annotation effort, but validated that the judge's scoring rubric aligns with human judgment.

---

### Decision 12 — Editorial "Warm White & Beige" Design System
- **Decision:** Styled the frontend using a refined editorial palette (`#FAF8F3` warm background, `#E8DDCC` soft beige, `#26231F` deep slate text) rather than generic dark-mode cyberpunk neon aesthetics.
- **Why:** The tool is designed as serious customer support decision infrastructure for enterprise support leadership and evaluators, requiring clarity, readability, and visual calm.
- **Trade-off:** Demanded custom Tailwind color tokens and restrained CSS styling rather than default template libraries.
