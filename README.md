# 🍺 BrewOps Data Platform — End-to-End Enterprise Lakehouse Architecture

![CI/CD Status](https://github.com/ericksootano/brewops-azure-data-platform/actions/workflows/ci_cd.yml/badge.svg)

> **Plataforma de datos empresarial e híbrida para la industria cervecera y de consumo masivo (FMCG).**  
> Diseñada bajo arquitectura Medallion en Azure Databricks con Unity Catalog, orquestación metadata-driven en Azure Data Factory, almacenamiento seguro en ADLS Gen2 y gobierno centralizado con Azure Key Vault.

---

## 🏢 1. Contexto de Negocio & El Desafío (Business Problem & Opportunity)

### La Empresa: *BrewOps Brewery Group*
**BrewOps** es una compañía cervecera de consumo masivo (FMCG) que opera múltiples plantas cerveceras industriales y artesanales, gestiona un portafolio multimarca (*Lager Tradicional, IPA Artesanal, Stout Imperial, Pilsner Premium*) y distribuye sus productos a través de una red heterogénea de distribuidores mayoristas y socios logísticos.

### Los Desafíos Identificados (Pain Points)
Antes de esta iniciativa, la organización enfrentaba cuatro cuellos de botella críticos:

1. **Silos Desarticulados de Datos:**  
   Las transacciones de órdenes de venta operaban en un motor OLTP (**PostgreSQL**), mientras que la telemetría de distribución vehicular y las cotizaciones externas de materias primas llegaban en archivos **CSV** por feeds desconectados. No existía una vista unificada de la operación.
2. **Pipelines Rígidos y Deuda Técnica (Falta de Escalabilidad):**  
   Cualquier nueva tabla requería diseñar, probar y desplegar un pipeline exclusivo en el orquestador. El equipo de datos invertía el 70% de su tiempo en mantenimiento rutinario en lugar de entregar valor analítico.
3. **Riesgo Crediticio en Distribuidores sin Monitoreo Activo:**  
   Los distribuidores solicitaban despachos sin que el equipo comercial pudiera contrastar de forma inmediata su saldo consumido contra el límite de crédito asignado, generando un alto riesgo de incobrabilidad.
4. **Barrera de Acceso a la Información para la Alta Dirección:**  
   Los gerentes de producción y finanzas dependían de solicitudes ad-hoc al equipo técnico para responder preguntas comerciales simples, con tiempos de respuesta de hasta 72 horas.

### La Solución Implementada: *Lakehouse Empresarial BrewOps*
Para resolver estos retos de raíz, se diseñó e implementó una plataforma de datos moderna de extremo a extremo que:
- **Automatiza la ingesta vía Metadatos:** Un motor dinámico en **Azure SQL Serverless** y **Azure Data Factory** orquesta cargas completas e incrementales sin tocar código.
- **Garantiza calidad y deduplicación con Medallion & Delta Lake:** Transforma transacciones crudas en tablas Silver saneadas vía `MERGE INTO`, culminando en un modelo Gold (Star Schema) de rendimiento operativo y comercial.
- **Democratiza el acceso con BI & GenAI:** Proporciona un **Executive Cockpit (Lakeview)** para seguimiento de KPIs en tiempo real y habilita a directores sin conocimientos de SQL a interactuar con los datos mediante lenguaje natural en **Databricks Genie AI Space**.
- **Eficiencia de Costos (FinOps Ready):** Diseñado con servicios serverless y auto-pausa (Azure SQL Serverless y Databricks Auto-Termination), manteniendo los costos de desarrollo e infraestructura por debajo de **$2.00 USD**.

---

## 🏛️ 2. Arquitectura de Datos Oficial (Azure & Databricks Architecture)

Diagrama técnico oficial estructurado según los estándares de diseño del **Microsoft Azure Architecture Center**:

![BrewOps Architecture Diagram](assets/brewops_architecture.drawio.svg)

---

## 🎨 3. Infografía de Flujo de Datos (Data Pipeline Overview)

Flujo secuencial de extremo a extremo que ilustra el recorrido de los datos, las tablas de control y las capas Medallion:

![BrewOps Architecture Infography](assets/Overview%20Project%20Infografy.png)

---

## 📸 4. Evidencias de Ejecución & Capa de Analítica

### A. Databricks Lakeview Dashboard (Executive Cockpit)
Visualización ejecutiva con KPIs principales ($120.54K USD de ingresos, 36.44K litros), desglose por categoría de cerveza, mezcla de empaques (retornable vs lata), utilización de plantas cerveceras y matriz de riesgo crediticio de distribuidores:
![BrewOps Executive Dashboard](assets/BrewOps%20Executive%20Dashboard.png)

### B. Databricks Genie AI Space (Consultas en Lenguaje Natural)
Interacción con el modelo semántico en lenguaje natural respondiendo preguntas complejas de márgenes y ventas sin escribir código SQL:
![BrewOps AI Data Assistant Q&A](assets/BrewOps%20AI%20Data%20Assistant%20Q%26A.png)

### C. Pipeline Orquestador Maestro en Azure Data Factory
Orquestación parametrizada de extremo a extremo (Source $\rightarrow$ Landing $\rightarrow$ Bronze $\rightarrow$ Silver $\rightarrow$ Gold) validada al 100% en verde con auditoría de ejecución:
![ADF Studio pipeline](assets/ADF%20Studio%20pipeline.png)

---

## 🚀 5. Stack Tecnológico & Componentes Cloud

| Componente | Servicio Azure / Cloud | Rol en la Arquitectura |
| :--- | :--- | :--- |
| **Fuentes Operacionales** | Neon PostgreSQL (Serverless) & ADLS Gen2 | Simulación de transacciones de ventas y feeds externos de materias primas. |
| **Landing & Storage** | Azure Data Lake Storage Gen2 (HNS) | Jerarquía POSIX en contenedor `landing` y almacenamiento de tablas Delta Lake. |
| **Control de Acceso** | Azure Key Vault & Managed Identities | Gestión centralizada de secretos sin credenciales en texto plano (Zero-Trust). |
| **Motor de Metadatos** | Azure SQL Database (Serverless) | Gobernanza de pipelines mediante tablas `table_config`, `watermark` y `audit_log`. |
| **Orquestación** | Azure Data Factory (ADF V2) | Pipelines dinámicos y parametrizados para cargas FULL e INCREMENTALES (Watermark). |
| **Procesamiento** | Azure Databricks (Runtime 15.4 LTS) | Motor PySpark con Delta Lake para transformaciones Medallion (Landing $\rightarrow$ Bronze $\rightarrow$ Silver $\rightarrow$ Gold). |
| **Gobernanza** | Unity Catalog & Storage Volumes | Catálogo unificado, control de esquemas y volúmenes externos sin mounts antiguos. |
| **Consumo & BI** | Lakeview Dashboards & Genie AI | Analítica visual de autoservicio y consultas conversacionales NLQ. |
| **CI/CD** | GitHub Actions | Validación automática de sintaxis PySpark, esquemas JSON de ADF y scripts DDL. |

---

## 📊 6. Modelo de Datos Medallion

### Capa Bronze (Raw / Inmutable)
* `bronze.breweries`, `bronze.brands`, `bronze.distributors`, `bronze.orders`.
* Conserva la historia completa de extracciones con marcas de tiempo `landing_timestamp` e `insert_timestamp`.

### Capa Silver (Enriquecida & MERGE)
* Aplicación de **Delta Upserts (`MERGE INTO`)** usando claves de negocio (`distributor_id`, `order_id`).
* Deduplicación, limpieza de datos y tipado estricto.
* Dimensión temporal `silver.calendar` generada dinámicamente (2020–2030).

### Capa Gold (Métricas & KPIs Ejecutivos)
1. **`gold.sales_performance_daily`:** Ingresos brutos, cajas vendidas, litros despachados e ingreso promedio por litro por región y planta cervecera.
2. **`gold.distributor_360`:** Volumen histórico de compras, recurrencia de pedidos y porcentaje de utilización de línea de crédito.
3. **`gold.brewery_efficiency_summary`:** Volumen despachado en Hectolitros (hl) comparado contra la capacidad mensual instalada de cada cervecería.

---

## 🛠️ 7. Automatización & CI/CD con GitHub Actions

El repositorio cuenta con un pipeline automatizado (`.github/workflows/ci_cd.yml`) que se ejecuta en cada `push` o `pull_request` a la rama `main`:
1. **Linting de Notebooks:** Verificación estricta de código Python/PySpark mediante `ruff`.
2. **Validación de JSON de ADF:** Comprobación sintáctica de definiciones declarativas de pipelines antes del despliegue.
3. **Chequeo de Integridad SQL:** Validación de dependencias y scripts DDL para esquemas de Postgres y Azure SQL.

---

## 💰 8. Eficiencia de Costos & FinOps (Validación Cloud)

Toda la arquitectura fue aprovisionada, ejecutada y testeada con un perfil de costos ultra-eficiente en Azure (**gasto acumulado de desarrollo < $1.50 USD**):
* **Azure Databricks:** Clusters configurados con auto-apagado agresivo (*Auto-Termination a 20 min*) y single-node runtime para pruebas.
* **Azure SQL Serverless:** Auto-pausa a los 60 min de inactividad, evitando facturación de vCores ociosa.
* **Azure Data Factory:** Cómputo por demanda que solo consume Data Integration Units (DIUs) durante los minutos exactos de ejecución.
* **ADLS Gen2:** Almacenamiento caliente por niveles de consumo real (Pay-as-you-go).
