from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum
import logging
import os
import sys

os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-17-openjdk-amd64"
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_spark_session(app_name="DataTransformation") -> SparkSession:
    return SparkSession.builder.appName(app_name).getOrCreate()

def transform_data(input_path="data/intermediate_cleaned.parquet", output_path="data/intermediate_transformed.parquet") -> str:
    try:
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Archivo no encontrado: {input_path}")

        spark = create_spark_session()
        df = spark.read.parquet(input_path)

        logging.info(f"[Transformación] Registros leídos: {df.count()}")

        required_cols = ["fecha_transaccion", "canal", "total_venta"]
        for col_name in required_cols:
            if col_name not in df.columns:
                raise ValueError(f"Falta columna requerida: {col_name}")

        df_agg = df.groupBy("fecha_transaccion", "canal").agg(
            spark_sum(col("total_venta")).alias("total_venta_diaria")
        ).withColumnRenamed("fecha_transaccion", "fecha")

        df_agg.write.mode("overwrite").parquet(output_path)
        logging.info(f"[Transformación] Guardado en: {output_path}")
        df_agg.show(5)

        return "Transformación completada correctamente"
    except Exception as e:
        logging.error(f"[Transformación] Error: {e}")
        raise

if __name__ == "__main__":
    transform_data()
