# Databricks notebook source
# DBTITLE 1,Capa Gold: Resumen Diario de Rendimiento y Ventas
# MAGIC %md
# MAGIC # NB_sales_performance_daily
# MAGIC Construye `adb_brewops_dev.gold.sales_performance_daily` agregando órdenes, marcas, plantas cerveceras y calendario.

# COMMAND ----------
# MAGIC %sql
# MAGIC CREATE SCHEMA IF NOT EXISTS adb_brewops_dev.gold;
# MAGIC
# MAGIC CREATE OR REPLACE TABLE adb_brewops_dev.gold.sales_performance_daily AS
# MAGIC WITH daily_sales AS (
# MAGIC   SELECT
# MAGIC     brewery_id,
# MAGIC     brand_id,
# MAGIC     order_date,
# MAGIC     CAST(COUNT(order_id) AS INT) AS total_orders,
# MAGIC     CAST(COUNT(DISTINCT distributor_id) AS INT) AS active_distributors_count,
# MAGIC     CAST(SUM(crates_ordered) AS INT) AS total_crates_sold,
# MAGIC     CAST(SUM(total_liters) AS DECIMAL(12,2)) AS total_liters_sold,
# MAGIC     CAST(SUM(total_amount_usd) AS DECIMAL(14,2)) AS gross_revenue_usd,
# MAGIC     CAST(SUM(CASE WHEN status = 'Delivered' THEN total_amount_usd ELSE 0 END) AS DECIMAL(14,2)) AS delivered_revenue_usd
# MAGIC   FROM adb_brewops_dev.silver.orders
# MAGIC   GROUP BY brewery_id, brand_id, order_date
# MAGIC )
# MAGIC SELECT
# MAGIC   s.order_date,
# MAGIC   c.year,
# MAGIC   c.quarter,
# MAGIC   c.month_name,
# MAGIC   c.day_name,
# MAGIC   c.is_weekend,
# MAGIC   bw.brewery_name,
# MAGIC   bw.city AS brewery_city,
# MAGIC   bw.region AS brewery_region,
# MAGIC   b.brand_name,
# MAGIC   b.category AS beer_category,
# MAGIC   b.package_type,
# MAGIC   b.unit_price_usd,
# MAGIC   s.total_orders,
# MAGIC   s.active_distributors_count,
# MAGIC   s.total_crates_sold,
# MAGIC   s.total_liters_sold,
# MAGIC   s.gross_revenue_usd,
# MAGIC   s.delivered_revenue_usd,
# MAGIC   ROUND(s.gross_revenue_usd / NULLIF(s.total_liters_sold, 0), 2) AS revenue_per_liter_usd,
# MAGIC   current_timestamp() AS gold_ingestion_timestamp
# MAGIC FROM daily_sales s
# MAGIC LEFT JOIN adb_brewops_dev.silver.breweries bw ON s.brewery_id = bw.brewery_id
# MAGIC LEFT JOIN adb_brewops_dev.silver.brands b ON s.brand_id = b.brand_id
# MAGIC LEFT JOIN adb_brewops_dev.silver.calendar c ON s.order_date = c.date;

# COMMAND ----------
# MAGIC %sql
# MAGIC SELECT * FROM adb_brewops_dev.gold.sales_performance_daily LIMIT 10;
