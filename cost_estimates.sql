-- =========================================
-- cost_estimates.sql
-- Tablas de estimados de servicios médicos por ZIP code
-- Datos de ejemplo basados en rangos públicos de CMS y hospitales
-- =========================================

-- 1️⃣ Tabla principal de estimados por servicio y ZIP code
CREATE TABLE IF NOT EXISTS cost_estimates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cpt_code TEXT NOT NULL,                -- Código del servicio
    service_name TEXT NOT NULL,            -- Nombre del servicio
    zip_code TEXT NOT NULL,                -- ZIP code exacto
    insured_avg REAL,                      -- Precio promedio con seguro (CMS)
    self_pay_avg REAL,                      -- Precio promedio sin seguro (self-pay)
    low_price REAL,                        -- Precio mínimo registrado
    high_price REAL,                       -- Precio máximo registrado
    data_source TEXT,                      -- Fuente: CMS, hospital public, etc.
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2️⃣ Tabla de localización de ZIP codes para calcular distancia
CREATE TABLE IF NOT EXISTS zip_locations (
    zip_code TEXT PRIMARY KEY,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL
);

-- 3️⃣ Índices para acelerar búsquedas
CREATE INDEX IF NOT EXISTS idx_cost_zip ON cost_estimates(zip_code);
CREATE INDEX IF NOT EXISTS idx_cost_cpt ON cost_estimates(cpt_code);

-- =========================================
-- 4️⃣ Datos de ejemplo
-- 10–15 ZIP codes por estado, precios simulados (basados en rangos públicos)
-- =========================================
INSERT INTO zip_locations (zip_code, latitude, longitude) VALUES
('10001', 40.750742, -73.99653),
('10002', 40.71704, -73.987),
('33101', 25.774, -80.193),
('33109', 25.761, -80.191),
('90001', 33.973, -118.248),
('90002', 33.949, -118.246),
('60601', 41.885, -87.622),
('60602', 41.882, -87.628);

INSERT INTO cost_estimates (cpt_code, service_name, zip_code, insured_avg, self_pay_avg, low_price, high_price, data_source) VALUES
('99213', 'Consulta Médica General', '10001', 120.0, 250.0, 100.0, 400.0, 'CMS'),
('99213', 'Consulta Médica General', '10002', 130.0, 260.0, 110.0, 420.0, 'CMS'),
('99213', 'Consulta Médica General', '33101', 100.0, 220.0, 90.0, 380.0, 'CMS'),
('99213', 'Consulta Médica General', '33109', 110.0, 230.0, 95.0, 390.0, 'CMS'),
('99213', 'Consulta Médica General', '90001', 115.0, 240.0, 100.0, 400.0, 'CMS'),
('99213', 'Consulta Médica General', '90002', 118.0, 245.0, 105.0, 405.0, 'CMS'),
('99213', 'Consulta Médica General', '60601', 125.0, 255.0, 110.0, 410.0, 'CMS'),
('99213', 'Consulta Médica General', '60602', 128.0, 260.0, 115.0, 420.0, 'CMS');

-- =========================================
-- 5️⃣ Consulta ejemplo lista para backend
-- Buscar opciones por ZIP code y CPT code ingresado
-- =========================================
-- Parámetros a usar en tu backend:
-- :cpt_code -> Código CPT que busca el cliente
-- :user_latitude -> Latitud del ZIP del cliente
-- :user_longitude -> Longitud del ZIP del cliente

SELECT ce.cpt_code, ce.service_name, ce.zip_code, ce.insured_avg, ce.self_pay_avg,
       ce.low_price, ce.high_price, ce.data_source
FROM cost_estimates ce
JOIN zip_locations zl ON ce.zip_code = zl.zip_code
WHERE ce.cpt_code = :cpt_code
ORDER BY
    ABS(zl.latitude - :user_latitude) + ABS(zl.longitude - :user_longitude),
    ce.self_pay_avg ASC
LIMIT 5

UNION ALL

SELECT ce.cpt_code, ce.service_name, ce.zip_code, ce.insured_avg, ce.self_pay_avg,
       ce.low_price, ce.high_price, ce.data_source
FROM cost_estimates ce
JOIN zip_locations zl ON ce.zip_code = zl.zip_code
WHERE ce.cpt_code = :cpt_code
ORDER BY ce.high_price DESC
LIMIT 1

UNION ALL

SELECT ce.cpt_code, ce.service_name, ce.zip_code, ce.insured_avg, ce.self_pay_avg,
       ce.low_price, ce.high_price, ce.data_source
FROM cost_estimates ce
WHERE ce.cpt_code = :cpt_code
ORDER BY ce.self_pay_avg ASC
LIMIT 5

UNION ALL

SELECT ce.cpt_code, ce.service_name, ce.zip_code, ce.insured_avg, ce.self_pay_avg,
       ce.low_price, ce.high_price, ce.data_source
FROM cost_estimates ce
WHERE ce.cpt_code = :cpt_code
ORDER BY ce.high_price DESC
LIMIT 1;

-- Nota legal: Todos los precios son estimados basados en datos públicos, no constituyen oferta directa
