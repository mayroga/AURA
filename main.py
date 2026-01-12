import os
import stripe
from datetime import datetime
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import openai
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# Configuración Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Price IDs para planes normales
PRICE_IDS = {
    "rapido": "price_1Snam1BOA5mT4t0PuVhT2ZIq",
    "standard": "price_1SnaqMBOA5mT4t0PppRG2PuE",
    "special": "price_1SnatfBOA5mT4t0PZouWzfpw"
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Servir index.html
@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

# Estimado de precios
@app.post("/estimado")
async def obtener_estimado(
    zip_code: str = Form(...),
    consulta: str = Form(...),
    plan_type: str = Form(...),
    is_admin: str = Form("false")
):
    hoy = datetime.now()
    if is_admin == "true":
        tiempo = "Ilimitado"
    elif plan_type == "rapido":
        tiempo = "7 min"
    elif plan_type == "standard":
        tiempo = "15 min"
    elif plan_type == "special":
        tiempo = "35 min"
    else:
        tiempo = "Acceso por Pago"

    prompt = f"""
ERES EL ASESOR JEFE DE 'AURA BY MAY ROGA LLC'.
Misión: Inteligencia de Precios para Ahorro del Cliente.

1. Encuentra la opción más barata para {consulta} en el ZIP code {zip_code} (muestra nombre de clínica/hospital, ZIP, precio).
2. Encuentra 3 opciones más baratas dentro del mismo condado, mostrando nombre de clínica/hospital, ZIP, precio. Estas mismas opciones se consideran dentro del mismo estado.
3. Encuentra 6 opciones más baratas fuera del estado si existen, mostrando nombre de clínica/hospital, ZIP, condado, estado, precio.
4. Indica cuánto dinero ahorra el cliente al elegir la opción más barata.
5. Presenta todo en HTML limpio, usando <b> y <br> para claridad.
6. BLINDAJE LEGAL: "Este reporte es emitido por Aura by May Roga LLC, Agencia Informativa Independiente. No somos médicos ni seguros. Solo informamos costos de mercado."
"""

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        respuesta = response.text
    except Exception:
        try:
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            res = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
            respuesta = res.choices[0].message.content
        except:
            respuesta = "Aura está procesando altos volúmenes de datos. Por favor, refresque y reintente."

    return {"estimado": f"<strong>ACCESO CONCEDIDO: {tiempo}</strong><br><br>{respuesta.replace(chr(10), '<br>')}"}

# Checkout para planes normales
@app.post("/create-checkout-session")
async def create_checkout_session(plan: str = Form(...)):
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

# Donación directa (sin Price ID)
@app.post("/donate")
async def donate(amount: int = Form(...)):
    """
    amount en centavos. Ejemplo: $10 → 1000
    """
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": "Donación AURA"},
                    "unit_amount": amount
                },
                "quantity": 1
            }],
            mode="payment",
            success_url="https://aura-iyxa.onrender.com/?success=true",
            cancel_url="https://aura-iyxa.onrender.com/?cancel=true"
        )
        return {"url": session.url}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
