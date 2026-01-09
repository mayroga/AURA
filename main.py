import os
import sqlite3
import stripe
from datetime import datetime
from fastapi import FastAPI, Form, Depends, HTTPException, status
from fastapi.responses import JSONResponse, HTMLResponse  # Importaciones para Python 3.13
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = FastAPI(title="Aura by May Roga LLC")

# --- SEGURIDAD ---
security = HTTPBasic()
ADMIN_USER = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASS = os.getenv("ADMIN_PASSWORD", "password")

# --- STRIPE ---
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

PRICE_IDS = {
    "rapido": "price_1Snam1BOA5mT4t0PuVhT2ZIq",   # $5.99
    "standard": "price_1SnaqMBOA5mT4t0PppRG2PuE", # $9.99
    "special": "price_1SnatfBOA5mT4t0PZouWzfpw"   # $19.99
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- INICIALIZACIÓN DE BASE DE DATOS ---
def init_db():
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    try:
        sql_path = 'cost_estimates.sql'
        if os.path.exists(sql_path):
            with open(sql_path, 'r', encoding='utf-8') as f:
                conn.executescript(f.read())
            print("Base de datos Aura (50 Estados) cargada exitosamente.")
        else:
            print("Error: No se encontró el archivo cost_estimates.sql")
    except Exception as e:
        print(f"Error cargando los datos de Aura: {e}")
    return conn

db_conn = init_db()

# --- CARGA DE INTERFAZ VISUAL ---
@app.get("/", response_class=HTMLResponse)
async def read_index():
    # Este endpoint hace que al entrar a la URL se vea el index.html
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"<h1>Error: No se encontró el archivo index.html</h1><p>{str(e)}</p>"

# --- ENDPOINTS DE SERVICIO ---

@app.post("/estimado")
async def obtener_estimado(
    zip_code: str = Form(...), 
    code: str = Form(...), 
    plan_type: str = Form(...)
):
    dia_actual = datetime.now().day
    plan = plan_type.lower()
    
    # Lógica de tiempos de acceso Aura (Resolviendo necesidad real)
    if plan == "rapido":
        tiempo = 7
    elif plan == "standard":
        tiempo = 15
    elif plan == "special":
        tiempo = 35 if dia_actual <= 2 else 6
    else:
        return JSONResponse(content={"error": "Plan no válido"}, status_code=400)

    cursor = db_conn.cursor()
    query = "SELECT description, low_price, high_price, state FROM cost_estimates WHERE cpt_code = ? AND zip_code = ?"
    cursor.execute(query, (code.upper(), zip_code))
    row = cursor.fetchone()

    if row:
        return {
            "empresa": "Aura by May Roga LLC",
            "procedimiento": row[0],
            "rango": f"${row[1]} - ${row[2]}",
            "ubicacion": f"Estado: {row[3]} | ZIP: {zip_code}",
            "tiempo_concedido": f"{tiempo} min",
            "nota": "Estimado oficial basado en transparencia de códigos."
        }
    
    return JSONResponse(
        content={
            "empresa": "Aura by May Roga LLC",
            "error": "Código no localizado en esta zona.",
            "tiempo_concedido": f"{tiempo} min"
        }, 
        status_code=404
    )

@app.post("/create-checkout-session")
async def create_checkout_session(plan: str = Form(...)):
    plan = plan.lower()
    if plan not in PRICE_IDS:
        return JSONResponse(content={"error": "Plan inválido"}, status_code=400)

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": PRICE_IDS[plan], "quantity": 1}],
            mode="subscription" if plan == "special" else "payment",
            success_url="https://aura-iyxa.onrender.com/?success=true",
            cancel_url="https://aura-iyxa.onrender.com/?cancel=true",
        )
        return {"url": session.url}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# --- SEGURIDAD ADMIN ---
def get_current_user(credentials: HTTPBasicCredentials = Depends(HTTPBasic())):
    if credentials.username != ADMIN_USER or credentials.password != ADMIN_PASS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Acceso Denegado",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/admin/status")
async def check_status(username: str = Depends(get_current_user)):
    return {"sistema": "Aura Online", "admin": username}
