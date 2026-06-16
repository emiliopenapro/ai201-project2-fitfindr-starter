"""
test_tools.py — one test per tool plus one per failure mode.

The suggest_outfit / create_fit_card tests make real Groq API calls, so they
require GROQ_API_KEY (in .env) and a network connection.
"""

from tools import search_listings, suggest_outfit, create_fit_card
from utils.data_loader import get_example_wardrobe, get_empty_wardrobe


# ── search_listings ───────────────────────────────────────────────────────────

def test_search_returns_results():
    results = search_listings("vintage graphic tee", max_price=30)
    assert isinstance(results, list)
    assert len(results) > 0
    assert all(isinstance(r, dict) for r in results)


def test_search_empty_results():
    # Impossible query — must return [] (not None, not an exception)
    results = search_listings("designer ballgown", size="XXS", max_price=5)
    assert results == []


def test_search_price_filter():
    results = search_listings("jacket", max_price=40)
    assert all(r["price"] <= 40 for r in results)


def test_search_size_filter():
    # Normalized substring match (DEC-007): every result's size contains "M"
    results = search_listings("tee", size="M")
    assert all("m" in str(r["size"]).lower() for r in results)


# ── suggest_outfit ────────────────────────────────────────────────────────────

def test_suggest_outfit_with_wardrobe():
    item = search_listings("vintage graphic tee", max_price=30)[0]
    result = suggest_outfit(item, get_example_wardrobe())
    assert isinstance(result, str)
    assert result.strip() != ""


def test_suggest_outfit_empty_wardrobe():
    item = search_listings("vintage graphic tee", max_price=30)[0]
    result = suggest_outfit(item, get_empty_wardrobe())
    assert isinstance(result, str)
    assert result.strip() != ""


# ── create_fit_card ───────────────────────────────────────────────────────────

def test_fit_card_returns_string():
    item = search_listings("vintage graphic tee", max_price=30)[0]
    outfit = "Pair it with baggy jeans and chunky white sneakers."
    result = create_fit_card(outfit, item)
    assert isinstance(result, str)
    assert result.strip() != ""


def test_fit_card_empty_outfit():
    item = search_listings("vintage graphic tee", max_price=30)[0]
    result = create_fit_card("", item)
    assert result == "Cannot create a fit card without an outfit suggestion."


def test_fit_card_varies():
    item = search_listings("vintage graphic tee", max_price=30)[0]
    outfit = "Pair it with baggy jeans and chunky white sneakers."
    outputs = {create_fit_card(outfit, item) for _ in range(3)}
    # At least 2 of the 3 calls must differ
    assert len(outputs) >= 2
