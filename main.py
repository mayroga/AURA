import os
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import stripe

# Cargar variables de entorno
load_dotenv()

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
BASE_URL = os.getenv("BASE_URL") or "https://aura-iyxa.onrender.com"

stripe.api_key = STRIPE_SECRET_KEY

app = FastAPI()

# Permitir CORS desde cualquier origen (para pruebas)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "SmartCargo API funcionando"}

@app.post("/create-checkout-session")
async def create_checkout_session(price_id: str = Form(...)):
    """
    Crea una sesión de Stripe Checkout para un plan específico.
    price_id: el ID del precio de Stripe
    """
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price": price_id,
                "quantity": 1
            }],
            mode="subscription",
            success_url=f"{BASE_URL}?success=true",
            cancel_url=f"{BASE_URL}?canceled=true",
        )
        return JSONResponse({"url": session.url})
    except stripe.error.InvalidRequestError as e:
        return JSONResponse({"error": str(e)}, status_code=400)
    except Exception as e:
        return JSONResponse({"error": "Error interno del servidor"}, status_code=500)
