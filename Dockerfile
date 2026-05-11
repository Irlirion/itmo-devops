FROM apache/airflow:2.7.1

WORKDIR /opt/airflow

USER root
RUN apt-get update && apt-get -y install procps default-jre && apt-get clean && rm -rf /var/lib/apt/lists/*

USER airflow
COPY ./dags/* ./dags/
COPY ./spark/* ./spark/

RUN pip3 install apache-airflow-providers-apache-spark==4.1.1 pyspark==3.5.0

ENV SPARK_HOME=/home/airflow/.local/lib/python3.8/site-packages/pyspark
ENV PATH="${SPARK_HOME}/bin:${PATH}"
