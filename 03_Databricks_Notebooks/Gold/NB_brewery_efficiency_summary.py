# Databricks notebook source
# DBTITLE 1,Capa Gold: Eficiencia y Utilización de Plantas Cerveceras
# MAGIC %md
# MAGIC # NB_brewery_efficiency_summary
# MAGIC Construye `adb_brewops_dev.gold.brewery_efficiency_summary` evaluando el volumen despachado respecto a la capacidad instalada por cervecería.

# COMMAND ----------
# MAGIC %sql
# MAGIC CREATE SCHEMA IF NOT EXISTS adb_brewops_dev.gold;
# MAGIC
# MAGIC CREATE OR REPLACE TABLE adb_brewops_dev.gold.brewery_efficiency_summary AS
# MAGIC WITH monthly_output AS (
# MAGIC   SELECT
# MAGIC     brewery_id,
# MAGIC     trunc(order_date, 'month') AS production_month,
# MAGIC     CAST(SUM(total_liters) AS DECIMAL(14,2)) AS liters_shipped,
# MAGIC     -- 1 Hectolitro (hl) = 100 Litros
# MAGIC     ROUND(SUM(total_liters) / 100.0, 2) AS hl_shipped
# MAGIC   FROM adb_brewops_dev.silver.orders
# MAGIC   GROUP BY brewery_id, trunc(order_date, 'month')
# MAGIC )
# MAGIC SELECT
# MAGIC   b.brewery_id,
# MAGIC   b.brewery_name,
# MAGIC   b.city,
# MAGIC   b.region,
# MAGIC   b.brewery_type,
# MAGIC   b.capacity_hl AS monthly_capacity_hl,
# MAGIC   m.production_month,
# MAGIC   COALESCE(m.liters_shipped, 0.00) AS total_liters_shipped,
# MAGIC   COALESCE(m.hl_shipped, 0.00) AS total_hl_shipped,
# MAGIC   ROUND(COALESCE(m.hl_shipped, 0.00) / NULLIF(b.capacity_hl, 0) * 100, 2) AS capacity_utilization_pct,
# MAGIC   current_timestamp() AS gold_ingestion_timestamp
# MAGIC FROM adb_brewops_dev.silver.breweries b
# MAGIC LEFT JOIN monthly_output m ON b.brewery_id = m.brewery_id;

# COMMAND ----------
# MAGIC %sql
# MAGIC SELECT * FROM adb_brewops_dev.gold.brewery_efficiency_summary;
