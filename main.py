import os
import stripe
from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Price IDs
PRICE_IDS = {
    "TRIAL": "price_1SnYkMBOA5mT4t0P2Ra3NpYy",
    "BASIC": "price_1SnYuABOA5mT4t0Pv706amhC",
    "PREMIUM": "price_1SnZ0eBOA5mT4t0Phwt58d4k"
}

# URL base
BASE_URL = os.getenv("BASE_URL", "https://aura-iyxa.onrender.com")

# RUTA PRINCIPAL: Servir el index.html
@app.get("/")
async def root():
    index_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    else:
        return JSONResponse({"detail": "Archivo index.html no encontrado"}, status_code=404)

# Crear sesión de pago Stripe
@app.post("/create-checkout-session")
async def create_checkout_session(plan: str = Form(...)):
    if plan not in PRICE_IDS:
        raise HTTPException(status_code=400, detail="Plan inválido")

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price": PRICE_IDS[plan],
                "quantity": 1
            }],
            mode="subscription",
            success_url=f"{BASE_URL}/?success=true",
            cancel_url=f"{BASE_URL}/?canceled=true"
        )
        return {"url": session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Estimado de costos (simulación)
@app.post("/estimado")
async def estimado(
    state: str = Form(...),
    zip: str = Form(...),
    code: str = Form(...),
    insured: bool = Form(False),
    plan_type: str = Form("BASIC")
):
    # Aquí puedes integrar la lógica real de tu base de datos o cálculo
    estimado_min = 50
    estimado_max = 200
    return {
        "min": estimado_min,
        "max": estimado_max,
        "plan_type": plan_type,
        "insured": insured
    }

# Donación (simulación)
@app.post("/donacion")
async def donacion(
    amount: float = Form(...),
    currency: str = Form("usd")
):
    # Aquí puedes crear una sesión de pago Stripe para donación si quieres
    return {"status": "ok", "amount": amount, "currency": currency}

# Endpoint de prueba para idioma automático
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    # Detección automática de idioma básica
    if any(c in user_message.lower() for c in ["hello", "hi"]):
        reply = "Hello! How can I help you?"
    elif any(c in user_message.lower() for c in ["bonjour", "bonsoir"]):
        reply = "Bonjour! Comment puis-je vous aider?"
    else:
        reply = "¡Hola! ¿En qué puedo ayudarte?"
    return {"reply": reply}
