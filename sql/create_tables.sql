CREATE TABLE IF NOT EXISTS crypto_prices (
    id          SERIAL PRIMARY KEY,
    coin_id     VARCHAR(50),
    symbol      VARCHAR(20),
    name        VARCHAR(100),
    current_price     NUMERIC,
    market_cap        BIGINT,
    total_volume      BIGINT,
    price_change_24h  NUMERIC,
    fetched_at        TIMESTAMP DEFAULT NOW()
);