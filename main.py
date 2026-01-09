import os
import sqlite3
import stripe
from datetime import datetime
from fastapi import FastAPI, Form, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# IDs de Stripe actualizados
PRICE_IDS = {
    "rapido": "price_1Snam1BOA5mT4t0PuVhT2ZIq",
    "standard": "price_1SnaqMBOA5mT4t0PppRG2PuE",
    "special": "price_1SnatfBOA5mT4t0PZouWzfpw"
}

stripe.api_key = os.getenv("STRIPE_API_KEY")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Carga de base de datos SQL (Abarca los 50 estados según tu archivo)
def init_db():
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    if os.path.exists('cost_estimates.sql'):
        with open('cost_estimates.sql', 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
    return conn

db = init_db()

@app.post("/estimado")
async def estimado(zip_code: str = Form(...), code: str = Form(...), plan_type: str = Form(...)):
    dia = datetime.now().day
    plan = plan_type.lower()
    
    # Lógica de tiempos de acceso Aura
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
            "ubicacion": f"Estado: {row[3]} | ZIP: {zip_code}",
            "minutos": tiempo,
            "nota": "Estimado basado en códigos oficiales públicos."
        }
    return {"error": "Código no encontrado en este ZIP. Intente con un código CPT/CDT oficial."}

@app.post("/create-checkout-session")
async def payment(plan: str = Form(...)):
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
        return {"error": str(e)}
