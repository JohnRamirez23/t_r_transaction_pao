FROM apache/airflow:2.8.1-python3.10

USER root

# Instala Java y herramientas necesarias
RUN apt-get update && \
    apt-get install -y default-jdk curl bash ca-certificates && \
    apt-get clean

# Variables de entorno para Spark y Java
ENV SPARK_VERSION=3.5.1
ENV HADOOP_PROFILE=hadoop3
ENV SPARK_HOME=/opt/spark
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="$SPARK_HOME/bin:$PATH"

# Instala Spark 3.5.1 (descarga oficial, URL válida)
RUN curl -fSL https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-${HADOOP_PROFILE}.tgz | \
    tar -xz -C /opt/ && \
    mv /opt/spark-${SPARK_VERSION}-bin-${HADOOP_PROFILE} $SPARK_HOME

# Fuerza Spark a usar Python 3.10 para driver y worker
ENV PYSPARK_PYTHON=/usr/local/bin/python
ENV PYSPARK_DRIVER_PYTHON=/usr/local/bin/python

# Regresa al usuario airflow
USER airflow

# Instala dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
