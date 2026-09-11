"""
Conversation Reconstruction & Splitting Script.

Extracts multi-turn support conversation pairs for the target brand from the full TWCS CSV.
Guarantees clean data separation:
- Train split (80%): Indexed in vector store & used for training intent classifier
- Dev split (10%): Used for tuning confidence thresholds & escalation hyperparameters
- Test split (10%): Reserved for evaluation
- Golden Set: Evaluated separately to ensure zero contamination / zero retrieval leakage.
"""
import re
import sys
import json
from pathlib import Path
import pandas as pd
import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

PROJECT_ROOT = Path(__file__).parent.parent
RAW_CSV = PROJECT_ROOT / "data" / "raw" / "twcs.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
CONFIG_FILE = PROJECT_ROOT / "config" / "config.yaml"


def normalize_id(val) -> str:
    """Normalize tweet ID to clean string without float decimals."""
    if pd.isna(val):
        return ""
    try:
        return str(int(float(val)))
    except (ValueError, TypeError):
        return str(val).strip()


def clean_text(text: str) -> str:
    """Clean tweet text while preserving support semantics."""
    if not isinstance(text, str):
        return ""
    # Remove leading handle mentions e.g. @SpotifyCares @105847
    cleaned = re.sub(r"^(@\w+\s*)+", "", text).strip()
    # Unescape HTML entities
    cleaned = cleaned.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    # Clean excessive whitespace
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def extract_brand_conversations(brand: str = "SpotifyCares", max_pairs: int = 10000, seed: int = 42):
    """
    Two-pass extraction:
    Pass 1: Find all brand outbound tweets and collect all requested inbound tweet IDs.
    Pass 2: Stream through TWCS to locate the corresponding customer messages.
    """
    print(f"[INFO] Pass 1: Scanning for {brand} outbound tweets in {RAW_CSV}...")
    brand_tweets = []
    needed_customer_ids = set()

    for chunk in pd.read_csv(
        RAW_CSV,
        chunksize=100000,
        dtype=str,
        on_bad_lines="skip",
    ):
        brand_subset = chunk[(chunk["inbound"] == "False") & (chunk["author_id"] == brand)]
        for _, row in brand_subset.iterrows():
            irt = row.get("in_response_to_tweet_id")
            if pd.notna(irt) and str(irt).strip():
                irt_clean = normalize_id(irt)
                if irt_clean:
                    brand_tweets.append({
                        "brand_tweet_id": normalize_id(row["tweet_id"]),
                        "customer_tweet_id": irt_clean,
                        "brand_response": clean_text(row.get("text", "")),
                        "brand_raw": row.get("text", ""),
                        "created_at": row.get("created_at", ""),
                        "brand": brand,
                    })
                    needed_customer_ids.add(irt_clean)

    print(f"[INFO] Found {len(brand_tweets):,} brand tweets referencing {len(needed_customer_ids):,} customer tweets.")

    print(f"[INFO] Pass 2: Retrieving customer parent tweets from {RAW_CSV}...")
    customer_tweets = {}

    for chunk in pd.read_csv(
        RAW_CSV,
        chunksize=100000,
        dtype=str,
        on_bad_lines="skip",
    ):
        chunk["clean_id"] = chunk["tweet_id"].apply(normalize_id)
        matched = chunk[chunk["clean_id"].isin(needed_customer_ids)]
        for _, row in matched.iterrows():
            cid = row["clean_id"]
            if cid not in customer_tweets:
                customer_tweets[cid] = {
                    "customer_message": clean_text(row.get("text", "")),
                    "customer_raw": row.get("text", ""),
                    "inbound": row.get("inbound", "True"),
                }

    print(f"[INFO] Successfully resolved {len(customer_tweets):,} parent customer tweets.")

    # Pair them together
    pairs = []
    for bt in brand_tweets:
        cid = bt["customer_tweet_id"]
        if cid in customer_tweets:
            cust = customer_tweets[cid]
            cust_msg = cust["customer_message"]
            brand_resp = bt["brand_response"]

            # Quality filters: ensure non-trivial text
            if len(cust_msg) >= 10 and len(brand_resp) >= 15:
                pairs.append({
                    "conversation_id": bt["brand_tweet_id"],
                    "customer_tweet_id": cid,
                    "brand_tweet_id": bt["brand_tweet_id"],
                    "customer_message": cust_msg,
                    "brand_response": brand_resp,
                    "customer_raw": cust["customer_raw"],
                    "brand_raw": bt["brand_raw"],
                    "created_at": bt["created_at"],
                    "brand": brand,
                })

    df = pd.DataFrame(pairs)
    print(f"[INFO] Formed {len(df):,} valid (customer, brand) conversation pairs.")

    if len(df) > max_pairs:
        df = df.sample(n=max_pairs, random_state=seed).reset_index(drop=True)
        print(f"[INFO] Sampled down to {len(df):,} pairs for rapid, reproducible training.")

    # Save full conversation dataset
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    full_csv = OUTPUT_DIR / "conversations.csv"
    df.to_csv(full_csv, index=False, encoding="utf-8")
    print(f"[INFO] Saved full conversation pairs to {full_csv}")

    # Create Train / Dev / Test splits (80% / 10% / 10%)
    rng = np.random.default_rng(seed)
    indices = np.arange(len(df))
    rng.shuffle(indices)

    n_train = int(0.80 * len(df))
    n_dev = int(0.10 * len(df))

    train_idx = indices[:n_train]
    dev_idx = indices[n_train:n_train + n_dev]
    test_idx = indices[n_train + n_dev:]

    train_df = df.iloc[train_idx].copy()
    dev_df = df.iloc[dev_idx].copy()
    test_df = df.iloc[test_idx].copy()

    train_df.to_csv(OUTPUT_DIR / "train.csv", index=False, encoding="utf-8")
    dev_df.to_csv(OUTPUT_DIR / "dev.csv", index=False, encoding="utf-8")
    test_df.to_csv(OUTPUT_DIR / "test.csv", index=False, encoding="utf-8")

    # Also save a sample for quick inspection
    samples_dir = PROJECT_ROOT / "data" / "samples"
    samples_dir.mkdir(parents=True, exist_ok=True)
    df.head(50).to_csv(samples_dir / "sample_conversations.csv", index=False, encoding="utf-8")

    print(f"[INFO] Dataset splits created:")
    print(f"       Train: {len(train_df):,} pairs (80%) -> used for index & classifier")
    print(f"       Dev:   {len(dev_df):,} pairs (10%)")
    print(f"       Test:  {len(test_df):,} pairs (10%)")

    # Update config.yaml to ensure brand is set to SpotifyCares
    config_text = CONFIG_FILE.read_text(encoding="utf-8")
    config_text = re.sub(r'^brand:.*$', f'brand: "{brand}"', config_text, flags=re.MULTILINE)
    config_text = re.sub(r'^brand_twitter_handle:.*$', f'brand_twitter_handle: "{brand}"', config_text, flags=re.MULTILINE)
    CONFIG_FILE.write_text(config_text, encoding="utf-8")

    return df


if __name__ == "__main__":
    extract_brand_conversations(brand="SpotifyCares", max_pairs=8000, seed=42)
