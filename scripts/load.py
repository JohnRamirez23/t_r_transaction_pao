from pyspark.sql import SparkSession
import logging
import os
import sys

os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-17-openjdk-amd64"
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_spark_session(app_name="DataLoad") -> SparkSession:
    return SparkSession.builder \
        .appName(app_name) \
        .config("spark.jars.packages", "mysql:mysql-connector-java:8.0.33") \
        .getOrCreate()

def load_data(input_path="data/intermediate_transformed.parquet", db_url="jdbc:mysql://mysql:3306/ventas_db",
              table_name="resumen_ventas", user="user", password="password") -> str:
    try:
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Archivo no encontrado: {input_path}")

        spark = create_spark_session()
        df = spark.read.parquet(input_path)

        logging.info(f"[Carga] Registros a insertar: {df.count()}")

        df.write \
            .format("jdbc") \
            .option("url", db_url) \
            .option("dbtable", table_name) \
            .option("user", user) \
            .option("password", password) \
            .option("driver", "com.mysql.cj.jdbc.Driver") \
            .mode("overwrite") \
            .save()

        logging.info(f"[Carga] Cargados correctamente en la tabla `{table_name}`.")
        return "Carga completada correctamente"
    except Exception as e:
        logging.error(f"[Carga] Error al cargar los datos: {e}")
        raise

if __name__ == "__main__":
    load_data()
