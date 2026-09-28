# Databricks notebook source
# DBTITLE 1,Capa Gold: Visión 360 del Distribuidor
# MAGIC %md
# MAGIC # NB_distributor_360
# MAGIC Construye `adb_brewops_dev.gold.distributor_360` agregando el comportamiento de compra, límites de crédito y métricas de entrega por distribuidor.

# COMMAND ----------
# MAGIC %sql
# MAGIC CREATE SCHEMA IF NOT EXISTS adb_brewops_dev.gold;
# MAGIC
# MAGIC CREATE OR REPLACE TABLE adb_brewops_dev.gold.distributor_360 AS
# MAGIC WITH order_summary AS (
# MAGIC   SELECT
# MAGIC     distributor_id,
# MAGIC     CAST(COUNT(order_id) AS INT) AS total_lifetime_orders,
# MAGIC     CAST(SUM(crates_ordered) AS INT) AS total_lifetime_crates,
# MAGIC     CAST(SUM(total_liters) AS DECIMAL(14,2)) AS total_lifetime_liters,
# MAGIC     CAST(SUM(total_amount_usd) AS DECIMAL(14,2)) AS total_lifetime_spend_usd,
# MAGIC     MAX(order_date) AS last_order_date,
# MAGIC     MIN(order_date) AS first_order_date
# MAGIC   FROM adb_brewops_dev.silver.orders
# MAGIC   GROUP BY distributor_id
# MAGIC )
# MAGIC SELECT
# MAGIC   d.distributor_id,
# MAGIC   d.distributor_name,
# MAGIC   d.channel_type,
# MAGIC   d.city,
# MAGIC   d.credit_limit_usd,
# MAGIC   d.is_active,
# MAGIC   COALESCE(os.total_lifetime_orders, 0) AS total_lifetime_orders,
# MAGIC   COALESCE(os.total_lifetime_crates, 0) AS total_lifetime_crates,
# MAGIC   COALESCE(os.total_lifetime_liters, 0.00) AS total_lifetime_liters,
# MAGIC   COALESCE(os.total_lifetime_spend_usd, 0.00) AS total_lifetime_spend_usd,
# MAGIC   ROUND(COALESCE(os.total_lifetime_spend_usd, 0.00) / NULLIF(d.credit_limit_usd, 0) * 100, 2) AS credit_utilization_pct,
# MAGIC   os.first_order_date,
# MAGIC   os.last_order_date,
# MAGIC   current_timestamp() AS gold_ingestion_timestamp
# MAGIC FROM adb_brewops_dev.silver.distributors d
# MAGIC LEFT JOIN order_summary os ON d.distributor_id = os.distributor_id;

# COMMAND ----------
# MAGIC %sql
# MAGIC SELECT * FROM adb_brewops_dev.gold.distributor_360;
