from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
from Getdata import team,player

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2020, 11, 8),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'GCP_dag',
    default_args=default_args,
    description='GCP dag',
    schedule_interval=timedelta(days=1),
)

run1 = PythonOperator(
    task_id='allteam',
    python_callable=team,
    dag=dag, 
)
run2 = PythonOperator(
    task_id='playerstat',
    python_callable=player,
    dag=dag, 
)



run1>>run2