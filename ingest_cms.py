import pandas as pd
import psycopg2
import requests
import io
import os
from datetime import date

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": 5432
}

def run_ingest():
    print("🔹 Descargando datos CMS...")
    CMS_URL = "https://data.cms.gov/data-api/v1/dataset/medicare-physician-fee-schedule.csv"
    r = requests.get(CMS_URL, timeout=120)
    df = pd.read_csv(io.BytesIO(r.content))

    print("🔹 Procesando y Normalizando...")
    df = df.rename(columns={
        "hcpcs_code": "cpt",
        "average_submitted_charge_amount": "price",
        "provider_state": "state",
        "provider_zip_code": "zip"
    })
    df = df[["cpt", "state", "zip", "price"]].dropna()
    df["price"] = df["price"].astype(float)
    df["zip"] = df["zip"].astype(str).str[:5]

    # Agregación inteligente
    agg = df.groupby(["cpt", "state", "zip"]).agg(
        avg_price=("price", "mean"),
        fair_price=("price", "median"),
        min_price=("price", "min"),
        max_price=("price", "max")
    ).reset_index()

    print("🔹 Conectando a Postgres y Actualizando...")
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS aura_cpt_benchmarks (
        cpt TEXT, state CHAR(2), zip CHAR(5),
        avg_price NUMERIC, fair_price NUMERIC,
        min_price NUMERIC, max_price NUMERIC,
        updated_at DATE,
        PRIMARY KEY (cpt, state, zip)
    );
    """)

    for _, row in agg.iterrows():
        cur.execute("""
        INSERT INTO aura_cpt_benchmarks (cpt, state, zip, avg_price, fair_price, min_price, max_price, updated_at)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (cpt, state, zip) DO UPDATE SET
            avg_price = EXCLUDED.avg_price,
            fair_price = EXCLUDED.fair_price,
            updated_at = '""" + str(date.today()) + """';
        """, (row.cpt, row.state, row.zip, row.avg_price, row.fair_price, row.min_price, row.max_price, date.today()))

    conn.commit()
    cur.close()
    conn.close()
    print("✅ INGESTA EXITOSA")

if __name__ == "__main__":
    run_ingest()
