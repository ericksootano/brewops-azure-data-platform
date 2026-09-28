# Databricks notebook source
# COMMAND ----------
# MAGIC %md
# MAGIC # Bronze to Silver Transformation & Upsert (MERGE / FULL / APPEND)
# MAGIC Procesa datos de Bronze y aplica lógica idempotente en Silver con Delta Lake.

# COMMAND ----------
dbutils.widgets.text("landing_timestamp", "")
dbutils.widgets.text("table_name", "")
dbutils.widgets.text("merge_keys", "")
dbutils.widgets.text("load_type", "")

landing_timestamp = dbutils.widgets.get("landing_timestamp")
table_name = dbutils.widgets.get("table_name")
merge_keys = dbutils.widgets.get("merge_keys")
load_type = dbutils.widgets.get("load_type")

# COMMAND ----------
print("[STEP 1] Reading source bronze table")
source_query = f"SELECT * FROM adb_brewops_dev.bronze.{table_name} WHERE landing_timestamp = '{landing_timestamp}'"
print(f"[SOURCE QUERY] {source_query}")

bronze_df = spark.read.table(f"adb_brewops_dev.bronze.{table_name}").filter(
    f"landing_timestamp='{landing_timestamp}'"
)

print(f"[STEP 1 COMPLETE] Rows read: {bronze_df.count()}")
print(f"[SOURCE COLUMNS] {bronze_df.columns}")

# COMMAND ----------
from pyspark.sql import functions as F

print("[STEP 2] Preparing load metadata")
target_table = f"adb_brewops_dev.silver.{table_name}"
normalized_load_type = (load_type or "FULL").strip().upper()
merge_key_list = [key.strip() for key in merge_keys.split(",") if key.strip()]

print(f"[TARGET TABLE] {target_table}")
print(f"[LOAD TYPE] {normalized_load_type}")
print(f"[MERGE KEYS] {merge_key_list}")

if normalized_load_type == "MERGE":
    if not merge_key_list:
        raise ValueError("merge_keys must be provided when load_type is 'MERGE'.")
    missing_merge_keys = [key for key in merge_key_list if key not in bronze_df.columns]
    if missing_merge_keys:
        raise ValueError(f"merge_keys not found in source data: {missing_merge_keys}")

# Agregamos timestamps de auditoría para la capa Silver
updated_df = (
    bronze_df.withColumn("insert_timestamp", F.current_timestamp())
    .withColumn("update_timestamp", F.current_timestamp())
)

# COMMAND ----------
print(f"[STEP 3] Starting write to target table: {target_table}")

if normalized_load_type == "FULL":
    print(f"[WRITE MODE FULL] Overwriting target table {target_table}")
    updated_df.write.mode("overwrite").saveAsTable(target_table)
    print("[STEP 3 COMPLETE] FULL overwrite finished.")

elif normalized_load_type == "APPEND":
    print(f"[WRITE MODE APPEND] Appending records into {target_table}")
    updated_df.write.mode("append").saveAsTable(target_table)
    print("[STEP 3 COMPLETE] APPEND finished.")

elif normalized_load_type == "MERGE":
    print(f"[WRITE MODE MERGE] Performing Delta Upsert on {target_table}")
    target_exists = spark.catalog.tableExists(target_table)

    if not target_exists:
        print("[MERGE INITIAL] Target table does not exist. Creating table.")
        updated_df.write.mode("overwrite").saveAsTable(target_table)
        print("[STEP 3 COMPLETE] Initial table created.")
    else:
        source_view = "silver_merge_source"
        updated_df.createOrReplaceTempView(source_view)

        merge_condition = " AND ".join(
            [f"target.`{key}` = source.`{key}`" for key in merge_key_list]
        )
        update_assignments = ", ".join(
            [
                f"target.`{column}` = source.`{column}`"
                for column in updated_df.columns
                if column != "insert_timestamp"
            ]
        )
        insert_columns = ", ".join([f"`{column}`" for column in updated_df.columns])
        insert_values = ", ".join([f"source.`{column}`" for column in updated_df.columns])

        merge_sql = f"""
            MERGE INTO {target_table} AS target
            USING {source_view} AS source
            ON {merge_condition}
            WHEN MATCHED THEN UPDATE SET {update_assignments}
            WHEN NOT MATCHED THEN INSERT ({insert_columns})
            VALUES ({insert_values})
        """.strip()

        spark.sql(merge_sql)
        print("[STEP 3 COMPLETE] MERGE finished successfully.")

else:
    raise ValueError("load_type must be one of: FULL, APPEND, MERGE")

# COMMAND ----------
print("[STEP 4] Computing processed record count")
record_count = updated_df.count()
print(f"[STEP 4 COMPLETE] Processed record count: {record_count}")
dbutils.notebook.exit(str(record_count))
