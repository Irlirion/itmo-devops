# CHANGES

## Lab 2 (vs Lab 1)

### Dockerfile
- Added `USER root` / `USER airflow` blocks to install system packages as root
- Installed `procps` and `default-jre` (required for `spark-submit` inside the container)
- Added `COPY ./spark/* ./spark/` to include Spark job scripts
- Installed Python packages: `apache-airflow-providers-apache-spark==4.1.1`, `pyspark==3.5.0`
- Set `SPARK_HOME` and updated `PATH` to point to the pyspark distribution

### docker-compose.yml
- Added `./spark:/opt/airflow/spark` and `./logs:/opt/airflow/logs` volume mounts to all Airflow services
- Added `SPARK_HOME` environment variable to all Airflow services
- Added `spark-master` service (`apache/spark:3.5.0`) with healthcheck on port 7077
- Added `spark-worker` service connected to `spark-master:7077`
- Updated `airflow-init` to depend on `spark-master` and `spark-worker` (healthy) — enforces startup order: postgres → spark-master → spark-worker → airflow-init → airflow
- Added automatic `spark_local` connection creation in `airflow-init`

### New files
- `spark/data_pipeline_spark.py` — PySpark job (generates data, computes stats, transforms, saves JSON)
- `dags/spark_pipeline.py` — Airflow DAG using `SparkSubmitOperator`
