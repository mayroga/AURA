import os
import stripe
import httpx
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from dotenv import load_dotenv

load_dotenv()

# Configuración de Stripe
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")  # Tu clave secreta de Stripe
BASE_URL = os.getenv("BASE_URL", "https://aura-iyxa.onrender.com")

stripe.api_key = STRIPE_API_KEY

# Price IDs
PRICE_IDS = {
    "trial": "price_1SnYkMBOA5mT4t0P2Ra3NpYy",
    "basic": "price_1SnYuABOA5mT4t0Pv706amhC",
    "premium": "price_1SnZ0eBOA5mT4t0Phwt58d4k"
}

# App FastAPI
app = FastAPI(title="Aura API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# Endpoint raíz
# ==============================
@app.get("/")
async def root():
    return {"message": "Aura API funcionando"}

# ==============================
# Endpoint de estimado
# ==============================
@app.post("/estimado")
async def estimado(
    estado: str = Form(...),
    zip_code: str = Form(...),
    code: str = Form(...),
    asegurado: bool = Form(False),
    plan_type: str = Form("BASIC")
):
    # Simulación de cálculo de costos (puedes conectar con DB real)
    min_price, max_price = 50, 500
    if plan_type.lower() == "premium":
        min_price, max_price = 100, 1000
    elif plan_type.lower() == "trial":
        min_price, max_price = 0, 1

    return {
        "plan_type": plan_type.upper(),
        "estado": estado,
        "zip": zip_code,
        "code": code,
        "insured": asegurado,
        "min": min_price,
        "max": max_price
    }

# ==============================
# Endpoint de proveedores
# ==============================
@app.post("/proveedores")
async def proveedores(
    estado: str = Form(...),
    zip_code: str = Form(...)
):
    # Simulación de proveedores
    sample_providers = [
        {"id": 1, "name": "Clínica Aura", "specialty": "General", "zip": zip_code, "in_network": True},
        {"id": 2, "name": "Dental Aura", "specialty": "Dental", "zip": zip_code, "in_network": False},
    ]
    return sample_providers

# ==============================
# Endpoint de pago Stripe
# ==============================
@app.post("/create-checkout-session")
async def create_checkout_session(plan: str = Form(...)):
    plan = plan.lower()
    if plan not in PRICE_IDS:
        return JSONResponse({"error": True, "message": "Plan inválido"}, status_code=400)

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price": PRICE_IDS[plan],
                "quantity": 1,
            }],
            mode="subscription" if plan != "trial" else "payment",
            success_url=f"{BASE_URL}/?success=true",
            cancel_url=f"{BASE_URL}/?canceled=true"
        )
        return {"url": session.url}
    except Exception as e:
        return JSONResponse({"error": True, "message": str(e)}, status_code=500)

# ==============================
# Endpoint de donación / pago único
# ==============================
@app.post("/donacion")
async def donacion(amount: int = Form(...)):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": "Donación Aura"},
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
        return JSONResponse({"error": True, "message": str(e)}, status_code=500)
