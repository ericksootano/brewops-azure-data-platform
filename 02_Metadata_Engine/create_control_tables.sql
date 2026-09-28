/* =====================================================================
   BrewOps Platform — Control & Metadata Framework
   Target: Azure SQL Database
   Creates the ctrl schema + 3 control tables:
     1. ctrl.table_config (define cada origen, tipo de carga, claves y capas)
     2. ctrl.watermark    (almacena la última marca de agua por tabla)
     3. ctrl.audit_log    (registra ejecuciones, tiempos y conteo de filas)
   ===================================================================== */

IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = 'ctrl')
BEGIN
    EXEC('CREATE SCHEMA ctrl');
END
GO

/* ---------------------------------------------------------------------
   1. ctrl.table_config — Configuración centralizada de pipelines
   --------------------------------------------------------------------- */
IF OBJECT_ID('ctrl.table_config', 'U') IS NOT NULL DROP TABLE ctrl.table_config;
GO

CREATE TABLE ctrl.table_config (
    table_id             INT IDENTITY(1,1) PRIMARY KEY,
    source_system        VARCHAR(50)   NOT NULL,   -- neon_postgres, adls_csv, silver
    source_schema_name   VARCHAR(100)  NULL,        -- SQL sources only
    source_table_name    VARCHAR(200)  NULL,        -- table name, o nombre de archivo lógico
    source_file_format   VARCHAR(20)   NULL,        -- csv, parquet
    source_path          VARCHAR(500)  NULL,        -- contenedor/carpeta para CSVs
    bronze_table_name    VARCHAR(200)  NULL,
    silver_table_name    VARCHAR(200)  NULL,
    gold_table_name      VARCHAR(200)  NULL,
    load_type            VARCHAR(20)   NOT NULL CHECK (load_type IN ('FULL','APPEND','MERGE')),
    watermark_column     VARCHAR(100)  NULL,        -- requerida cuando load_type = APPEND o MERGE
    merge_keys           VARCHAR(200)  NULL,        -- clave primaria de negocio para MERGE
    stage                VARCHAR(20)   NOT NULL CHECK (stage IN ('SOURCE_TO_SILVER','SILVER_TO_GOLD')),
    is_active            BIT           NOT NULL DEFAULT 1,
    created_timestamp    DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME(),
    updated_timestamp    DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME()
);
GO

/* ---------------------------------------------------------------------
   2. ctrl.watermark — Último valor de watermark procesado
   --------------------------------------------------------------------- */
IF OBJECT_ID('ctrl.watermark', 'U') IS NOT NULL DROP TABLE ctrl.watermark;
GO

CREATE TABLE ctrl.watermark (
    table_id               INT           NOT NULL PRIMARY KEY
                                          REFERENCES ctrl.table_config (table_id),
    watermark_value        VARCHAR(200)  NULL,
    last_updated_timestamp DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME()
);
GO

/* ---------------------------------------------------------------------
   3. ctrl.audit_log — Trazabilidad de ejecuciones de ADF y Databricks
   --------------------------------------------------------------------- */
IF OBJECT_ID('ctrl.audit_log', 'U') IS NOT NULL DROP TABLE ctrl.audit_log;
GO

CREATE TABLE ctrl.audit_log (
    audit_id           INT IDENTITY(1,1) PRIMARY KEY,
    adf_run_id         VARCHAR(100)  NOT NULL,
    table_id           INT           NOT NULL REFERENCES ctrl.table_config (table_id),
    stage              VARCHAR(20)   NOT NULL CHECK (stage IN ('SOURCE_TO_SILVER','SILVER_TO_GOLD')),
    status             VARCHAR(20)   NOT NULL CHECK (status IN ('SUCCESS','FAILED','IN_PROGRESS')),
    records_written    INT           NULL,
    start_time         DATETIME2     NULL,
    end_time           DATETIME2     NULL,
    created_timestamp  DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME()
);
GO

/* =====================================================================
   Seed data — ctrl.table_config (Fase 1: Orígenes a Silver)
   4 tablas de Neon PostgreSQL + 2 orígenes CSV en ADLS
   ===================================================================== */
INSERT INTO ctrl.table_config
    (source_system, source_schema_name, source_table_name, source_file_format, source_path,
     bronze_table_name, silver_table_name, gold_table_name,
     load_type, watermark_column, merge_keys, stage, is_active)
VALUES
    -- 1. Plantas de elaboración (Carga FULL)
    ('neon_postgres', 'public', 'breweries', NULL, NULL,
     'breweries', 'breweries', NULL,
     'FULL', NULL, NULL, 'SOURCE_TO_SILVER', 1),

    -- 2. Portafolio de cervezas (Carga FULL)
    ('neon_postgres', 'public', 'brands', NULL, NULL,
     'brands', 'brands', NULL,
     'FULL', NULL, NULL, 'SOURCE_TO_SILVER', 1),

    -- 3. Clientes / Distribuidores (Carga INCREMENTAL / MERGE)
    ('neon_postgres', 'public', 'distributors', NULL, NULL,
     'distributors', 'distributors', NULL,
     'MERGE', 'updated_at', 'distributor_id', 'SOURCE_TO_SILVER', 1),

    -- 4. Pedidos y ventas (Carga INCREMENTAL / MERGE)
    ('neon_postgres', 'public', 'orders', NULL, NULL,
     'orders', 'orders', NULL,
     'MERGE', 'updated_at', 'order_id', 'SOURCE_TO_SILVER', 1),

    -- 5. Feeds de Costos de Materia Prima / Commodities (Carga FULL desde ADLS CSV)
    ('adls_csv', NULL, 'raw_material_prices', 'csv', 'raw_material_prices',
     'raw_material_prices', 'raw_material_prices', NULL,
     'FULL', NULL, NULL, 'SOURCE_TO_SILVER', 1),

    -- 6. Telemetría de Rutas y Despacho Logístico (Carga APPEND desde ADLS CSV)
    ('adls_csv', NULL, 'fleet_telemetry', 'csv', 'fleet_telemetry',
     'fleet_telemetry', 'fleet_telemetry', NULL,
     'APPEND', 'timestamp', NULL, 'SOURCE_TO_SILVER', 1);
GO

/* =====================================================================
   Seed data — ctrl.watermark
   Marcas de agua iniciales para tablas APPEND y MERGE
   ===================================================================== */
INSERT INTO ctrl.watermark (table_id, watermark_value, last_updated_timestamp)
SELECT table_id, '1900-01-01T00:00:00', SYSUTCDATETIME()
FROM ctrl.table_config
WHERE load_type IN ('APPEND', 'MERGE');
GO

/* =====================================================================
   Seed data — ctrl.table_config (Fase 2: Capa Gold Analytics)
   ===================================================================== */
INSERT INTO ctrl.table_config
    (source_system, source_schema_name, source_table_name, source_file_format, source_path,
     bronze_table_name, silver_table_name, gold_table_name,
     load_type, watermark_column, merge_keys, stage, is_active)
VALUES
    ('silver', NULL, NULL, NULL, NULL,
     NULL, NULL, 'sales_performance_daily',
     'FULL', NULL, NULL, 'SILVER_TO_GOLD', 1),

    ('silver', NULL, NULL, NULL, NULL,
     NULL, NULL, 'distributor_360',
     'FULL', NULL, NULL, 'SILVER_TO_GOLD', 1),

    ('silver', NULL, NULL, NULL, NULL,
     NULL, NULL, 'brewery_efficiency_summary',
     'FULL', NULL, NULL, 'SILVER_TO_GOLD', 1);
GO
