import os

import psycopg2

from airflow.hooks.postgres_hook import PostgresHook


def execute_query_with_conn(qry: str) -> None:
    hook = PostgresHook(postgres_conn_id="defi_connection")
    conn = hook.get_conn()
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    cursor.execute(qry)
    cursor.close()
    conn.commit()
