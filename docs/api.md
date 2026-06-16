# API Integrations

## Groq LLM API

- **Endpoint:** `https://api.groq.com/openai/v1/chat/completions`
- **Model:** `llama-3.3-70b-versatile`
- **Auth:** `GROQ_API_KEY` from `.env`
- **Client:** `groq` Python SDK

### Used By
- `suggest_outfit()` — sends wardrobe + item context, gets outfit narrative
- `create_fit_card()` — sends outfit + item, gets social caption

### suggest_outfit System Prompt (DO NOT soften without logging in decisions.md)
```
You are a personal stylist helping someone style a thrifted find. 
Given the new item and the user's existing wardrobe, suggest one complete outfit combination. 
Be specific about which wardrobe pieces to pair with the new item. 
Keep the suggestion to 2-3 sentences. Sound like a real stylist, not a product description.
```

### create_fit_card System Prompt (DO NOT soften without logging in decisions.md)
```
You are writing a short Instagram caption for a thrift find outfit post.
Write 1-2 sentences in a casual, authentic voice — like a real person sharing their outfit, not a brand.
Include the item name, price, and platform it was found on. Use 1-2 relevant emojis naturally.
Make it sound different every time — vary the structure and phrasing.
```

### LLM Call Template
```python
from groq import Groq
import os

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_CONTENT}
    ],
    temperature=0.9  # Higher temp for create_fit_card to ensure variation
)
result = response.choices[0].message.content
```

### Temperature Settings
| Tool              | Temperature | Reason                                           |
|-------------------|-------------|--------------------------------------------------|
| `suggest_outfit`  | 0.7         | Consistent styling advice with some creativity   |
| `create_fit_card` | 0.9         | Must produce different output on repeated calls  |
