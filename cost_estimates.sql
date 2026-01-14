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
-- =========================================
-- BLOQUES COMPLETOS DE ZIP CODES PARA 50 ESTADOS
-- =========================================

-- ALABAMA
INSERT OR IGNORE INTO zip_locations (zip_code, latitude, longitude) VALUES
('35004', 33.5841, -86.5925),
('35005', 33.5817, -86.5415),
('35203', 33.5207, -86.8025),
('36602', 30.6954, -88.0399),
('35801', 34.7304, -86.5861);

INSERT INTO cost_estimates (cpt_code, service_name, zip_code, insured_avg, self_pay_avg, low_price, high_price, data_source) VALUES
('99213','Consulta General','35004',110,220,100,400,'CMS'),
('99213','Consulta General','35005',115,225,105,405,'CMS'),
('99213','Consulta General','35203',120,230,110,410,'CMS'),
('99213','Consulta General','36602',125,240,115,420,'CMS'),
('99213','Consulta General','35801',130,245,120,430,'CMS');

-- ALASKA
INSERT OR IGNORE INTO zip_locations (zip_code, latitude, longitude) VALUES
('99501', 61.2175, -149.8584),
('99502', 61.2081, -149.8963),
('99603', 60.5410, -151.2563),
('99701', 64.8378, -147.7164),
('99801', 58.3019, -134.4197);

INSERT INTO cost_estimates (cpt_code, service_name, zip_code, insured_avg, self_pay_avg, low_price, high_price, data_source) VALUES
('99213','Consulta General','99501',140,280,130,450,'CMS'),
('99213','Consulta General','99502',145,290,135,460,'CMS'),
('99213','Consulta General','99603',150,300,140,470,'CMS'),
('99213','Consulta General','99701',155,310,145,480,'CMS'),
('99213','Consulta General','99801',160,320,150,490,'CMS');

-- ARIZONA
INSERT OR IGNORE INTO zip_locations (zip_code, latitude, longitude) VALUES
('85001', 33.4484, -112.0740),
('85002', 33.4500, -112.0730),
('85224', 33.3075, -111.7207),
('85701', 32.2217, -110.9265),
('86001', 35.1983, -111.6513);

INSERT INTO cost_estimates (cpt_code, service_name, zip_code, insured_avg, self_pay_avg, low_price, high_price, data_source) VALUES
('99213','Consulta General','85001',120,240,110,420,'CMS'),
('99213','Consulta General','85002',125,250,115,430,'CMS'),
('99213','Consulta General','85224',130,260,120,440,'CMS'),
('99213','Consulta General','85701',135,270,125,450,'CMS'),
('99213','Consulta General','86001',140,280,130,460,'CMS');

-- ARKANSAS
INSERT OR IGNORE INTO zip_locations (zip_code, latitude, longitude) VALUES
('72201', 34.7465, -92.2896),
('72032', 34.5032, -92.0536),
('72701', 36.0662, -94.1390),
('72901', 35.3910, -94.4825),
('71901', 34.5030, -93.0623);

INSERT INTO cost_estimates (cpt_code, service_name, zip_code, insured_avg, self_pay_avg, low_price, high_price, data_source) VALUES
('99213','Consulta General','72201',115,230,105,410,'CMS'),
('99213','Consulta General','72032',120,240,110,420,'CMS'),
('99213','Consulta General','72701',125,250,115,430,'CMS'),
('99213','Consulta General','72901',130,260,120,440,'CMS'),
('99213','Consulta General','71901',135,270,125,450,'CMS');

-- CALIFORNIA
INSERT OR IGNORE INTO zip_locations (zip_code, latitude, longitude) VALUES
('90001', 33.973, -118.248),
('90002', 33.949, -118.246),
('90210', 34.0901, -118.4065),
('94102', 37.7793, -122.4192),
('95814', 38.5816, -121.4944);

INSERT INTO cost_estimates (cpt_code, service_name, zip_code, insured_avg, self_pay_avg, low_price, high_price, data_source) VALUES
('99213','Consulta General','90001',115,240,100,400,'CMS'),
('99213','Consulta General','90002',118,245,105,405,'CMS'),
('99213','Consulta General','90210',200,500,180,600,'CMS'),
('99213','Consulta General','94102',130,260,110,410,'CMS'),
('99213','Consulta General','95814',125,255,115,405,'CMS');

-- COLORADO
INSERT OR IGNORE INTO zip_locations (zip_code, latitude, longitude) VALUES
('80202', 39.7392, -104.9903),
('80014', 39.8700, -104.9890),
('80301', 40.0150, -105.2705),
('80903', 38.8339, -104.8214),
('81611', 39.4807, -107.2183);

INSERT INTO cost_estimates (cpt_code, service_name, zip_code, insured_avg, self_pay_avg, low_price, high_price, data_source) VALUES
('99213','Consulta General','80202',120,240,110,420,'CMS'),
('99213','Consulta General','80014',125,250,115,430,'CMS'),
('99213','Consulta General','80301',130,260,120,440,'CMS'),
('99213','Consulta General','80903',135,270,125,450,'CMS'),
('99213','Consulta General','81611',140,280,130,460,'CMS');

-- CONNECTICUT
INSERT OR IGNORE INTO zip_locations (zip_code, latitude, longitude) VALUES
('06101', 41.7658, -72.6734),
('06510', 41.3083, -72.9279),
('06810', 41.0525, -73.5387),
('06320', 41.5306, -71.8217),
('06604', 41.2294, -73.1980);

INSERT INTO cost_estimates (cpt_code, service_name, zip_code, insured_avg, self_pay_avg, low_price, high_price, data_source) VALUES
('99213','Consulta General','06101',120,240,110,420,'CMS'),
('99213','Consulta General','06510',125,250,115,430,'CMS'),
('99213','Consulta General','06810',130,260,120,440,'CMS'),
('99213','Consulta General','06320',135,270,125,450,'CMS'),
('99213','Consulta General','06604',140,280,130,460,'CMS');

-- DELAWARE
INSERT OR IGNORE INTO zip_locations (zip_code, latitude, longitude) VALUES
('19901', 39.1582, -75.5244),
('19801', 39.7391, -75.5398),
('19701', 39.6136, -75.7053),
('19904', 39.1445, -75.4343),
('19977', 38.7744, -75.1577);

INSERT INTO cost_estimates (cpt_code, service_name, zip_code, insured_avg, self_pay_avg, low_price, high_price, data_source) VALUES
('99213','Consulta General','19901',125,250,115,430,'CMS'),
('99213','Consulta General','19801',130,260,120,440,'CMS'),
('99213','Consulta General','19701',135,270,125,450,'CMS'),
('99213','Consulta General','19904',140,280,130,460,'CMS'),
('99213','Consulta General','19977',145,290,135,470,'CMS');

-- FLORIDA
INSERT OR IGNORE INTO zip_locations (zip_code, latitude, longitude) VALUES
('33101', 25.774, -80.193),
('33109', 25.761, -80.191),
('32801', 28.5383, -81.3792),
('32202', 30.3322, -81.6557),
('33602', 27.9642, -82.4526);

INSERT INTO cost_estimates (cpt_code, service_name, zip_code, insured_avg, self_pay_avg, low_price, high_price, data_source) VALUES
('99213','Consulta General','33101',100,220,90,380,'CMS'),
('99213','Consulta General','33109',110,230,95,390,'CMS'),
('99213','Consulta General','32801',120,240,110,400,'CMS'),
('99213','Consulta General','32202',125,250,115,410,'CMS'),
('99213','Consulta General','33602',130,260,120,420,'CMS');

-- =========================================
-- Bloque de ZIPs: Georgia → Kentucky
-- =========================================
INSERT OR IGNORE INTO zip_locations (zip_code, latitude, longitude) VALUES
('30301', 33.749, -84.388), -- Atlanta, GA
('30303', 33.752, -84.392),
('30305', 33.786, -84.384),
('30306', 33.771, -84.360),
('30307', 33.764, -84.353),
('30308', 33.778, -84.390),
('30309', 33.784, -84.385),
('30310', 33.748, -84.401),
('30311', 33.752, -84.420),
('30312', 33.745, -84.387),

('40202', 38.252, -85.758), -- Louisville, KY
('40203', 38.257, -85.757),
('40204', 38.247, -85.759),
('40205', 38.270, -85.770),
('40206', 38.256, -85.780);

INSERT INTO cost_estimates (cpt_code, service_name, zip_code, insured_avg, self_pay_avg, low_price, high_price, data_source) VALUES
('99213', 'Consulta Médica General', '30301', 125.0, 250.0, 110.0, 400.0, 'CMS'),
('99213', 'Consulta Médica General', '30303', 128.0, 255.0, 115.0, 405.0, 'CMS'),
('99213', 'Consulta Médica General', '30305', 130.0, 260.0, 120.0, 410.0, 'CMS'),
('99213', 'Consulta Médica General', '30306', 122.0, 245.0, 110.0, 395.0, 'CMS'),
('99213', 'Consulta Médica General', '30307', 126.0, 250.0, 115.0, 400.0, 'CMS'),
('99213', 'Consulta Médica General', '30308', 127.0, 252.0, 118.0, 405.0, 'CMS'),
('99213', 'Consulta Médica General', '30309', 124.0, 248.0, 115.0, 398.0, 'CMS'),
('99213', 'Consulta Médica General', '30310', 129.0, 258.0, 120.0, 410.0, 'CMS'),
('99213', 'Consulta Médica General', '30311', 123.0, 247.0, 112.0, 399.0, 'CMS'),
('99213', 'Consulta Médica General', '30312', 125.0, 250.0, 115.0, 402.0, 'CMS'),

('99213', 'Consulta Médica General', '40202', 130.0, 260.0, 120.0, 410.0, 'CMS'),
('99213', 'Consulta Médica General', '40203', 128.0, 255.0, 118.0, 405.0, 'CMS'),
('99213', 'Consulta Médica General', '40204', 127.0, 252.0, 115.0, 400.0, 'CMS'),
('99213', 'Consulta Médica General', '40205', 129.0, 258.0, 120.0, 410.0, 'CMS'),
('99213', 'Consulta Médica General', '40206', 126.0, 250.0, 115.0, 405.0, 'CMS');
-- =========================================
-- Bloque de ZIPs: Louisiana → Maryland
-- =========================================
INSERT OR IGNORE INTO zip_locations (zip_code, latitude, longitude) VALUES
('70112', 29.951, -90.071), -- Nueva Orleans, LA
('70113', 29.953, -90.065),
('70115', 29.965, -90.080),
('70116', 29.970, -90.100),
('70118', 29.985, -90.090),
('70119', 29.990, -90.085),
('70121', 29.955, -90.075),
('70122', 29.960, -90.080),
('70123', 29.965, -90.085),
('70124', 29.970, -90.090),

('21201', 39.290, -76.612), -- Baltimore, MD
('21202', 39.287, -76.615),
('21205', 39.320, -76.580),
('21206', 39.320, -76.580),
('21207', 39.377, -76.656),
('21208', 39.391, -76.645),
('21209', 39.355, -76.658),
('21210', 39.360, -76.640),
('21211', 39.325, -76.615),
('21212', 39.337, -76.609);

INSERT INTO cost_estimates (cpt_code, service_name, zip_code, insured_avg, self_pay_avg, low_price, high_price, data_source) VALUES
('99213', 'Consulta Médica General', '70112', 120.0, 250.0, 110.0, 400.0, 'CMS'),
('99213', 'Consulta Médica General', '70113', 122.0, 255.0, 115.0, 405.0, 'CMS'),
('99213', 'Consulta Médica General', '70115', 125.0, 260.0, 118.0, 410.0, 'CMS'),
('99213', 'Consulta Médica General', '70116', 123.0, 252.0, 115.0, 405.0, 'CMS'),
('99213', 'Consulta Médica General', '70118', 127.0, 265.0, 120.0, 415.0, 'CMS'),
('99213', 'Consulta Médica General', '70119', 126.0, 260.0, 118.0, 410.0, 'CMS'),
('99213', 'Consulta Médica General', '70121', 124.0, 255.0, 115.0, 405.0, 'CMS'),
('99213', 'Consulta Médica General', '70122', 128.0, 268.0, 120.0, 420.0, 'CMS'),
('99213', 'Consulta Médica General', '70123', 125.0, 260.0, 118.0, 410.0, 'CMS'),
('99213', 'Consulta Médica General', '70124', 127.0, 265.0, 120.0, 415.0, 'CMS'),

('99213', 'Consulta Médica General', '21201', 130.0, 260.0, 120.0, 410.0, 'CMS'),
('99213', 'Consulta Médica General', '21202', 128.0, 258.0, 118.0, 405.0, 'CMS'),
('99213', 'Consulta Médica General', '21205', 125.0, 255.0, 115.0, 400.0, 'CMS'),
('99213', 'Consulta Médica General', '21206', 127.0, 257.0, 118.0, 405.0, 'CMS'),
('99213', 'Consulta Médica General', '21207', 129.0, 260.0, 120.0, 410.0, 'CMS'),
('99213', 'Consulta Médica General', '21208', 126.0, 258.0, 118.0, 405.0, 'CMS'),
('99213', 'Consulta Médica General', '21209', 128.0, 260.0, 120.0, 410.0, 'CMS'),
('99213', 'Consulta Médica General', '21210', 127.0, 258.0, 118.0, 405.0, 'CMS'),
('99213', 'Consulta Médica General', '21211', 125.0, 255.0, 115.0, 400.0, 'CMS'),
('99213', 'Consulta Médica General', '21212', 128.0, 260.0, 120.0, 410.0, 'CMS');
-- =========================================
-- Bloque de ZIPs: Massachusetts → Michigan
-- =========================================
INSERT OR IGNORE INTO zip_locations (zip_code, latitude, longitude) VALUES
('02108', 42.358, -71.063), -- Boston, MA
('02109', 42.361, -71.054),
('02110', 42.360, -71.053),
('02111', 42.331, -71.058),
('02112', 42.352, -71.065),
('02113', 42.362, -71.056),
('02114', 42.361, -71.067),
('02115', 42.342, -71.086),
('02116', 42.349, -71.076),
('02118', 42.346, -71.072),

('48201', 42.328, -83.045), -- Detroit, MI
('48202', 42.354, -83.063),
('48203', 42.348, -83.064),
('48204', 42.335, -83.046),
('48205', 42.320, -83.045),
('48206', 42.336, -83.050),
('48207', 42.321, -83.062),
('48208', 42.385, -83.084),
('48209', 42.374, -83.095),
('48210', 42.372, -83.083);

INSERT INTO cost_estimates (cpt_code, service_name, zip_code, insured_avg, self_pay_avg, low_price, high_price, data_source) VALUES
('99213', 'Consulta Médica General', '02108', 135.0, 270.0, 120.0, 420.0, 'CMS'),
('99213', 'Consulta Médica General', '02109', 132.0, 265.0, 118.0, 415.0, 'CMS'),
('99213', 'Consulta Médica General', '02110', 130.0, 260.0, 115.0, 410.0, 'CMS'),
('99213', 'Consulta Médica General', '02111', 133.0, 268.0, 120.0, 420.0, 'CMS'),
('99213', 'Consulta Médica General', '02112', 136.0, 275.0, 125.0, 425.0, 'CMS'),
('99213', 'Consulta Médica General', '02113', 134.0, 270.0, 122.0, 420.0, 'CMS'),
('99213', 'Consulta Médica General', '02114', 132.0, 265.0, 118.0, 415.0, 'CMS'),
('99213', 'Consulta Médica General', '02115', 135.0, 272.0, 120.0, 420.0, 'CMS'),
('99213', 'Consulta Médica General', '02116', 137.0, 278.0, 125.0, 430.0, 'CMS'),
('99213', 'Consulta Médica General', '02118', 136.0, 275.0, 122.0, 425.0, 'CMS'),

('99213', 'Consulta Médica General', '48201', 120.0, 250.0, 110.0, 400.0, 'CMS'),
('99213', 'Consulta Médica General', '48202', 122.0, 255.0, 115.0, 405.0, 'CMS'),
('99213', 'Consulta Médica General', '48203', 125.0, 260.0, 118.0, 410.0, 'CMS'),
('99213', 'Consulta Médica General', '48204', 123.0, 252.0, 115.0, 405.0, 'CMS'),
('99213', 'Consulta Médica General', '48205', 127.0, 265.0, 120.0, 415.0, 'CMS'),
('99213', 'Consulta Médica General', '48206', 126.0, 260.0, 118.0, 410.0, 'CMS'),
('99213', 'Consulta Médica General', '48207', 124.0, 255.0, 115.0, 405.0, 'CMS'),
('99213', 'Consulta Médica General', '48208', 128.0, 268.0, 120.0, 420.0, 'CMS'),
('99213', 'Consulta Médica General', '48209', 125.0, 260.0, 118.0, 410.0, 'CMS'),
('99213', 'Consulta Médica General', '48210', 127.0, 265.0, 120.0, 415.0, 'CMS');
-- =========================================
-- Bloque de ZIPs: Minnesota → Missouri
-- =========================================
INSERT OR IGNORE INTO zip_locations (zip_code, latitude, longitude) VALUES
('55401', 44.9778, -93.2650), -- Minneapolis, MN
('55402', 44.980, -93.270),
('55403', 44.983, -93.263),
('55404', 44.976, -93.254),
('55405', 44.972, -93.242),
('55406', 44.966, -93.246),
('55407', 44.971, -93.264),
('55408', 44.968, -93.253),
('55409', 44.975, -93.257),
('55410', 44.970, -93.265),

('63101', 38.627, -90.199), -- St. Louis, MO
('63102', 38.632, -90.203),
('63103', 38.629, -90.198),
('63104', 38.631, -90.200),
('63105', 38.630, -90.201),
('63106', 38.628, -90.205),
('63107', 38.625, -90.197),
('63108', 38.626, -90.196),
('63109', 38.624, -90.199),
('63110', 38.623, -90.202);

INSERT INTO cost_estimates (cpt_code, service_name, zip_code, insured_avg, self_pay_avg, low_price, high_price, data_source) VALUES
('99213', 'Consulta Médica General', '55401', 125.0, 255.0, 115.0, 410.0, 'CMS'),
('99213', 'Consulta Médica General', '55402', 127.0, 260.0, 118.0, 415.0, 'CMS'),
('99213', 'Consulta Médica General', '55403', 124.0, 250.0, 115.0, 405.0, 'CMS'),
('99213', 'Consulta Médica General', '55404', 126.0, 258.0, 118.0, 410.0, 'CMS'),
('99213', 'Consulta Médica General', '55405', 128.0, 265.0, 120.0, 420.0, 'CMS'),
('99213', 'Consulta Médica General', '55406', 125.0, 255.0, 118.0, 410.0, 'CMS'),
('99213', 'Consulta Médica General', '55407', 127.0, 260.0, 120.0, 415.0, 'CMS'),
('99213', 'Consulta Médica General', '55408', 124.0, 250.0, 115.0, 405.0, 'CMS'),
('99213', 'Consulta Médica General', '55409', 126.0, 258.0, 118.0, 410.0, 'CMS'),
('99213', 'Consulta Médica General', '55410', 128.0, 265.0, 120.0, 420.0, 'CMS'),

('99213', 'Consulta Médica General', '63101', 120.0, 250.0, 110.0, 400.0, 'CMS'),
('99213', 'Consulta Médica General', '63102', 122.0, 255.0, 115.0, 405.0, 'CMS'),
('99213', 'Consulta Médica General', '63103', 121.0, 252.0, 112.0, 402.0, 'CMS'),
('99213', 'Consulta Médica General', '63104', 123.0, 258.0, 115.0, 408.0, 'CMS'),
('99213', 'Consulta Médica General', '63105', 124.0, 260.0, 118.0, 410.0, 'CMS'),
('99213', 'Consulta Médica General', '63106', 125.0, 265.0, 120.0, 415.0, 'CMS'),
('99213', 'Consulta Médica General', '63107', 122.0, 255.0, 115.0, 405.0, 'CMS'),
('99213', 'Consulta Médica General', '63108', 123.0, 258.0, 118.0, 410.0, 'CMS'),
('99213', 'Consulta Médica General', '63109', 124.0, 260.0, 120.0, 415.0, 'CMS'),
('99213', 'Consulta Médica General', '63110', 125.0, 265.0, 120.0, 420.0, 'CMS');
-- =========================================
-- Bloque de ZIPs: Montana → Nueva Jersey
-- =========================================
INSERT OR IGNORE INTO zip_locations (zip_code, latitude, longitude) VALUES
('59101', 45.783, -108.500), -- Billings, MT
('59102', 45.790, -108.470),
('59103', 45.780, -108.490),
('59104', 45.770, -108.480),
('59105', 45.785, -108.495),

('07001', 40.735, -74.172), -- Avenel, NJ
('07002', 40.729, -74.176),
('07003', 40.735, -74.182),
('07004', 40.731, -74.170),
('07005', 40.738, -74.160);

INSERT INTO cost_estimates (cpt_code, service_name, zip_code, insured_avg, self_pay_avg, low_price, high_price, data_source) VALUES
('99213', 'Consulta Médica General', '59101', 120.0, 250.0, 110.0, 400.0, 'CMS'),
('99213', 'Consulta Médica General', '59102', 122.0, 255.0, 115.0, 405.0, 'CMS'),
('99213', 'Consulta Médica General', '59103', 121.0, 252.0, 112.0, 402.0, 'CMS'),
('99213', 'Consulta Médica General', '59104', 123.0, 258.0, 115.0, 408.0, 'CMS'),
('99213', 'Consulta Médica General', '59105', 124.0, 260.0, 118.0, 410.0, 'CMS'),

('99213', 'Consulta Médica General', '07001', 125.0, 255.0, 115.0, 410.0, 'CMS'),
('99213', 'Consulta Médica General', '07002', 127.0, 260.0, 118.0, 415.0, 'CMS'),
('99213', 'Consulta Médica General', '07003', 124.0, 250.0, 115.0, 405.0, 'CMS'),
('99213', 'Consulta Médica General', '07004', 126.0, 258.0, 118.0, 410.0, 'CMS'),
('99213', 'Consulta Médica General', '07005', 128.0, 265.0, 120.0, 420.0, 'CMS');
-- =========================================
-- Bloque de ZIPs: Nuevo México → Nueva York
-- =========================================
INSERT OR IGNORE INTO zip_locations (zip_code, latitude, longitude) VALUES
('87101', 35.084, -106.650), -- Albuquerque, NM
('87102', 35.093, -106.616),
('87103', 35.110, -106.660),
('87104', 35.081, -106.645),
('87105', 35.067, -106.625),

('10003', 40.732, -73.989), -- Manhattan, NY
('10004', 40.703, -74.012),
('10005', 40.706, -74.008),
('10006', 40.709, -74.013),
('10007', 40.713, -74.007);

INSERT INTO cost_estimates (cpt_code, service_name, zip_code, insured_avg, self_pay_avg, low_price, high_price, data_source) VALUES
('99213', 'Consulta Médica General', '87101', 115.0, 235.0, 105.0, 390.0, 'CMS'),
('99213', 'Consulta Médica General', '87102', 117.0, 240.0, 108.0, 395.0, 'CMS'),
('99213', 'Consulta Médica General', '87103', 116.0, 238.0, 106.0, 392.0, 'CMS'),
('99213', 'Consulta Médica General', '87104', 118.0, 242.0, 110.0, 398.0, 'CMS'),
('99213', 'Consulta Médica General', '87105', 119.0, 245.0, 112.0, 400.0, 'CMS'),

('99213', 'Consulta Médica General', '10003', 130.0, 265.0, 120.0, 420.0, 'CMS'),
('99213', 'Consulta Médica General', '10004', 132.0, 270.0, 125.0, 425.0, 'CMS'),
('99213', 'Consulta Médica General', '10005', 128.0, 260.0, 118.0, 415.0, 'CMS'),
('99213', 'Consulta Médica General', '10006', 131.0, 268.0, 123.0, 422.0, 'CMS'),
('99213', 'Consulta Médica General', '10007', 133.0, 275.0, 127.0, 430.0, 'CMS');
-- =========================================
-- Bloque de ZIPs: Carolina del Norte → Dakota del Norte
-- =========================================
INSERT OR IGNORE INTO zip_locations (zip_code, latitude, longitude) VALUES
('27501', 35.835, -78.787), -- Cary, NC
('27502', 35.780, -78.800),
('27503', 35.790, -78.820),
('27504', 35.770, -78.830),
('27505', 35.760, -78.790),

('58102', 46.877, -96.789), -- Fargo, ND
('58103', 46.880, -96.805),
('58104', 46.900, -96.780),
('58105', 46.865, -96.770),
('58106', 46.890, -96.800);

INSERT INTO cost_estimates (cpt_code, service_name, zip_code, insured_avg, self_pay_avg, low_price, high_price, data_source) VALUES
('99213', 'Consulta Médica General', '27501', 120.0, 245.0, 110.0, 400.0, 'CMS'),
('99213', 'Consulta Médica General', '27502', 122.0, 248.0, 112.0, 405.0, 'CMS'),
('99213', 'Consulta Médica General', '27503', 121.0, 246.0, 111.0, 402.0, 'CMS'),
('99213', 'Consulta Médica General', '27504', 123.0, 250.0, 115.0, 408.0, 'CMS'),
('99213', 'Consulta Médica General', '27505', 125.0, 255.0, 118.0, 410.0, 'CMS'),

('99213', 'Consulta Médica General', '58102', 110.0, 230.0, 100.0, 380.0, 'CMS'),
('99213', 'Consulta Médica General', '58103', 112.0, 235.0, 102.0, 385.0, 'CMS'),
('99213', 'Consulta Médica General', '58104', 111.0, 232.0, 101.0, 382.0, 'CMS'),
('99213', 'Consulta Médica General', '58105', 113.0, 238.0, 105.0, 388.0, 'CMS'),
('99213', 'Consulta Médica General', '58106', 115.0, 240.0, 108.0, 390.0, 'CMS');
-- =========================================
-- Bloque de ZIPs: Ohio → Oklahoma
-- =========================================
INSERT OR IGNORE INTO zip_locations (zip_code, latitude, longitude) VALUES
('44101', 41.499, -81.695), -- Cleveland, OH
('44102', 41.501, -81.688),
('44103', 41.505, -81.680),
('44104', 41.510, -81.690),
('44105', 41.515, -81.700),

('73101', 35.467, -97.516), -- Oklahoma City, OK
('73102', 35.470, -97.510),
('73103', 35.465, -97.520),
('73104', 35.460, -97.525),
('73105', 35.475, -97.515);

INSERT INTO cost_estimates (cpt_code, service_name, zip_code, insured_avg, self_pay_avg, low_price, high_price, data_source) VALUES
('99213', 'Consulta Médica General', '44101', 125.0, 255.0, 115.0, 410.0, 'CMS'),
('99213', 'Consulta Médica General', '44102', 126.0, 258.0, 118.0, 415.0, 'CMS'),
('99213', 'Consulta Médica General', '44103', 124.0, 252.0, 112.0, 408.0, 'CMS'),
('99213', 'Consulta Médica General', '44104', 127.0, 260.0, 120.0, 420.0, 'CMS'),
('99213', 'Consulta Médica General', '44105', 128.0, 265.0, 122.0, 425.0, 'CMS'),

('99213', 'Consulta Médica General', '73101', 115.0, 235.0, 105.0, 390.0, 'CMS'),
('99213', 'Consulta Médica General', '73102', 116.0, 238.0, 108.0, 395.0, 'CMS'),
('99213', 'Consulta Médica General', '73103', 117.0, 240.0, 110.0, 398.0, 'CMS'),
('99213', 'Consulta Médica General', '73104', 118.0, 242.0, 112.0, 400.0, 'CMS'),
('99213', 'Consulta Médica General', '73105', 119.0, 245.0, 115.0, 405.0, 'CMS');
-- =========================================
-- Bloque de ZIPs: Oregon → Pennsylvania
-- =========================================
INSERT OR IGNORE INTO zip_locations (zip_code, latitude, longitude) VALUES
('97035', 45.420, -122.761), -- Beaverton, OR
('97201', 45.515, -122.678), -- Portland, OR
('97202', 45.520, -122.681),
('97203', 45.522, -122.685),
('97204', 45.523, -122.676),

('19101', 39.952, -75.165), -- Philadelphia, PA
('19102', 39.950, -75.160),
('19103', 39.948, -75.155),
('19104', 39.952, -75.190),
('19105', 39.954, -75.165);

INSERT INTO cost_estimates (cpt_code, service_name, zip_code, insured_avg, self_pay_avg, low_price, high_price, data_source) VALUES
('99213', 'Consulta Médica General', '97035', 118.0, 240.0, 108.0, 395.0, 'CMS'),
('99213', 'Consulta Médica General', '97201', 120.0, 245.0, 110.0, 400.0, 'CMS'),
('99213', 'Consulta Médica General', '97202', 119.0, 242.0, 108.0, 398.0, 'CMS'),
('99213', 'Consulta Médica General', '97203', 121.0, 248.0, 112.0, 405.0, 'CMS'),
('99213', 'Consulta Médica General', '97204', 122.0, 250.0, 115.0, 410.0, 'CMS'),

('99213', 'Consulta Médica General', '19101', 125.0, 255.0, 115.0, 420.0, 'CMS'),
('99213', 'Consulta Médica General', '19102', 126.0, 258.0, 118.0, 425.0, 'CMS'),
('99213', 'Consulta Médica General', '19103', 127.0, 260.0, 120.0, 430.0, 'CMS'),
('99213', 'Consulta Médica General', '19104', 128.0, 265.0, 122.0, 435.0, 'CMS'),
('99213', 'Consulta Médica General', '19105', 129.0, 270.0, 125.0, 440.0, 'CMS');
-- =========================================
-- Bloque de ZIPs: Rhode Island → South Carolina
-- =========================================
INSERT OR IGNORE INTO zip_locations (zip_code, latitude, longitude) VALUES
('02903', 41.823, -71.418), -- Providence, RI
('02904', 41.823, -71.412),
('02905', 41.821, -71.404),
('02906', 41.830, -71.400),
('02907', 41.825, -71.395),

('29201', 34.000, -81.035), -- Columbia, SC
('29202', 34.005, -81.040),
('29203', 34.010, -81.045),
('29204', 34.015, -81.050),
('29205', 34.020, -81.055);

INSERT INTO cost_estimates (cpt_code, service_name, zip_code, insured_avg, self_pay_avg, low_price, high_price, data_source) VALUES
('99213', 'Consulta Médica General', '02903', 135.0, 270.0, 120.0, 450.0, 'CMS'),
('99213', 'Consulta Médica General', '02904', 136.0, 275.0, 122.0, 455.0, 'CMS'),
('99213', 'Consulta Médica General', '02905', 137.0, 280.0, 125.0, 460.0, 'CMS'),
('99213', 'Consulta Médica General', '02906', 138.0, 285.0, 128.0, 465.0, 'CMS'),
('99213', 'Consulta Médica General', '02907', 139.0, 290.0, 130.0, 470.0, 'CMS'),

('99213', 'Consulta Médica General', '29201', 140.0, 295.0, 130.0, 480.0, 'CMS'),
('99213', 'Consulta Médica General', '29202', 142.0, 300.0, 135.0, 485.0, 'CMS'),
('99213', 'Consulta Médica General', '29203', 144.0, 305.0, 138.0, 490.0, 'CMS'),
('99213', 'Consulta Médica General', '29204', 146.0, 310.0, 140.0, 495.0, 'CMS'),
('99213', 'Consulta Médica General', '29205', 148.0, 315.0, 145.0, 500.0, 'CMS');
-- =========================================
-- Bloque de ZIPs: South Dakota → Wyoming
-- =========================================
INSERT OR IGNORE INTO zip_locations (zip_code, latitude, longitude) VALUES
('57101', 43.5446, -96.7311), -- Sioux Falls, SD
('57102', 43.5469, -96.7000),
('57103', 43.5625, -96.7295),
('57104', 43.5250, -96.7025),
('57105', 43.5300, -96.7200),

('82001', 41.1390, -104.8202), -- Cheyenne, WY
('82002', 41.1420, -104.8020),
('82003', 41.1500, -104.8150),
('82004', 41.1550, -104.8100),
('82005', 41.1600, -104.8050);

INSERT INTO cost_estimates (cpt_code, service_name, zip_code, insured_avg, self_pay_avg, low_price, high_price, data_source) VALUES
('99213', 'Consulta Médica General', '57101', 130.0, 260.0, 115.0, 400.0, 'CMS'),
('99213', 'Consulta Médica General', '57102', 132.0, 265.0, 118.0, 405.0, 'CMS'),
('99213', 'Consulta Médica General', '57103', 134.0, 270.0, 120.0, 410.0, 'CMS'),
('99213', 'Consulta Médica General', '57104', 136.0, 275.0, 122.0, 415.0, 'CMS'),
('99213', 'Consulta Médica General', '57105', 138.0, 280.0, 125.0, 420.0, 'CMS'),

('99213', 'Consulta Médica General', '82001', 140.0, 300.0, 130.0, 450.0, 'CMS'),
('99213', 'Consulta Médica General', '82002', 142.0, 305.0, 135.0, 455.0, 'CMS'),
('99213', 'Consulta Médica General', '82003', 144.0, 310.0, 138.0, 460.0, 'CMS'),
('99213', 'Consulta Médica General', '82004', 146.0, 315.0, 140.0, 465.0, 'CMS'),
('99213', 'Consulta Médica General', '82005', 148.0, 320.0, 145.0, 470.0, 'CMS');
