from __future__ import annotations

# [START tutorial]
# [START import_module]
from datetime import datetime, timedelta
from textwrap import dedent

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.python import PythonOperator, get_current_context
from airflow.operators.bash import BashOperator


def setup_env():
    import os
    if not os.path.exists("tmp_data"):
        os.mkdir("tmp_data")

def read_daily_data():
    import pandas as pd
    import glob
    import os

    context = get_current_context()
    execution_date = context["execution_date"]

    year = execution_date.strftime("%Y")
    month = execution_date.strftime("%m")
    day = execution_date.strftime("%d")
    parent_path = f"raw_data/year={year}/month={month}/day={day}/"
    
    files = []
    for hour in range(25):
        hourly_path = f"{parent_path}/hour={hour}"
        for filename in os.listdir(hourly_path):
            files.append(f"{hourly_path}/{filename}")
    df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

    destination_path = f"tmp_data/{execution_date.strftime('%Y-%m-%d')}"
    if not os.path.exists(destination_path):
        os.mkdir(destination_path)

    df.to_csv(f"{destination_path}/load.csv", index=False)


def clean_data():
    import pandas as pd

    context = get_current_context()
    execution_date = context["execution_date"]

    df = pd.read_csv(f"tmp_data/{execution_date.strftime('%Y-%m-%d')}/load.csv")

    df["is_logged"] = df["is_logged"].astype('bool')
    df["date"] = execution_date.date()

    df.to_csv(f"tmp_data/{execution_date.strftime('%Y-%m-%d')}/clean.csv", index=False)

def load_into_db():
    from sqlalchemy import create_engine
    import pandas as pd

    context = get_current_context()
    execution_date = context["execution_date"]

    df = pd.read_csv(f"tmp_data/{execution_date.strftime('%Y-%m-%d')}/clean.csv")[1:]

    engine = create_engine('postgresql://airflow:airflow@postgres:5432/postgres')
    df.to_sql(name="raw_data", schema="public", con=engine, if_exists="append", index=False)

def cleanup_env():
    import shutil
    context = get_current_context()
    execution_date = context["execution_date"]

    shutil.rmtree(f"tmp_data/{execution_date.strftime('%Y-%m-%d')}/")


with DAG(
    "raw_data_load",
    description="Sample DAG to load raw_data into DB",
    schedule=timedelta(days=1),
    start_date=datetime(2023, 10, 1),
    catchup=True
) as dag:

    setup_env = PythonOperator(
        task_id="setup_env",
        python_callable=setup_env,
        dag=dag
    )

    read_daily_data = PythonOperator(
        task_id="read_daily_data",
        python_callable=read_daily_data,
        dag=dag
    )

    clean_data = PythonOperator(
        task_id="clean_data",
        python_callable=clean_data,
        dag=dag
    )

    load_into_db = PythonOperator(
        task_id="load_into_db",
        python_callable=load_into_db,
        dag=dag
    )

    cleanup_env = PythonOperator(
        task_id="cleanup_env",
        python_callable=cleanup_env,
        dag=dag
    )

    setup_env >> read_daily_data >> clean_data >> load_into_db >> cleanup_env
