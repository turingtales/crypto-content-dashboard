import requests
import json
import os

HF_TOKEN = os.environ["HF_TOKEN"]

MODEL_URL = "https://router.huggingface.co/hf-inference/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

def get_market_data():
    url = "https://api.coingecko.com/api/v3/global"
    r = requests.get(url).json()
    market_cap = r["data"]["total_market_cap"]["usd"]
    dominance = r["data"]["market_cap_percentage"]["btc"]
    return f"Total market cap: ${market_cap:,.0f}. BTC dominance: {dominance:.2f}%."

def generate_posts(summary):

    prompt = f"""
    You are a crypto content assistant.

    Based on this crypto summary:
    {summary}

    Return ONLY valid JSON with this exact structure:

    {{
      "market_summary": "string",
      "narratives": ["item1","item2","item3"],
      "unlocks": ["item1","item2"],
      "binance_posts": ["post1","post2","post3"],
      "x_posts": ["post1","post2","post3"]
    }}
    """

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 700,
            "temperature": 0.7,
            "return_full_text": False
        }
    }

    response = requests.post(MODEL_URL, headers=headers, json=payload)
    result = response.json()

    if isinstance(result, dict) and "error" in result:
        raise Exception(result["error"])

    generated_text = result[0]["generated_text"].strip()

    json_start = generated_text.find("{")
    json_text = generated_text[json_start:]

    return json.loads(json_text)

def main():
    market = get_market_data()
    summary = market + " AI tokens trending. ETH ecosystem active."

    output = generate_posts(summary)

    with open("data/today.json", "w") as f:
        json.dump(output, f, indent=2)

if __name__ == "__main__":
    main()
