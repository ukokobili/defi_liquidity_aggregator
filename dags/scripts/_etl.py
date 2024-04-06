from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from python.liquidity_aggregator import run_pipeline
from utils.utils import execute_query_with_conn

# Define the DAG
dag = DAG(
    dag_id="defi_data_pipeline",
    start_date=datetime(2024, 4, 6),  # Set your desired start date
    schedule_interval="10 * * * *",  # Replace with a suitable schedule if needed
)

# Define tasks for each step of the pipeline
extract_transform_data = PythonOperator(
    task_id="extract_transform_data",
    python_callable=run_pipeline,
    # op_kwargs={"file_path": "./data/customers.csv"},
    dag=dag,
)

establish_db_connection = PythonOperator(
    task_id="establish_db_connection",
    python_callable=execute_query_with_conn,
    # op_kwargs={"file_path": "./data/orders.csv"},
    dag=dag,
)


# ... (Similar tasks for cleaning orders and products)

# merge_data_task = PythonOperator(
#     task_id="merge_data",
#     python_callable=merge_data,
#     op_kwargs={
#         "clean_customers_data": "{{ ti.xcom_pull(task_ids='clean_customers') }}",
#         "clean_orders_data": "{{ ti.xcom_pull(task_ids='clean_orders') }}",
#         "clean_products_data": "{{ ti.xcom_pull(task_ids='clean_products') }}",
#     },
#     dag=dag,
# )

# load_data_task = PythonOperator(
#     task_id="load_data",
#     python_callable=load_data,
#     op_kwargs={
#         "db_data": "{{ ti.xcom_pull(task_ids='merge_data') }}",
#         "database_name": "ecommerce.db",
#         "table_name": "ecommerce_data",
#     },
#     dag=dag,
# )

extract_transform_data