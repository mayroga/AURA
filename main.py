import os
import json
import stripe
import hashlib
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from pymongo import MongoClient

# ===============================
# ENVIRONMENT VARIABLES (RENDER)
# ===============================
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

DATABASE_URI = os.getenv("DATABASE_URI")
EMAIL_API_KEY = os.getenv("EMAIL_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

BASE_URL = os.getenv("BASE_URL")
LEGAL_VERSION = os.getenv("LEGAL_VERSION", "2026-01-08-v1")

# ===============================
# STRIPE INIT
# ===============================
stripe.api_key = STRIPE_SECRET_KEY

# ===============================
# DATABASE
# ===============================
client = MongoClient(DATABASE_URI)
db = client["health_cost_app"]
users_col = db["users"]
logs_col = db["logs"]

# ===============================
# FASTAPI APP
# ===============================
app = FastAPI(title="Healthcare Cost Transparency API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # frontend móvil
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===============================
# MODELS
# ===============================
class EstimateRequest(BaseModel):
    state: str
    zip: str
    code: str
    insured: bool
    plan_type: str

class ProviderRequest(BaseModel):
    state: str
    zip: str

class CheckoutRequest(BaseModel):
    plan: str

# ===============================
# UTILS
# ===============================
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def log_event(event: str, data: dict):
    logs_col.insert_one({
        "event": event,
        "data": data,
        "timestamp": datetime.utcnow(),
        "legal_version": LEGAL_VERSION
    })

# ===============================
# CORE ENDPOINTS
# ===============================

@app.post("/estimate")
def get_estimate(payload: EstimateRequest):
    """
    Estimados únicamente
    NO diagnóstico
    NO precios garantizados
    """

    # Simulación basada en rangos públicos
    base_min = 120
    base_max = 600

    if payload.insured:
        base_min *= 0.6
        base_max *= 0.8

    if payload.plan_type == "PREMIUM":
        base_min *= 0.9
        base_max *= 0.9

    estimate = {
        "min": round(base_min, 2),
        "max": round(base_max, 2),
        "code": payload.code,
        "state": payload.state,
        "zip": payload.zip,
        "insured": payload.insured,
        "plan_type": payload.plan_type,
        "legal_version": LEGAL_VERSION,
        "disclaimer": "Estimates only. No medical advice. No price guarantee."
    }

    log_event("estimate_generated", estimate)

    return estimate

# ===============================

@app.post("/providers")
def get_providers(payload: ProviderRequest):
    """
    Proveedores ficticios (placeholder)
    Información pública solamente
    """

    providers = [
        {
            "id": "prov1",
            "name": "Local Health Clinic",
            "zip": payload.zip,
            "specialty": "General Practice",
            "in_network": True
        },
        {
            "id": "prov2",
            "name": "Downtown Dental Center",
            "zip": payload.zip,
            "specialty": "Dental",
            "in_network": False
        }
    ]

    log_event("providers_lookup", payload.dict())

    return providers

# ===============================
# STRIPE CHECKOUT
# ===============================
PRICE_MAP = {
    "BASIC_MONTHLY": "price_BASIC_MONTHLY_ID",
    "BASIC_DAILY": "price_BASIC_DAILY_ID",
    "PREMIUM_MONTHLY": "price_PREMIUM_MONTHLY_ID"
}

@app.post("/create-checkout-session")
def create_checkout_session(payload: CheckoutRequest):
    if payload.plan not in PRICE_MAP:
        raise HTTPException(status_code=400, detail="Invalid plan")

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="subscription" if "MONTHLY" in payload.plan else "payment",
        line_items=[{
            "price": PRICE_MAP[payload.plan],
            "quantity": 1
        }],
        success_url=f"{BASE_URL}/success",
        cancel_url=f"{BASE_URL}/cancel"
    )

    log_event("checkout_created", {"plan": payload.plan})

    return {"url": session.url}

# ===============================
# STRIPE WEBHOOK
# ===============================
@app.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Webhook error")

    if event["type"] == "checkout.session.completed":
        log_event("payment_completed", event["data"]["object"])

    if event["type"] == "invoice.payment_failed":
        log_event("payment_failed", event["data"]["object"])

    return {"status": "success"}

# ===============================
# ADMIN (BÁSICO)
# ===============================
@app.post("/admin/login")
def admin_login(username: str, password: str):
    if (
        username == ADMIN_USERNAME
        and hash_password(password) == hash_password(ADMIN_PASSWORD)
    ):
        return {"status": "ok"}

    raise HTTPException(status_code=401, detail="Unauthorized")

# ===============================
# HEALTH CHECK
# ===============================
@app.get("/")
def root():
    return {
        "status": "running",
        "service": "Healthcare Cost Transparency API",
        "legal_version": LEGAL_VERSION
    }
