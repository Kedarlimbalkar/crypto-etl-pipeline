# 🪙 Crypto ETL Pipeline

> An end-to-end production-grade ETL pipeline that extracts live cryptocurrency market data from the CoinGecko API, transforms it using Pandas, and loads it into PostgreSQL — fully orchestrated with Apache Airflow and containerised with Docker.

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Airflow](https://img.shields.io/badge/Apache_Airflow-2.8.1-017CEE?logo=apacheairflow)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Containerised-2496ED?logo=docker)
![Status](https://img.shields.io/badge/Pipeline-Active-success)

---

## 📌 Project Overview

This project simulates a real-world data engineering workflow used in fintech and crypto analytics teams. It automatically fetches the **top 20 cryptocurrencies by market cap** every day, cleans and validates the data, and stores it in a structured PostgreSQL database — all without manual intervention.

**Key highlights:**
- Fully automated daily scheduling with Apache Airflow DAGs
- Modular ETL design (Extract → Transform → Load as separate Python modules)
- Docker Compose setup for zero-config local deployment
- Production-ready error handling with retries and logging
- Clean SQL schema design for downstream analytics

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Apache Airflow (Orchestration)              │
│                     Scheduled: @daily                        │
│                                                              │
│   ┌───────────┐    ┌──────────────┐    ┌─────────────────┐  │
│   │  Extract  │───▶│  Transform   │───▶│      Load       │  │
│   │           │    │              │    │                 │  │
│   │ CoinGecko │    │ Pandas clean │    │   PostgreSQL    │  │
│   │    API    │    │ & validate   │    │   crypto_prices │  │
│   └───────────┘    └──────────────┘    └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                    Containerised with Docker
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10 | Core ETL scripting |
| Apache Airflow 2.8.1 | Pipeline orchestration & scheduling |
| PostgreSQL 15 | Data warehouse / storage |
| Pandas | Data transformation & cleaning |
| Docker & Docker Compose | Containerisation & environment setup |
| Requests | HTTP API calls to CoinGecko |
| Psycopg2 | PostgreSQL Python connector |

---

## 📁 Project Structure

```
crypto-etl-pipeline/
│
├── dags/
│   └── crypto_etl_dag.py       # Airflow DAG definition (schedule, tasks)
│
├── etl/
│   ├── extract.py              # Fetches data from CoinGecko API
│   ├── transform.py            # Cleans & transforms raw data with Pandas
│   └── load.py                 # Loads transformed data into PostgreSQL
│
├── sql/
│   └── create_tables.sql       # PostgreSQL schema definition
│
├── docker-compose.yml          # Airflow + PostgreSQL services
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not pushed)
├── .gitignore
└── README.md
```

---

## 📊 Data Pipeline Details

### Extract
- Calls the CoinGecko `/coins/markets` public API
- Fetches top 20 coins by market capitalisation in USD
- Returns raw JSON with 20+ fields per coin

### Transform
- Selects relevant columns: `id`, `symbol`, `name`, `current_price`, `market_cap`, `total_volume`, `price_change_24h`
- Drops null/missing values
- Normalises symbol to uppercase
- Returns a clean Pandas DataFrame

### Load
- Connects to PostgreSQL using environment variables
- Inserts each row into `crypto_prices` table
- Commits transaction and closes connection safely

### Database Schema

```sql
CREATE TABLE crypto_prices (
    id               SERIAL PRIMARY KEY,
    coin_id          VARCHAR(50),
    symbol           VARCHAR(20),
    name             VARCHAR(100),
    current_price    NUMERIC,
    market_cap       BIGINT,
    total_volume     BIGINT,
    price_change_24h NUMERIC,
    fetched_at       TIMESTAMP DEFAULT NOW()
);
```

---

## 🚀 How to Run Locally

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- Git

### Steps

**1. Clone the repository**
```bash
git clone https://github.com/Kedarlimbalkar/crypto-etl-pipeline.git
cd crypto-etl-pipeline
```

**2. Start all services**
```bash
docker-compose up -d
```

**3. Create the Airflow admin user**
```bash
docker exec -it crypto-etl-pipeline-airflow-webserver-1 airflow users create \
  --username admin \
  --firstname Kedar \
  --lastname Limbalkar \
  --role Admin \
  --email kedarlimbalkar@gmail.com \
  --password admin
```

**4. Create the database and table**
```bash
docker exec -it crypto-etl-pipeline-postgres-1 psql -U airflow -c "CREATE DATABASE cryptodb;"

docker exec -it crypto-etl-pipeline-postgres-1 psql -U airflow -d cryptodb -c "
CREATE TABLE IF NOT EXISTS crypto_prices (
    id SERIAL PRIMARY KEY,
    coin_id VARCHAR(50), symbol VARCHAR(20), name VARCHAR(100),
    current_price NUMERIC, market_cap BIGINT, total_volume BIGINT,
    price_change_24h NUMERIC, fetched_at TIMESTAMP DEFAULT NOW()
);"
```

**5. Open Airflow UI**

Go to `http://localhost:8080` and login with:
- Username: `admin`
- Password: `admin`

**6. Trigger the DAG**

Enable `crypto_etl_pipeline` and click ▶ to trigger it manually.

**7. Verify data in PostgreSQL**
```bash
docker exec -it crypto-etl-pipeline-postgres-1 psql -U airflow -d cryptodb \
  -c "SELECT coin_id, symbol, current_price, market_cap FROM crypto_prices LIMIT 10;"
```

---

## ✅ Pipeline Output

After a successful run, data looks like this:

| coin_id | symbol | current_price | market_cap |
|---------|--------|--------------|------------|
| bitcoin | BTC | 67234.50 | 1324567890000 |
| ethereum | ETH | 3521.20 | 423456789000 |
| tether | USDT | 1.00 | 112345678900 |

---

## 🔄 DAG Configuration

| Property | Value |
|----------|-------|
| DAG ID | `crypto_etl_pipeline` |
| Schedule | `@daily` |
| Owner | `kedar` |
| Retries | `2` |
| Retry Delay | `5 minutes` |
| Tags | `crypto`, `etl`, `coingecko` |

---

## 🔮 Future Improvements

- [ ] Add **dbt** for SQL-based data transformations and data modelling
- [ ] Integrate **Apache Kafka** for real-time streaming ingestion
- [ ] Deploy to **GCP Cloud Composer** (managed Airflow)
- [ ] Add **data quality checks** using Great Expectations
- [ ] Build a **Grafana dashboard** on top of PostgreSQL
- [ ] Add **Slack/email alerts** on pipeline failure
- [ ] Implement **incremental loading** to avoid duplicate records

---

## 👤 Author

**Kedar Limbalkar**
- 📧 kedarlimbalkar@gmail.com
- 💼 [LinkedIn](https://linkedin.com/in/kedar-limbalkar)
- 🐙 [GitHub](https://github.com/Kedarlimbalkar)
- 🌐 [Portfolio](https://kedarlimbalkar.in)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
