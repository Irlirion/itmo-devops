from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import random
import json

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
}


def generate_data(**context):
    data = [random.randint(1, 100) for _ in range(50)]
    context["task_instance"].xcom_push(key="raw_data", value=data)
    print(f"Generated {len(data)} random numbers")
    return data


def calculate_statistics(**context):
    data = context["task_instance"].xcom_pull(key="raw_data", task_ids="generate_data")
    total = sum(data)
    average = total / len(data)
    minimum = min(data)
    maximum = max(data)

    stats = {
        "total": total,
        "average": round(average, 2),
        "min": minimum,
        "max": maximum,
        "count": len(data),
    }

    context["task_instance"].xcom_push(key="statistics", value=stats)
    print(f"Statistics: {stats}")
    return stats


def transform_data(**context):
    data = context["task_instance"].xcom_pull(key="raw_data", task_ids="generate_data")
    stats = context["task_instance"].xcom_pull(task_ids="calculate_statistics")

    transformed = [x * 2 for x in data]
    above_avg = [x for x in transformed if x > stats["average"] * 2]

    result = {
        "transformed_count": len(transformed),
        "above_average_count": len(above_avg),
        "original_avg": stats["average"],
        "transformed_avg": round(sum(transformed) / len(transformed), 2),
    }

    print(f"Transformed data: {result}")
    return result


def save_results(**context):
    stats = context["task_instance"].xcom_pull(task_ids="calculate_statistics")
    transformed = context["task_instance"].xcom_pull(task_ids="transform_data")

    result = {
        "generated_at": datetime.now().isoformat(),
        "statistics": stats,
        "transformation": transformed,
    }

    with open("/opt/airflow/output/result.json", "w") as f:
        json.dump(result, f, indent=2)

    print(f"Results saved to /opt/airflow/output/result.json")
    return result


with DAG(
    "data_pipeline_dag",
    default_args=default_args,
    description="Data processing pipeline with statistics calculation",
    schedule_interval=timedelta(hours=1),
    catchup=False,
    tags=["analytics", "pipeline"],
) as dag:
    start_task = BashOperator(
        task_id="start",
        bash_command='echo "Starting data pipeline"',
    )

    generate_data_task = PythonOperator(
        task_id="generate_data",
        python_callable=generate_data,
    )

    calculate_stats_task = PythonOperator(
        task_id="calculate_statistics",
        python_callable=calculate_statistics,
    )

    transform_task = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data,
    )

    save_results_task = PythonOperator(
        task_id="save_results",
        python_callable=save_results,
    )

    end_task = BashOperator(
        task_id="end",
        bash_command='echo "Pipeline completed successfully"',
    )

    (
        start_task
        >> generate_data_task
        >> calculate_stats_task
        >> transform_task
        >> save_results_task
        >> end_task
    )
