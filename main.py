import os
from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = int(os.getenv("DB_PORT", 5432))

app = FastAPI(title="Aura Verdict API", version="1.0")

# Permitir CORS para tu frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

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

# -------------------------
# Endpoint de estimado
# -------------------------
@app.post("/estimado")
def estimado(consulta: str = Form(...), lang: str = Form("es"), zip_user: str = Form(None)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cpt_code = consulta.upper()

    # Consulta con ZIP
    if zip_user:
        cursor.execute("""
            SELECT * FROM aura_cpt_benchmarks
            WHERE cpt=%s AND state=(SELECT state FROM aura_cpt_benchmarks WHERE zip=%s LIMIT 1)
        """, (cpt_code, zip_user))
    else:
        cursor.execute("""
            SELECT * FROM aura_cpt_benchmarks
            WHERE cpt=%s
        """, (cpt_code,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return JSONResponse({"resultado": lang=="es" and "Código no encontrado" or "Code not found"}, status_code=404)

    resultado = f"""
CPT: {row['cpt']}
Estado: {row['state']}
Precio justo (Mediana CMS): ${row['fair_price']:.2f}
Precio local ajustado (GPCI): ${row['local_price']:.2f}
Precio premium (p85 percentil): ${row['p85_price']:.2f}
Fuente: CMS + GPCI + Percentiles públicos
Nota legal: Estimado legalmente defendible, datos públicos.
"""
    return {"resultado": resultado.strip()}

# -------------------------
# Login Admin GRATIS
# -------------------------
@app.post("/login-admin")
def login_admin(user: str = Form(...), pw: str = Form(...)):
    # Usuario y contraseña simples para acceso gratuito
    if user=="admin" and pw=="aura2026":
        return {"success": True}
    else:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

# -------------------------
# Health check
# -------------------------
@app.get("/health")
def health():
    try:
        conn = get_db_connection()
        conn.close()
        return {"status": "ok"}
    except:
        raise HTTPException(status_code=500, detail="DB connection failed")
