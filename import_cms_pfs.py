import sqlite3
import requests
import os
from datetime import datetime

# ==============================
# 1️⃣ Configuración DB
# ==============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "cost_estimates.db")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Crear la tabla (si no existe)
c.execute("""
CREATE TABLE IF NOT EXISTS cost_estimates (
    procedure_name TEXT,
    cpt_code TEXT,
    state TEXT,
    county TEXT,
    zip_code TEXT,
    low_price REAL,
    high_price REAL,
    low_price_ins REAL,
    high_price_ins REAL,
    notes TEXT,
    last_updated DATE,
    PRIMARY KEY (cpt_code, state, zip_code)
)
""")
conn.commit()

# ==============================
# 2️⃣ URLs oficiales CMS
# ==============================
CMS_PFS_URL = "https://data.cms.gov/resource/m5b5-2h3b.json?$limit=50000"
CMS_DENTAL_URL = "https://data.cms.gov/resource/6fea9d79-0129-4e4c-b1b8-23cd86a4f435.json?$limit=50000"

def download_json(url):
    try:
        print(f"🔹 Descargando datos desde {url} ...")
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[ERROR DOWNLOAD] {url} -> {e}")
        return []

cms_medical = download_json(CMS_PFS_URL)
cms_dental = download_json(CMS_DENTAL_URL)

# ==============================
# 3️⃣ Procesar y limpiar datos
# ==============================
rows = []

# Médicos CPT
for item in cms_medical:
    try:
        cpt = item.get("hcpcs_code")
        desc = item.get("short_description") or item.get("long_description") or "Sin descripción"
        medicare_price = float(item.get("medicare_payment", 0))
        national_price = float(item.get("national_payment_amount", 0))
        state = item.get("state") or "US"
        county = item.get("county") or "All"
        zip_code = item.get("zip_code") or "00000"
        last_updated = datetime.today().date()
        low_price = medicare_price
        high_price = national_price
        low_price_ins = medicare_price * 0.5
        high_price_ins = national_price * 0.7
        notes = "Datos oficiales CMS/PFS Médico 2026"

        rows.append((
            desc, cpt, state, county, zip_code,
            low_price, high_price, low_price_ins, high_price_ins,
            notes, last_updated
        ))
    except Exception as e:
        print(f"[ERROR PROCESS CPT] {item} -> {e}")

# Dentales CDT
for item in cms_dental:
    try:
        cdt = item.get("procedure_code")
        desc = item.get("description") or item.get("short_description") or "Sin descripción"
        low_price = float(item.get("medicaid_payment", 0))
        high_price = float(item.get("usual_and_customary", 0))
        state = item.get("state") or "US"
        county = item.get("county") or "All"
        zip_code = item.get("zip_code") or "00000"
        last_updated = datetime.today().date()
        low_price_ins = low_price * 0.5
        high_price_ins = high_price * 0.7
        notes = "Datos oficiales CMS/PFS Dental 2026"

        rows.append((
            desc, cdt, state, county, zip_code,
            low_price, high_price, low_price_ins, high_price_ins,
            notes, last_updated
        ))
    except Exception as e:
        print(f"[ERROR PROCESS CDT] {item} -> {e}")

# ==============================
# 4️⃣ Insertar / Actualizar en DB
# ==============================
for fila in rows:
    try:
        c.execute("""
        INSERT INTO cost_estimates (
            procedure_name, cpt_code, state, county, zip_code,
            low_price, high_price, low_price_ins, high_price_ins,
            notes, last_updated
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(cpt_code, state, zip_code) DO UPDATE SET
            procedure_name=excluded.procedure_name,
            low_price=excluded.low_price,
            high_price=excluded.high_price,
            low_price_ins=excluded.low_price_ins,
            high_price_ins=excluded.high_price_ins,
            notes=excluded.notes,
            last_updated=excluded.last_updated
        """, fila)
    except Exception as e:
        print(f"[ERROR INSERT DB] {fila} -> {e}")

conn.commit()
conn.close()
print(f"✅ Importación CMS/PFS completada. {len(rows)} registros cargados/actualizados en cost_estimates.db.")
