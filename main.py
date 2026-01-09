# main.py
import os
import time
import stripe
import httpx
import openai
import asyncio
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

app = FastAPI()

# Permitir CORS para frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========================
# CONFIGURACIONES
# ========================
BASE_URL = os.getenv("BASE_URL", "https://aura-iyxa.onrender.com")

# Admin para acceso gratuito y pruebas
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "1234")

# Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_BASIC_PLAN_ID = os.getenv("STRIPE_BASIC_PLAN_ID", "price_basic")
STRIPE_PREMIUM_PLAN_ID = os.getenv("STRIPE_PREMIUM_PLAN_ID", "price_premium")
STRIPE_TRIAL_PLAN_ID = os.getenv("STRIPE_TRIAL_PLAN_ID", "price_trial")

# IA
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Puedes usar otra variable si quieres

# Tiempo de uso por plan (en segundos)
PLAN_USAGE = {
    "TRIAL": 40,       # 40 segundos de prueba
    "BASIC": 3600,     # 1 hora
    "PREMIUM": 3600    # 1 hora por pago premium
}

# Historial de uso por usuario (temporal, reinicia al reiniciar app)
USER_USAGE = {}  # {"user_id": timestamp_final_uso}

# ========================
# SERVIR FRONTEND
# ========================
@app.get("/")
def root():
    """Sirve el index.html"""
    return FileResponse("index.html")


# ========================
# FUNCIONES AUXILIARES IA
# ========================
async def query_openai(prompt: str) -> str:
    """Consulta OpenAI con timeout"""
    try:
        async with httpx.AsyncClient(timeout=50) as client:
            headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
            json_data = {"model": "gpt-3.5-turbo", "messages": [{"role":"user","content":prompt}]}
            resp = await client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=json_data)
            data = resp.json()
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        return None

async def query_gemini(prompt: str) -> str:
    """Consulta Gemini con timeout"""
    try:
        async with httpx.AsyncClient(timeout=50) as client:
            headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}
            json_data = {"prompt": prompt}
            resp = await client.post("https://api.gemini.com/v1/completions", headers=headers, json=json_data)
            data = resp.json()
            return data.get("text")
    except Exception as e:
        return None

async def get_cost_estimate(prompt: str) -> str:
    """Usa OpenAI primero, si falla usa Gemini"""
    result = await query_openai(prompt)
    if not result:
        result = await query_gemini(prompt)
    if not result:
        result = "No se pudo generar el estimado en este momento. Intenta más tarde."
    return result


# ========================
# ENDPOINTS
# ========================
@app.post("/estimate")
async def estimate(
    state: str = Form(...),
    zip: str = Form(...),
    code: str = Form(...),
    insured: bool = Form(...),
    plan_type: str = Form("BASIC"),
    username: Optional[str] = Form(None),
    password: Optional[str] = Form(None)
):
    """Endpoint principal de estimado"""

    # Permite admin gratuito
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        pass
    else:
        # Control de tiempo de uso por plan
        user_key = username or f"{state}_{zip}_{code}"
        now = time.time()
        final_time = USER_USAGE.get(user_key, now)
        usage_time = PLAN_USAGE.get(plan_type.upper(), 40)
        if now < final_time:
            remaining = int(final_time - now)
            return {"error": True, "message": f"Tiempo de uso agotado. Espera {remaining} segundos o paga más tiempo."}
        USER_USAGE[user_key] = now + usage_time

    prompt = f"Genera un estimado de costos para {state}, ZIP {zip}, código {code}, asegurado: {insured}, plan: {plan_type}"
    result = await get_cost_estimate(prompt)
    return {"estimate": result, "plan_type": plan_type, "user": username or "guest"}


@app.post("/providers")
async def providers(
    state: str = Form(...),
    zip: str = Form(...)
):
    """Devuelve proveedores cercanos (simulado)"""
    providers_list = [
        {"id": 1, "name": "Clinica Aura", "specialty": "General", "zip": zip, "in_network": True},
        {"id": 2, "name": "Dental Smile", "specialty": "Dental", "zip": zip, "in_network": False}
    ]
    return providers_list


@app.post("/create-checkout-session")
def create_checkout_session(plan: str = Form(...)):
    """Crea sesión de pago Stripe"""
    plan = plan.upper()
    if plan == "BASIC":
        price_id = STRIPE_BASIC_PLAN_ID
    elif plan == "PREMIUM":
        price_id = STRIPE_PREMIUM_PLAN_ID
    elif plan == "TRIAL":
        price_id = STRIPE_TRIAL_PLAN_ID
    else:
        raise HTTPException(status_code=400, detail="Plan no válido")

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
        success_url=f"{BASE_URL}/?success=true",
        cancel_url=f"{BASE_URL}/?canceled=true"
    )
    return {"url": session.url}


# ========================
# MAIN
# ========================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
