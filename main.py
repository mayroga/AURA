import os
import sqlite3
import stripe
from datetime import datetime
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import openai
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="Aura by May Roga LLC")

# Configuración Dual IA (Redundancia Crítica)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
openai.api_key = os.getenv("OPENAI_API_KEY")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Credenciales de Administrador (Variables de Render)
ADMIN_USER = os.getenv("ADMIN_USERNAME")
ADMIN_PASS = os.getenv("ADMIN_PASSWORD")

# IDS DE PRECIO (Vincúlalos con tus IDs de Stripe)
PRICE_IDS = {
    "rapido": "price_1Snam1BOA5mT4t0PuVhT2ZIq",   # $5.99
    "standard": "price_1SnaqMBOA5mT4t0PppRG2PuE", # $9.99
    "special": "price_1SnatfBOA5mT4t0PZouWzfpw",  # $19.99 (Suscripción)
    "donacion": "price_DONACION_ID_AQUI"          # Donación
}

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/login-owner")
async def login_owner(username: str = Form(...), password: str = Form(...)):
    if username == ADMIN_USER and password == ADMIN_PASS:
        return {"access": "granted"}
    raise HTTPException(status_code=401)

@app.post("/estimado")
async def obtener_estimado(
    zip_code: str = Form(...), 
    consulta: str = Form(...), 
    plan_type: str = Form(...),
    is_admin: str = Form("false")
):
    # Lógica de Tiempos
    hoy = datetime.now()
    if is_admin == "true":
        tiempo = "Acceso Ilimitado (Dueño)"
    elif plan_type == "rapido":
        tiempo = "7 Minutos"
    elif plan_type == "standard":
        tiempo = "15 Minutos"
    elif plan_type == "special":
        tiempo = "35 Minutos" if hoy.day <= 2 else "6 Minutos"
    else:
        tiempo = "Consulta de cortesía"

    # Prompt de Inteligencia Nacional de Ahorro
    prompt = f"""
    Actúa como experto de la Agencia Informativa 'Aura by May Roga LLC'. 
    El cliente busca '{consulta}' en el ZIP {zip_code}.
    MISIÓN: Ahorro Nacional (Turismo Médico Interno).
    1. Da el estimado en el ZIP {zip_code}.
    2. Da 4 o 5 opciones comparativas en estados o ciudades cercanas más baratas (Ej. NY vs PA, FL vs GA, Hialeah vs Homestead).
    3. Sugiere si conviene volar, manejar o usar Telemedicina.
    4. Explica que estos datos son para que el cliente llame al proveedor y negocie.
    5. BLINDAJE: Finaliza diciendo que somos una Agencia Informativa, no médicos ni seguros.
    """
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        respuesta = model.generate_content(prompt).text
    except:
        res = openai.ChatCompletion.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
        respuesta = res.choices[0].message.content

    return {
        "estimado": f"<strong>Tiempo de Acceso: {tiempo}</strong><br><br>{respuesta.replace('\n', '<br>')}",
        "mensaje_social": "Su consulta ayuda a May Roga LLC a crear empleos."
    }

@app.post("/create-checkout-session")
async def pay(plan: str = Form(...)):
    try:
        mode = "subscription" if plan.lower() == "special" else "payment"
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": PRICE_IDS[plan.lower()], "quantity": 1}],
            mode=mode,
            success_url="https://aura-iyxa.onrender.com/?success=true",
            cancel_url="https://aura-iyxa.onrender.com/?cancel=true"
        )
        return {"url": session.url}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
