# 📱 Slides & Carrusel para LinkedIn — BrewOps Data Platform

Este documento contiene la estructura y contenido exacto de **7 láminas de alto impacto (formato PDF/Carrusel 1080x1350 o 1080x1080)** listo para exportar a Canva / PowerPoint o publicar directamente en LinkedIn, junto con el **Copy (Texto del Post)** optimizado con storytelling técnico de Data Engineering.

---

## 📝 1. Copy Recomendado para el Post de LinkedIn

```text
🚀 Construí una Plataforma Lakehouse End-to-End en Azure & Databricks: BrewOps Data Platform 🍺⚡

Como Ingenieros de Datos, nuestro trabajo no es solo mover datos de un punto A a un punto B; es garantizar gobernanza, costos controlados, latencia predecible y valor de negocio accesible.

Para resolver los retos analíticos de una cervecera industrial ficticia (BrewOps), diseñé e implementé una plataforma empresarial en Azure con arquitectura Medallion gobernada por Unity Catalog.

🔥 ¿Qué componentes clave construí?
1️⃣ Ingesta Basada en Metadatos: Orquestador dinámico en Azure Data Factory guiado por tablas de control (`ctrl.table_config`, `watermark`) en Azure SQL Serverless. Cero pipelines duplicados para nuevas tablas.
2️⃣ Almacenamiento Seguro (ADLS Gen2 HNS): Jerarquía POSIX nativa y Unity Catalog Volumes para desacoplar el almacenamiento de las credenciales de cómputo.
3️⃣ Procesamiento Medallion con PySpark & Delta Lake: 
   - Bronze: Ingesta raw inmutable con tracking temporal.
   - Silver: Upserts atómicos con `MERGE INTO` deduplicando pedidos y distribuidores.
   - Gold: Modelo dimensional Star Schema optimizado para consumo ejecutivo.
4️⃣ Analítica y GenAI: Databricks Lakeview Dashboard con KPIs comerciales ($120.5K ingresos) y Databricks Genie AI Space para consultas en lenguaje natural (NLQ).
5️⃣ Seguridad Zero-Trust: Gestión de secretos centralizada en Azure Key Vault mediante Managed Identities (cero credenciales en texto plano).

👉 En el carrusel adjunto desgloso la arquitectura, la infografía del pipeline y las evidencias de ejecución en producción.

🔗 Repositorio completo en GitHub (código PySpark, DDLs y CI/CD):
https://github.com/ericksootano/brewops-azure-data-platform

¿Qué patrón de ingesta prefieres en tus proyectos: metadata-driven o code-first con orquestadores tipo Airflow? ¡Te leo en los comentarios! 👇

#DataEngineering #Azure #Databricks #DeltaLake #ApacheSpark #AzureDataFactory #UnityCatalog #DataArchitecture #PowerBI #Lakehouse
```

---

## 📑 2. Estructura Slide por Slide (Carrusel PDF)

### 📌 Slide 1: Portada (Hook Visual)
- **Titular:** 🍺 BrewOps Data Platform
- **Subtítulo:** Arquitectura Empresarial Lakehouse en Azure & Databricks con Unity Catalog
- **Badge:** End-to-End Project • Production Grade
- **Visual:** Logo de BrewOps y vista previa estilizada del Lakehouse.
- **Pie:** Por Erick Claudio | Data Engineer

---

### 📌 Slide 2: El Reto de Negocio & Principios de Diseño
- **Titular:** ¿Cuál era el desafío de BrewOps?
- **Puntos clave:**
  - 📉 Múltiples fuentes desarticuladas (Postgres OLTP + feeds de distribuidores en CSV).
  - 🔄 Necesidad de ingestas Full e Incrementales sin crear un pipeline por cada tabla.
  - 🛡️ Cero credenciales expuestas y gobierno centralizado de datos.
- **Decisión de Arquitectura:** Enfoque **Metadata-Driven** + **Arquitectura Medallion (Delta Lake)**.

---

### 📌 Slide 3: Arquitectura Técnica Oficial
- **Titular:** Arquitectura de Datos — Cloud Blueprints
- **Visual:** Imagen del diagrama oficial `assets/brewops_architecture.drawio.svg`.
- **Highlights en viñetas:**
  - Ingesta Orquestada: Azure Data Factory (ADF V2).
  - Procesamiento Distribuido: Apache Spark en Databricks Runtime 15.4 LTS.
  - Almacenamiento: ADLS Gen2 con Namespace Jerárquico (POSIX).
  - Gobierno y Auditoría: Unity Catalog + Azure SQL Database.

---

### 📌 Slide 4: Ingesta Metadata-Driven & Seguridad Zero-Trust
- **Titular:** El Motor de Metadatos & Orquestación
- **Visual:** Captura de ADF Studio (`assets/ADF Studio pipeline.png`) mostrando el pipeline en verde.
- **Detalle Técnico:**
  - Azure SQL Serverless aloja `ctrl.table_config` y `ctrl.watermark`.
  - ADF ejecuta un `Lookup` inicial, itera con `ForEach` y evalúa dinámicamente si aplica carga `FULL` o incremental `DELTA` por fecha de corte.
  - Autenticación 100% por Managed Identity contra Azure Key Vault.

---

### 📌 Slide 5: Procesamiento Medallion con Delta Lake
- **Titular:** Transformaciones de Datos en Databricks
- **Visual:** Esquema de Bronze $\rightarrow$ Silver $\rightarrow$ Gold (o fragmento de la infografía).
- **Detalle Técnico:**
  - **Bronze:** Append raw inmutable con metadata de auditoría (`landing_timestamp`).
  - **Silver:** `MERGE INTO` de PySpark con llaves compuestas deduplicando transacciones en tiempo real.
  - **Gold:** Agregaciones diarias (`NB_sales_performance_daily`, `NB_distributor_360`) listas para BI.

---

### 📌 Slide 6: Consumo Analítico & Databricks Genie AI
- **Titular:** De los Datos al Valor: Lakeview & Genie
- **Visual:** Split screen con el Dashboard (`assets/BrewOps Executive Dashboard.png`) y el asistente IA (`assets/BrewOps AI Data Assistant Q&A.png`).
- **Impacto:**
  - Cockpit ejecutivo para gerentes de operaciones y finanzas.
  - Asistente de IA generativa (Genie) que permite a usuarios no técnicos preguntar: *"¿Cuáles distribuidores tienen mayor riesgo crediticio?"* en lenguaje natural.

---

### 📌 Slide 7: Cierre & Repositorio GitHub
- **Titular:** Código, DDLs y CI/CD Disponibles
- **Visual:** Badge de GitHub Actions + URL del proyecto.
- **Llamado a la acción (CTA):**
  - ⭐ Revisa el código completo en: `github.com/ericksootano/brewops-azure-data-platform`
  - 💬 ¿Implementarías un motor metadata-driven en tu empresa? Déjamelo saber en los comentarios.
