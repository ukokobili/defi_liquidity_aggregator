import datetime
import os
import sys
from typing import *

import duckdb as db
import pandas as pd
import psycopg2.extras as p
import requests
from utils.db import WarehouseConnection
from utils.sde_config import get_warehouse_creds


def get_utc_from_unix_time(
    unix_ts: Optional[Any], second: int = 1000
) -> Optional[datetime.datetime]:
    """Returns a timezone-aware datetime object in UTC from a Unix timestamp."""

    if unix_ts:
        unix_ts_seconds = (
            int(unix_ts) / second
        )  # Convert milliseconds to seconds if needed
        return datetime.datetime.fromtimestamp(
            unix_ts_seconds, datetime.timezone.utc
        )  # Create timezone-aware UTC datetime
    else:
        return None


def get_token_data(token_ids, vs_currency) -> Dict[str, Any]:
    token_ids_str = ','.join(token_ids)
    URL = f"https://api.coingecko.com/api/v3/simple/price?ids={token_ids_str}&vs_currencies={vs_currency}&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true&precision=5"
    api_key = os.getenv('API_KEY', '')
    headers = {"x-cg-demo-api-key": api_key}
    response = requests.get(URL, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data:", response.status_code)
    return {}


def transform_to_add_datetime(token_data) -> pd.DataFrame:
    columns = [
        'token_name',
        'usd',
        'usd_market_cap',
        'usd_24h_vol',
        'usd_24h_change',
        'last_updated_at',
    ]
    df = pd.DataFrame(token_data).T.reset_index()
    df.columns = columns
    df['updated_dt'] = df['last_updated_at'].apply(get_utc_from_unix_time)
    df['updated_dt'] = df['updated_dt'].apply(
        lambda x: str(x.replace(tzinfo=None))
    )
    return df


def get_token_insert_query(data_frame: pd.DataFrame) -> str:
    return '''
        INSERT INTO defi.token (
        token_name, 
        usd, 
        usd_market_cap, 
        usd_24h_vol, 
        usd_24h_change,
        last_updated_at,
        updated_at
        )
        SELECT
            token_name, 
            usd, 
            usd_market_cap, 
            usd_24h_vol, 
            usd_24h_change,
            last_updated_at,
            updated_at
        FROM {}
        );
        '''.format(
        'data_frame'
    )


def write_to_postgres_from_data_frame(insert_query):
    with WarehouseConnection(get_warehouse_creds()).managed_cursor() as curr:
        curr.execute(insert_query)


def run_pipeline() -> None:

    token_ids = ['Solana', 'Marscoin', 'ethereum', 'bitcoin']
    vs_currency = 'usd'
    token_data = get_token_data(token_ids, vs_currency)
    data_frame = transform_to_add_datetime(token_data)
    insert_query = get_token_insert_query(data_frame)
    write_to_postgres_from_data_frame(insert_query)


if __name__ == '__main__':
    run_pipeline()
