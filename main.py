import os
import stripe
from datetime import datetime
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import openai
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# ================================
# CONFIGURACIONES
# ================================

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

DOMAIN = "https://aura-iyxa.onrender.com"

PRICE_IDS = {
    "rapido": "price_1Snam1BOA5mT4t0PuVhT2ZIq",   
    "standard": "price_1SnaqMBOA5mT4t0PppRG2PuE", 
    "special": "price_1SnatfBOA5mT4t0PZouWzfpw"
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================================
# FRONTEND
# ================================

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

# ================================
# ESTIMADOS
# ================================

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
        tiempo = "7 minutos"
    elif plan_type == "standard":
        tiempo = "15 minutos"
    elif plan_type == "special":
        tiempo = "35 minutos" if hoy.day <= 2 else "6 minutos"
    else:
        tiempo = "Acceso limitado"

    prompt = f"""
    ERES EL ASESOR JEFE DE 'AURA BY MAY ROGA LLC'.

    MISIÓN: Inteligencia de precios para ayudar al cliente a ahorrar dinero en USA.

    Tarea:
    1. Encuentra los 5 precios más bajos disponibles en Estados Unidos para:
       {consulta} cerca de {zip_code}.
    2. Muestra diferencias de precio por estado o condado.
    3. Indica cuánto dinero se ahorra el paciente al NO pagar precios inflados.
    4. Explica que estos precios sirven para negociar directamente con clínicas y proveedores.
    5. Incluye este blindaje legal:

    "Este reporte es emitido por Aura by May Roga LLC, una Agencia Informativa Independiente.
    No somos médicos, hospitales ni compañías de seguros. No damos diagnósticos ni tratamientos.
    Solo informamos precios de mercado para ahorro del consumidor."
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        resultado = response.text
    except:
        try:
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            res = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
            resultado = res.choices[0].message.content
        except:
            resultado = "Aura está procesando altos volúmenes. Intente nuevamente."

    return {
        "estimado": f"<strong>ACCESO CONCEDIDO: {tiempo}</strong><br><br>{resultado.replace('\n','<br>')}"
    }

# ================================
# PAGOS POR PLAN (PRICE_ID)
# ================================

@app.post("/create-checkout-session")
async def create_checkout(plan: str = Form(...)):
    try:
        plan = plan.lower()
        if plan not in PRICE_IDS:
            return JSONResponse({"error": "Plan inválido"}, status_code=400)

        mode = "subscription" if plan == "special" else "payment"

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price": PRICE_IDS[plan],
                "quantity": 1
            }],
            mode=mode,
            success_url=f"{DOMAIN}/?success=true",
            cancel_url=f"{DOMAIN}/?cancel=true"
        )

        return {"url": session.url}

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# ================================
# DONACIÓN REAL (SIN PRICE ID)
# ================================

@app.post("/donate")
async def donate(amount: int = Form(1000)):
    """
    amount en CENTAVOS. 
    Ejemplo: 1000 = $10.00
    """
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": "Donación - Aura by May Roga LLC",
                        "description": "Apoyo para mantener la plataforma y crear empleos"
                    },
                    "unit_amount": amount
                },
                "quantity": 1
            }],
            success_url=f"{DOMAIN}/?donation=success",
            cancel_url=f"{DOMAIN}/?donation=cancel"
        )

        return {"url": session.url}

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
