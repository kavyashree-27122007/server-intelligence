"""
Unit tests for retrieval systems: lexical, semantic, and hybrid.
"""
import pytest
from app.retrieval.retriever import LexicalRetriever, SemanticVectorRetriever, HybridSupportRetriever


@pytest.fixture
def sample_records():
    return [
        {
            "customer_message": "My songs keep pausing every 30 seconds on iPhone",
            "brand_response": "Hi! Have you tried restarting your device and clearing cache?",
            "conversation_id": "1001",
            "brand": "SpotifyCares",
            "intent": "Audio & Playback Issues",
            "created_at": "2017-10-10",
        },
        {
            "customer_message": "How do I update my payment card for my family subscription?",
            "brand_response": "You can update billing information at spotify.com/account.",
            "conversation_id": "1002",
            "brand": "SpotifyCares",
            "intent": "Subscription & Billing",
            "created_at": "2017-10-11",
        },
        {
            "customer_message": "Can't login, forgot my password and reset email won't arrive",
            "brand_response": "Check your spam folder or verify the email registered with us.",
            "conversation_id": "1003",
            "brand": "SpotifyCares",
            "intent": "Account Access & Login",
            "created_at": "2017-10-12",
        },
    ]


def test_lexical_retriever(sample_records):
    retriever = LexicalRetriever()
    retriever.fit(sample_records)
    results = retriever.retrieve("songs keep pausing on mobile", top_k=2)
    assert len(results) >= 1
    assert results[0].conversation_id == "1001"
    assert results[0].similarity > 0.10


def test_semantic_retriever(sample_records):
    retriever = SemanticVectorRetriever()
    retriever.fit(sample_records)
    results = retriever.retrieve("songs pausing iPhone", top_k=2, min_similarity=0.0)
    assert len(results) >= 1
    assert results[0].conversation_id == "1001"


def test_hybrid_retriever_intent_filtering(sample_records):
    retriever = HybridSupportRetriever()
    retriever.fit(sample_records)
    # Search with explicit intent filter
    results = retriever.retrieve_similar_messages(
        query="payment card details",
        brand="SpotifyCares",
        intent="Subscription & Billing",
        top_k=1,
    )
    assert len(results) == 1
    assert results[0].conversation_id == "1002"
