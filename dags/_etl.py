import os
import sys
from typing import *
import requests
import pandas as pd
import datetime
import psycopg2

import pendulum
from airflow.decorators  import task, dag
from airflow.operators.python import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator


# Define the DAG
@dag(
    schedule="1 * * * *", # Run at 8:00 AM every day
    start_date=pendulum.datetime(2024, 4, 6, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
    tags=["defi_liquidity_aggregator"],
)

def defi_data_pipeline():

    @task
    def get_token_data() -> Dict[str, Any]:
        vs_currency = 'usd'
        token_ids = ['Solana', 'Marscoin', 'ethereum', 'bitcoin']
        token_ids_str = ','.join(token_ids)
        URL = f"https://api.coingecko.com/api/v3/simple/price?ids={token_ids_str}&vs_currencies={vs_currency}&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true&precision=5"
        api_key = os.getenv('API_KEY', '')
        headers = {"x-cg-demo-api-key": api_key}
        response = requests.get(URL, headers=headers)
        if response.status_code == 200:
            api_data = response.json()
            return api_data            
        else:
            print("Failed to fetch data:", response.status_code)
        return {}

    @task
    def transformed_to_datetime(token_data) -> pd.DataFrame:
        columns = [
            'token_name',
            'usd',
            'usd_market_cap',
            'usd_24h_vol',
            'usd_24h_change',
            'last_updated_at',
        ]
        transformed_data = pd.DataFrame(token_data).T.reset_index()
        transformed_data.columns = columns
        # Convert 'last_updated_at' to datetimes (assuming it holds Unix timestamps)
        transformed_data['updated_dt'] = pd.to_datetime(transformed_data['last_updated_at'], unit='s')
        # Remove timezone information and convert to string
        transformed_data['updated_dt'] = transformed_data['updated_dt'].dt.tz_localize(None).dt.strftime('%Y-%m-%d %H:%M:%S')
        return transformed_data

    
    @task
    def establish_database_conn(data_frame: pd.DataFrame) -> None:
        qry = '''
        INSERT INTO token (
            token_name, 
            usd, 
            usd_market_cap, 
            usd_24h_vol, 
            usd_24h_change,
            last_updated_at,
            updated_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        '''
        hook = PostgresHook(postgres_conn_id="defi_connection")
        conn = hook.get_conn()
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        for record in data_frame.itertuples(index=False):
            cursor.execute(qry, (record))
        cursor.close()
        conn.commit()
           

    token_data = get_token_data()
    data_frame = transformed_to_datetime(token_data)
    establish_database_conn(data_frame)

dag = defi_data_pipeline()