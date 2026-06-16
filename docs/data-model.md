# Data Model

## Listing Object (from data/listings.json)
| Field        | Type     | Description                                      |
|--------------|----------|--------------------------------------------------|
| `id`         | string   | Unique listing identifier                        |
| `title`      | string   | Item name (e.g., "Faded Band Tee")               |
| `description`| string   | Free-text description of the item                |
| `category`   | string   | Clothing category (e.g., "tops", "outerwear")    |
| `style_tags` | list[str]| Style descriptors (e.g., ["vintage", "grunge"])  |
| `size`       | string   | Size label (e.g., "M", "L", "XL")               |
| `condition`  | string   | Item condition (e.g., "Good", "Like New")        |
| `price`      | float    | Listed price in USD                              |
| `colors`     | list[str]| Color(s) of the item                             |
| `brand`      | string   | Brand name (may be null/unknown)                 |
| `platform`   | string   | Source platform (e.g., "Depop", "ThredUp")       |

## Wardrobe Object (from data/wardrobe_schema.json)
```json
{
  "items": [
    {
      "name": "baggy jeans",
      "category": "bottoms",
      "colors": ["blue"],
      "style_tags": ["casual", "streetwear"]
    }
  ],
  "style_preferences": ["vintage", "streetwear"],
  "preferred_colors": ["black", "white", "earth tones"]
}
```

## Session State Object (managed in agent.py)
| Key                  | Type          | Set by                  | Description                          |
|----------------------|---------------|-------------------------|--------------------------------------|
| `query`              | string        | user input              | Original natural language request    |
| `selected_item`      | dict or None  | search_listings         | Top listing result                   |
| `outfit_suggestion`  | string or None| suggest_outfit          | LLM-generated outfit suggestion      |
| `fit_card`           | string or None| create_fit_card         | LLM-generated shareable caption      |
| `error`              | string or None| any tool on failure     | Human-readable error message         |

## search_listings Return Type
```python
list[dict]  # each dict is a listing object from listings.json
# Returns [] if no matches found — never raises an exception
```

## suggest_outfit Return Type
```python
str  # outfit suggestion narrative
# Returns informative message string on empty wardrobe or LLM error
```

## create_fit_card Return Type
```python
str  # shareable social caption
# Returns descriptive error string if outfit input is empty
```
