from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "spark_data_pipeline",
    default_args=default_args,
    description="Data pipeline running on Apache Spark cluster",
    schedule_interval=timedelta(hours=1),
    catchup=False,
    tags=["spark", "analytics"],
) as dag:
    spark_job = SparkSubmitOperator(
        task_id="spark_data_pipeline_job",
        application="/opt/airflow/spark/data_pipeline_spark.py",
        name="spark_data_pipeline",
        conn_id="spark_local",
        dag=dag,
    )
