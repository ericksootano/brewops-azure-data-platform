/* =====================================================================
   BrewOps Platform — Cervecería & Distribución (OLTP)
   Target: Neon Postgres (schema: public)
   Creates:
     1. breweries (Cervecerías / Plantas de elaboración) -> Carga FULL
     2. brands (Marcas y tipos de cerveza) -> Carga FULL
     3. distributors (Centros de distribución / Clientes) -> Carga INCREMENTAL
     4. orders (Pedidos y ventas transaccionales) -> Carga INCREMENTAL
   ===================================================================== */

DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS distributors;
DROP TABLE IF EXISTS brands;
DROP TABLE IF EXISTS breweries;

/* ---------------------------------------------------------------------
   1. breweries — Plantas cerveceras (Carga FULL)
   Equivalente arquitectónico a 'hospitals' del video
   --------------------------------------------------------------------- */
CREATE TABLE breweries (
    brewery_id      SERIAL PRIMARY KEY,
    brewery_name    VARCHAR(150) NOT NULL,
    city            VARCHAR(100),
    region          VARCHAR(100),
    brewery_type    VARCHAR(50),   -- Industrial, Artesanal, Microbrewery
    capacity_hl     INT,           -- Capacidad mensual en hectolitros
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

INSERT INTO breweries (brewery_name, city, region, brewery_type, capacity_hl) VALUES
('Planta Central Haina', 'Santo Domingo', 'Ozama', 'Industrial', 250000),
('Cervecería del Cibao', 'Santiago', 'Cibao Norte', 'Industrial', 180000),
('Cervecería Punta Cana Craft', 'Bávaro', 'Yuma', 'Artesanal', 15000),
('Destilería & Brewhouse Sur', 'San Cristóbal', 'Valdesia', 'Microbrewery', 8000);

/* ---------------------------------------------------------------------
   2. brands — Portafolio de cervezas y marcas (Carga FULL)
   --------------------------------------------------------------------- */
CREATE TABLE brands (
    brand_id        SERIAL PRIMARY KEY,
    brand_name      VARCHAR(100) NOT NULL,
    category        VARCHAR(50),   -- Pilsener, Cerveza Negra, Light, Sin Alcohol, IPA
    abv             NUMERIC(4,2),  -- Grado de alcohol (% Alcohol by Volume)
    package_type    VARCHAR(50),   -- Botella Retornable 650ml, Lata 355ml, Botella 350ml
    unit_price_usd  NUMERIC(10,2) NOT NULL,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

INSERT INTO brands (brand_name, category, abv, package_type, unit_price_usd) VALUES
('Ambar Clásica Especial', 'Pilsener', 5.0, 'Botella Retornable 650ml', 1.85),
('Ambar Light Suave', 'Light', 3.9, 'Botella Retornable 650ml', 1.80),
('Quisqueya Dorada', 'Pilsener', 5.2, 'Lata 355ml', 1.25),
('Caribe Stout Negra', 'Cerveza Negra', 6.5, 'Botella 350ml', 2.40),
('Isla Cero 0.0%', 'Sin Alcohol', 0.0, 'Lata 355ml', 1.10),
('Tropical Hazy IPA', 'IPA', 6.2, 'Lata 355ml', 2.75);

/* ---------------------------------------------------------------------
   3. distributors — Clientes y centros de despacho (Carga INCREMENTAL)
   Equivalente arquitectónico a 'doctors' del video
   --------------------------------------------------------------------- */
CREATE TABLE distributors (
    distributor_id   SERIAL PRIMARY KEY,
    distributor_name VARCHAR(150) NOT NULL,
    channel_type     VARCHAR(50),   -- Supermercado, Mayorista, Cadena Hotelera, Colmados
    city             VARCHAR(100),
    credit_limit_usd NUMERIC(12,2),
    is_active        BOOLEAN DEFAULT TRUE,
    created_at       TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMP NOT NULL DEFAULT NOW()
);

INSERT INTO distributors (distributor_name, channel_type, city, credit_limit_usd, updated_at) VALUES
('Distribuidora del Este S.A.', 'Mayorista', 'La Romana', 150000.00, '2026-09-20 08:30:00'),
('Supermercados El Caribe', 'Supermercado', 'Santo Domingo', 300000.00, '2026-09-20 09:00:00'),
('Consorcio Hotelero Bavaro Resorts', 'Cadena Hotelera', 'Punta Cana', 220000.00, '2026-09-20 09:15:00'),
('Abastecedora Cibao Central', 'Mayorista', 'Santiago', 180000.00, '2026-09-20 10:00:00'),
('Red de Colmados Metropolitana', 'Colmados', 'Santo Domingo', 95000.00, '2026-09-20 11:30:00');

/* ---------------------------------------------------------------------
   4. orders — Transacciones de venta y despacho (Carga INCREMENTAL)
   Equivalente arquitectónico a 'patients' del video
   --------------------------------------------------------------------- */
CREATE TABLE orders (
    order_id         SERIAL PRIMARY KEY,
    distributor_id   INT REFERENCES distributors(distributor_id),
    brewery_id       INT REFERENCES breweries(brewery_id),
    brand_id         INT REFERENCES brands(brand_id),
    crates_ordered   INT NOT NULL,           -- Cajas de cervezas
    total_liters     NUMERIC(10,2) NOT NULL,
    total_amount_usd NUMERIC(12,2) NOT NULL,
    status           VARCHAR(50),            -- Delivered, In-Transit, Processing, Cancelled
    order_date       DATE NOT NULL,
    created_at       TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMP NOT NULL DEFAULT NOW()
);

INSERT INTO orders (distributor_id, brewery_id, brand_id, crates_ordered, total_liters, total_amount_usd, status, order_date, updated_at) VALUES
(1, 1, 1, 500, 7800.00, 22200.00, 'Delivered', '2026-09-21', '2026-09-21 14:00:00'),
(2, 1, 2, 800, 12480.00, 34560.00, 'Delivered', '2026-09-21', '2026-09-21 16:30:00'),
(3, 3, 6, 250, 2130.00, 16500.00, 'Delivered', '2026-09-22', '2026-09-22 11:15:00'),
(4, 2, 1, 600, 9360.00, 26640.00, 'In-Transit', '2026-09-22', '2026-09-22 17:45:00'),
(5, 1, 3, 400, 3408.00, 12000.00, 'Processing', '2026-09-23', '2026-09-23 09:20:00'),
(2, 2, 4, 150, 1260.00, 8640.00, 'Delivered', '2026-09-23', '2026-09-23 15:10:00');
