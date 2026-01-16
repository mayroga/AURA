import pandas as pd
import sqlite3
import requests
import os
from datetime import date

DB_PATH = "cost_estimates.db"

PUBLIC_REPOS = [
    "https://raw.githubusercontent.com/owid/health-expenditure-data/master/prices_us_hospital.csv",
    "https://raw.githubusercontent.com/CDCgov/price-transparency/main/aggregated_prices.csv"
]

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS cost_estimates (
    procedure_name TEXT,
    cpt_code TEXT,
    state TEXT,
    zip_code TEXT,
    low_price REAL,
    high_price REAL,
    low_price_ins REAL,
    high_price_ins REAL,
    notes TEXT,
    last_updated DATE
)
""")

for url in PUBLIC_REPOS:
    print(f"🔹 Descargando {url}")
    df = pd.read_csv(url)
    df.columns = [c.lower().strip() for c in df.columns]

    for _, r in df.iterrows():
        c.execute("""
        INSERT INTO cost_estimates VALUES (?,?,?,?,?,?,?,?,?,?)
        """, (
            r.get("procedure","UNKNOWN"),
            r.get("code",""),
            r.get("state","US"),
            r.get("zip","00000"),
            float(r.get("low",0)),
            float(r.get("high",0)),
            float(r.get("low",0))*0.6,
            float(r.get("high",0))*0.75,
            "Public price transparency repository",
            date.today()
        ))

conn.commit()
conn.close()
print("✅ Base interna creada correctamente desde repositorios públicos.")
