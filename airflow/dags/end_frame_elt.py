from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import pandas as pd
import sys
import os
from scripts.extract import Extract
from scripts.persistence import Persistence

default_args = {
    'owner': 'reiten',
    'depends_on_past': False,
    'email': ['haylemicheal.mekonnen.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'start_date': datetime(2022, 11, 5),
    'retry_delay': timedelta(minutes=5)
}


def read_and_merge_data():
    """csv data reading
    """
    load = Extract()
    data = []
    df_emotions_extracted = load.dataloader("/opt/airflow/data/endframe_emotions_extracted_data.csv")
    data.append(df_emotions_extracted)
    df_object_count = load.dataloader("/opt/airflow/data/endframe_object_count_data.csv")
    data.append(df_object_count)
    df_end_frame_color = load.dataloader("/opt/airflow/data/end_frame_dom_colors.csv")
    data.append(df_end_frame_color)
    df_cta_data = load.dataloader("/opt/airflow/data/cta_data.csv")
    data.append(df_cta_data)
    df_output = load.dataloader("/opt/airflow/data/performance_data.csv")
    data.append(df_output)
    load.merge_data(data, "/opt/airflow/data/endframe_merged_data.csv")
def create_table():
    print("Create table")

def insert_data_to_db():
    print("Insert data")


with DAG(
    dag_id='image-feature-orchestration_endframe',
    default_args=default_args,
    description='Read csv, extract, and put to postgres',
    schedule_interval='@once',
    catchup=False
) as dag:
    data_reader_merger = PythonOperator(
        task_id='read_data_and_merge',
        python_callable=read_and_merge_data
    )
    table_creator = PythonOperator(
        task_id='table_creator',
        python_callable=create_table
    )
    insert_data = PythonOperator(
        task_id='insert_data_to_db',
        python_callable=insert_data_to_db
    )

data_reader_merger>>table_creator>>insert_data


