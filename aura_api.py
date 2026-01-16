import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Cargar variables de entorno desde .env si existe
load_dotenv()

# ---------------------------
# Configuración de la DB
# ---------------------------
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = int(os.getenv("DB_PORT", 5432))  # Default PostgreSQL port

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB connection failed: {e}")

# ---------------------------
# Inicialización FastAPI
# ---------------------------
app = FastAPI(title="Aura Verdict API", version="1.0")

# ---------------------------
# Endpoint Aura Verdict
# ---------------------------
@app.get("/aura_verdict")
def aura_verdict(
    cpt: str = Query(..., description="CPT/CDT code"),
    state: str = Query(..., min_length=2, max_length=2, description="US State code (e.g., FL, TX)"),
    zip: str = Query(None, description="Optional ZIP code for info only"),
    quoted_price: float = Query(None, description="Optional quoted price to calculate overprice")
):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Consulta principal
    cursor.execute("""
        SELECT *
        FROM aura_cpt_benchmarks
        WHERE cpt = %s AND state = %s
    """, (cpt.upper(), state.upper()))

    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="CPT code or state not found in benchmarks")

    response = {
        "cpt": row["cpt"],
        "state": state.upper(),
        "zip": zip,
        "fair_price": float(row["fair_price"]),
        "local_price": float(row["local_price"]),
        "premium_price": float(row["p85_price"]),
        "source": "CMS Federal Benchmarks + GPCI + Percentiles",
        "legal_note": "Calculated using CMS Medicare Paid Amounts, GPCI adjustments, and public percentiles. No PHI used. Fully compliant."
    }

    if quoted_price:
        overprice_pct = ((quoted_price - row["fair_price"]) / row["fair_price"]) * 100
        estimated_savings = quoted_price - row["local_price"]
        response["quoted_price"] = quoted_price
        response["overprice_pct"] = round(overprice_pct, 2)
        response["estimated_savings"] = round(estimated_savings, 2)

    return JSONResponse(content=response)

# ---------------------------
# Health check endpoint
# ---------------------------
@app.get("/health")
def health():
    try:
        conn = get_db_connection()
        conn.close()
        return {"status": "ok", "message": "DB connection successful"}
    except:
        raise HTTPException(status_code=500, detail="DB connection failed")
