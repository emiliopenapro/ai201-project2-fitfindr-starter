# Tool Interface Specifications

All three tools are implemented in `tools.py`. Stubs already exist in the starter repo — implement into them.

---

## Tool 1: search_listings

```python
def search_listings(description: str, size: str | None, max_price: float | None) -> list[dict]:
```

**What it does:** Searches `data/listings.json` for items matching the description, size, and price constraints.

**Inputs:**
| Parameter     | Type          | Meaning                                         |
|---------------|---------------|-------------------------------------------------|
| `description` | str           | Natural language description (e.g., "vintage graphic tee") |
| `size`        | str or None   | Size filter (e.g., "M"). None = no size filter  |
| `max_price`   | float or None | Maximum price in USD. None = no price filter    |

**Matching logic:**
- Match on `title`, `description`, and `style_tags` fields
- Filter by `size` if provided (exact match)
- Filter by `price <= max_price` if provided
- Sort by relevance (keyword matches descending)

**Returns:** `list[dict]` — matched listing objects. Empty list `[]` if no matches.

**Error behavior:** NEVER raises an exception. Returns `[]` on any error or no match.

---

## Tool 2: suggest_outfit

```python
def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
```

**What it does:** Calls Groq LLM to suggest a complete outfit pairing for the new item using the user's wardrobe.

**Inputs:**
| Parameter  | Type | Meaning                                       |
|------------|------|-----------------------------------------------|
| `new_item` | dict | A listing object from `search_listings`       |
| `wardrobe` | dict | Wardrobe object (may be empty — handle it)    |

**Empty wardrobe handling:** If `wardrobe["items"]` is empty or missing, suggest a complete outfit using only the new item and common generic pieces. Do NOT crash or return an empty string.

**Returns:** `str` — outfit suggestion narrative (2–3 sentences).

**Error behavior:** Returns a descriptive error string if LLM call fails. Never raises an exception.

---

## Tool 3: create_fit_card

```python
def create_fit_card(outfit: str, new_item: dict) -> str:
```

**What it does:** Calls Groq LLM to generate a short, shareable social media caption for the outfit.

**Inputs:**
| Parameter | Type | Meaning                                              |
|-----------|------|------------------------------------------------------|
| `outfit`  | str  | The outfit suggestion from `suggest_outfit`          |
| `new_item`| dict | The listing object (for price, platform, title)      |

**Empty outfit guard:** If `outfit` is empty or whitespace, return `"Cannot create a fit card without an outfit suggestion."` — do NOT call the LLM.

**Variation requirement:** Must produce meaningfully different output on repeated calls with the same input. Use temperature=0.9.

**Returns:** `str` — social caption (1–2 sentences with emojis).

**Error behavior:** Returns a descriptive error string if LLM call fails. Never raises an exception.

---

## Planning Loop Rules (in agent.py)

```
IF search_listings returns [] :
    session["error"] = "No listings found for your search. Try broader terms or a higher budget."
    session["selected_item"] = None
    RETURN session immediately — do NOT call suggest_outfit or create_fit_card

IF search_listings returns results :
    session["selected_item"] = results[0]
    CALL suggest_outfit(selected_item, wardrobe)
    session["outfit_suggestion"] = result
    CALL create_fit_card(outfit_suggestion, selected_item)
    session["fit_card"] = result
    RETURN session
```
