"""
Retrieval System for Support Intelligence.

Provides:
1. Lexical Retrieval Baseline (TF-IDF Vector Space Model + Cosine Similarity)
2. Semantic Dense Retrieval (Embeddings + Vector Index with Metadata Filtering)
3. Hybrid Retrieval with Intent Filtering and Fallbacks
"""
import os
import json
import pickle
from pathlib import Path
from typing import List, Optional, Dict, Any

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.core.config import settings
from app.core.logging import logger
from app.models.schemas import EvidenceItem


class LexicalRetriever:
    """
    TF-IDF Vector Space Model Baseline for lexical matching.
    Calculates cosine similarity over customer support turns.
    """

    def __init__(self):
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.doc_vectors = None
        self.records: List[Dict[str, Any]] = []

    def fit(self, records: List[Dict[str, Any]]):
        """Fit TF-IDF on customer messages."""
        self.records = records
        corpus = [r.get("customer_message", "") for r in records]
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=15000,
            sublinear_tf=True,
            stop_words="english",
        )
        self.doc_vectors = self.vectorizer.fit_transform(corpus)
        logger.info(f"Fitted LexicalRetriever with {len(records)} historical records")

    def retrieve(
        self,
        query: str,
        brand: Optional[str] = None,
        intent: Optional[str] = None,
        top_k: int = 5,
        min_similarity: float = 0.05,
    ) -> List[EvidenceItem]:
        if self.vectorizer is None or self.doc_vectors is None:
            return []

        query_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(query_vec, self.doc_vectors)[0]

        # Apply metadata filtering
        ranked_indices = np.argsort(sims)[::-1]

        results = []
        for idx in ranked_indices:
            score = float(sims[idx])
            if score < min_similarity:
                break

            rec = self.records[idx]
            if brand and rec.get("brand") and rec.get("brand") != brand:
                continue
            if intent and rec.get("intent") and rec.get("intent") != intent:
                continue

            results.append(
                EvidenceItem(
                    customer_message=rec.get("customer_message", ""),
                    brand_response=rec.get("brand_response", ""),
                    conversation_id=str(rec.get("conversation_id", "")),
                    similarity=round(score, 4),
                    timestamp=rec.get("created_at"),
                    retrieval_method="lexical",
                )
            )
            if len(results) >= top_k:
                break

        return results

    def save(self, filepath: Path):
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "wb") as f:
            pickle.dump(
                {
                    "vectorizer": self.vectorizer,
                    "doc_vectors": self.doc_vectors,
                    "records": self.records,
                },
                f,
            )

    def load(self, filepath: Path):
        with open(filepath, "rb") as f:
            data = pickle.load(f)
            self.vectorizer = data["vectorizer"]
            self.doc_vectors = data["doc_vectors"]
            self.records = data["records"]


class SemanticVectorRetriever:
    """
    Dense Semantic Retriever.
    Supports Sentence-Transformers embeddings or dense TF-IDF SVD dense index,
    with cosine similarity / FAISS vector indexing and metadata filtering.
    """

    def __init__(self, embedding_model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = embedding_model_name
        self.records: List[Dict[str, Any]] = []
        self.embeddings: Optional[np.ndarray] = None
        self._st_model = None

    def _get_st_model(self):
        if self._st_model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._st_model = SentenceTransformer(self.model_name)
            except Exception as e:
                logger.warning(f"Could not load sentence_transformers: {e}. Falling back to dense TF-IDF.")
                self._st_model = False
        return self._st_model

    def encode(self, texts: List[str]) -> np.ndarray:
        model = self._get_st_model()
        if model:
            embs = model.encode(texts, show_progress_bar=False, normalize_embeddings=True)
            return np.array(embs, dtype=np.float32)
        else:
            # High-dimensional normalized dense projection fallback
            from sklearn.feature_extraction.text import HashingVectorizer
            hv = HashingVectorizer(n_features=384, norm="l2")
            return hv.transform(texts).toarray().astype(np.float32)

    def fit(self, records: List[Dict[str, Any]]):
        self.records = records
        texts = [r.get("customer_message", "") for r in records]
        logger.info(f"Encoding {len(texts)} texts for SemanticVectorRetriever...")
        self.embeddings = self.encode(texts)
        # Normalize for exact dot-product cosine similarity
        norms = np.linalg.norm(self.embeddings, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        self.embeddings = self.embeddings / norms
        logger.info(f"SemanticVectorRetriever indexed {len(self.records)} records (dim={self.embeddings.shape[1]})")

    def retrieve(
        self,
        query: str,
        brand: Optional[str] = None,
        intent: Optional[str] = None,
        top_k: int = 5,
        min_similarity: float = 0.05,
    ) -> List[EvidenceItem]:
        if self.embeddings is None or len(self.records) == 0:
            return []

        query_emb = self.encode([query])[0]
        q_norm = np.linalg.norm(query_emb)
        if q_norm > 0:
            query_emb = query_emb / q_norm

        sims = np.dot(self.embeddings, query_emb)
        ranked_indices = np.argsort(sims)[::-1]

        results = []
        for idx in ranked_indices:
            score = float(sims[idx])
            if score < min_similarity:
                break

            rec = self.records[idx]
            if brand and rec.get("brand") and rec.get("brand") != brand:
                continue
            if intent and rec.get("intent") and rec.get("intent") != intent:
                continue

            results.append(
                EvidenceItem(
                    customer_message=rec.get("customer_message", ""),
                    brand_response=rec.get("brand_response", ""),
                    conversation_id=str(rec.get("conversation_id", "")),
                    similarity=round(score, 4),
                    timestamp=rec.get("created_at"),
                    retrieval_method="semantic",
                )
            )
            if len(results) >= top_k:
                break

        return results

    def save(self, filepath: Path):
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "wb") as f:
            pickle.dump(
                {
                    "records": self.records,
                    "embeddings": self.embeddings,
                    "model_name": self.model_name,
                },
                f,
            )

    def load(self, filepath: Path):
        with open(filepath, "rb") as f:
            data = pickle.load(f)
            self.records = data["records"]
            self.embeddings = data["embeddings"]
            self.model_name = data.get("model_name", self.model_name)
        logger.info(f"Loaded SemanticVectorRetriever with {len(self.records)} records")


class HybridSupportRetriever:
    """
    Orchestrates semantic dense retrieval + lexical retrieval baseline
    with brand filtering, intent routing, and fallbacks.
    """

    def __init__(self):
        self.semantic = SemanticVectorRetriever()
        self.lexical = LexicalRetriever()

    def fit(self, records: List[Dict[str, Any]]):
        self.semantic.fit(records)
        self.lexical.fit(records)

    def retrieve_similar_messages(
        self,
        query: str,
        brand: Optional[str] = None,
        intent: Optional[str] = None,
        top_k: int = 5,
        similarity_threshold: Optional[float] = None,
    ) -> List[EvidenceItem]:
        threshold = similarity_threshold or settings.retrieval.similarity_threshold

        # 1. Primary: Semantic dense search
        results = self.semantic.retrieve(
            query=query, brand=brand, intent=intent, top_k=top_k, min_similarity=threshold
        )

        # 2. If semantic yields few results, relax intent constraint
        if len(results) < 2 and intent:
            relaxed = self.semantic.retrieve(
                query=query, brand=brand, intent=None, top_k=top_k, min_similarity=threshold
            )
            for r in relaxed:
                if not any(existing.conversation_id == r.conversation_id for existing in results):
                    results.append(r)
                if len(results) >= top_k:
                    break

        # 3. If still empty, fall back to lexical
        if not results:
            results = self.lexical.retrieve(
                query=query, brand=brand, intent=None, top_k=top_k, min_similarity=0.05
            )

        return results[:top_k]

    def save(self, directory: Path):
        directory.mkdir(parents=True, exist_ok=True)
        self.semantic.save(directory / "semantic_index.pkl")
        self.lexical.save(directory / "lexical_index.pkl")

    def load(self, directory: Path):
        if (directory / "semantic_index.pkl").exists():
            self.semantic.load(directory / "semantic_index.pkl")
        if (directory / "lexical_index.pkl").exists():
            self.lexical.load(directory / "lexical_index.pkl")
