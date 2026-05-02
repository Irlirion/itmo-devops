# Lab 1: Apache Airflow with Docker Compose

## Description

This project deploys Apache Airflow 2.7.1 using Docker Compose and includes a custom data processing DAG.

## Files

- `Dockerfile` - Custom Airflow image with DAGs
- `docker-compose.yml` - Docker Compose configuration
- `dags/data_pipeline.py` - Custom DAG with data processing pipeline

## DAG Overview

The `data_pipeline_dag` performs the following tasks:

1. **generate_data** - Generates 50 random numbers
2. **calculate_statistics** - Calculates total, average, min, max
3. **transform_data** - Multiplies data by 2 and filters above average
4. **save_results** - Saves results to JSON file
5. **start/end** - Bash operators for logging

## Deployment

### Prerequisites

- Docker
- Docker Compose

### Steps

1. Build and start containers:
   ```bash
   docker-compose up -d --build
   ```

2. Wait for containers to become healthy:
   ```bash
   docker ps
   ```

3. Access Airflow UI at: http://localhost:8080/
   - Username: `airflow`
   - Password: `airflow`

4. The DAG should appear in the Airflow UI and can be triggered manually.

## Cleanup

```bash
docker-compose down -v
```