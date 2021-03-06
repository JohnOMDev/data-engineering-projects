#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 31 23:45:14 2021

@author: john
"""
import os, sys
import logging
from datetime import timedelta, datetime
from airflow import DAG

from airflow.operators.python_operator import PythonOperator

from airflow.utils.dates import days_ago
sys.path.append('../../')
from etl import main as etl_main
from create_tables import main as create_main
from api_connection import get_exporo_data_to_df

logging.basicConfig(format="%(asctime)s %(name)s %(levelname)-10s %(message)s")
LOG = logging.getLogger("api_connector.py")
LOG.setLevel(os.environ.get("LOG_LEVEL", logging.DEBUG))


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(0,0,0,0,0),
    'email': ['contact@johnomole.me'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
    }

dag = DAG(
    'exporo-dag',
    default_args=default_args,
    description='Exporo api connection dag',
    schedule_interval=timedelta(days=1),
    )

run_table_create = PythonOperator(
    task_id='exporo_table_create_' + datetime.now().strftime("%Y_%m_%d"),
    python_callable=create_main,
    dag=dag
    )

run_api_connection = PythonOperator(
    task_id='exporo_api_connection_' + datetime.now().strftime("%Y_%m_%d"),
    python_callable=get_exporo_data_to_df,
    dag=dag
    )

run_etl = PythonOperator(
    task_id='exporo_etl' + datetime.now().strftime("%Y_%m_%d"),
    python_callable=etl_main,
    dag=dag
    )

run_table_create >> run_api_connection >> run_etl