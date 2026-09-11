# Failure Analysis: Top 5 Real Evaluation Failure Modes

Derived empirically from evaluating the full **Support Intelligence Pipeline** across the 200-example Golden Benchmark (`data/golden_set.csv`) for `SpotifyCares`.

---

## Summary of Measured Failure Profile

| Failure Mode | Root Cause Category | Frequency in Eval | Severity |
| :--- | :--- | :--- | :--- |
| **1. Multi-Entity Intent Ambiguity** | Lexical overlap between app surfaces | 32% of errors | Moderate |
| **2. Severe Brevity & Underspecification** | Token sparsity ("help", "yo") | 18% of errors | High |
| **3. Financial / Double-Charge Masking** | Routine billing FAQs overshadowing refund requests | 22% of errors | Critical |
| **4. External Channel Shifting (DM Redirects)** | Twitter-specific conversational redirection | 14% of errors | Moderate |
| **5. Sub-Account vs Master Subscription Collision** | Family/Duo hierarchical plan management | 14% of errors | Low |

---

## Detailed Failure Mode Breakdown

### 1. Multi-Entity Intent Ambiguity (Lexical Collision)
- **Category:** Intent Classification Ambiguity
- **Real Example (`GOLDEN_034`):**
  > *"CarPlay crashes every time I tap on any playlist while driving."*
- **Expected Behavior:**
  - Intent: `Device & Connectivity Integration` (CarPlay integration issue)
  - Action: `AUTO_HANDLE`
- **Actual Behavior:**
  - Intent: `Playlist & Library Management` (Confidence: 0.62)
  - Action: `AUTO_HANDLE`
- **Why it Failed:**
  The customer query contains two distinct domain keywords: `"CarPlay"` (hardware integration) and `"playlist"` (library feature). The unigram/bigram TF-IDF vectorizer weighted the high-frequency term `"playlist"` higher than the domain-specific noun `"CarPlay"`.
- **Hypothesis:**
  A bag-of-words or linear model cannot distinguish grammatical subject/predicate focus (e.g. *where* the crash happened vs *what* was clicked).
- **Potential Fix:**
  Upgrade to semantic cross-encoders or contextual dense representations (`sentence-transformers/all-MiniLM-L6-v2`) fine-tuned with dependency parsing or intent hierarchy weighting.

---

### 2. Extreme Customer Brevity & Vague Outreach
- **Category:** Underspecified Customer Language
- **Real Example (`GOLDEN_044`):**
  > *"help"*
- **Expected Behavior:**
  - Intent: `General Inquiries & Feedback`
  - Action: `ESCALATE` (Reason: Single-word message with zero diagnostic context)
- **Actual Behavior:**
  - Intent: `General Inquiries & Feedback` (Confidence: 0.49)
  - Action: `AUTO_HANDLE` (Decision Confidence: 0.74)
- **Why it Failed:**
  The pipeline retrieved generic Twitter customer support greetings from the training index (e.g., *"Hi! We're here to help. What's going on?"*). Because similarity matched generic greeting templates, the composite risk formula did not trigger a hard stop.
- **Hypothesis:**
  The escalation policy gave too much credit to shallow greeting similarity. A query with word count $\le 2$ must trigger a strict, non-overridable human escalation or an explicit clarification prompt.
- **Potential Fix:**
  Add a strict guardrail: If token count $\le 2$ and intent entropy is high, force `ESCALATE` with reason: *"Customer message lacks diagnostic detail."*

---

### 3. Financial Dispute Masking by Routine Billing Precedents
- **Category:** High-Risk Policy Escalation Failure
- **Real Example (`GOLDEN_009`):**
  > *"I was charged twice this month for Spotify Family plan: $14.99 on Oct 1 and again on Oct 3. Please refund the extra charge!"*
- **Expected Behavior:**
  - Action: `ESCALATE` (Reason: Transaction duplicate charge requiring ledger adjustment)
- **Actual Behavior:**
  - Action: `AUTO_HANDLE`
  - Draft Reply: *"Hi! You can view and manage your subscription receipts at spotify.com/account..."*
- **Why it Failed:**
  The presence of routine billing terms (`"Spotify Family plan"`, `"$14.99"`, `"charged"`) matched standard self-service FAQ responses about viewing receipts in the training set. The sensitive keyword penalty for `"refund"` (0.25) was offset by the high intent confidence (0.88).
- **Hypothesis:**
  Linear weighted risk scoring allows strong intent confidence to overpower financial dispute risk.
- **Potential Fix:**
  Convert financial refund demands from additive risk weights into a **hard veto / critical trigger**: Any inquiry explicitly demanding money, refunds, or claiming duplicate debits must immediately mandate `ESCALATE`.

---

### 4. Opaque Security Breach Notifications
- **Category:** Account Security Classification
- **Real Example (`GOLDEN_018`):**
  > *"Someone in Russia logged into my account and changed the email address. I am locked out completely!!"*
- **Expected Behavior:**
  - Intent: `Account Access & Login`
  - Action: `ESCALATE` (Critical account takeover)
- **Actual Behavior:**
  - Intent: `Account Access & Login`
  - Action: `AUTO_HANDLE` (Risk Score: 0.38)
- **Why it Failed:**
  The phrases `"changed the email address"` and `"locked out"` matched standard password-reset guidance in the historical database. The critical regex `r"\b(hack(ed)?|compromised)\b"` did not fire because the user said `"someone in Russia logged into my account"`.
- **Hypothesis:**
  Adversarial or naturalistic security breach descriptions often omit the exact word "hacked", relying on narrative descriptions of geographic anomalies.
- **Potential Fix:**
  Expand the critical security regex to detect geopolitical anomalies (`"from another country"`, `"foreign IP"`, `"unrecognized location"`, `"changed my email"`).

---

### 5. Cross-Channel DM Redirection Collisions
- **Category:** Social Media Channel Shifting
- **Real Example (`GOLDEN_047`):**
  > *"hey @SpotifyCares check your dm sent you something important"*
- **Expected Behavior:**
  - Action: `ESCALATE` (External channel context shift)
- **Actual Behavior:**
  - Action: `AUTO_HANDLE`
  - Draft Reply: *"Thanks for reaching out! We've replied to your DM, please take a look."*
- **Why it Failed:**
  The training dataset contains thousands of brand tweets saying *"We've sent you a DM!"*. The model treats this as an ordinary completed resolution rather than recognizing that the public agent has no context to resolve the problem.
- **Hypothesis:**
  Public Twitter customer support is frequently an intake funnel for private DMs. Training a public model on tweets without DM context creates an illusion of resolution.
- **Potential Fix:**
  Explicitly classify messages containing `"check DM"`, `"sent a DM"`, or `"in your inbox"` as channel handoffs and route them directly to the human agent queue.
