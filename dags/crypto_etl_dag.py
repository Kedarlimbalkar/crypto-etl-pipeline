from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, '/opt/airflow')

from etl.extract import extract_crypto_data
from etl.transform import transform_crypto_data
from etl.load import load_to_postgres

default_args = {
    'owner': 'kedar',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

def run_etl():
    print("Starting ETL Pipeline...")
    raw_data = extract_crypto_data()
    df = transform_crypto_data(raw_data)
    load_to_postgres(df)
    print("ETL Pipeline completed successfully!")

with DAG(
    dag_id='crypto_etl_pipeline',
    default_args=default_args,
    description='Daily crypto price ETL from CoinGecko API to PostgreSQL',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['crypto', 'etl', 'coingecko'],
) as dag:

    run_etl_task = PythonOperator(
        task_id='run_crypto_etl',
        python_callable=run_etl,
    )