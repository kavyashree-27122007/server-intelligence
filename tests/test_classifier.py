"""
Unit tests for intent classification and baselines.
"""
import pytest
from app.classification.classifier import (
    TfidfIntentClassifier,
    MajorityBaselineClassifier,
    clean_tweet_text,
)


def test_clean_tweet_text():
    raw = "@SpotifyCares I can't log in https://spotify.com &amp; check my account"
    cleaned = clean_tweet_text(raw)
    assert "@" not in cleaned
    assert "https://" not in cleaned
    assert "&amp;" not in cleaned
    assert "&" in cleaned
    assert "can't log in" in cleaned


def test_majority_baseline():
    clf = MajorityBaselineClassifier()
    texts = ["a", "b", "c", "d"]
    labels = ["Billing", "Billing", "Audio", "Billing"]
    clf.fit(texts, labels)
    res = clf.predict("some random query")
    assert res.name == "Billing"
    assert res.confidence == 0.75


def test_tfidf_classifier_training_and_prediction():
    clf = TfidfIntentClassifier()
    texts = [
        "I was charged twice on my credit card this month",
        "Refund my payment please for family plan",
        "Music keeps pausing and skipping songs audio",
        "Audio cuts out and song sound stopped playing",
        "I forgot my account password and cannot login",
        "Reset password link not received in email",
    ]
    labels = [
        "Subscription & Billing",
        "Subscription & Billing",
        "Audio & Playback Issues",
        "Audio & Playback Issues",
        "Account Access & Login",
        "Account Access & Login",
    ]
    clf.fit(texts, labels)

    res_billing = clf.predict("Why was my credit card billed twice?")
    assert res_billing.name == "Subscription & Billing"
    assert res_billing.confidence > 0.30

    res_audio = clf.predict("My song is stuttering and sound stopped")
    assert res_audio.name == "Audio & Playback Issues"
    assert res_audio.confidence > 0.30

    res_login = clf.predict("Cannot login with my username and password")
    assert res_login.name == "Account Access & Login"
    assert res_login.confidence > 0.30


def test_tfidf_classifier_empty_input():
    clf = TfidfIntentClassifier()
    clf.fit(["hello support", "need billing help"], ["General", "Billing"])
    res = clf.predict("   ")
    assert res.name == "Other / Unclear"
    assert res.confidence == 0.1
