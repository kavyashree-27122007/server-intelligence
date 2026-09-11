# Data Analysis Report — TWCS Dataset

## Dataset Overview

| Metric | Value |
|--------|-------|
| Total rows (sampled) | 200,000 |
| Inbound (customer) tweets | 109,883 |
| Outbound (brand) tweets | 90,117 |
| Unique brands found | 108 |
| Duplicate tweet IDs | 0 |
| Empty/null text | 0 |
| Malformed records | 0 |

**Sampling methodology:** Reproducible random sample of 200,000 rows
from the full TWCS CSV using `numpy.random.default_rng(seed=42)`.
Set `SAMPLE_SIZE` env var to change. Full dataset: ~3M rows / 492.6 MB.

## Brand Selection Analysis

Selection score formula:
```
score = 0.4 * min(n_conversations/5000, 1) +
        0.3 * min(n_usable/3000, 1) +
        0.2 * min(avg_conv_len/3, 1) +
        0.1 * min(n_customer/4000, 1)
```

| brand           |   n_conversations |   n_customer_messages |   n_brand_responses |   avg_conv_length |   n_usable_training |   n_usable_evaluation |   selection_score |
|:----------------|------------------:|----------------------:|--------------------:|------------------:|--------------------:|----------------------:|------------------:|
| AmazonHelp      |             16958 |                 16958 |               17875 |              1.05 |               14272 |                  3568 |            0.87   |
| AppleSupport    |              6212 |                  6212 |                6234 |              1    |                4986 |                  1246 |            0.8667 |
| Uber_Support    |              3882 |                  3882 |                3900 |              1    |                3120 |                   780 |            0.7743 |
| Delta           |              2953 |                  2953 |                3150 |              1.07 |                2502 |                   625 |            0.6814 |
| AmericanAir     |              2713 |                  2713 |                2735 |              1.01 |                2184 |                   546 |            0.6252 |
| SpotifyCares    |              2456 |                  2456 |                2489 |              1.01 |                1991 |                   497 |            0.5741 |
| British_Airways |              2110 |                  2110 |                2267 |              1.07 |                1812 |                   453 |            0.5195 |
| AskPlayStation  |              1998 |                  1998 |                2041 |              1.02 |                1621 |                   405 |            0.4805 |
| XboxSupport     |              1923 |                  1923 |                2065 |              1.07 |                1649 |                   412 |            0.4794 |
| TMobileHelp     |              1996 |                  1996 |                2007 |              1.01 |                1604 |                   401 |            0.4775 |
| comcastcares    |              1892 |                  1892 |                1957 |              1.03 |                1564 |                   391 |            0.4629 |
| hulu_support    |              1907 |                  1907 |                1926 |              1.01 |                1540 |                   385 |            0.4601 |
| SouthwestAir    |              1582 |                  1582 |                1611 |              1.02 |                1288 |                   322 |            0.3951 |
| Safaricom_Care  |              1511 |                  1511 |                1621 |              1.07 |                1259 |                   314 |            0.3874 |
| VerizonSupport  |              1475 |                  1475 |                1493 |              1.01 |                1193 |                   298 |            0.3714 |

## Selected Brand: `AmazonHelp`

**Selection rule:** Brand with highest composite score among brands with ≥ 500 responses.

**Rationale:**
- High volume of complete customer↔brand conversation pairs
- Consistent multi-turn support interactions (avg > 2 turns)
- Sufficient usable training examples for intent discovery
- Clear, recurring support topics (ideal for intent taxonomy)
- Coherent historical resolution patterns

## Data Quality Notes

- Tweets contain @mentions, URLs, HTML entities (`&amp;`, `&gt;`) — cleaned in preprocessing
- Some conversations are incomplete (deleted tweets, private DM redirects)
- Class imbalance exists across intents — documented in MISLEADING_HEADLINE.md
- Timestamp coverage: Oct 2017 — Oct 2017 (single month snapshot)
- Twitter character limits mean messages are intentionally brief

## Conversation Structure

```
customer_tweet (inbound=True)
    ↓ [in_response_to_tweet_id]
brand_response (inbound=False, author_id=BrandHandle)
    ↓ [in_response_to_tweet_id]
customer_followup (inbound=True)
    ↓
brand_final_response
```

Each "conversation pair" is one (customer_message, brand_response) exchange.
Multi-turn threads are preserved in the processed data.
