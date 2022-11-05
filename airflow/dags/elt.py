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
    df_emotions_extracted = load.dataloader("/opt/airflow/data/emotions_extracted_data.csv")
    data.append(df_emotions_extracted)
    df_edge_data = load.dataloader("/opt/airflow/data/edge_data.csv")
    data.append(df_edge_data)
    df_object_count = load.dataloader("/opt/airflow/data/object_count_data.csv")
    data.append(df_object_count)
    df_start_frame_color = load.dataloader("/opt/airflow/data/start_frame_dom_colors.csv")
    data.append(df_start_frame_color)
    df_logo_data = load.dataloader("/opt/airflow/data/logo_data.csv")
    data.append(df_logo_data)
    df_output = load.dataloader("/opt/airflow/data/performance_data.csv")
    data.append(df_output)
    load.merge_data(data, "/opt/airflow/data/merged_data.csv")
    

def create_table():
    persist = Persistence()
    persist.create_table()
    

def insert_data_to_db():
    """Insert data to db"""
    load = Extract()
    persist = Persistence()
    df_emotions_extracted = load.dataloader("/opt/airflow/data/emotions_extracted_data.csv")
    persist.insert_data("face_emotions",df_emotions_extracted , persist.face_emotions_schema)
    df_edge_data = load.dataloader("/opt/airflow/data/edge_data.csv")
    persist.insert_data("edge",df_edge_data , persist.edge_schema)
    df_object_count = load.dataloader("/opt/airflow/data/object_count_data.csv")
    persist.insert_data("objects",df_object_count , persist.object_count_schema)
    df_start_frame_color = load.dataloader("/opt/airflow/data/start_frame_dom_colors.csv")
    persist.insert_data("colors", df_start_frame_color, persist.dominat_color_schema)
    df_logo_data = load.dataloader("/opt/airflow/data/logo_data.csv")
    persist.insert_data("logos", df_logo_data, persist.logo_schema)
    df_output = load.dataloader("/opt/airflow/data/performance_data.csv")
    persist.insert_data("performance", df_output, persist.performance_schema)

with DAG(
    dag_id='image-feature-orchestration',
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


