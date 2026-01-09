-- ===========================================
-- TABLA cost_estimates
-- ===========================================
CREATE TABLE IF NOT EXISTS cost_estimates (
    id SERIAL PRIMARY KEY,
    cpt_code VARCHAR(20) NOT NULL,
    description TEXT,
    state CHAR(2) NOT NULL,
    zip_code VARCHAR(10) NOT NULL,
    low_price NUMERIC(10,2) NOT NULL,
    high_price NUMERIC(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_cpt_state_zip
ON cost_estimates(cpt_code, state, zip_code);

-- ===========================================
-- INSERTS DE EJEMPLO
-- ESTADOS: A–M
-- ===========================================

-- ALABAMA (AL)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','AL','35004',70,140),
('D1120','Prophylaxis Child','AL','35004',55,110),
('D2750','Crown - porcelain fused to metal','AL','35004',750,1400),
('99213','Office visit established patient','AL','35004',90,180),
('80053','Comprehensive metabolic panel','AL','35004',40,100),
('D4341','Periodontal scaling & root planing','AL','35004',170,400),
('D0210','Full mouth X-ray','AL','35004',100,220),
('99214','Office visit, moderate complexity','AL','35004',130,260),
('80048','Basic metabolic panel','AL','35004',35,90),
('D2330','Resin-based composite, anterior','AL','35004',130,300);

-- ALASKA (AK)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','AK','99501',80,160),
('D1120','Prophylaxis Child','AK','99501',65,130),
('D2750','Crown - porcelain fused to metal','AK','99501',850,1500),
('99213','Office visit established patient','AK','99501',100,200),
('80053','Comprehensive metabolic panel','AK','99501',50,120),
('D4341','Periodontal scaling & root planing','AK','99501',200,450),
('D0210','Full mouth X-ray','AK','99501',120,250),
('99214','Office visit, moderate complexity','AK','99501',150,300),
('80048','Basic metabolic panel','AK','99501',40,100),
('D2330','Resin-based composite, anterior','AK','99501',150,350);

-- ARKANSAS (AR)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','AR','72201',68,135),
('D1120','Prophylaxis Child','AR','72201',55,110),
('D2750','Crown - porcelain fused to metal','AR','72201',740,1380),
('99213','Office visit established patient','AR','72201',88,175),
('80053','Comprehensive metabolic panel','AR','72201',38,95),
('D4341','Periodontal scaling & root planing','AR','72201',165,390),
('D0210','Full mouth X-ray','AR','72201',95,215),
('99214','Office visit, moderate complexity','AR','72201',125,250),
('80048','Basic metabolic panel','AR','72201',35,85),
('D2330','Resin-based composite, anterior','AR','72201',125,290);

-- CALIFORNIA (CA)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','CA','90001',80,160),
('D1120','Prophylaxis Child','CA','90001',65,130),
('D2750','Crown - porcelain fused to metal','CA','90001',850,1500),
('99213','Office visit established patient','CA','90001',100,200),
('80053','Comprehensive metabolic panel','CA','90001',55,125),
('D4341','Periodontal scaling & root planing','CA','90001',200,450),
('D0210','Full mouth X-ray','CA','90001',120,250),
('99214','Office visit, moderate complexity','CA','90001',150,300),
('80048','Basic metabolic panel','CA','90001',40,100),
('D2330','Resin-based composite, anterior','CA','90001',150,350);

-- COLORADO (CO)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','CO','80201',78,155),
('D1120','Prophylaxis Child','CO','80201',63,125),
('D2750','Crown - porcelain fused to metal','CO','80201',820,1480),
('99213','Office visit established patient','CO','80201',98,195),
('80053','Comprehensive metabolic panel','CO','80201',50,120),
('D4341','Periodontal scaling & root planing','CO','80201',190,440),
('D0210','Full mouth X-ray','CO','80201',115,245),
('99214','Office visit, moderate complexity','CO','80201',145,290),
('80048','Basic metabolic panel','CO','80201',42,105),
('D2330','Resin-based composite, anterior','CO','80201',145,340);

-- CONNECTICUT (CT)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','CT','06101',85,165),
('D1120','Prophylaxis Child','CT','06101',70,135),
('D2750','Crown - porcelain fused to metal','CT','06101',870,1520),
('99213','Office visit established patient','CT','06101',105,210),
('80053','Comprehensive metabolic panel','CT','06101',58,130),
('D4341','Periodontal scaling & root planing','CT','06101',210,460),
('D0210','Full mouth X-ray','CT','06101',125,260),
('99214','Office visit, moderate complexity','CT','06101',155,310),
('80048','Basic metabolic panel','CT','06101',45,110),
('D2330','Resin-based composite, anterior','CT','06101',155,360);

-- DELAWARE (DE)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','DE','19901',75,150),
('D1120','Prophylaxis Child','DE','19901',60,120),
('D2750','Crown - porcelain fused to metal','DE','19901',800,1450),
('99213','Office visit established patient','DE','19901',95,190),
('80053','Comprehensive metabolic panel','DE','19901',45,115),
('D4341','Periodontal scaling & root planing','DE','19901',180,420),
('D0210','Full mouth X-ray','DE','19901',110,240),
('99214','Office visit, moderate complexity','DE','19901',140,280),
('80048','Basic metabolic panel','DE','19901',38,95),
('D2330','Resin-based composite, anterior','DE','19901',140,330);

-- DISTRICT OF COLUMBIA (DC)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','DC','20001',80,160),
('D1120','Prophylaxis Child','DC','20001',65,130),
('D2750','Crown - porcelain fused to metal','DC','20001',850,1500),
('99213','Office visit established patient','DC','20001',100,200),
('80053','Comprehensive metabolic panel','DC','20001',50,120),
('D4341','Periodontal scaling & root planing','DC','20001',200,450),
('D0210','Full mouth X-ray','DC','20001',120,250),
('99214','Office visit, moderate complexity','DC','20001',150,300),
('80048','Basic metabolic panel','DC','20001',40,100),
('D2330','Resin-based composite, anterior','DC','20001',150,350);

-- FLORIDA (FL)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','FL','33101',78,155),
('D1120','Prophylaxis Child','FL','33101',63,125),
('D2750','Crown - porcelain fused to metal','FL','33101',820,1480),
('99213','Office visit established patient','FL','33101',98,195),
('80053','Comprehensive metabolic panel','FL','33101',50,120),
('D4341','Periodontal scaling & root planing','FL','33101',190,440),
('D0210','Full mouth X-ray','FL','33101',115,245),
('99214','Office visit, moderate complexity','FL','33101',145,290),
('80048','Basic metabolic panel','FL','33101',42,105),
('D2330','Resin-based composite, anterior','FL','33101',145,340);

-- GEORGIA (GA)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','GA','30301',75,150),
('D1120','Prophylaxis Child','GA','30301',60,120),
('D2750','Crown - porcelain fused to metal','GA','30301',800,1450),
('99213','Office visit established patient','GA','30301',95,190),
('80053','Comprehensive metabolic panel','GA','30301',45,115),
('D4341','Periodontal scaling & root planing','GA','30301',180,420),
('D0210','Full mouth X-ray','GA','30301',110,240),
('99214','Office visit, moderate complexity','GA','30301',140,280),
('80048','Basic metabolic panel','GA','30301',38,95),
('D2330','Resin-based composite, anterior','GA','30301',140,330);

-- HAWAII (HI)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','HI','96801',85,170),
('D1120','Prophylaxis Child','HI','96801',70,135),
('D2750','Crown - porcelain fused to metal','HI','96801',870,1520),
('99213','Office visit established patient','HI','96801',105,210),
('80053','Comprehensive metabolic panel','HI','96801',58,130),
('D4341','Periodontal scaling & root planing','HI','96801',210,460),
('D0210','Full mouth X-ray','HI','96801',125,260),
('99214','Office visit, moderate complexity','HI','96801',155,310),
('80048','Basic metabolic panel','HI','96801',45,110),
('D2330','Resin-based composite, anterior','HI','96801',155,360);

-- IDAHO (ID)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','ID','83201',72,145),
('D1120','Prophylaxis Child','ID','83201',58,115),
('D2750','Crown - porcelain fused to metal','ID','83201',780,1420),
('99213','Office visit established patient','ID','83201',92,185),
('80053','Comprehensive metabolic panel','ID','83201',42,105),
('D4341','Periodontal scaling & root planing','ID','83201',175,410),
('D0210','Full mouth X-ray','ID','83201',105,225),
('99214','Office visit, moderate complexity','ID','83201',135,270),
('80048','Basic metabolic panel','ID','83201',37,95),
('D2330','Resin-based composite, anterior','ID','83201',135,310);

-- ILLINOIS (IL)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','IL','60601',78,155),
('D1120','Prophylaxis Child','IL','60601',65,130),
('D2750','Crown - porcelain fused to metal','IL','60601',820,1480),
('99213','Office visit established patient','IL','60601',100,200),
('80053','Comprehensive metabolic panel','IL','60601',50,120),
('D4341','Periodontal scaling & root planing','IL','60601',190,440),
('D0210','Full mouth X-ray','IL','60601',115,245),
('99214','Office visit, moderate complexity','IL','60601',145,290),
('80048','Basic metabolic panel','IL','60601',42,105),
('D2330','Resin-based composite, anterior','IL','60601',145,340);

-- INDIANA (IN)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','IN','46201',75,150),
('D1120','Prophylaxis Child','IN','46201',60,120),
('D2750','Crown - porcelain fused to metal','IN','46201',800,1450),
('99213','Office visit established patient','IN','46201',95,190),
('80053','Comprehensive metabolic panel','IN','46201',45,115),
('D4341','Periodontal scaling & root planing','IN','46201',180,420),
('D0210','Full mouth X-ray','IN','46201',110,240),
('99214','Office visit, moderate complexity','IN','46201',140,280),
('80048','Basic metabolic panel','IN','46201',38,95),
('D2330','Resin-based composite, anterior','IN','46201',140,330);

-- IOWA (IA)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','IA','50301',70,140),
('D1120','Prophylaxis Child','IA','50301',55,110),
('D2750','Crown - porcelain fused to metal','IA','50301',750,1400),
('99213','Office visit established patient','IA','50301',90,180),
('80053','Comprehensive metabolic panel','IA','50301',40,100),
('D4341','Periodontal scaling & root planing','IA','50301',170,400),
('D0210','Full mouth X-ray','IA','50301',100,220),
('99214','Office visit, moderate complexity','IA','50301',130,260),
('80048','Basic metabolic panel','IA','50301',35,90),
('D2330','Resin-based composite, anterior','IA','50301',130,300);

-- KANSAS (KS)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','KS','66101',72,145),
('D1120','Prophylaxis Child','KS','66101',58,115),
('D2750','Crown - porcelain fused to metal','KS','66101',780,1420),
('99213','Office visit established patient','KS','66101',92,185),
('80053','Comprehensive metabolic panel','KS','66101',42,105),
('D4341','Periodontal scaling & root planing','KS','66101',175,410),
('D0210','Full mouth X-ray','KS','66101',105,225),
('99214','Office visit, moderate complexity','KS','66101',135,270),
('80048','Basic metabolic panel','KS','66101',37,95),
('D2330','Resin-based composite, anterior','KS','66101',135,310);

-- KENTUCKY (KY)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','KY','40201',70,140),
('D1120','Prophylaxis Child','KY','40201',55,110),
('D2750','Crown - porcelain fused to metal','KY','40201',750,1400),
('99213','Office visit established patient','KY','40201',90,180),
('80053','Comprehensive metabolic panel','KY','40201',40,100),
('D4341','
-- ===========================================
-- INSERTS DE EJEMPLO
-- ESTADOS: N–WY
-- ===========================================

-- NEBRASKA (NE)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','NE','68101',70,140),
('D1120','Prophylaxis Child','NE','68101',55,110),
('D2750','Crown - porcelain fused to metal','NE','68101',750,1400),
('99213','Office visit established patient','NE','68101',90,180),
('80053','Comprehensive metabolic panel','NE','68101',40,100),
('D4341','Periodontal scaling & root planing','NE','68101',170,400),
('D0210','Full mouth X-ray','NE','68101',100,220),
('99214','Office visit, moderate complexity','NE','68101',130,260),
('80048','Basic metabolic panel','NE','68101',35,90),
('D2330','Resin-based composite, anterior','NE','68101',130,300);

-- NEVADA (NV)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','NV','89501',80,160),
('D1120','Prophylaxis Child','NV','89501',65,130),
('D2750','Crown - porcelain fused to metal','NV','89501',850,1500),
('99213','Office visit established patient','NV','89501',100,200),
('80053','Comprehensive metabolic panel','NV','89501',50,120),
('D4341','Periodontal scaling & root planing','NV','89501',200,450),
('D0210','Full mouth X-ray','NV','89501',120,250),
('99214','Office visit, moderate complexity','NV','89501',150,300),
('80048','Basic metabolic panel','NV','89501',40,100),
('D2330','Resin-based composite, anterior','NV','89501',150,350);

-- NEW HAMPSHIRE (NH)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','NH','03301',85,165),
('D1120','Prophylaxis Child','NH','03301',70,135),
('D2750','Crown - porcelain fused to metal','NH','03301',870,1520),
('99213','Office visit established patient','NH','03301',105,210),
('80053','Comprehensive metabolic panel','NH','03301',58,130),
('D4341','Periodontal scaling & root planing','NH','03301',210,460),
('D0210','Full mouth X-ray','NH','03301',125,260),
('99214','Office visit, moderate complexity','NH','03301',155,310),
('80048','Basic metabolic panel','NH','03301',45,110),
('D2330','Resin-based composite, anterior','NH','03301',155,360);

-- NEW JERSEY (NJ)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','NJ','07001',85,165),
('D1120','Prophylaxis Child','NJ','07001',70,135),
('D2750','Crown - porcelain fused to metal','NJ','07001',870,1520),
('99213','Office visit established patient','NJ','07001',105,210),
('80053','Comprehensive metabolic panel','NJ','07001',58,130),
('D4341','Periodontal scaling & root planing','NJ','07001',210,460),
('D0210','Full mouth X-ray','NJ','07001',125,260),
('99214','Office visit, moderate complexity','NJ','07001',155,310),
('80048','Basic metabolic panel','NJ','07001',45,110),
('D2330','Resin-based composite, anterior','NJ','07001',155,360);

-- NEW MEXICO (NM)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','NM','87501',75,150),
('D1120','Prophylaxis Child','NM','87501',60,120),
('D2750','Crown - porcelain fused to metal','NM','87501',800,1450),
('99213','Office visit established patient','NM','87501',95,190),
('80053','Comprehensive metabolic panel','NM','87501',45,115),
('D4341','Periodontal scaling & root planing','NM','87501',180,420),
('D0210','Full mouth X-ray','NM','87501',110,240),
('99214','Office visit, moderate complexity','NM','87501',140,280),
('80048','Basic metabolic panel','NM','87501',38,95),
('D2330','Resin-based composite, anterior','NM','87501',140,330);

-- NEW YORK (NY)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','NY','10001',85,165),
('D1120','Prophylaxis Child','NY','10001',70,135),
('D2750','Crown - porcelain fused to metal','NY','10001',870,1520),
('99213','Office visit established patient','NY','10001',105,210),
('80053','Comprehensive metabolic panel','NY','10001',58,130),
('D4341','Periodontal scaling & root planing','NY','10001',210,460),
('D0210','Full mouth X-ray','NY','10001',125,260),
('99214','Office visit, moderate complexity','NY','10001',155,310),
('80048','Basic metabolic panel','NY','10001',45,110),
('D2330','Resin-based composite, anterior','NY','10001',155,360);

-- NORTH CAROLINA (NC)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','NC','27501',75,150),
('D1120','Prophylaxis Child','NC','27501',60,120),
('D2750','Crown - porcelain fused to metal','NC','27501',800,1450),
('99213','Office visit established patient','NC','27501',95,190),
('80053','Comprehensive metabolic panel','NC','27501',45,115),
('D4341','Periodontal scaling & root planing','NC','27501',180,420),
('D0210','Full mouth X-ray','NC','27501',110,240),
('99214','Office visit, moderate complexity','NC','27501',140,280),
('80048','Basic metabolic panel','NC','27501',38,95),
('D2330','Resin-based composite, anterior','NC','27501',140,330);

-- NORTH DAKOTA (ND)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','ND','58102',70,140),
('D1120','Prophylaxis Child','ND','58102',55,110),
('D2750','Crown - porcelain fused to metal','ND','58102',750,1400),
('99213','Office visit established patient','ND','58102',90,180),
('80053','Comprehensive metabolic panel','ND','58102',40,100),
('D4341','Periodontal scaling & root planing','ND','58102',170,400),
('D0210','Full mouth X-ray','ND','58102',100,220),
('99214','Office visit, moderate complexity','ND','58102',130,260),
('80048','Basic metabolic panel','ND','58102',35,90),
('D2330','Resin-based composite, anterior','ND','58102',130,300);

-- OHIO (OH)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','OH','43004',70,140),
('D1120','Prophylaxis Child','OH','43004',55,110),
('D2750','Crown - porcelain fused to metal','OH','43004',750,1400),
('99213','Office visit established patient','OH','43004',90,180),
('80053','Comprehensive metabolic panel','OH','43004',40,100),
('D4341','Periodontal scaling & root planing','OH','43004',170,400),
('D0210','Full mouth X-ray','OH','43004',100,220),
('99214','Office visit, moderate complexity','OH','43004',130,260),
('80048','Basic metabolic panel','OH','43004',35,90),
('D2330','Resin-based composite, anterior','OH','43004',130,300);

-- OKLAHOMA (OK)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','OK','73101',68,135),
('D1120','Prophylaxis Child','OK','73101',55,110),
('D2750','Crown - porcelain fused to metal','OK','73101',740,1380),
('99213','Office visit established patient','OK','73101',88,175),
('80053','Comprehensive metabolic panel','OK','73101',38,95),
('D4341','Periodontal scaling & root planing','OK','73101',165,390),
('D0210','Full mouth X-ray','OK','73101',95,215),
('99214','Office visit, moderate complexity','OK','73101',125,250),
('80048','Basic metabolic panel','OK','73101',35,85),
('D2330','Resin-based composite, anterior','OK','73101',125,290);

-- OREGON (OR)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','OR','97001',75,150),
('D1120','Prophylaxis Child','OR','97001',60,120),
('D2750','Crown - porcelain fused to metal','OR','97001',800,1450),
('99213','Office visit established patient','OR','97001',95,190),
('80053','Comprehensive metabolic panel','OR','97001',45,115),
('D4341','Periodontal scaling & root planing','OR','97001',180,420),
('D0210','Full mouth X-ray','OR','97001',110,240),
('99214','Office visit, moderate complexity','OR','97001',140,280),
('80048','Basic metabolic panel','OR','97001',38,95),
('D2330','Resin-based composite, anterior','OR','97001',140,330);

-- PENNSYLVANIA (PA)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','PA','19019',75,150),
('D1120','Prophylaxis Child','PA','19019',60,120),
('D2750','Crown - porcelain fused to metal','PA','19019',800,1450),
('99213','Office visit established patient','PA','19019',95,190),
('80053','Comprehensive metabolic panel','PA','19019',45,115),
('D4341','Periodontal scaling & root planing','PA','19019',180,420),
('D0210','Full mouth X-ray','PA','19019',110,240),
('99214','Office visit, moderate complexity','PA','19019',140,280),
('80048','Basic metabolic panel','PA','19019',38,95),
('D2330','Resin-based composite, anterior','PA','19019',140,330);

-- RHODE ISLAND (RI)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','RI','02901',80,160),
('D1120','Prophylaxis Child','RI','02901',65,130),
('D2750','Crown - porcelain fused to metal','RI','02901',850,1500),
('99213','Office visit established patient','RI','02901',100,200),
('80053','Comprehensive metabolic panel','RI','02901',50,120),
('D4341','Periodontal scaling & root planing','RI','02901',200,450),
('D0210','Full mouth X-ray','RI','02901',120,250),
('99214','Office visit, moderate complexity','RI','02901',150,300),
('80048','Basic metabolic panel','RI','02901',40,100),
('D2330','Resin-based composite, anterior','RI','02901',150,350);

-- SOUTH CAROLINA (SC)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','SC','29201',70,140),
('D1120','Prophylaxis Child','SC','29201',55,110),
('D2750','Crown - porcelain fused to metal','SC','29201',750,1400),
('99213','Office visit established patient','SC','29201',90,180),
('80053','Comprehensive metabolic panel','SC','29201',40,100),
('D4341','Periodontal scaling & root planing','SC','29201',170,400),
('D0210','Full mouth X-ray','SC','29201',100,220),
('99214','Office visit, moderate complexity','SC','29201',130,260),
('80048','Basic metabolic panel','SC','29201',35,90),
('D2330','Resin-based composite, anterior','SC','29201',130,300);

-- SOUTH DAKOTA (SD)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','SD','57101',70,140),
('D1120','Prophylaxis Child','SD','57101',55,110),
('D2750','Crown - porcelain fused to metal','SD','57101',750,1400),
('99213','Office visit established patient','SD','57101',90,180),
('80053','Comprehensive metabolic panel','SD','57101',40,100),
('D4341','Periodontal scaling & root planing','SD','57101',170,400),
('D0210','Full mouth X-ray','SD','57101',100,220),
('99214','Office visit, moderate complexity','SD','57101',130,260),
('80048','Basic metabolic panel','SD','57101',35,90),
('D2330','Resin-based composite, anterior','SD','57101',130,300);

-- TENNESSEE (TN)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','TN','37201',70,140),
('D1120','Prophylaxis Child','TN','37201',55,110),
('D2750','Crown - porcelain fused to metal','TN','37201',750,1400),
('99213','Office visit established patient','TN','37201',90,180),
('80053','Comprehensive metabolic panel','TN','37201',40,100),
('D4341','Periodontal scaling & root planing','TN','37201',170,400),
('D0210','Full mouth X-ray','TN','37201',100,220),
('99214','Office visit, moderate complexity','TN','37201',130,260),
('80048','Basic metabolic panel','TN','37201',35,90),
('D2330','Resin-based composite, anterior','TN','37201',130,300);

-- TEXAS (TX)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','TX','73301',70,140),
('D1120','Prophylaxis Child','TX','73301',55,110),
('D2750','Crown - porcelain fused to metal','TX','73301',750,1400),
('99213','Office visit established patient','TX','73301',90,180),
('80053','Comprehensive metabolic panel','TX','73301',40,100),
('D4341','Periodontal scaling & root planing','TX','73301',170,400),
('D0210','Full mouth X-ray','TX','73301',100,220),
('99214','Office visit, moderate complexity','TX','73301',130,260),
('80048','Basic metabolic panel','TX','73301',35,90),
('D2330','Resin-based composite, anterior','TX','73301',130,300);

-- UTAH (UT)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','UT','84101',72,145),
('D1120','Prophylaxis Child','UT','84101',58,115),
('D2750','Crown - porcelain fused to metal','UT','84101',780,1420),
('99213','Office visit established patient','UT','84101',92,185),
('80053','Comprehensive metabolic panel','UT','84101',42,105),
('D4341','Periodontal scaling & root planing','UT','84101',175,410),
('D0210','Full mouth X-ray','UT','84101',105,225),
('99214','Office visit, moderate complexity','UT','84101',135,270),
('80048','Basic metabolic panel','UT','84101',37,95),
('D2330','Resin-based composite, anterior','UT','84101',135,310);

-- VERMONT (VT)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','VT','05601',75,150),
('D1120','Prophylaxis Child','VT','05601',60,120),
('D2750','Crown - porcelain fused to metal','VT','05601',800,1450),
('99213','Office visit established patient','VT','05601',95,190),
('80053','Comprehensive metabolic panel','VT','05601',45,115),
('D4341','Periodontal scaling & root planing','VT','05601',180,420),
('D0210','Full mouth X-ray','VT','05601',110,240),
('99214','Office visit, moderate complexity','VT','05601',140,280),
('80048','Basic metabolic panel','VT','05601',38,95),
('D2330','Resin-based composite, anterior','VT','05601',140,330);

-- VIRGINIA (VA)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','VA','20101',75,150),
('D1120','Prophylaxis Child','VA','20101',60,120),
('D2750','Crown - porcelain fused to metal','VA','20101',800,1450),
('99213','Office visit established patient','VA','20101',95,190),
('80053','Comprehensive metabolic panel','VA','20101',45,115),
('D4341','Periodontal scaling & root planing','VA','20101',180,420),
('D0210','Full mouth X-ray','VA','20101',110,240),
('99214','Office visit, moderate complexity','VA','20101',140,280),
('80048','Basic metabolic panel','VA','20101',38,95),
('D2330','Resin-based composite, anterior','VA','20101',140,330);

-- WASHINGTON (WA)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','WA','98001',80,160),
('D1120','Prophylaxis Child','WA','98001',65,130),
('D2750','Crown - porcelain fused to metal','WA','98001',850,1500),
('99213','Office visit established patient','WA','98001',100,200),
('80053','Comprehensive metabolic panel','WA','98001',50,120),
('D4341','Periodontal scaling & root planing','WA','98001',200,450),
('D0210','Full mouth X-ray','WA','98001',120,250),
('99214','Office visit, moderate complexity','WA','98001',150,300),
('80048','Basic metabolic panel','WA','98001',40,100),
('D2330','Resin-based composite, anterior','WA','98001',150,350);

-- WEST VIRGINIA (WV)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','WV','25301',70,140),
('D1120','Prophylaxis Child','WV','25301',55,110),
('D2750','Crown - porcelain fused to metal','WV','25301',750,1400),
('99213','Office visit established patient','WV','25301',90,180),
('80053','Comprehensive metabolic panel','WV','25301',40,100),
('D4341','Periodontal scaling & root planing','WV','25301',170,400),
('D0210','Full mouth X-ray','WV','25301',100,220),
('99214','Office visit, moderate complexity','WV','25301',130,260),
('80048','Basic metabolic panel','WV','25301',35,90),
('D2330','Resin-based composite, anterior','WV','25301',130,300);

-- WISCONSIN (WI)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','WI','53201',75,150),
('D1120','Prophylaxis Child','WI','53201',60,120),
('D2750','Crown - porcelain fused to metal','WI','53201',800,1450),
('99213','Office visit established patient','WI','53201',95,190),
('80053','Comprehensive metabolic panel','WI','53201',45,115),
('D4341','Periodontal scaling & root planing','WI','53201',180,420),
('D0210','Full mouth X-ray','WI','53201',110,240),
('99214','Office visit, moderate complexity','WI','53201',140,280),
('80048','Basic metabolic panel','WI','53201',38,95),
('D2330','Resin-based composite, anterior','WI','53201',140,330);

-- WYOMING (WY)
INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
VALUES
('D1110','Prophylaxis Adult','WY','82001',72,145),
('D1120','Prophylaxis Child','WY','82001',58,115),
('D2750','Crown - porcelain fused to metal','WY','82001',780,1420),
('99213','Office visit established patient','WY','82001',92,185),
('80053','Comprehensive metabolic panel','WY','82001',42,105),
('D4341','Periodontal scaling & root planing','WY','82001',175,410),
('D0210','Full mouth X-ray','WY','82001',105,225),
('99214','Office visit, moderate complexity','WY','82001',135,270),
('80048','Basic metabolic panel','WY','82001',37,95),
('D2330','Resin-based composite, anterior','WY','82001',135,310);
