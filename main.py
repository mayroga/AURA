import os
import sqlite3
import stripe
from datetime import datetime
from fastapi import FastAPI, Form, JSONResponse, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURACIÓN DE SEGURIDAD ---
app = FastAPI(title="Aura by May Roga LLC")
security = HTTPBasic()

# Credenciales de Admin (desde tus variables)
ADMIN_USER = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASS = os.getenv("ADMIN_PASSWORD", "password")

# --- CONFIGURACIÓN DE STRIPE ---
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

# IDs de tus Planes (Asegúrate de que coincidan con los de tu Stripe Dashboard)
PRICE_IDS = {
    "rapido": "price_1Snam1BOA5mT4t0PuVhT2ZIq",   # $5.99
    "standard": "price_1SnaqMBOA5mT4t0PppRG2PuE", # $9.99
    "special": "price_1SnatfBOA5mT4t0PZouWzfpw"   # $19.99
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- INICIALIZACIÓN DE BASE DE DATOS ---
# Usamos tu archivo SQL para cargar los precios de los 50 estados
def init_db():
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    try:
        with open('cost_estimates.sql', 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        print("Base de datos Aura cargada correctamente.")
    except Exception as e:
        print(f"Error cargando SQL: {e}")
    return conn

db = init_db()

# --- SEGURIDAD ADMIN ---
def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != ADMIN_USER or credentials.password != ADMIN_PASS:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return credentials.username

# --- ENDPOINTS ---

@app.post("/estimado")
async def estimado(zip_code: str = Form(...), code: str = Form(...), plan_type: str = Form(...)):
    dia = datetime.now().day
    plan = plan_type.lower()
    
    # Lógica de tiempos Aura
    if plan == "rapido": tiempo = 7
    elif plan == "standard": tiempo = 15
    elif plan == "special": tiempo = 35 if dia <= 2 else 6
    else: return JSONResponse({"error": "Plan no válido"}, status_code=400)

    cursor = db.cursor()
    cursor.execute("SELECT description, low_price, high_price, state FROM cost_estimates WHERE cpt_code = ? AND zip_code = ?", (code.upper(), zip_code))
    row = cursor.fetchone()

    if row:
        return {
            "empresa": "Aura by May Roga LLC",
            "procedimiento": row[0],
            "rango": f"${row[1]} - ${row[2]}",
            "ubicacion": f"{row[3]} | ZIP: {zip_code}",
            "minutos": tiempo,
            "blindaje": "Protección total al bolsillo frente a sobrecargos."
        }
    return {"error": "Código no encontrado. Use códigos oficiales CPT/CDT."}

@app.post("/create-checkout-session")
async def create_checkout_session(plan: str = Form(...)):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": PRICE_IDS[plan.lower()], "quantity": 1}],
            mode="subscription" if plan.lower() == "special" else "payment",
            success_url="https://aura-iyxa.onrender.com/?success=true",
            cancel_url="https://aura-iyxa.onrender.com/?cancel=true"
        )
        return {"url": session.url}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/donacion")
async def donacion(amount: int = Form(...)):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": "Donación Solidaria Aura",
                        "description": "Fondo para medios de trabajo y mantenimiento."
                    },
                    "unit_amount": amount * 100,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url="https://aura-iyxa.onrender.com/?success=true",
            cancel_url="https://aura-iyxa.onrender.com/?cancel=true"
        )
        return {"url": session.url}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# Panel de administración simple para ver que la API está viva
@app.get("/admin/status")
async def admin_status(username: str = Depends(get_current_user)):
    return {"status": "Aura System Online", "admin": username, "db_active": True}
