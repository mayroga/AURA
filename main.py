import os
import stripe
import sqlite3
from datetime import datetime
from fastapi import FastAPI, Form, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Aura by May Roga LLC - Healthcare Transparency")

# 1. Configuración de Stripe y Planes
stripe.api_key = os.getenv("STRIPE_API_KEY")
BASE_URL = os.getenv("BASE_URL", "https://aura-iyxa.onrender.com")

PRICE_IDS = {
    "rapido": "price_1Snam1BOA5mT4t0PuVhT2ZIq",   # $5.99 - 7 min
    "standard": "price_1SnaqMBOA5mT4t0PppRG2PuE", # $9.99 - 15 min
    "special": "price_1SnatfBOA5mT4t0PZouWzfpw"   # $19.99 - 35min/6min
}

# 2. Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Conexión a la Base de Datos SQL
def get_db_connection():
    # Asegúrate de haber creado 'aura.db' con tu archivo cost_estimates.sql
    conn = sqlite3.connect('aura.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
async def root():
    return {"message": "Aura API - Transparency System Active"}

@app.post("/estimado")
async def obtener_estimado(
    zip_code: str = Form(...),
    code: str = Form(...),
    plan_type: str = Form(...)
):
    plan = plan_type.lower()
    dia_actual = datetime.now().day
    
    # Lógica de Tiempos Aura
    if plan == "rapido": 
        tiempo = 7
    elif plan == "standard": 
        tiempo = 15
    elif plan == "special":
        tiempo = 35 if dia_actual <= 2 else 6
    else:
        return JSONResponse({"error": "Plan no reconocido"}, status_code=400)

    # Consulta a tu tabla cost_estimates
    try:
        conn = get_db_connection()
        query = "SELECT * FROM cost_estimates WHERE cpt_code = ? AND zip_code = ?"
        result = conn.execute(query, (code.upper(), zip_code)).fetchone()
        conn.close()
    except Exception as e:
        return JSONResponse({"error": "Error de base de datos"}, status_code=500)

    if not result:
        return {
            "empresa": "Aura by May Roga LLC",
            "status": "partial",
            "minutos_sesion": tiempo,
            "mensaje": "No hay datos locales para este ZIP. Mostrando promedio general.",
            "rango_estimado": "$150 - $400",
            "legal": "Estimados informativos. No es garantía de precio final."
        }

    return {
        "empresa": "Aura by May Roga LLC",
        "plan": plan.upper(),
        "minutos_concedidos": tiempo,
        "procedimiento": result["description"],
        "codigo": result["cpt_code"],
        "estado": result["state"],
        "zip": result["zip_code"],
        "rango_estimado": f"${result['low_price']} - ${result['high_price']}",
        "legal": "Información analítica basada en datos históricos. Aura System."
    }

@app.post("/create-checkout-session")
async def create_checkout_session(plan: str = Form(...)):
    plan = plan.lower()
    if plan not in PRICE_IDS:
        return JSONResponse({"error": "Plan inválido"}, status_code=400)

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": PRICE_IDS[plan], "quantity": 1}],
            mode="subscription" if plan == "special" else "payment",
            success_url=f"{BASE_URL}/?success=true",
            cancel_url=f"{BASE_URL}/?canceled=true"
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
                        "name": "Donación Solidaria - Aura",
                        "description": "Apoyo a mantenimiento y herramientas de trabajo para necesitados."
                    },
                    "unit_amount": amount * 100,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=f"{BASE_URL}/?success=true",
            cancel_url=f"{BASE_URL}/?canceled=true"
        )
        return {"url": session.url}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
