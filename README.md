# Crypto ETL Pipeline

An end-to-end ETL pipeline that extracts live cryptocurrency data from the CoinGecko API, transforms it using Pandas, and loads it into PostgreSQL — orchestrated with Apache Airflow and containerised with Docker.

## Architecture

Extract (CoinGecko API) → Transform (Pandas) → Load (PostgreSQL) → Orchestrate (Airflow)

## Tech Stack

- Python 3.10
- Apache Airflow 2.8.1
- PostgreSQL 15
- Docker & Docker Compose
- Pandas, Requests, Psycopg2

## Project Structure