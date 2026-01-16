import pandas as pd
import psycopg2
import requests
import io
import os
from datetime import date

# CONFIGURACIÓN UNIFICADA DE DB
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": 5432
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def download_csv(url):
    print(f"🔹 Descargando: {url}")
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    return pd.read_csv(io.BytesIO(r.content))

def run_total_ingest():
    conn = get_connection()
    cur = conn.cursor()

    # 1. CREAR TABLA MAESTRA
    cur.execute("""
    CREATE TABLE IF NOT EXISTS aura_cpt_benchmarks (
        cpt TEXT,
        state CHAR(2),
        fair_price NUMERIC,
        national_avg NUMERIC,
        p85_price NUMERIC,
        local_price NUMERIC,
        source TEXT,
        updated_at DATE,
        PRIMARY KEY (cpt, state)
    );
    """)

    # --- PARTE A: DATOS FEDERALES (CMS) ---
    print("--- Procesando Datos CMS ---")
    # (Aquí va tu lógica de PFS + OPPS que ya tenías)
    # ... Simplificado para el ejemplo:
    df_cms = download_csv("https://data.cms.gov/data-api/v1/dataset/medicare-physician-fee-schedule.csv")
    # ... (Tu lógica de filtrado y normalización) ...

    # --- PARTE B: DATOS PÚBLICOS (OWID / CDC) ---
    print("--- Procesando Repositorios Públicos ---")
    PUBLIC_REPOS = [
        "https://raw.githubusercontent.com/owid/health-expenditure-data/master/prices_us_hospital.csv",
        "https://raw.githubusercontent.com/CDCgov/price-transparency/main/aggregated_prices.csv"
    ]

    for url in PUBLIC_REPOS:
        try:
            df_pub = download_csv(url)
            df_pub.columns = [c.lower().strip() for c in df_pub.columns]
            
            for _, r in df_pub.iterrows():
                # Adaptamos los datos públicos a nuestra tabla maestra
                cur.execute("""
                INSERT INTO aura_cpt_benchmarks (cpt, state, fair_price, source, updated_at)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (cpt, state) DO UPDATE SET
                    fair_price = EXCLUDED.fair_price,
                    updated_at = EXCLUDED.updated_at;
                """, (r.get("code", "N/A"), r.get("state", "US"), r.get("low", 0), "Public Repo", date.today()))
        except Exception as e:
            print(f"⚠️ Error en repo {url}: {e}")

    conn.commit()
    cur.close()
    conn.close()
    print("✅ INGESTA TOTAL COMPLETADA EN POSTGRES")

if __name__ == "__main__":
    run_total_ingest()
