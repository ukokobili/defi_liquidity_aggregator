import os
import pandas as pd
import psycopg2

from airflow.hooks.postgres_hook import PostgresHook


def establish_database_conn(qry: str, transform_data: pd.DataFrame) -> None:
    hook = PostgresHook(postgres_conn_id="defi_connection")
    conn = hook.get_conn()
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    for d in transform_data:
        cursor.execute(qry, d)
    cursor.close()
    conn.commit()
