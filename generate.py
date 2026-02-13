import requests
import json
import os
from datetime import datetime

OPENAI_KEY = os.environ["OPENAI_KEY"]

def get_market_data():
    url = "https://api.coingecko.com/api/v3/global"
    r = requests.get(url).json()
    market_cap = r["data"]["total_market_cap"]["usd"]
    dominance = r["data"]["market_cap_percentage"]["btc"]
    return f"Total market cap: ${market_cap:,.0f}. BTC dominance: {dominance:.2f}%."

def get_news():
    return "AI tokens trending. Bitcoin steady. ETH ecosystem active."

def generate_posts(summary):
    headers = {
        "Authorization": f"Bearer {OPENAI_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    Based on this crypto summary:
    {summary}

    Create:
    3 Binance Square posts detailed but engaging.
    3 X posts under 280 characters.

    Return JSON with:
    market_summary
    narratives array
    unlocks array
    binance_posts array
    x_posts array
    """

    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}]
    }

    r = requests.post("https://api.openai.com/v1/chat/completions",
                      headers=headers, json=data)

    content = r.json()["choices"][0]["message"]["content"]
    return json.loads(content)

def main():
    market = get_market_data()
    news = get_news()
    summary = market + " " + news
    output = generate_posts(summary)

    with open("data/today.json", "w") as f:
        json.dump(output, f, indent=2)

if __name__ == "__main__":
    main()
