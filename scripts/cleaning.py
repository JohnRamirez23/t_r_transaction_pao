from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date
import logging
import os
import sys

os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-17-openjdk-amd64"
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_spark_session(app_name="DataCleaning") -> SparkSession:
    return SparkSession.builder.appName(app_name).getOrCreate()

def clean_data(input_path="data/intermediate_ingested.parquet", output_path="data/intermediate_cleaned.parquet") -> str:
    try:
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Archivo no encontrado: {input_path}")

        spark = create_spark_session()
        df = spark.read.parquet(input_path)

        logging.info(f"[Limpieza] Registros originales: {df.count()}")

        required_cols = ["cliente_id", "fecha_transaccion"]
        for col_name in required_cols:
            if col_name not in df.columns:
                raise ValueError(f"Falta columna obligatoria: {col_name}")

        df_clean = df.dropDuplicates().dropna(subset=required_cols)
        df_clean = df_clean.withColumn("fecha_transaccion", to_date(col("fecha_transaccion")))

        df_clean.write.mode("overwrite").parquet(output_path)
        logging.info(f"[Limpieza] Registros limpios: {df_clean.count()}")
        df_clean.show(5)

        return "Limpieza completada correctamente"
    except Exception as e:
        logging.error(f"[Limpieza] Error: {e}")
        raise

if __name__ == "__main__":
    clean_data()
