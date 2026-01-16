import pandas as pd
import psycopg2
import requests
import io
import os
from datetime import date

# ======================
# CONFIG
# ======================
CMS_CSV_URL = "https://data.cms.gov/data-api/v1/dataset/medicare-physician-fee-schedule.csv"
# (puedes cambiar dataset sin tocar lógica)

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": 5432
}

# ======================
# DOWNLOAD CMS DATA
# ======================
print("Descargando datos CMS...")
response = requests.get(CMS_CSV_URL, timeout=120)
response.raise_for_status()

df = pd.read_csv(io.BytesIO(response.content))

# ======================
# NORMALIZE
# ======================
print("Normalizando datos...")

df = df.rename(columns={
    "hcpcs_code": "cpt",
    "average_submitted_charge_amount": "avg_price",
    "provider_zip_code": "zip",
    "provider_state": "state"
})

df = df[["cpt", "state", "zip", "avg_price"]]
df = df.dropna()

df["zip"] = df["zip"].astype(str).str[:5]
df["avg_price"] = df["avg_price"].astype(float)

# ======================
# AGGREGATE
# ======================
agg = df.groupby(["cpt", "state", "zip"]).agg(
    avg_price=("avg_price", "mean"),
    min_price=("avg_price", "min"),
    max_price=("avg_price", "max")
).reset_index()

agg["updated_at"] = date.today()
agg["source"] = "CMS"

# ======================
# INSERT POSTGRES
# ======================
print("Insertando en Postgres...")

conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS prices_cpt (
    cpt TEXT,
    state CHAR(2),
    zip CHAR(5),
    avg_price NUMERIC,
    min_price NUMERIC,
    max_price NUMERIC,
    source TEXT,
    updated_at DATE,
    PRIMARY KEY (cpt, state, zip)
);
""")

for _, row in agg.iterrows():
    cur.execute("""
    INSERT INTO prices_cpt (cpt, state, zip, avg_price, min_price, max_price, source, updated_at)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    ON CONFLICT (cpt, state, zip)
    DO UPDATE SET
        avg_price = EXCLUDED.avg_price,
        min_price = EXCLUDED.min_price,
        max_price = EXCLUDED.max_price,
        updated_at = EXCLUDED.updated_at;
    """, tuple(row))

conn.commit()
cur.close()
conn.close()

print("INGESTA COMPLETA ✔")
