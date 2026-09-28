# Databricks notebook source
# COMMAND ----------
# MAGIC %md
# MAGIC # Landing to Bronze Ingestion
# MAGIC Ingesta dinámica desde el Volume de Landing hacia las tablas Delta de la capa Bronze.

# COMMAND ----------
dbutils.widgets.text("source_system", "")
dbutils.widgets.text("table_name", "")
dbutils.widgets.text("landing_timestamp", "")
dbutils.widgets.text("source_file_format", "")

source_system = dbutils.widgets.get("source_system")
table_name = dbutils.widgets.get("table_name")
landing_timestamp = dbutils.widgets.get("landing_timestamp")
source_file_format = dbutils.widgets.get("source_file_format")

# COMMAND ----------
# Ruta en el Volume de Unity Catalog
base_landing_path = "/Volumes/adb_brewops_dev/landing/landing_volume"
source_path = f"{base_landing_path}/{source_system}"
table_path = f"{source_path}/{table_name}"
landing_path = f"{table_path}/{landing_timestamp}/"

def path_exists(path: str) -> bool:
    try:
        dbutils.fs.ls(path)
        return True
    except Exception:
        return False

missing_path = next((path for path in [source_path, table_path, landing_path] if not path_exists(path)), None)

if missing_path:
    message = (
        f"No new files received for source_system={source_system}, "
        f"table_name={table_name}, landing_timestamp={landing_timestamp}."
    )
    print(message)
    dbutils.notebook.exit(message)

# COMMAND ----------
# Lectura dinámica según el formato de archivo
if source_file_format == "csv":
    landing_df = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(landing_path)
else:
    landing_df = spark.read.format("parquet").load(landing_path)

# COMMAND ----------
# Auditoría: preservar timestamp de ingesta
from pyspark.sql import functions as F

updated_df = landing_df.withColumn("landing_timestamp", F.lit(landing_timestamp)) \
    .withColumn("insert_timestamp", F.current_timestamp())

# COMMAND ----------
# Escritura en modo Append en la capa Bronze
target_table = f"adb_brewops_dev.bronze.{table_name}"
updated_df.write.mode("append").saveAsTable(target_table)
print(f"[SUCCESS] Ingested into {target_table} successfully.")
