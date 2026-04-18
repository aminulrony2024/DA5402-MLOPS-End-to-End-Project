"""
Airflow DAG for FinPredict Data Pipeline
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from data_ingestion import load_raw_data
from data_validation import validate_schema
from data_cleaning import clean_data
from feature_engineering import engineer_features
from encode_and_scale import encode_and_scale
from split_data import split_and_save
from trigger_training import trigger_training

DEFAULT_ARGS = {
    'owner': 'finpredict',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='finpredict_data_pipeline',
    default_args=DEFAULT_ARGS,
    description='FinPredict end-to-end data ingestion and training pipeline',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    tags=['finpredict', 'mlops'],
) as dag:

    t1 = PythonOperator(task_id='data_ingestion',      python_callable=load_raw_data)
    t2 = PythonOperator(task_id='data_validation',     python_callable=validate_schema)
    t3 = PythonOperator(task_id='data_cleaning',       python_callable=clean_data)
    t4 = PythonOperator(task_id='feature_engineering', python_callable=engineer_features)
    t5 = PythonOperator(task_id='encode_and_scale',    python_callable=encode_and_scale)
    t6 = PythonOperator(task_id='train_test_split',    python_callable=split_and_save)
    t7 = PythonOperator(task_id='trigger_training',    python_callable=trigger_training)

    t1 >> t2 >> t3 >> t4 >> t5 >> t6 >> t7
