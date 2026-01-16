import os
from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Aura Verdict API - Aura by May Roga LLC", version="2.0")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_db_connection():
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
    zip_user: str = Form(None),
    quoted_price: float = Form(None)
):
    conn = get_db_connection()
    cur = conn.cursor()
    cpt = consulta.upper().strip()
    st = state.upper().strip()

    # 1. BÚSQUEDA POR ZIP (Si el usuario lo proporciona)
    row = None
    if zip_user:
        cur.execute("""
            SELECT * FROM aura_cpt_benchmarks 
            WHERE cpt = %s AND zip = %s 
            LIMIT 1
        """, (cpt, zip_user))
        row = cur.fetchone()

    # 2. FALLBACK: BÚSQUEDA POR ESTADO (Si no hay ZIP o no se encontró)
    if not row:
        cur.execute("""
            SELECT cpt, state, 'ESTADO' as zip,
            AVG(fair_price) as fair_price, 
            AVG(local_price) as local_price,
            AVG(p85_price) as p85_price
            FROM aura_cpt_benchmarks 
            WHERE cpt = %s AND state = %s
            GROUP BY cpt, state
        """, (cpt, st))
        row = cur.fetchone()

    conn.close()

    if not row or row['fair_price'] is None:
        raise HTTPException(status_code=404, detail="Código CPT no encontrado en nuestra base de datos.")

    # Estructura de Respuesta Aura by May Roga LLC
    fair = float(row['fair_price'])
    local = float(row['local_price']) if row['local_price'] else fair
    premium = float(row['p85_price']) if row['p85_price'] else fair * 1.3

    response = {
        "empresa": "Aura by May Roga LLC",
        "cpt": row['cpt'],
        "ubicacion": f"{st} - {row['zip']}",
        "precio_justo": round(fair, 2),
        "precio_local_ajustado": round(local, 2),
        "precio_premium_p85": round(premium, 2),
        "fuente": "CMS Federal + GPCI + Public Repos",
        "nota_legal": "Estimado legalmente defendible para transparencia de costos."
    }

    if quoted_price:
        ahorro = quoted_price - local
        response["analisis_cotizacion"] = {
            "precio_cotizado": quoted_price,
            "sobreprecio_pct": round(((quoted_price - fair) / fair) * 100, 2),
            "ahorro_potencial": round(ahorro, 2) if ahorro > 0 else 0
        }

    return response

@app.get("/health")
def health():
    return {"status": "ok", "provider": "Aura by May Roga LLC"}
