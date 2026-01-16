import os
from fastapi import FastAPI, Form, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Aura Verdict API v2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=5432,
        cursor_factory=RealDictCursor
    )

@app.post("/estimado")
async def estimado(
    consulta: str = Form(...), 
    state: str = Form(...), 
    zip_code: str = Form(None),
    quoted_price: float = Form(None)
):
    conn = get_db()
    cur = conn.cursor()
    cpt = consulta.upper()
    st = state.upper()

    # 1. Intentar por ZIP exacto
    query = "SELECT * FROM aura_cpt_benchmarks WHERE cpt=%s AND state=%s"
    params = [cpt, st]
    
    if zip_code:
        query += " AND zip=%s"
        params.append(zip_code)

    cur.execute(query, params)
    row = cur.fetchone()

    # 2. Fallback a promedio del Estado si el ZIP no existe
    if not row:
        cur.execute("""
            SELECT cpt, state, 'ALL' as zip, 
            AVG(fair_price) as fair_price, AVG(avg_price) as avg_price 
            FROM aura_cpt_benchmarks WHERE cpt=%s AND state=%s 
            GROUP BY cpt, state
        """, (cpt, st))
        row = cur.fetchone()

    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Código CPT no encontrado para esta región.")

    # Cálculos de ahorro
    fair = float(row['fair_price'])
    res = {
        "cpt": row['cpt'],
        "state": row['state'],
        "fair_price": round(fair, 2),
        "note": "Basado en CMS Federal Benchmarks"
    }

    if quoted_price:
        savings = quoted_price - fair
        res["overprice_pct"] = round(((quoted_price - fair) / fair) * 100, 2)
        res["potential_savings"] = round(savings, 2) if savings > 0 else 0

    return res

@app.get("/health")
def health():
    return {"status": "online"}
