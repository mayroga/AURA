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
    print("🚀 Iniciando Ingesta Maestra para Aura by May Roga LLC")
    
    # 1. DESCARGAR CMS PFS
    print("🔹 Descargando Medicare PFS...")
    url_pfs = "https://data.cms.gov/data-api/v1/dataset/medicare-physician-fee-schedule.csv"
    r = requests.get(url_pfs)
    df = pd.read_csv(io.BytesIO(r.content))

    # Normalizar columnas
    df = df.rename(columns={
        "hcpcs_code": "cpt",
        "average_submitted_charge_amount": "price",
        "provider_state": "state",
        "provider_zip_code": "zip"
    })
    
    # Limpieza básica
    df = df[["cpt", "state", "zip", "price"]].dropna()
    df["price"] = df["price"].astype(float)
    df["zip"] = df["zip"].astype(str).str[:5]

    # Agrupar datos para obtener métricas
    agg = df.groupby(["cpt", "state", "zip"]).agg(
        fair_price=("price", "median"),
        national_avg=("price", "mean"),
        p85_price=("price", lambda x: x.quantile(0.85))
    ).reset_index()

    # 2. CONECTAR A POSTGRES
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS aura_cpt_benchmarks (
            cpt TEXT,
            state CHAR(2),
            zip CHAR(5),
            fair_price NUMERIC,
            national_avg NUMERIC,
            p85_price NUMERIC,
            local_price NUMERIC,
            updated_at DATE,
            PRIMARY KEY (cpt, state, zip)
        );
    """)

    print(f"🔹 Insertando {len(agg)} registros...")
    for _, row in agg.iterrows():
        # Simulamos local_price como fair_price para este ejemplo inicial
        cur.execute("""
            INSERT INTO aura_cpt_benchmarks 
            (cpt, state, zip, fair_price, national_avg, p85_price, local_price, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (cpt, state, zip) DO UPDATE SET
                fair_price = EXCLUDED.fair_price,
                updated_at = EXCLUDED.updated_at;
        """, (row.cpt, row.state, row.zip, row.fair_price, row.national_avg, row.p85_price, row.fair_price, date.today()))

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Ingesta Completada con Éxito.")

if __name__ == "__main__":
    run_ingest()
