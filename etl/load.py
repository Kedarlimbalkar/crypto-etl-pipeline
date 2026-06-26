import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def load_to_postgres(df):
    """
    Loads transformed DataFrame into PostgreSQL crypto_prices table.
    """
    print("[LOAD] Connecting to PostgreSQL...")
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        database=os.getenv("POSTGRES_DB", "cryptodb"),
        user=os.getenv("POSTGRES_USER", "airflow"),
        password=os.getenv("POSTGRES_PASSWORD", "airflow"),
        port=os.getenv("POSTGRES_PORT", "5432")
    )
    cursor = conn.cursor()

    print("[LOAD] Inserting records...")
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO crypto_prices
            (coin_id, symbol, name, current_price, market_cap, total_volume, price_change_24h)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            row["id"],
            row["symbol"],
            row["name"],
            row["current_price"],
            row["market_cap"],
            row["total_volume"],
            row["price_change_24h"]
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"[LOAD] Successfully inserted {len(df)} records into PostgreSQL.")