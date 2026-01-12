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

-- =========================================================
-- PARTE 1: ALABAMA, ALASKA, ARIZONA, ARKANSAS, CALIFORNIA
-- INCLUYE: DENTAL, MÉDICA, PSICOLOGÍA, TERAPIA Y RAYOS X
-- =========================================================

INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price) VALUES
-- ALABAMA (AL)
('D1110','Limpieza Dental Adulto','AL','35203',75,150),
('D2750','Corona Porcelana','AL','35203',800,1500),
('D7140','Extracción Simple de Muela','AL','35203',130,280),
('99213','Consulta Médica General','AL','35203',95,190),
('90834','Psicoterapia Individual (45 min)','AL','35203',100,210),
('97110','Terapia Física (Ejercicios)','AL','35203',85,170),
('71045','Rayos X de Tórax','AL','35203',70,180),
('76700','Ultrasonido Abdominal','AL','35203',220,500),
('80053','Panel Metabólico (Sangre)','AL','35203',35,90),
('99283','Visita Urgencias (Nivel Medio)','AL','35203',450,1100),
('D0210','Rayos X Dentales Completos','AL','35203',90,180),
('90791','Evaluación Psicológica Inicial','AL','35203',150,300),
('93000','Electrocardiograma (EKG)','AL','35203',60,150),
('D2330','Empaste Dental (Resina)','AL','35203',110,230),
('99214','Consulta Médica Compleja','AL','35203',130,260),

-- ALASKA (AK)
('D1110','Limpieza Dental Adulto','AK','99501',110,210),
('D2750','Corona Porcelana','AK','99501',1100,1900),
('D7140','Extracción Simple de Muela','AK','99501',200,420),
('99213','Consulta Médica General','AK','99501',145,290),
('90834','Psicoterapia Individual (45 min)','AK','99501',160,320),
('97110','Terapia Física','AK','99501',130,260),
('76700','Ultrasonido Abdominal','AK','99501',350,850),
('99283','Visita Urgencias','AK','99501',850,2200),
('80053','Panel Metabólico','AK','99501',60,140),
('90791','Evaluación Psicológica Inicial','AK','99501',240,480),

-- ARIZONA (AZ)
('D1110','Limpieza Dental Adulto','AZ','85001',85,170),
('D2750','Corona Porcelana','AZ','85001',850,1600),
('D7140','Extracción Simple de Muela','AZ','85001',145,310),
('99213','Consulta Médica General','AZ','85001',105,220),
('90834','Psicoterapia Individual (45 min)','AZ','85001',120,240),
('97110','Terapia Física','AZ','85001',95,190),
('76700','Ultrasonido Abdominal','AZ','85001',280,620),
('99283','Visita Urgencias','AZ','85001',550,1400),
('D4341','Limpieza Profunda (Raspado)','AZ','85001',220,450),
('90847','Terapia Familiar','AZ','85001',150,300),

-- ARKANSAS (AR)
('D1110','Limpieza Dental Adulto','AR','72201',70,140),
('D2750','Corona Porcelana','AR','72201',780,1450),
('D7140','Extracción Simple de Muela','AR','72201',125,260),
('99213','Consulta Médica General','AR','72201',90,185),
('90834','Psicoterapia Individual (45 min)','AR','72201',105,215),

-- CALIFORNIA (CA)
('D1110','Limpieza Dental Adulto','CA','90001',125,250),
('D2750','Corona Porcelana','CA','90001',1200,2200),
('D7140','Extracción Simple de Muela','CA','90001',210,480),
('99213','Consulta Médica General','CA','90001',165,340),
('90834','Psicoterapia Individual (45 min)','CA','90001',180,360),
('90837','Psicoterapia Individual (60 min)','CA','90001',240,480),
('97110','Terapia Física (Ejercicios)','CA','90001',140,290),
('71045','Rayos X de Tórax','CA','90001',120,310),
('76700','Ultrasonido Abdominal','CA','90001',380,950),
('80053','Panel Metabólico (Sangre)','CA','90001',65,160),
('99283','Visita Urgencias (Nivel Medio)','CA','90001',950,2600),
('70450','TAC de Cabeza','CA','90001',650,1800),
('90791','Evaluación Psicológica Inicial','CA','90001',260,550),
('D4341','Limpieza Profunda (Raspado)','CA','90001',300,650),
('85025','Hemograma Completo','CA','90001',45,95);

-- PARTE 2: COLORADO, CONNECTICUT, DELAWARE, FLORIDA
-- COBERTURA: DENTAL, MÉDICA, PSICOLOGÍA, TERAPIA Y DIAGNÓSTICO

INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price) VALUES
-- COLORADO (CO)
('D1110','Limpieza Dental Adulto','CO','80201',90,180),
('D2750','Corona Porcelana','CO','80201',950,1700),
('D7140','Extracción Simple de Muela','CO','80201',160,340),
('99213','Consulta Médica General','CO','80201',115,240),
('90834','Psicoterapia Individual (45 min)','CO','80201',130,260),
('90837','Psicoterapia Individual (60 min)','CO','80201',175,340),
('97110','Terapia Física (Ejercicios)','CO','80201',105,210),
('71045','Rayos X de Tórax (Pecho)','CO','80201',95,240),
('76700','Ultrasonido Abdominal','CO','80201',310,680),
('80053','Panel Metabólico (Sangre)','CO','80201',45,120),
('99283','Visita Urgencias (Nivel Medio)','CO','80201',650,1600),
('70450','TAC de Cabeza / Cerebro (Sin contraste)','CO','80201',550,1400),
('90791','Evaluación Psicológica Inicial','CO','80201',210,420),
('D4341','Limpieza Profunda (Raspado por Cuadrante)','CO','80201',240,510),
('85025','Hemograma Completo (CBC)','CO','80201',30,75),

-- CONNECTICUT (CT)
('D1110','Limpieza Dental Adulto','CT','06101',100,200),
('D2750','Corona Porcelana','CT','06101',1050,1850),
('D7140','Extracción Simple de Muela','CT','06101',180,380),
('99213','Consulta Médica General','CT','06101',135,280),
('90834','Psicoterapia Individual (45 min)','CT','06101',150,300),
('90837','Psicoterapia Individual (60 min)','CT','06101',195,380),
('97110','Terapia Física (Ejercicios)','CT','06101',120,245),
('71045','Rayos X de Tórax (Pecho)','CT','06101',110,290),
('76700','Ultrasonido Abdominal','CT','06101',340,790),
('80053','Panel Metabólico (Sangre)','CT','06101',55,145),
('99283','Visita Urgencias (Nivel Medio)','CT','06101',800,2100),
('D0210','Serie Completa de Rayos X Dental','CT','06101',130,260),
('99203','Consulta Especialista (Nuevo)','CT','06101',190,420),
('90847','Terapia Familiar / Pareja','CT','06101',180,350),
('76805','Ultrasonido de Embarazo (Completo)','CT','06101',380,850),

-- DELAWARE (DE)
('D1110','Limpieza Dental Adulto','DE','19901',85,165),
('D2750','Corona Porcelana','DE','19901',880,1550),
('D7140','Extracción Simple de Muela','DE','19901',140,295),
('99213','Consulta Médica General','DE','19901',105,215),
('90834','Psicoterapia Individual (45 min)','DE','19901',120,235),
('90837','Psicoterapia Individual (60 min)','DE','19901',165,315),
('97110','Terapia Física (Ejercicios)','DE','19901',95,190),
('71045','Rayos X de Tórax (Pecho)','DE','19901',85,210),
('76700','Ultrasonido Abdominal','DE','19901',285,630),
('80053','Panel Metabólico (Sangre)','DE','19901',40,110),
('99283','Visita Urgencias (Nivel Medio)','DE','19901',580,1450),
('D2330','Empaste Dental (Resina 1 superficie)','DE','19901',125,260),
('93000','Electrocardiograma (EKG)','DE','19901',75,170),
('90832','Psicoterapia (30 min)','DE','19901',85,170),
('97140','Terapia Manual','DE','19901',90,185),

-- FLORIDA (FL)
('D1110','Limpieza Dental Adulto','FL','33101',80,160),
('D2750','Corona Porcelana','FL','33101',850,1500),
('D7140','Extracción Simple de Muela','FL','33101',140,310),
('99213','Consulta Médica General','FL','33101',100,210),
('90834','Psicoterapia Individual (45 min)','FL','33101',115,230),
('90837','Psicoterapia Individual (60 min)','FL','33101',160,310),
('97110','Terapia Física (Ejercicios)','FL','33101',90,185),
('71045','Rayos X de Tórax (Pecho)','FL','33101',80,210),
('76700','Ultrasonido Abdominal','FL','33101',270,610),
('80053','Panel Metabólico (Sangre)','FL','33101',40,105),
('99283','Visita Urgencias (Nivel Medio)','FL','33101',550,1350),
('70450','TAC de Cabeza / Cerebro (Sin contraste)','FL','33101',450,1100),
('90791','Evaluación Psicológica Inicial','FL','33101',190,390),
('D4341','Limpieza Profunda (Raspado por Cuadrante)','FL','33101',210,460),
('76805','Ultrasonido de Embarazo (Completo)','FL','33101',320,720);

-- PARTE 3: GEORGIA, HAWAII, IDAHO, ILLINOIS, INDIANA, IOWA, KANSAS, KENTUCKY
-- COBERTURA: DENTAL, MÉDICA, PSICOLOGÍA, TERAPIA Y DIAGNÓSTICO

INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price) VALUES
-- GEORGIA (GA)
('D1110','Limpieza Dental Adulto','GA','30301',80,165),
('D2750','Corona Porcelana','GA','30301',840,1550),
('D7140','Extracción Simple de Muela','GA','30301',145,320),
('99213','Consulta Médica General','GA','30301',100,215),
('90834','Psicoterapia Individual (45 min)','GA','30301',115,235),
('90837','Psicoterapia Individual (60 min)','GA','30301',165,320),
('97110','Terapia Física (Ejercicios)','GA','30301',95,195),
('71045','Rayos X de Tórax (Pecho)','GA','30301',85,220),
('76700','Ultrasonido Abdominal','GA','30301',275,630),
('80053','Panel Metabólico (Sangre)','GA','30301',42,110),
('99283','Visita Urgencias (Nivel Medio)','GA','30301',560,1400),
('70450','TAC de Cabeza / Cerebro (Sin contraste)','GA','30301',480,1200),
('90791','Evaluación Psicológica Inicial','GA','30301',200,410),
('D4341','Limpieza Profunda (Raspado por Cuadrante)','GA','30301',220,480),
('85025','Hemograma Completo (CBC)','GA','30301',32,78),

-- HAWAII (HI)
('D1110','Limpieza Dental Adulto','HI','96801',115,220),
('D2750','Corona Porcelana','HI','96801',1150,2000),
('D7140','Extracción Simple de Muela','HI','96801',210,450),
('99213','Consulta Médica General','HI','96801',155,310),
('90834','Psicoterapia Individual (45 min)','HI','96801',170,340),
('97110','Terapia Física (Ejercicios)','HI','96801',140,285),
('71045','Rayos X de Tórax (Pecho)','HI','96801',130,320),
('76700','Ultrasonido Abdominal','HI','96801',400,980),
('80053','Panel Metabólico (Sangre)','HI','96801',70,170),
('99283','Visita Urgencias (Nivel Medio)','HI','96801',900,2400),
('70450','TAC de Cabeza (Sin contraste)','HI','96801',700,1950),
('D0210','Serie Completa Rayos X Dental','HI','96801',150,310),
('90837','Psicoterapia Individual (60 min)','HI','96801',230,460),
('97140','Terapia Manual','HI','96801',150,300),
('99203','Consulta Especialista (Nuevo)','HI','96801',240,520),

-- ILLINOIS (IL)
('D1110','Limpieza Dental Adulto','IL','60601',95,195),
('D2750','Corona Porcelana','IL','60601',980,1750),
('D7140','Extracción Simple de Muela','IL','60601',170,370),
('99213','Consulta Médica General','IL','60601',125,260),
('90834','Psicoterapia Individual (45 min)','IL','60601',140,285),
('97110','Terapia Física (Ejercicios)','IL','60601',115,230),
('71045','Rayos X de Tórax (Pecho)','IL','60601',100,270),
('76700','Ultrasonido Abdominal','IL','60601',330,760),
('80053','Panel Metabólico (Sangre)','IL','60601',50,135),
('99283','Visita Urgencias (Nivel Medio)','IL','60601',750,1950),
('70450','TAC de Cabeza (Sin contraste)','IL','60601',550,1450),
('90791','Evaluación Psicológica Inicial','IL','60601',220,460),
('D4341','Limpieza Profunda (Raspado por Cuadrante)','IL','60601',250,540),
('90837','Psicoterapia (60 min)','IL','60601',190,380),
('85025','Hemograma Completo (CBC)','IL','60601',35,85),

-- KENTUCKY (KY)
('D1110','Limpieza Dental Adulto','KY','40201',75,155),
('D2750','Corona Porcelana','KY','40201',810,1480),
('D7140','Extracción Simple de Muela','KY','40201',135,290),
('99213','Consulta Médica General','KY','40201',98,205),
('90834','Psicoterapia Individual (45 min)','KY','40201',110,225),
('97110','Terapia Física (Ejercicios)','KY','40201',88,180),
('71045','Rayos X de Tórax (Pecho)','KY','40201',82,210),
('76700','Ultrasonido Abdominal','KY','40201',265,600),
('80053','Panel Metabólico (Sangre)','KY','40201',38,100),
('99283','Visita Urgencias (Nivel Medio)','KY','40201',530,1300),
('D2330','Empaste Dental (Resina 1 sup)','KY','40201',115,245),
('93000','Electrocardiograma (EKG)','KY','40201',70,160),
('90837','Psicoterapia (60 min)','KY','40201',155,300),
('97140','Terapia Manual','KY','40201',85,175),
('76805','Ultrasonido Embarazo','KY','40201',310,690);

-- PARTE 4: LOUISIANA, MAINE, MARYLAND, MASSACHUSETTS, MICHIGAN, MINNESOTA, MISSISSIPPI, MISSOURI, MONTANA
-- COBERTURA: DENTAL, MÉDICA, PSICOLOGÍA, TERAPIA Y DIAGNÓSTICO

INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price) VALUES
-- LOUISIANA (LA)
('D1110','Limpieza Dental Adulto','LA','70112',75,155),
('D2750','Corona Porcelana','LA','70112',810,1480),
('D7140','Extracción Simple de Muela','LA','70112',135,300),
('99213','Consulta Médica General','LA','70112',95,200),
('90834','Psicoterapia Individual (45 min)','LA','70112',110,225),
('90837','Psicoterapia Individual (60 min)','LA','70112',155,305),
('97110','Terapia Física (Ejercicios)','LA','70112',88,180),
('71045','Rayos X de Tórax (Pecho)','LA','70112',80,210),
('76700','Ultrasonido Abdominal','LA','70112',260,590),
('80053','Panel Metabólico (Sangre)','LA','70112',38,100),
('99283','Visita Urgencias (Nivel Medio)','LA','70112',530,1250),
('70450','TAC de Cabeza (Sin contraste)','LA','70112',450,1150),
('90791','Evaluación Psicológica Inicial','LA','70112',195,400),
('D4341','Limpieza Profunda (Raspado)','LA','70112',215,470),
('85025','Hemograma Completo (CBC)','LA','70112',30,75),

-- MASSACHUSETTS (MA)
('D1110','Limpieza Dental Adulto','MA','02101',110,220),
('D2750','Corona Porcelana','MA','02101',1150,2100),
('D7140','Extracción Simple de Muela','MA','02101',195,430),
('99213','Consulta Médica General','MA','02101',150,320),
('90834','Psicoterapia Individual (45 min)','MA','02101',170,345),
('90837','Psicoterapia Individual (60 min)','MA','02101',230,450),
('97110','Terapia Física (Ejercicios)','MA','02101',135,280),
('71045','Rayos X de Tórax (Pecho)','MA','02101',125,330),
('76700','Ultrasonido Abdominal','MA','02101',390,920),
('80053','Panel Metabólico (Sangre)','MA','02101',65,160),
('99283','Visita Urgencias (Nivel Medio)','MA','02101',900,2500),
('70450','TAC de Cabeza (Sin contraste)','MA','02101',720,1900),
('D0210','Serie Completa Rayos X Dental','MA','02101',155,320),
('99203','Consulta Especialista (Nuevo)','MA','02101',250,540),
('90791','Evaluación Psicológica Inicial','MA','02101',260,560),

-- MISSISSIPPI (MS)
('D1110','Limpieza Dental Adulto','MS','39201',65,135),
('D2750','Corona Porcelana','MS','39201',720,1380),
('D7140','Extracción Simple de Muela','MS','39201',115,250),
('99213','Consulta Médica General','MS','39201',85,175),
('90834','Psicoterapia Individual (45 min)','MS','39201',95,190),
('90837','Psicoterapia Individual (60 min)','MS','39201',135,260),
('97110','Terapia Física (Ejercicios)','MS','39201',75,155),
('71045','Rayos X de Tórax (Pecho)','MS','39201',70,180),
('76700','Ultrasonido Abdominal','MS','39201',230,520),
('80053','Panel Metabólico (Sangre)','MS','39201',32,85),
('99283','Visita Urgencias (Nivel Medio)','MS','39201',460,1100),
('D2330','Empaste Dental (Resina 1 sup)','MS','39201',100,215),
('93000','Electrocardiograma (EKG)','MS','39201',60,140),
('90791','Evaluación Psicológica Inicial','MS','39201',160,330),
('76805','Ultrasonido Embarazo','MS','39201',280,630),

-- MISSOURI (MO)
('D1110','Limpieza Dental Adulto','MO','63101',82,165),
('D2750','Corona Porcelana','MO','63101',850,1550),
('D7140','Extracción Simple de Muela','MO','63101',145,315),
('99213','Consulta Médica General','MO','63101',105,215),
('90834','Psicoterapia Individual (45 min)','MO','63101',120,240),
('97110','Terapia Física (Ejercicios)','MO','63101',95,195),
('71045','Rayos X de Tórax (Pecho)','MO','63101',88,220),
('76700','Ultrasonido Abdominal','MO','63101',285,640),
('80053','Panel Metabólico (Sangre)','MO','63101',42,110),
('99283','Visita Urgencias (Nivel Medio)','MO','63101',580,1450),
('70450','TAC de Cabeza (Sin contraste)','MO','63101',490,1250),
('D4341','Limpieza Profunda (Raspado)','MO','63101',225,490),
('90837','Psicoterapia (60 min)','MO','63101',165,325),
('90791','Evaluación Psicológica Inicial','MO','63101',205,420),
('85025','Hemograma Completo (CBC)','MO','63101',32,80);

-- PARTE 5: NEBRASKA, NEVADA, NEW JERSEY, NEW MEXICO, NEW YORK, NORTH CAROLINA, NORTH DAKOTA, OHIO, OKLAHOMA, OREGON, PENNSYLVANIA
-- COBERTURA: DENTAL, MÉDICA, PSICOLOGÍA, TERAPIA Y DIAGNÓSTICO

INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price) VALUES
-- NEW JERSEY (NJ)
('D1110','Limpieza Dental Adulto','NJ','07101',105,210),
('D2750','Corona Porcelana','NJ','07101',1100,2000),
('D7140','Extracción Simple de Muela','NJ','07101',185,410),
('99213','Consulta Médica General','NJ','07101',140,290),
('90834','Psicoterapia Individual (45 min)','NJ','07101',160,320),
('90837','Psicoterapia Individual (60 min)','NJ','07101',210,410),
('97110','Terapia Física (Ejercicios)','NJ','07101',125,260),
('71045','Rayos X de Tórax (Pecho)','NJ','07101',115,290),
('76700','Ultrasonido Abdominal','NJ','07101',360,820),
('80053','Panel Metabólico (Sangre)','NJ','07101',60,150),
('99283','Visita Urgencias (Nivel Medio)','NJ','07101',850,2300),
('70450','TAC de Cabeza (Sin contraste)','NJ','07101',680,1750),
('90791','Evaluación Psicológica Inicial','NJ','07101',245,510),
('D4341','Limpieza Profunda (Raspado)','NJ','07101',280,600),
('85025','Hemograma Completo (CBC)','NJ','07101',40,95),

-- NEW YORK (NY)
('D1110','Limpieza Dental Adulto','NY','10001',125,250),
('D2750','Corona Porcelana','NY','10001',1300,2400),
('D7140','Extracción Simple de Muela','NY','10001',220,500),
('99213','Consulta Médica General','NY','10001',170,360),
('90834','Psicoterapia Individual (45 min)','NY','10001',190,380),
('90837','Psicoterapia Individual (60 min)','NY','10001',250,500),
('97110','Terapia Física (Ejercicios)','NY','10001',150,310),
('71045','Rayos X de Tórax (Pecho)','NY','10001',135,350),
('76700','Ultrasonido Abdominal','NY','10001',420,1100),
('80053','Panel Metabólico (Sangre)','NY','10001',75,180),
('99283','Visita Urgencias (Nivel Medio)','NY','10001',1100,3200),
('70450','TAC de Cabeza (Sin contraste)','NY','10001',850,2200),
('D0210','Serie Completa Rayos X Dental','NY','10001',170,340),
('99203','Consulta Especialista (Nuevo)','NY','10001',280,600),
('90791','Evaluación Psicológica Inicial','NY','10001',280,600),

-- OHIO (OH)
('D1110','Limpieza Dental Adulto','OH','43201',80,165),
('D2750','Corona Porcelana','OH','43201',840,1520),
('D7140','Extracción Simple de Muela','OH','43201',140,310),
('99213','Consulta Médica General','OH','43201',100,210),
('90834','Psicoterapia Individual (45 min)','OH','43201',115,230),
('90837','Psicoterapia Individual (60 min)','OH','43201',160,310),
('97110','Terapia Física (Ejercicios)','OH','43201',92,190),
('71045','Rayos X de Tórax (Pecho)','OH','43201',85,215),
('76700','Ultrasonido Abdominal','OH','43201',275,620),
('80053','Panel Metabólico (Sangre)','OH','43201',40,105),
('99283','Visita Urgencias (Nivel Medio)','OH','43201',560,1380),
('D2330','Empaste Dental (Resina 1 sup)','OH','43201',120,250),
('93000','Electrocardiograma (EKG)','OH','43201',75,170),
('90791','Evaluación Psicológica Inicial','OH','43201',195,400),
('76805','Ultrasonido Embarazo','OH','43201',315,700),

-- PENNSYLVANIA (PA)
('D1110','Limpieza Dental Adulto','PA','19101',90,185),
('D2750','Corona Porcelana','PA','19101',920,1650),
('D7140','Extracción Simple de Muela','PA','19101',160,350),
('99213','Consulta Médica General','PA','19101',120,250),
('90834','Psicoterapia Individual (45 min)','PA','19101',135,275),
('90837','Psicoterapia Individual (60 min)','PA','19101',180,350),
('97110','Terapia Física (Ejercicios)','PA','19101',110,220),
('71045','Rayos X de Tórax (Pecho)','PA','19101',100,260),
('76700','Ultrasonido Abdominal','PA','19101',320,720),
('80053','Panel Metabólico (Sangre)','PA','19101',50,130),
('99283','Visita Urgencias (Nivel Medio)','PA','19101',680,1700),
('70450','TAC de Cabeza (Sin contraste)','PA','19101',580,1500),
('90791','Evaluación Psicológica Inicial','PA','19101',220,450),
('D4341','Limpieza Profunda (Raspado)','PA','19101',245,530),
('85025','Hemograma Completo (CBC)','PA','19101',35,85);

-- PARTE 6: RHODE ISLAND, SOUTH CAROLINA, SOUTH DAKOTA, TENNESSEE, TEXAS, UTAH, VERMONT, VIRGINIA, WASHINGTON, WEST VIRGINIA, WISCONSIN, WYOMING
-- COBERTURA: DENTAL, MÉDICA, PSICOLOGÍA, TERAPIA Y DIAGNÓSTICO

INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price) VALUES
-- TEXAS (TX)
('D1110','Limpieza Dental Adulto','TX','73301',85,175),
('D2750','Corona Porcelana','TX','73301',880,1650),
('D7140','Extracción Simple de Muela','TX','73301',150,330),
('99213','Consulta Médica General','TX','73301',110,230),
('90834','Psicoterapia Individual (45 min)','TX','73301',125,250),
('90837','Psicoterapia Individual (60 min)','TX','73301',170,330),
('97110','Terapia Física (Ejercicios)','TX','73301',98,205),
('71045','Rayos X de Tórax (Pecho)','TX','73301',90,230),
('76700','Ultrasonido Abdominal','TX','73301',290,650),
('80053','Panel Metabólico (Sangre)','TX','73301',45,115),
('99283','Visita Urgencias (Nivel Medio)','TX','73301',600,1500),
('70450','TAC de Cabeza (Sin contraste)','TX','73301',520,1300),
('90791','Evaluación Psicológica Inicial','TX','73301',210,430),
('D4341','Limpieza Profunda (Raspado)','TX','73301',235,510),
('85025','Hemograma Completo (CBC)','TX','73301',35,85),

-- VIRGINIA (VA)
('D1110','Limpieza Dental Adulto','VA','23218',90,185),
('D2750','Corona Porcelana','VA','23218',950,1750),
('D7140','Extracción Simple de Muela','VA','23218',165,360),
('99213','Consulta Médica General','VA','23218',125,265),
('90834','Psicoterapia Individual (45 min)','VA','23218',140,290),
('90837','Psicoterapia Individual (60 min)','VA','23218',190,370),
('97110','Terapia Física (Ejercicios)','VA','23218',115,240),
('71045','Rayos X de Tórax (Pecho)','VA','23218',105,270),
('76700','Ultrasonido Abdominal','VA','23218',330,750),
('80053','Panel Metabólico (Sangre)','VA','23218',55,140),
('99283','Visita Urgencias (Nivel Medio)','VA','23218',720,1850),
('70450','TAC de Cabeza (Sin contraste)','VA','23218',600,1600),
('D2330','Empaste Dental (Resina 1 sup)','VA','23218',135,285),
('90791','Evaluación Psicológica Inicial','VA','23218',230,480),
('76805','Ultrasonido Embarazo','VA','23218',350,780),

-- WASHINGTON (WA)
('D1110','Limpieza Dental Adulto','WA','98101',115,230),
('D2750','Corona Porcelana','WA','98101',1200,2250),
('D7140','Extracción Simple de Muela','WA','98101',205,450),
('99213','Consulta Médica General','WA','98101',160,335),
('90834','Psicoterapia Individual (45 min)','WA','98101',185,370),
('90837','Psicoterapia Individual (60 min)','WA','98101',245,490),
('97110','Terapia Física (Ejercicios)','WA','98101',145,300),
('71045','Rayos X de Tórax (Pecho)','WA','98101',130,340),
('76700','Ultrasonido Abdominal','WA','98101',410,1050),
('80053','Panel Metabólico (Sangre)','WA','98101',70,175),
('99283','Visita Urgencias (Nivel Medio)','WA','98101',1000,2800),
('70450','TAC de Cabeza (Sin contraste)','WA','98101',800,2100),
('90791','Evaluación Psicológica Inicial','WA','98101',275,580),
('D4341','Limpieza Profunda (Raspado)','WA','98101',310,680),
('99203','Consulta Especialista (Nuevo)','WA','98101',265,580),

-- WYOMING (WY)
('D1110','Limpieza Dental Adulto','WY','82001',75,160),
('D2750','Corona Porcelana','WY','82001',820,1500),
('D7140','Extracción Simple de Muela','WY','82001',140,305),
('99213','Consulta Médica General','WY','82001',100,215),
('90834','Psicoterapia Individual (45 min)','WY','82001',115,240),
('97110','Terapia Física (Ejercicios)','WY','82001',92,190),
('71045','Rayos X de Tórax (Pecho)','WY','82001',85,225),
('76700','Ultrasonido Abdominal','WY','82001',270,610),
('80053','Panel Metabólico (Sangre)','WY','82001',42,110),
('99283','Visita Urgencias (Nivel Medio)','WY','82001',540,1350),
('D2330','Empaste Dental (Resina 1 sup)','WY','82001',120,255),
('93000','Electrocardiograma (EKG)','WY','82001',75,165),
('90837','Psicoterapia (60 min)','WY','82001',165,320),
('97140','Terapia Manual','WY','82001',90,185),
('85025','Hemograma Completo (CBC)','WY','82001',32,80);
CREATE INDEX idx_cpt_state_zip ON cost_estimates(cpt_code, state, zip_code);
