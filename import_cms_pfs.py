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

# Crear tabla si no existe
c.execute("""
CREATE TABLE IF NOT EXISTS cost_estimates (
    procedure_name TEXT,
    cpt_code TEXT PRIMARY KEY,
    state TEXT,
    county TEXT,
    zip_code TEXT,
    low_price REAL,
    high_price REAL,
    low_price_ins REAL,
    high_price_ins REAL,
    notes TEXT,
    last_updated DATE
)
""")
conn.commit()

# ==============================
# 2️⃣ Descargar datos CMS/PFS
# ==============================
CMS_API_URL = "https://data.cms.gov/resource/m5b5-2h3b.json"

try:
    print("🔹 Descargando datos CMS/PFS...")
    response = requests.get(CMS_API_URL)
    response.raise_for_status()
    cms_data = response.json()
except Exception as e:
    print(f"[ERROR CMS DOWNLOAD] {e}")
    cms_data = []

# ==============================
# 3️⃣ Procesar y limpiar datos
# ==============================
rows = []
for item in cms_data:
    try:
        cpt = item.get("hcpcs_code")
        desc = item.get("short_description") or item.get("long_description")
        medicare_price = float(item.get("medicare_payment", 0))
        national_price = float(item.get("national_payment_amount", 0))
        gpci_adjustment = float(item.get("geographic_practice_cost_index", 1))
        last_updated = datetime.today().date()

        # Notas y placeholders para ZIP/estado/condado (rellenar luego según ubicación)
        state = "US"
        county = "All"
        zip_code = "00000"
        low_price = medicare_price
        high_price = national_price
        low_price_ins = medicare_price * 0.5
        high_price_ins = national_price * 0.7
        notes = "Datos oficiales CMS/PFS 2026"

        rows.append((
            desc, cpt, state, county, zip_code,
            low_price, high_price, low_price_ins, high_price_ins,
            notes, last_updated
        ))
    except Exception as e:
        print(f"[ERROR PROCESS ITEM] {item} -> {e}")

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
        ON CONFLICT(cpt_code) DO UPDATE SET
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
print(f"✅ Importación CMS/PFS completada. {len(rows)} procedimientos cargados/actualizados.")
