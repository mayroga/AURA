-- TABLA OFICIAL AURA POR MAY ROGA LLC
DROP TABLE IF EXISTS cost_estimates;
CREATE TABLE cost_estimates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cpt_code TEXT NOT NULL,
    description TEXT,
    state TEXT NOT NULL,
    zip_code TEXT NOT NULL,
    low_price REAL NOT NULL,
    high_price REAL NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- INSERTS ESTADOS A - M
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price) VALUES
-- ALABAMA (AL)
('D1110','Limpieza Adulto','AL','35004',70,140),('D2750','Corona Porcelana','AL','35004',750,1400),('99213','Consulta Médica','AL','35004',90,180),
-- ALASKA (AK)
('D1110','Limpieza Adulto','AK','99501',85,170),('D2750','Corona Porcelana','AK','99501',900,1600),('99213','Consulta Médica','AK','99501',110,220),
-- ARIZONA (AZ)
('D1110','Limpieza Adulto','AZ','85001',75,150),('D2750','Corona Porcelana','AZ','85001',800,1450),('99213','Consulta Médica','AZ','85001',95,190),
-- ARKANSAS (AR)
('D1110','Limpieza Adulto','AR','72201',68,135),('D2750','Corona Porcelana','AR','72201',740,1380),('99213','Consulta Médica','AR','72201',85,170),
-- CALIFORNIA (CA)
('D1110','Limpieza Adulto','CA','90001',95,190),('D2750','Corona Porcelana','CA','90001',950,1800),('99213','Consulta Médica','CA','90001',120,250),
-- COLORADO (CO)
('D1110','Limpieza Adulto','CO','80201',80,160),('D2750','Corona Porcelana','CO','80201',850,1500),('99213','Consulta Médica','CO','80201',100,210),
-- CONNECTICUT (CT)
('D1110','Limpieza Adulto','CT','06101',88,175),('D2750','Corona Porcelana','CT','06101',880,1550),('99213','Consulta Médica','CT','06101',110,230),
-- DELAWARE (DE)
('D1110','Limpieza Adulto','DE','19901',78,155),('D2750','Corona Porcelana','DE','19901',820,1480),('99213','Consulta Médica','DE','19901',95,200),
-- FLORIDA (FL)
('D1110','Limpieza Adulto','FL','33101',85,165),('D2750','Corona Porcelana','FL','33101',850,1550),('99213','Consulta Médica','FL','33101',100,210),
-- GEORGIA (GA)
('D1110','Limpieza Adulto','GA','30301',76,155),('D2750','Corona Porcelana','GA','30301',810,1490),('99213','Consulta Médica','GA','30301',95,195),
-- HAWAII (HI)
('D1110','Limpieza Adulto','HI','96801',98,190),('D2750','Corona Porcelana','HI','96801',980,1750),('99213','Consulta Médica','HI','96801',130,260),
-- IDAHO (ID)
('D1110','Limpieza Adulto','ID','83201',72,145),('D2750','Corona Porcelana','ID','83201',780,1420),('99213','Consulta Médica','ID','83201',90,185),
-- ILLINOIS (IL)
('D1110','Limpieza Adulto','IL','60601',82,165),('D2750','Corona Porcelana','IL','60601',860,1550),('99213','Consulta Médica','IL','60601',105,215),
-- INDIANA (IN)
('D1110','Limpieza Adulto','IN','46201',74,150),('D2750','Corona Porcelana','IN','46201',790,1440),('99213','Consulta Médica','IN','46201',92,185),
-- IOWA (IA)
('D1110','Limpieza Adulto','IA','50301',71,142),('D2750','Corona Porcelana','IA','50301',760,1410),('99213','Consulta Médica','IA','50301',88,175),
-- KANSAS (KS)
('D1110','Limpieza Adulto','KS','66101',73,148),('D2750','Corona Porcelana','KS','66101',785,1430),('99213','Consulta Médica','KS','66101',90,180),
-- KENTUCKY (KY)
('D1110','Limpieza Adulto','KY','40201',70,140),('D2750','Corona Porcelana','KY','40201',750,1400),('99213','Consulta Médica','KY','40201',85,175),
-- LOUISIANA (LA)
('D1110','Limpieza Adulto','LA','70112',75,155),('D2750','Corona Porcelana','LA','70112',810,1480),('99213','Consulta Médica','LA','70112',95,200),
-- MAINE (ME)
('D1110','Limpieza Adulto','ME','04101',79,160),('D2750','Corona Porcelana','ME','04101',840,1520),('99213','Consulta Médica','ME','04101',100,210),
-- MARYLAND (MD)
('D1110','Limpieza Adulto','MD','21201',85,170),('D2750','Corona Porcelana','MD','21201',890,1600),('99213','Consulta Médica','MD','21201',110,230),
-- MASSACHUSETTS (MA)
('D1110','Limpieza Adulto','MA','02101',95,195),('D2750','Corona Porcelana','MA','02101',980,1850),('99213','Consulta Médica','MA','02101',125,260),
-- MICHIGAN (MI)
('D1110','Limpieza Adulto','MI','48201',78,160),('D2750','Corona Porcelana','MI','48201',830,1500),('99213','Consulta Médica','MI','48201',100,205),
-- MINNESOTA (MN)
('D1110','Limpieza Adulto','MN','55401',82,165),('D2750','Corona Porcelana','MN','55401',860,1550),('99213','Consulta Médica','MN','55401',105,215),
-- MISSISSIPPI (MS)
('D1110','Limpieza Adulto','MS','39201',65,130),('D2750','Corona Porcelana','MS','39201',710,1350),('99213','Consulta Médica','MS','39201',80,160),
-- MISSOURI (MO)
('D1110','Limpieza Adulto','MO','63101',74,150),('D2750','Corona Porcelana','MO','63101',790,1450),('99213','Consulta Médica','MO','63101',90,190),
-- MONTANA (MT)
('D1110','Limpieza Adulto','MT','59101',70,145),('D2750','Corona Porcelana','MT','59101',760,1400),('99213','Consulta Médica','MT','59101',85,175);
-- INSERTS ESTADOS N - Z
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price) VALUES
-- NEBRASKA (NE)
('D1110','Limpieza Adulto','NE','68101',70,145),('D2750','Corona Porcelana','NE','68101',760,1410),('99213','Consulta Médica','NE','68101',88,180),
-- NEVADA (NV)
('D1110','Limpieza Adulto','NV','89101',82,165),('D2750','Corona Porcelana','NV','89101',880,1550),('99213','Consulta Médica','NV','89101',105,210),
-- NEW JERSEY (NJ)
('D1110','Limpieza Adulto','NJ','07101',92,185),('D2750','Corona Porcelana','NJ','07101',940,1750),('99213','Consulta Médica','NJ','07101',120,240),
-- NEW YORK (NY)
('D1110','Limpieza Adulto','NY','10001',105,210),('D2750','Corona Porcelana','NY','10001',1100,2100),('99213','Consulta Médica','NY','10001',140,290),
-- NORTH CAROLINA (NC)
('D1110','Limpieza Adulto','NC','27601',78,160),('D2750','Corona Porcelana','NC','27601',830,1500),('99213','Consulta Médica','NC','27601',100,205),
-- OHIO (OH)
('D1110','Limpieza Adulto','OH','43201',75,155),('D2750','Corona Porcelana','OH','43201',800,1480),('99213','Consulta Médica','OH','43201',95,195),
-- PENNSYLVANIA (PA)
('D1110','Limpieza Adulto','PA','19101',84,170),('D2750','Corona Porcelana','PA','19101',880,1600),('99213','Consulta Médica','PA','19101',110,225),
-- TEXAS (TX)
('D1110','Limpieza Adulto','TX','73301',82,165),('D2750','Corona Porcelana','TX','73301',870,1580),('99213','Consulta Médica','TX','73301',105,215),
-- UTAH (UT)
('D1110','Limpieza Adulto','UT','84101',76,155),('D2750','Corona Porcelana','UT','84101',810,1490),('99213','Consulta Médica','UT','84101',95,195),
-- VIRGINIA (VA)
('D1110','Limpieza Adulto','VA','23218',80,165),('D2750','Corona Porcelana','VA','23218',850,1550),('99213','Consulta Médica','VA','23218',105,220),
-- WASHINGTON (WA)
('D1110','Limpieza Adulto','WA','98101',92,185),('D2750','Corona Porcelana','WA','98101',940,1700),('99213','Consulta Médica','WA','98101',120,245),
-- WYOMING (WY)
('D1110','Limpieza Adulto','WY','82001',70,145),('D2750','Corona Porcelana','WY','82001',770,1420),('99213','Consulta Médica','WY','82001',88,180);

CREATE INDEX idx_cpt_state_zip ON cost_estimates(cpt_code, state, zip_code);
