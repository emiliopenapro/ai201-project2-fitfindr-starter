"""
tools.py

The three required FitFindr tools. Each tool is a standalone function that
can be called and tested independently before being wired into the agent loop.

Complete and test each tool before moving to agent.py.

Tools:
    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)              → str
    create_fit_card(outfit, new_item)               → str
"""

import os

from dotenv import load_dotenv
from groq import Groq

from utils.data_loader import load_listings

load_dotenv()

MODEL = "llama-3.3-70b-versatile"

SUGGEST_OUTFIT_SYSTEM_PROMPT = (
    "You are a personal stylist helping someone style a thrifted find. "
    "Given the new item and the user's existing wardrobe, suggest one complete "
    "outfit combination. Be specific about which wardrobe pieces to pair with the "
    "new item. Keep the suggestion to 2-3 sentences. Sound like a real stylist, "
    "not a product description."
)

CREATE_FIT_CARD_SYSTEM_PROMPT = (
    "You are writing a short Instagram caption for a thrift find outfit post. "
    "Write 1-2 sentences in a casual, authentic voice — like a real person sharing "
    "their outfit, not a brand. Include the item name, price, and platform it was "
    "found on. Use 1-2 relevant emojis naturally. Make it sound different every "
    "time — vary the structure and phrasing."
)


# ── Groq client ───────────────────────────────────────────────────────────────

def _get_groq_client():
    """Initialize and return a Groq client using GROQ_API_KEY from .env."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not set. Add it to a .env file in the project root."
        )
    return Groq(api_key=api_key)


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the mock listings dataset for items matching the description,
    optional size, and optional price ceiling.

    Args:
        description: Keywords describing what the user is looking for
                     (e.g., "vintage graphic tee").
        size:        Size string to filter by, or None to skip size filtering.
                     Matching is case-insensitive (e.g., "M" matches "S/M").
        max_price:   Maximum price (inclusive), or None to skip price filtering.

    Returns:
        A list of matching listing dicts, sorted by relevance (best match first).
        Returns an empty list if nothing matches — does NOT raise an exception.

    Each listing dict has the following fields:
        id, title, description, category, style_tags (list), size,
        condition, price (float), colors (list), brand, platform

    TODO:
        1. Load all listings with load_listings().
        2. Filter by max_price and size (if provided).
        3. Score each remaining listing by keyword overlap with `description`.
        4. Drop any listings with a score of 0 (no relevant matches).
        5. Sort by score, highest first, and return the listing dicts.

    Before writing code, fill in the Tool 1 section of planning.md.
    """
    try:
        listings = load_listings()
        keywords = [kw for kw in description.lower().split() if kw]

        scored: list[tuple[int, dict]] = []
        for item in listings:
            if max_price is not None and item.get("price", float("inf")) > max_price:
                continue
            # Normalized substring size match (DEC-007): "M" matches "S/M", "M/L", etc.
            if size and size.lower() not in str(item.get("size", "")).lower():
                continue

            searchable = (
                f"{item.get('title', '')} "
                f"{item.get('description', '')} "
                f"{' '.join(item.get('style_tags', []))}"
            ).lower()
            score = sum(1 for kw in keywords if kw in searchable)
            if score == 0:
                continue
            scored.append((score, item))

        scored.sort(key=lambda pair: pair[0], reverse=True)
        return [item for _, item in scored]
    except Exception:
        return []


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest 1–2 complete outfits.

    Args:
        new_item: A listing dict (the item the user is considering buying).
        wardrobe: A wardrobe dict with an 'items' key containing a list of
                  wardrobe item dicts. May be empty — handle this gracefully.

    Returns:
        A non-empty string with outfit suggestions.
        If the wardrobe is empty, offer general styling advice for the item
        rather than raising an exception or returning an empty string.

    TODO:
        1. Check whether wardrobe['items'] is empty.
        2. If empty: call the LLM with a prompt for general styling ideas
           (what kinds of items pair well, what vibe it suits, etc.).
        3. If not empty: format the wardrobe items into a prompt and ask
           the LLM to suggest specific outfit combinations using the new item
           and named pieces from the wardrobe.
        4. Return the LLM's response as a string.

    Before writing code, fill in the Tool 2 section of planning.md.
    """
    try:
        wardrobe_items = (wardrobe or {}).get("items", [])

        if wardrobe_items:
            wardrobe_desc = ", ".join(i["name"] for i in wardrobe_items)
            user_content = (
                f"New thrifted item: {new_item['title']} — {new_item['description']}\n"
                f"User's wardrobe: {wardrobe_desc}\n"
                "Suggest one complete outfit pairing the new item with specific "
                "pieces from this wardrobe."
            )
        else:
            user_content = (
                f"New thrifted item: {new_item['title']} — {new_item['description']}\n"
                "The user has no wardrobe entered yet. Suggest one complete outfit "
                "using the new item plus common wardrobe basics."
            )

        client = _get_groq_client()
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SUGGEST_OUTFIT_SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Could not generate outfit suggestion: {e}"


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Generate a short, shareable outfit caption for the thrifted find.

    Args:
        outfit:   The outfit suggestion string from suggest_outfit().
        new_item: The listing dict for the thrifted item.

    Returns:
        A 2–4 sentence string usable as an Instagram/TikTok caption.
        If outfit is empty or missing, return a descriptive error message
        string — do NOT raise an exception.

    The caption should:
    - Feel casual and authentic (like a real OOTD post, not a product description)
    - Mention the item name, price, and platform naturally (once each)
    - Capture the outfit vibe in specific terms
    - Sound different each time for different inputs (use higher LLM temperature)

    TODO:
        1. Guard against an empty or whitespace-only outfit string.
        2. Build a prompt that gives the LLM the item details and the outfit,
           and asks for a caption matching the style guidelines above.
        3. Call the LLM and return the response.

    Before writing code, fill in the Tool 3 section of planning.md.
    """
    if not outfit or not outfit.strip():
        return "Cannot create a fit card without an outfit suggestion."
    try:
        user_content = (
            f"Item: {new_item['title']} — ${new_item['price']} "
            f"from {new_item['platform']}\n"
            f"Outfit: {outfit}"
        )
        client = _get_groq_client()
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": CREATE_FIT_CARD_SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
            temperature=0.9,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Could not generate fit card: {e}"
