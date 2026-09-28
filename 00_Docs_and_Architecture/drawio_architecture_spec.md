# 🍺 BrewOps Platform — Arquitectura y Especificación Técnica para Draw.io / Excalidraw

Este documento contiene la estructura visual completa, cajas, conexiones y texto exacto para diagramar en **Draw.io** o **Excalidraw**.

---

## 1. Código Mermaid (Importable directamente en Draw.io: Arrange -> Insert -> Advanced -> Mermaid)

```mermaid
flowchart LR
    %% Subgraph Orígenes
    subgraph Fuentes ["1. Capa de Fuentes Operacionales"]
        P["Neon PostgreSQL (OLTP)\n- breweries (Full)\n- brands (Full)\n- distributors (Merge)\n- orders (Merge)"]
        CSV["ADLS Gen2 Feeds (CSV)\n- raw_material_prices.csv\n- fleet_telemetry.csv"]
    end

    %% Subgraph Seguridad y Metadatos
    subgraph Governance ["2. Seguridad & Control"]
        KV["Azure Key Vault\n(Secretos & Managed Identity)"]
        SQL[("Azure SQL DB (Serverless)\nctrl.table_config\nctrl.watermark\nctrl.audit_log")]
    end

    %% Subgraph Orquestación ADF
    subgraph Orquestacion ["3. Orquestador Azure Data Factory"]
        M["PL_MASTER"] --> S2S["PL_SOURCE_TO_SILVER_MAIN"]
        S2S --> S2G["PL_SILVER_TO_GOLD"]
        S2S -->|ForEach table_id| IN["PL_SOURCE_TO_SILVER_INNER"]
    end

    %% Subgraph Lakehouse Medallion
    subgraph Databricks ["4. Azure Databricks (Unity Catalog Lakehouse)"]
        direction TB
        VOL["Landing Volume\n(/Volumes/landing_volume)"] --> BZ["Capa BRONZE (Delta)\nData Cruda Inmutable\n+ landing_timestamp"]
        BZ -->|MERGE INTO / Upsert| SV["Capa SILVER (Delta)\nData Limpia, Deduplicada\n+ Dimension Calendar"]
        SV -->|Star Schema Aggregations| GD["Capa GOLD (Delta)\n- sales_performance_daily\n- distributor_360\n- brewery_efficiency_summary"]
    end

    %% Subgraph Analytics & AI
    subgraph Analytics ["5. Capa de Consumo & GenAI"]
        DB["Databricks Lakeview Dashboard\n(Executive Cockpit)"]
        GENIE["Databricks Genie AI Space\n(Consultas NLQ en Lenguaje Natural)"]
    end

    %% Conexiones
    KV -.->|Auth sin contraseñas| Orquestacion
    SQL <-->|Metadata & Audit Logs| Orquestacion
    P -->|Copy Data Parquet| VOL
    CSV -->|Binary Copy| VOL
    IN -->|Trigger PySpark Jobs| Databricks
    GD --> DB
    GD --> GENIE
```

---

## 2. Mapa de Bloques para Diagramar a Mano (Excalidraw / Draw.io)

### Bloque A (Izquierda - Fuentes):
* **Caja Azul 1:** `Neon PostgreSQL` (Logo de Postgres). Texto: *"Base Transaccional OLTP"*.
* **Caja Azul 2:** `Blob / ADLS Gen2` (Logo de Azure Storage). Texto: *"Feeds externos CSV de socios"*.

### Bloque B (Arriba Centro - Gobierno y Seguridad):
* **Caja Amarilla:** `Azure Key Vault`. Texto: *"Managed Identity (RBAC) - Cero secretos en código"*.
* **Caja Morada:** `Azure SQL Database`. Texto: *"Metadata Engine: table_config, watermark, audit_log"*.

### Bloque C (Centro - Orquestación):
* **Caja Azul Cielo:** `Azure Data Factory`. 
  * Flecha interna: `PL_MASTER` $\rightarrow$ `PL_SOURCE_TO_SILVER` $\rightarrow$ `PL_SILVER_TO_GOLD`.

### Bloque D (Derecha Centro - El Lakehouse):
* **Gran Caja Roja/Naranja:** `Azure Databricks + Unity Catalog`.
  * Dentro, 3 niveles verticales:
    1. **Bronze (Cobre):** Archivos Parquet crudos + timestamp.
    2. **Silver (Plata):** Tablas Delta con MERGE INTO (Upsert) + `silver.calendar`.
    3. **Gold (Oro):** Modelos analíticos preagregados.

### Bloque E (Extrema Derecha - Consumo):
* **Caja Verde:** `Lakeview Dashboard` + `Genie AI Agent`. Texto: *"BI Ejecutivo & Asistente Conversacional"*.
