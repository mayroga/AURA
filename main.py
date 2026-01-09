import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, text
import stripe

# ======================================================
# ENV VARIABLES
# ======================================================
DATABASE_URI = os.getenv("DATABASE_URI")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
BASE_URL = os.getenv("BASE_URL", "")
LEGAL_VERSION = os.getenv("LEGAL_VERSION", "1.0")

if not DATABASE_URI or not DATABASE_URI.startswith("postgresql"):
    raise RuntimeError("DATABASE_URI must be PostgreSQL")

stripe.api_key = STRIPE_SECRET_KEY

# ======================================================
# APP
# ======================================================
app = FastAPI(title="US Health Cost Estimator", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================================================
# DATABASE
# ======================================================
engine = create_engine(DATABASE_URI, pool_pre_ping=True)

def db():
    return engine.connect()

# ======================================================
# MODELS
# ======================================================
class EstimateRequest(BaseModel):
    cpt_code: str
    zip_code: str
    state: str
    insurance_type: str  # insured | uninsured | out_of_network

class CheckoutRequest(BaseModel):
    price_id: str

# ======================================================
# HEALTH CHECK
# ======================================================
@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "Cost Estimator",
        "legal_version": LEGAL_VERSION
    }

# ======================================================
# COST ESTIMATION (CORE LOGIC)
# ======================================================
@app.post("/estimate")
def estimate_cost(data: EstimateRequest):
    query = text("""
        SELECT low_price, high_price
        FROM cost_estimates
        WHERE cpt_code = :cpt
          AND zip_code = :zip
          AND state = :state
        LIMIT 1
    """)

    with db() as conn:
        result = conn.execute(query, {
            "cpt": data.cpt_code,
            "zip": data.zip_code,
            "state": data.state
        }).fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="No estimate available")

    low, high = result

    multiplier = {
        "insured": 0.85,
        "out_of_network": 1.15,
        "uninsured": 1.0
    }.get(data.insurance_type, 1.0)

    return {
        "cpt_code": data.cpt_code,
        "estimated_range": {
            "low": round(low * multiplier, 2),
            "high": round(high * multiplier, 2)
        },
        "disclaimer": "Estimated costs only. Not a medical or insurance service."
    }

# ======================================================
# STRIPE CHECKOUT
# ======================================================
@app.post("/checkout")
def create_checkout(data: CheckoutRequest):
    try:
        session = stripe.checkout.Session.create(
            mode="subscription",
            payment_method_types=["card"],
            line_items=[{
                "price": data.price_id,
                "quantity": 1
            }],
            success_url=f"{BASE_URL}/success.html",
            cancel_url=f"{BASE_URL}/cancel.html"
        )
        return {"url": session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ======================================================
# STRIPE WEBHOOK
# ======================================================
@app.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig, STRIPE_WEBHOOK_SECRET
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid webhook")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        # Aquí puedes marcar usuario como premium si deseas
        pass

    return {"received": True}
