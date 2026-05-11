# CHANGES

## Lab 3 (vs Lab 2)

### GitHub Actions CI/CD
- Added `.github/workflows/lab3-ci-cd.yml` as a GitHub Actions adaptation of the GitLab CI/CD assignment
- Added `test` job that runs on every branch and checks that `dags/`, `spark/`, `Dockerfile`, and `docker-compose.yml` exist
- Added Python syntax validation for DAG and Spark scripts
- Added Docker Compose configuration validation with `docker compose config --quiet`
- Added `build` job that builds the Airflow Docker image after successful tests
- Configured `build` to skip automatic runs for branches with the `feature/` prefix while still allowing manual `workflow_dispatch`
- Added `deploy` job that runs `docker compose up -d --build`
- Configured automatic deploy only for pushes to `main`, `master`, and `develop`
- Added manual deploy option through `workflow_dispatch` input `deploy`
- Pinned jobs to the GitHub Actions runner label `ubuntu-latest`, which is the GitHub Actions equivalent of selecting a tagged runner

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
