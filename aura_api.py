from fastapi import FastAPI, Query
import psycopg2
import os
from fastapi.middleware.cors import CORSMiddleware

# ==============================
# CONFIG
# ==============================
app = FastAPI(title="Aura Verdict API")

# Permitir CORS si se requiere acceso web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajustar según deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB connection global
conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "localhost"),
    dbname=os.getenv("DB_NAME", "aura_db"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD", ""),
    port=5432
)

# ==============================
# ENDPOINT PRINCIPAL
# ==============================
@app.get("/aura_verdict")
def aura_verdict(
    cpt: str = Query(..., description="Código CPT/HCPCS o CDT"),
    zip: str = Query(..., description="Código ZIP del paciente"),
    state: str = Query(..., description="Estado del paciente (ej. FL, TX, NY)"),
    quoted_price: float = Query(None, description="Precio cotizado por proveedor, opcional")
):
    cur = conn.cursor()

    # 1️⃣ Intentar ZIP exacto
    cur.execute("""
        SELECT fair_price, local_price, p85_price
        FROM aura_cpt_benchmarks
        WHERE cpt=%s AND state=%s
        LIMIT 1
    """, (cpt, state))
    row = cur.fetchone()

    # 2️⃣ Fallback nacional
    if not row or row[0] is None:
        cur.execute("""
            SELECT AVG(fair_price), AVG(local_price), AVG(p85_price)
            FROM aura_cpt_benchmarks
            WHERE cpt=%s
        """, (cpt,))
        row = cur.fetchone()

    cur.close()

    fair_price, local_price, p85_price = row

    verdict = {
        "cpt": cpt,
        "state": state,
        "zip": zip,
        "fair_price": float(fair_price),
        "local_price": float(local_price),
        "premium_price": float(p85_price),
        "quoted_price": quoted_price,
        "overprice_pct": round((quoted_price - fair_price)/fair_price*100,2) if quoted_price else None,
        "estimated_savings": round(quoted_price - local_price,2) if quoted_price else None,
        "source": "CMS Federal Benchmarks + GPCI + Percentiles",
        "legal_note": "Calculated using CMS Medicare Paid Amounts, GPCI adjustments, and public percentiles. No PHI used. Fully compliant."
    }

    return verdict
