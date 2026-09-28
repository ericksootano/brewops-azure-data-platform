# Databricks notebook source
# DBTITLE 1,Dimensión Calendario
# MAGIC %md
# MAGIC # Prepare Calendar Table (Dimensión Fecha)
# MAGIC Genera la tabla `adb_brewops_dev.silver.calendar` para enriquecimiento temporal de ventas y producción.

# COMMAND ----------
# MAGIC %sql
# MAGIC CREATE SCHEMA IF NOT EXISTS adb_brewops_dev.silver;
# MAGIC
# MAGIC CREATE OR REPLACE TABLE adb_brewops_dev.silver.calendar AS
# MAGIC WITH dates AS (
# MAGIC   SELECT explode(
# MAGIC     sequence(
# MAGIC       TO_DATE('2020-01-01'),
# MAGIC       TO_DATE('2030-12-31'),
# MAGIC       INTERVAL 1 DAY
# MAGIC     )
# MAGIC   ) AS calendar_date
# MAGIC )
# MAGIC SELECT
# MAGIC   CAST(date_format(calendar_date, 'yyyyMMdd') AS INT) AS date_key,
# MAGIC   calendar_date AS date,
# MAGIC   year(calendar_date) AS year,
# MAGIC   quarter(calendar_date) AS quarter,
# MAGIC   ((month(calendar_date) - 1) % 3) + 1 AS month_of_quarter,
# MAGIC   month(calendar_date) AS month,
# MAGIC   date_format(calendar_date, 'MMMM') AS month_name,
# MAGIC   date_format(calendar_date, 'MMM') AS month_name_short,
# MAGIC   concat(year(calendar_date), '-', lpad(month(calendar_date), 2, '0')) AS year_month,
# MAGIC   concat(year(calendar_date), lpad(month(calendar_date), 2, '0')) AS year_month_key,
# MAGIC   weekofyear(calendar_date) AS week_of_year,
# MAGIC   concat(year(calendar_date), '-W', lpad(weekofyear(calendar_date), 2, '0')) AS year_week,
# MAGIC   day(calendar_date) AS day_of_month,
# MAGIC   dayofyear(calendar_date) AS day_of_year,
# MAGIC   weekday(calendar_date) + 1 AS iso_day_of_week,
# MAGIC   dayofweek(calendar_date) AS us_day_of_week,
# MAGIC   date_format(calendar_date, 'EEEE') AS day_name,
# MAGIC   date_format(calendar_date, 'E') AS day_name_short,
# MAGIC   CASE WHEN dayofweek(calendar_date) IN (1, 7) THEN true ELSE false END AS is_weekend,
# MAGIC   CASE WHEN calendar_date = trunc(calendar_date, 'month') THEN true ELSE false END AS is_month_start,
# MAGIC   CASE WHEN calendar_date = last_day(calendar_date) THEN true ELSE false END AS is_month_end,
# MAGIC   trunc(calendar_date, 'month') AS month_start_date,
# MAGIC   last_day(calendar_date) AS month_end_date,
# MAGIC   trunc(calendar_date, 'year') AS year_start_date,
# MAGIC   date_sub(add_months(trunc(calendar_date, 'year'), 12), 1) AS year_end_date
# MAGIC FROM dates;

# COMMAND ----------
# MAGIC %sql
# MAGIC SELECT COUNT(*) AS total_dias FROM adb_brewops_dev.silver.calendar;
