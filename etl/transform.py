import pandas as pd

def transform_crypto_data(raw_data):
    """
    Cleans and transforms raw API data into a structured DataFrame.
    """
    print("[TRANSFORM] Transforming raw data...")
    df = pd.DataFrame(raw_data)
    
    df = df[[
        "id", "symbol", "name",
        "current_price", "market_cap",
        "total_volume", "price_change_percentage_24h"
    ]]
    
    df.rename(columns={
        "price_change_percentage_24h": "price_change_24h"
    }, inplace=True)
    
    df.dropna(inplace=True)
    df["symbol"] = df["symbol"].str.upper()
    
    print(f"[TRANSFORM] Transformed {len(df)} records.")
    return df