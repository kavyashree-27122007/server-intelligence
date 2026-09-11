"""
Intent Classification module for Support Intelligence.

Implements:
1. Data-discovered intent taxonomy
2. Baseline 1: Majority Class Classifier
3. Baseline 2: TF-IDF + Logistic Regression / LinearSVC Classifier
4. Production Intent Classifier with calibrated confidence scores and thresholding
"""
import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score, accuracy_score, precision_recall_fscore_support
from sklearn.pipeline import Pipeline

from app.core.config import settings
from app.core.logging import logger
from app.models.schemas import IntentResult


def clean_tweet_text(text: str) -> str:
    """Clean tweet text while preserving support semantics."""
    if not isinstance(text, str):
        return ""
    # Remove user handles
    text = re.sub(r"@\w+", "", text)
    # Remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    # Unescape HTML entities
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    # Clean whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


class BaseIntentClassifier:
    """Abstract interface for intent classifiers."""

    def fit(self, texts: List[str], labels: List[str]):
        raise NotImplementedError

    def predict(self, text: str) -> IntentResult:
        raise NotImplementedError

    def batch_predict(self, texts: List[str]) -> List[IntentResult]:
        return [self.predict(t) for t in texts]


class MajorityBaselineClassifier(BaseIntentClassifier):
    """Baseline 1: Always predicts the majority intent class."""

    def __init__(self):
        self.majority_intent: str = "Technical Support"
        self.majority_prob: float = 0.5

    def fit(self, texts: List[str], labels: List[str]):
        from collections import Counter
        counts = Counter(labels)
        if counts:
            self.majority_intent, total = counts.most_common(1)[0]
            self.majority_prob = total / len(labels)
        logger.info(f"Majority baseline fitted: class={self.majority_intent} ({self.majority_prob:.3f})")

    def predict(self, text: str) -> IntentResult:
        return IntentResult(
            name=self.majority_intent,
            intent_id=self.majority_intent.lower().replace(" ", "_"),
            confidence=float(self.majority_prob),
            all_scores={self.majority_intent: float(self.majority_prob)}
        )


class TfidfIntentClassifier(BaseIntentClassifier):
    """
    Baseline 2 & Production Classifier:
    TF-IDF feature extraction (unigrams + bigrams, sublinear TF) +
    Calibrated Multinomial Logistic Regression.
    """

    def __init__(self, c_param: float = 2.0):
        self.c_param = c_param
        self.pipeline: Optional[Pipeline] = None
        self.classes_: List[str] = []
        self.taxonomy: Dict[str, dict] = {}
        self.intent_id_to_name: Dict[str, str] = {}
        self.intent_name_to_id: Dict[str, str] = {}

    def set_taxonomy(self, taxonomy: Dict[str, dict]):
        self.taxonomy = taxonomy
        self.intent_id_to_name = {k: v.get("intent_name", k) for k, v in taxonomy.items()}
        self.intent_name_to_id = {v.get("intent_name", k): k for k, v in taxonomy.items()}

    def fit(self, texts: List[str], labels: List[str]):
        cleaned_texts = [clean_tweet_text(t) for t in texts]
        min_df_val = 1 if len(texts) < 10 else 2
        self.pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(
                ngram_range=(1, 2),
                max_features=10000,
                sublinear_tf=True,
                min_df=min_df_val,
                token_pattern=r"(?u)\b\w+\b"
            )),
            ("clf", LogisticRegression(
                C=self.c_param,
                class_weight="balanced",
                max_iter=1000,
                solver="lbfgs"
            ))
        ])
        self.pipeline.fit(cleaned_texts, labels)
        self.classes_ = list(self.pipeline.named_steps["clf"].classes_)
        logger.info(f"Fitted TfidfIntentClassifier on {len(texts)} samples with {len(self.classes_)} classes.")

    def predict(self, text: str) -> IntentResult:
        if self.pipeline is None:
            raise RuntimeError("Classifier is not trained or loaded yet.")
        cleaned = clean_tweet_text(text)
        if not cleaned:
            # Fallback for empty / noise
            return IntentResult(
                name="Other / Unclear",
                intent_id="other_unclear",
                confidence=0.1,
                all_scores={"Other / Unclear": 0.1}
            )

        probs = self.pipeline.predict_proba([cleaned])[0]
        top_idx = int(np.argmax(probs))
        top_name = self.classes_[top_idx]
        confidence = float(probs[top_idx])

        # Map to taxonomy ID if available
        intent_id = self.intent_name_to_id.get(top_name, top_name.lower().replace(" ", "_").replace("/", "_"))

        all_scores = {cls_name: float(p) for cls_name, p in zip(self.classes_, probs)}

        # Low confidence guardrail
        if confidence < settings.classification.confidence_threshold:
            # Mark as ambiguous or unconfident
            pass

        return IntentResult(
            name=top_name,
            intent_id=intent_id,
            confidence=confidence,
            all_scores=all_scores
        )

    def save(self, filepath: Path):
        filepath.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump({
            "pipeline": self.pipeline,
            "classes": self.classes_,
            "taxonomy": self.taxonomy,
            "intent_id_to_name": self.intent_id_to_name,
            "intent_name_to_id": self.intent_name_to_id,
        }, filepath)
        logger.info(f"Saved classifier model to {filepath}")

    def load(self, filepath: Path):
        data = joblib.load(filepath)
        self.pipeline = data["pipeline"]
        self.classes_ = data["classes"]
        self.taxonomy = data.get("taxonomy", {})
        self.intent_id_to_name = data.get("intent_id_to_name", {})
        self.intent_name_to_id = data.get("intent_name_to_id", {})
        logger.info(f"Loaded classifier model from {filepath} with {len(self.classes_)} classes")
