"""
Training and Indexing Pipeline for Support Intelligence.

Executes:
1. Intent labeling / pseudo-label discovery on train split using taxonomy keywords & heuristics
2. Training Production Intent Classifier (TF-IDF + Calibrated Logistic Regression)
3. Training Baseline 1 (Majority Class Intent Classifier)
4. Building Vector & Lexical Retrieval Index on TRAIN split ONLY (zero data leakage)
5. Saving artifacts to data/index/
"""
import json
import re
import sys
from pathlib import Path
import pandas as pd
import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.classification.classifier import TfidfIntentClassifier, MajorityBaselineClassifier
from app.retrieval.retriever import HybridSupportRetriever
from app.core.logging import logger

DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"
INDEX_DIR = DATA_DIR / "index"
TAXONOMY_FILE = DATA_DIR / "intent_taxonomy.json"


# Intent heuristic keyword rules based on the 9 discovered taxonomy intents
INTENT_RULES = [
    ("Subscription & Billing", [
        r"\b(charg(e|ed|ing)|bill(ing|ed)?|refund|payment|credit card|debit|paypal|cancel|subscri(be|ption)|price|cost|overcharg)\b",
        r"\b(\$|£|€|receipt|invoice|student discount|sheerid)\b",
    ]),
    ("Audio & Playback Issues", [
        r"\b(paus(e|ing|ed)|skip(ping|ped)?|play(back|ing)?|stop(ping|ped)?|stutter|buffer|sound|volume|distort|audio|loud|quiet)\b",
        r"\b(crash(es|ed|ing)?|freeze|won't play|can't play|error code|glitch|blank screen)\b",
    ]),
    ("Account Access & Login", [
        r"\b(log(in|ged|ging)?|sign(in|ned|ning)?|password|username|email|account|reset|hacked|stolen|unauthoriz|locked out|2fa|otp)\b",
        r"\b(authenticat|credential|unlink|facebook login|forgot)\b",
    ]),
    ("Offline Listening & Downloads", [
        r"\b(download(s|ed|ing)?|offline|airplane mode|storage|sd card|device limit|save offline|no internet|greyed out)\b",
    ]),
    ("Playlist & Library Management", [
        r"\b(playlist(s)?|library|liked songs|favourite(s)?|collaborat(e|ive)?|recover|disappear(ed)?|folder|sort(ing)?|cover art)\b",
    ]),
    ("Device & Connectivity Integration", [
        r"\b(connect|bluetooth|speaker(s)?|sonos|alexa|echo|carplay|android auto|watch|tv|playstation|ps4|xbox|chromecast|waze)\b",
    ]),
    ("Catalog & Content Inquiries", [
        r"\b(song|album|artist|track|lyric(s)?|explicit|censor|remov(ed)?|availab(le|ility)?|missing|single|release|podcast|episode)\b",
    ]),
    ("Family & Duo Administration", [
        r"\b(family|duo|address|member(s)?|invite|invitation|reside|parental|sub[- ]account|home address)\b",
    ]),
]


def assign_intent(text: str) -> str:
    """Classify text using taxonomy rules with fallback to General Inquiries."""
    text_lower = text.lower()
    scores = {}
    for intent_name, patterns in INTENT_RULES:
        count = 0
        for pat in patterns:
            matches = re.findall(pat, text_lower)
            count += len(matches)
        if count > 0:
            scores[intent_name] = count

    if scores:
        best_intent = max(scores.items(), key=lambda x: x[1])[0]
        return best_intent
    return "General Inquiries & Feedback"


def train_models():
    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    train_path = PROCESSED_DIR / "train.csv"
    if not train_path.exists():
        print(f"[ERROR] Train split not found at {train_path}. Run build_conversations.py first.")
        sys.exit(1)

    print(f"[INFO] Loading train data from {train_path}...")
    train_df = pd.read_csv(train_path)
    print(f"[INFO] Loaded {len(train_df):,} training examples.")

    # Assign taxonomy labels
    print("[INFO] Applying intent taxonomy rules to training data...")
    train_df["intent"] = train_df["customer_message"].apply(assign_intent)
    print("\nIntent Distribution in Training Data:")
    print(train_df["intent"].value_counts().to_string())

    # Load taxonomy definition
    taxonomy = {}
    if TAXONOMY_FILE.exists():
        with open(TAXONOMY_FILE, "r", encoding="utf-8") as f:
            tax_json = json.load(f)
            taxonomy = {item["intent_id"]: item for item in tax_json.get("intents", [])}

    # 1. Train Production Intent Classifier
    print("\n[INFO] Training Production Intent Classifier (TF-IDF + Calibrated Logistic Regression)...")
    clf = TfidfIntentClassifier(c_param=2.0)
    clf.set_taxonomy(taxonomy)
    clf.fit(train_df["customer_message"].tolist(), train_df["intent"].tolist())
    clf.save(INDEX_DIR / "classifier.joblib")
    print(f"[SUCCESS] Saved Production Classifier to {INDEX_DIR / 'classifier.joblib'}")

    # 2. Train Majority Baseline Classifier
    print("[INFO] Training Baseline 1 (Majority Class Classifier)...")
    majority_clf = MajorityBaselineClassifier()
    majority_clf.fit(train_df["customer_message"].tolist(), train_df["intent"].tolist())
    import joblib
    joblib.dump(majority_clf, INDEX_DIR / "majority_classifier.joblib")
    print(f"[SUCCESS] Saved Majority Classifier (Class: '{majority_clf.majority_intent}')")

    # 3. Build Retrieval Index (TRAIN SPLIT ONLY - Zero Data Leakage)
    print(f"\n[INFO] Indexing {len(train_df):,} records for Vector & Lexical Retrieval...")
    records = train_df.to_dict(orient="records")
    retriever = HybridSupportRetriever()
    retriever.fit(records)
    retriever.save(INDEX_DIR)
    print(f"[SUCCESS] Saved Semantic & Lexical Indices to {INDEX_DIR}")

    # Save intent label mapping for reference
    label_stats = train_df["intent"].value_counts().to_dict()
    with open(INDEX_DIR / "label_stats.json", "w", encoding="utf-8") as f:
        json.dump(label_stats, f, indent=2)

    print("\n✅ Training and Indexing complete! Artifacts ready in data/index/")


if __name__ == "__main__":
    train_models()
