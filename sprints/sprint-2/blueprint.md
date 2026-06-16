# Sprint 2 — Blueprint

## Implementation Order
Build and test one tool at a time. Do not move to the next tool until the current one passes its tests.

### 1. search_listings(description, size, max_price)
```python
def search_listings(description: str, size: str | None, max_price: float | None) -> list[dict]:
    try:
        listings = load_listings()           # from utils/data_loader.py
        results = []
        keywords = description.lower().split()
        
        for item in listings:
            # Score: count keyword matches in title + description + style_tags
            searchable = f"{item['title']} {item['description']} {' '.join(item.get('style_tags', []))}".lower()
            score = sum(1 for kw in keywords if kw in searchable)
            if score == 0:
                continue
            if size and item.get('size') != size:
                continue
            if max_price and item.get('price', 999) > max_price:
                continue
            results.append((score, item))
        
        results.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in results]
    except Exception:
        return []
```

### 2. suggest_outfit(new_item, wardrobe)
```python
def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    try:
        wardrobe_items = wardrobe.get("items", [])
        
        if wardrobe_items:
            wardrobe_desc = ", ".join([i["name"] for i in wardrobe_items])
            user_content = f"New thrifted item: {new_item['title']} — {new_item['description']}\nWardrobe: {wardrobe_desc}"
        else:
            user_content = f"New thrifted item: {new_item['title']} — {new_item['description']}\nWardrobe: empty — suggest an outfit using common basics."
        
        # Call Groq with suggest_outfit system prompt (see docs/api.md)
        # Return response string
    except Exception as e:
        return f"Could not generate outfit suggestion: {str(e)}"
```

### 3. create_fit_card(outfit, new_item)
```python
def create_fit_card(outfit: str, new_item: dict) -> str:
    if not outfit or not outfit.strip():
        return "Cannot create a fit card without an outfit suggestion."
    try:
        user_content = f"Item: {new_item['title']} — ${new_item['price']} from {new_item['platform']}\nOutfit: {outfit}"
        # Call Groq with create_fit_card system prompt, temperature=0.9 (see docs/api.md)
        # Return response string
    except Exception as e:
        return f"Could not generate fit card: {str(e)}"
```

## tests/test_tools.py Structure
```python
from tools import search_listings, suggest_outfit, create_fit_card
from utils.data_loader import get_example_wardrobe, get_empty_wardrobe

# search_listings tests
def test_search_returns_results(): ...
def test_search_empty_results(): ...          # returns [], not None, not exception
def test_search_price_filter(): ...           # all results have price <= max_price
def test_search_size_filter(): ...            # all results match size

# suggest_outfit tests
def test_suggest_outfit_with_wardrobe(): ...  # returns non-empty string
def test_suggest_outfit_empty_wardrobe(): ... # returns non-empty string, no exception

# create_fit_card tests
def test_fit_card_returns_string(): ...       # returns non-empty string
def test_fit_card_empty_outfit(): ...         # returns specific error message string
def test_fit_card_varies(): ...              # call 3 times, at least 2 must differ
```
