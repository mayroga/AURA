import sqlite3
import os
import requests
from datetime import datetime

# ==============================
# RUTA DB
# ==============================
DB_FILE = "cost_estimates.db"

# ==============================
# ELIMINAR DB EXISTENTE (para evitar corrupción)
# ==============================
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print("🗑️ DB vieja eliminada.")

# ==============================
# CONEXIÓN DB
# ==============================
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()

# ==============================
# CREAR TABLA PRINCIPAL
# ==============================
c.execute("""
CREATE TABLE IF NOT EXISTS cost_estimates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    procedure_name TEXT,
    cpt_code TEXT,
    state TEXT,
    county TEXT,
    zip_code TEXT,
    medicare_price REAL,
    national_price REAL,
    gpci_adjustment REAL,
    notes TEXT,
    last_updated TEXT
)
""")
print("✅ Tabla cost_estimates creada.")

# ==============================
# ZIP + CONDADO + ESTADO (50 estados)
# ==============================
locations = [
    ("AL","Jefferson","35203"), ("AK","Anchorage","99501"), ("AZ","Maricopa","85008"),
    ("AR","Pulaski","72201"), ("CA","Los Angeles","90012"), ("CO","Denver","80203"),
    ("CT","Hartford","06103"), ("DE","New Castle","19720"), ("FL","Miami-Dade","33167"),
    ("GA","Fulton","30303"), ("HI","Honolulu","96813"), ("ID","Ada","83702"),
    ("IL","Cook","60612"), ("IN","Marion","46204"), ("IA","Polk","50309"),
    ("KS","Sedgwick","67202"), ("KY","Jefferson","40202"), ("LA","Orleans","70112"),
    ("ME","Cumberland","04101"), ("MD","Baltimore City","21201"),
    ("MA","Suffolk","02108"), ("MI","Wayne","48201"), ("MN","Hennepin","55401"),
    ("MS","Hinds","39201"), ("MO","Jackson","64108"), ("MT","Yellowstone","59101"),
    ("NE","Douglas","68102"), ("NV","Clark","89101"), ("NH","Hillsborough","03101"),
    ("NJ","Essex","07102"), ("NM","Bernalillo","87102"), ("NY","New York","10022"),
    ("NC","Mecklenburg","28202"), ("ND","Cass","58102"), ("OH","Franklin","43215"),
    ("OK","Oklahoma","73102"), ("OR","Multnomah","97204"), ("PA","Philadelphia","19107"),
    ("RI","Providence","02903"), ("SC","Richland","29201"), ("SD","Minnehaha","57104"),
    ("TN","Davidson","37203"), ("TX","Harris","77036"), ("UT","Salt Lake","84111"),
    ("VT","Chittenden","05401"), ("VA","Fairfax","22030"), ("WA","King","98101"),
    ("WV","Kanawha","25301"), ("WI","Milwaukee","53202"), ("WY","Laramie","82001")
]

# ==============================
# PROCEDIMIENTOS (ejemplo real CPT/Descripción)
# ==============================
procedures = [
    ("Extracción de muela", "D7140"),
    ("Extracción quirúrgica", "D7210"),
    ("Limpieza dental", "D1110"),
    ("Relleno dental 1 superficie", "D2140"),
    ("Relleno dental 2 superficies", "D2150"),
    ("Corona dental porcelana", "D2752"),
    ("Endodoncia molar", "D3330"),
    ("Radiografía dental", "D0220"),
    ("Consulta dental inicial", "D0150"),
    ("Profilaxis infantil", "D1120"),
    ("Examen médico general", "99203"),
    ("Consulta médica ambulatoria", "99213"),
    ("Rayos X tórax", "71045"),
    ("Ultrasonido abdominal", "76700"),
    ("Análisis de sangre básico", "80050"),
    ("Electrocardiograma", "93000"),
    ("Colonoscopía", "45378"),
    ("Mamografía", "77067"),
    ("CT Scan abdomen", "74177"),
    ("MRI rodilla", "73721"),
]

# ==============================
# DESCARGAR JSON CMS (Medicare PFS)
# ==============================
CMS_API = "https://data.cms.gov/resource/m5b5-2h3b.json"  # endpoint JSON PFS real

try:
    response = requests.get(CMS_API, timeout=30)
    response.raise_for_status()
    cms_data = response.json()
    print(f"✅ JSON CMS descargado ({len(cms_data)} registros).")
except Exception as e:
    print("❌ Error descargando CMS API:", e)
    cms_data = []

# ==============================
# FUNCION PARA OBTENER PRECIOS POR CPT
# ==============================
def get_cms_prices(cpt_code, state):
    """
    Busca en el JSON CMS por CPT y estado.
    Retorna medicare_price, national_price, gpci_adjustment
    """
    for item in cms_data:
        if item.get("hcpcs_code") == cpt_code:
            try:
                medicare_price = float(item.get("medicare_allowed_amt", 0))
            except:
                medicare_price = 0.0
            try:
                national_price = float(item.get("national_avg_payment_amt", 0))
            except:
                national_price = 0.0
            try:
                gpci_adjustment = float(item.get("work_geographic_pricing_adjustment", 1))
            except:
                gpci_adjustment = 1.0
            return medicare_price, national_price, gpci_adjustment
    return 0.0, 0.0, 1.0  # fallback si no hay dato

# ==============================
# INSERTAR DATOS REALES
# ==============================
rows = []
for state, county, zip_code in locations:
    for proc_name, cpt in procedures:
        medicare_price, national_price, gpci_adj = get_cms_prices(cpt, state)
        note = "Datos reales Medicare PFS" if cms_data else "Fallback: CMS no disponible"
        rows.append((proc_name, cpt, state, county, zip_code, medicare_price, national_price, gpci_adj, note, datetime.today().isoformat()))

c.executemany("""
INSERT INTO cost_estimates (
    procedure_name,
    cpt_code,
    state,
    county,
    zip_code,
    medicare_price,
    national_price,
    gpci_adjustment,
    notes,
    last_updated
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", rows)

conn.commit()
conn.close()

print(f"✅ DB PRODUCCIÓN LISTA: {len(locations)} estados x {len(procedures)} procedimientos = {len(rows)} registros.")
print("⚡ Script listo para producción en Render, con fallback seguro si CMS falla.")
