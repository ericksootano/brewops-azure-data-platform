# Databricks Lakeview Dashboard: BrewOps Executive Cockpit

## Prompt para Databricks Assistant / Genie (Generación Automática del Dashboard)
Copia y pega este prompt directamente en Databricks al editar tu Dashboard o en el asistente:

```text
Act as a Principal BI Engineer. Build an executive Lakeview dashboard using the tables in catalog 'adb_brewops_dev', schema 'gold'. 

Layout & Visualizations:
1. Header Row (KPI Cards):
   - Total Gross Revenue USD: SUM(gross_revenue_usd) from sales_performance_daily. Formatted as Currency ($).
   - Total Hectoliters Shipped: SUM(hl_shipped) from brewery_efficiency_summary. Formatted as Number with commas.
   - Total Active Distributors: COUNT(DISTINCT distributor_id) from distributor_360 where is_active = true.
   - Average Credit Utilization: AVG(credit_utilization_pct) from distributor_360. Formatted as Percentage (%).

2. Main Analytics Row:
   - Left Chart (Clustered Column Chart): Revenue by Region and Beer Category. 
     X-axis: brewery_region, Y-axis: gross_revenue_usd, Group by: beer_category.
   - Right Chart (Donut Chart): Volume Distribution by Package Type (Botella Retornable 650ml vs Lata 355ml vs Botella 350ml).
     Category: package_type, Value: SUM(total_liters_sold).

3. Operations & Risk Row:
   - Left Chart (Bar Chart): Brewery Capacity Utilization vs Monthly Capacity.
     X-axis: brewery_name, Y-axis: capacity_utilization_pct with threshold reference line at 80%.
   - Right Table (Executive Table): Distributor Risk Monitor.
     Columns: distributor_name, channel_type, city, credit_limit_usd, total_lifetime_spend_usd, credit_utilization_pct, last_order_date.
     Apply conditional formatting: Highlight red when credit_utilization_pct > 80%, yellow between 60% and 80%, green under 60%.

Filters:
- Add a Global Date Filter for 'order_date'.
- Add a Region Filter for 'brewery_region'.
```

---

## Configuración de Databricks Genie Space (Genie Agent en 3 pasos)

En el minuto 5:37:00 del video, el autor configura **Databricks Genie**:

1. En el menú izquierdo de Databricks, ve a **Genie Spaces** (o **Genie**).
2. Haz clic en **+ New** (o Create Genie Space):
   * **Title:** `BrewOps AI Data Assistant`
   * **Default Warehouse:** Selecciona tu SQL Warehouse (o clúster activo).
   * **Tables:** Selecciona las 3 tablas de la capa Gold:
     * `adb_brewops_dev.gold.sales_performance_daily`
     * `adb_brewops_dev.gold.distributor_360`
     * `adb_brewops_dev.gold.brewery_efficiency_summary`
3. **Instrucciones del Espacio (System Prompt para Genie):**
   Pega esto en la pestaña *Instructions* para que responda con conocimiento cervecero:
   ```text
   You are the BrewOps AI Business Analyst for a beverage enterprise.
   - 1 Hectoliter (hl) = 100 Liters.
   - Revenue figures are in USD.
   - Credit utilization over 80% represents a credit risk for a distributor.
   - Return clean markdown tables and charts whenever possible.
   ```
4. **Preguntas de prueba para impresionar en capturas/LinkedIn:**
   * *"Which region generated the highest revenue and what was the top selling beer category there?"*
   * *"Which distributors are exceeding 70% of their credit limit?"*
   * *"Compare the operational capacity utilization across all breweries."*
