"""
Unit tests for data parsing, ID normalization, and text cleaning.
"""
import pytest
from scripts.build_conversations import clean_text, normalize_id


def test_normalize_id_standard():
    assert normalize_id(119237) == "119237"
    assert normalize_id("119237") == "119237"


def test_normalize_id_float_conversion():
    # Crucial test for preventing float-string lookup mismatches
    assert normalize_id(119237.0) == "119237"
    assert normalize_id("119237.0") == "119237"


def test_normalize_id_empty_and_nan():
    import numpy as np
    assert normalize_id(None) == ""
    assert normalize_id(np.nan) == ""


def test_clean_text_removes_leading_handles():
    raw = "@SpotifyCares @105847 My music won't play!"
    cleaned = clean_text(raw)
    assert cleaned == "My music won't play!"


def test_clean_text_unescapes_html_entities():
    raw = "Rock &amp; Roll music is awesome &lt;3"
    cleaned = clean_text(raw)
    assert cleaned == "Rock & Roll music is awesome <3"


def test_clean_text_whitespace():
    raw = "Too   many    spaces   in   this   sentence"
    cleaned = clean_text(raw)
    assert cleaned == "Too many spaces in this sentence"
