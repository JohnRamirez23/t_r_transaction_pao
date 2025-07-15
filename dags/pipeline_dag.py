from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from scripts.ingestion import ingest_data
from scripts.cleaning import clean_data
from scripts.transformation import transform_data
from scripts.load import load_data

default_args = {
    'owner': 'data_engineer',
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
}

with DAG(
        dag_id="pipeline_datos",
        default_args=default_args,
        description="Pipeline ETL de Ventas Diarias con PySpark y Airflow",
        schedule_interval="@daily",
        catchup=False
) as dag:

    t1 = PythonOperator(
        task_id="ingestion",
        python_callable=ingest_data,
        op_kwargs={
            "input_path": "data/Ventas_diarias.csv",
            "output_path": "data/intermediate_ingested.parquet"
        }
    )

    t2 = PythonOperator(
        task_id="cleaning",
        python_callable=clean_data,
        op_kwargs={
            "input_path": "data/intermediate_ingested.parquet",
            "output_path": "data/intermediate_cleaned.parquet"
        }
    )

    t3 = PythonOperator(
        task_id="transformation",
        python_callable=transform_data,
        op_kwargs={
            "input_path": "data/intermediate_cleaned.parquet",
            "output_path": "data/intermediate_transformed.parquet"
        }
    )

    t4 = PythonOperator(
        task_id="load",
        python_callable=load_data,
        op_kwargs={
            "input_path": "data/intermediate_transformed.parquet",
            "db_url": "jdbc:mysql://mysql:3306/ventas_db",
            "table_name": "resumen_ventas",
            "user": "user",
            "password": "password"
        }
    )

    t1 >> t2 >> t3 >> t4
