import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.sensors.filesystem import FileSensor
from docker.types import Mount

BASE_DIR = os.getenv("PROJECT_DIR", "/opt/airflow")

default_args = {
    'owner': 'tradecorp',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

MOUNTS = [
    Mount(source=f"{BASE_DIR}/src", target="/home/jovyan/src", type="bind"),
    Mount(source=f"{BASE_DIR}/data", target="/home/jovyan/data", type="bind"),
    Mount(source=f"{BASE_DIR}/.env", target="/home/jovyan/.env", type="bind"),
]

with DAG(
    'tradecorp_etl_pipeline',
    default_args=default_args,
    description='Pipeline ETL Tradecorp',
    schedule='0 6 * * *',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['tradecorp', 'etl', 'spark'],
) as dag:

    wait_for_trigger = FileSensor(
        task_id='wait_for_trigger',
        filepath='/opt/airflow/data/trigger/go.txt',
        poke_interval=30,
        timeout=3600,
        mode='reschedule',
    )

    fetch_exchange_rates = BashOperator(
        task_id='fetch_exchange_rates',
        bash_command='python /opt/airflow/src/fetch_exchange_rates.py',
    )

    reader = DockerOperator(
        task_id='reader',
        image='tradecorp-spark',
        container_name='airflow_reader',
        api_version='auto',
        auto_remove=True,
        mount_tmp_dir=False,
        command='spark-submit --master local[*] /home/jovyan/src/reader.py',
        docker_url='unix://var/run/docker.sock',
        network_mode='tradecorp_default',
        mounts=MOUNTS,
        tty=True,
        force_pull=False,
    )

    transformer = DockerOperator(
        task_id='transformer',
        image='tradecorp-spark',
        container_name='airflow_transformer',
        api_version='auto',
        auto_remove=True,
        mount_tmp_dir=False,
        command='spark-submit --master local[*] /home/jovyan/src/transformer.py',
        docker_url='unix://var/run/docker.sock',
        network_mode='tradecorp_default',
        mounts=MOUNTS,
        tty=True,
        force_pull=False,
    )

    writer = DockerOperator(
        task_id='writer',
        image='tradecorp-spark',
        container_name='airflow_writer',
        api_version='auto',
        auto_remove=True,
        mount_tmp_dir=False,
        command='spark-submit --master local[*] /home/jovyan/src/writer.py',
        docker_url='unix://var/run/docker.sock',
        network_mode='tradecorp_default',
        mounts=MOUNTS,
        tty=True,
        force_pull=False,
    )

    wait_for_trigger >> fetch_exchange_rates >> reader >> transformer >> writer