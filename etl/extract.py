import requests

def extract_crypto_data():
    """
    Fetches top 20 cryptocurrencies by market cap from CoinGecko API.
    Returns raw JSON list.
    """
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 20,
        "page": 1
    }
    print("[EXTRACT] Fetching data from CoinGecko API...")
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    print(f"[EXTRACT] Successfully fetched {len(data)} coins.")
    return data