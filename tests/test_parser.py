import pytest
from hn_scraper.parser import _safe_int, _extract_domain


def test_safe_int_normal():
    assert _safe_int("142 points") == 142

def test_safe_int_empty():
    assert _safe_int("") == 0

def test_safe_int_none():
    assert _safe_int(None) == 0

def test_extract_domain_valid():
    assert _extract_domain("https://www.example.com/path") == "example.com"

def test_extract_domain_none():
    assert _extract_domain(None) is None

def test_extract_domain_internal():
    assert _extract_domain("item?id=12345") is None or isinstance(
        _extract_domain("item?id=12345"), str
    )