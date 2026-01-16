import pandas as pd
import psycopg2
import requests
import io
import os
from datetime import date

# ==============================
# 1️⃣ CONFIGURACIÓN DB
# ==============================
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "dbname": os.getenv("DB_NAME", "aura_db"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
    "port": 5432
}

# ==============================
# 2️⃣ DATASETS FEDERALES
# ==============================
DATASETS = {
    "cpt_pfs": "https://data.cms.gov/data-api/v1/dataset/medicare-physician-fee-schedule.csv",
    "opps_asc": "https://data.cms.gov/data-api/v1/dataset/opps-asc.csv",
    "gpci": "https://data.cms.gov/data-api/v1/dataset/medicare-gpci.csv",
    "percentiles": "https://raw.githubusercontent.com/your-org/cms-percentiles/master/cms_percentiles.csv"
}

# ==============================
# 3️⃣ CONECTAR POSTGRES
# ==============================
conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS aura_cpt_benchmarks (
    cpt TEXT,
    state CHAR(2),
    fair_price NUMERIC,
    national_avg NUMERIC,
    p85_price NUMERIC,
    gpci NUMERIC,
    local_price NUMERIC,
    updated_at DATE,
    PRIMARY KEY (cpt, state)
);
""")
conn.commit()

# ==============================
# 4️⃣ FUNCIONES AUXILIARES
# ==============================
def download_csv(url):
    print(f"🔹 Descargando {url}")
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    return pd.read_csv(io.BytesIO(r.content))

# ==============================
# 5️⃣ DESCARGAR Y PROCESAR CPT / PFS
# ==============================
df_cpt = download_csv(DATASETS["cpt_pfs"])
df_cpt = df_cpt.rename(columns={
    "hcpcs_code": "cpt",
    "average_submitted_charge_amount": "avg_price",
    "provider_state": "state"
})
df_cpt = df_cpt[["cpt", "state", "avg_price"]].dropna()
df_cpt["avg_price"] = df_cpt["avg_price"].astype(float)

# ==============================
# 6️⃣ DESCARGAR Y PROCESAR OPPS / ASC
# ==============================
df_opps = download_csv(DATASETS["opps_asc"])
df_opps = df_opps.rename(columns={
    "hcpcs_code": "cpt",
    "average_submitted_charge_amount": "avg_price",
    "provider_state": "state"
})
df_opps = df_opps[["cpt", "state", "avg_price"]].dropna()
df_opps["avg_price"] = df_opps["avg_price"].astype(float)

# ==============================
# 7️⃣ COMBINAR PFS + OPPS
# ==============================
df_all = pd.concat([df_cpt, df_opps])
df_all = df_all.groupby(["cpt", "state"]).agg(
    fair_price=("avg_price", "median"),
    national_avg=("avg_price", "mean")
).reset_index()

# ==============================
# 8️⃣ DESCARGAR Y APLICAR GPCI
# ==============================
df_gpci = download_csv(DATASETS["gpci"])
df_gpci = df_gpci.rename(columns={"state": "state", "gpci": "gpci"})
df_all = df_all.merge(df_gpci[["state", "gpci"]], on="state", how="left")
df_all["local_price"] = df_all["fair_price"] * df_all["gpci"]

# ==============================
# 9️⃣ DESCARGAR PERCENTILES (P85)
# ==============================
df_pct = download_csv(DATASETS["percentiles"])
df_pct = df_pct.rename(columns={"cpt": "cpt", "state": "state", "p85": "p85_price"})
df_all = df_all.merge(df_pct[["cpt", "state", "p85_price"]], on=["cpt", "state"], how="left")

# ==============================
# 1️⃣0️⃣ INSERTAR / ACTUALIZAR EN DB
# ==============================
df_all["updated_at"] = date.today()

for _, row in df_all.iterrows():
    cur.execute("""
    INSERT INTO aura_cpt_benchmarks 
    (cpt, state, fair_price, national_avg, p85_price, gpci, local_price, updated_at)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    ON CONFLICT (cpt, state) DO UPDATE SET
        fair_price = EXCLUDED.fair_price,
        national_avg = EXCLUDED.national_avg,
        p85_price = EXCLUDED.p85_price,
        gpci = EXCLUDED.gpci,
        local_price = EXCLUDED.local_price,
        updated_at = EXCLUDED.updated_at
    """, (
        row.cpt, row.state, row.fair_price, row.national_avg,
        row.p85_price, row.gpci, row.local_price, row.updated_at
    ))

conn.commit()
cur.close()
conn.close()

print(f"✅ INGESTA COMPLETA: {len(df_all)} registros actualizados en aura_cpt_benchmarks")
