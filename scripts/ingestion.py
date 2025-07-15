from pyspark.sql import SparkSession
import logging
import os
import sys

os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-17-openjdk-amd64"
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_spark_session(app_name="DataIngestion") -> SparkSession:
    return SparkSession.builder.appName(app_name).getOrCreate()

def ingest_data(input_path="data/Ventas_diarias.csv", output_path="data/intermediate_ingested.parquet") -> str:
    try:
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Archivo no encontrado: {input_path}")

        spark = create_spark_session()
        df = spark.read.option("header", True).option("inferSchema", True).csv(input_path)

        if df.rdd.isEmpty():
            logging.warning("El archivo CSV está vacío.")
        else:
            logging.info(f"Ingestados {df.count()} registros con {len(df.columns)} columnas.")
            df.write.mode("overwrite").parquet(output_path)
            logging.info(f"Guardado en formato Parquet: {output_path}")
            df.printSchema()
            df.show(5)

        return "Ingesta completada correctamente"
    except Exception as e:
        logging.error(f"Error en la ingesta de datos: {e}")
        raise

if __name__ == "__main__":
    ingest_data()
