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

# Configuración de Seguridad y Cobro
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# IDs de Stripe - ASEGÚRATE DE COPIAR LOS DE TU DASHBOARD DE STRIPE
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

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

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
        tiempo = "35 min" if hoy.day <= 2 else "6 min"
    else: 
        tiempo = "Acceso por Pago"

    # Prompt para Gemini/OpenAI generando las opciones detalladas
    prompt = f"""
Eres el asesor jefe de 'AURA BY MAY ROGA LLC', Agencia Informativa de Mercado.
Objetivo: Inteligencia de precios y estimados de costos para servicios de salud y otros mercados.

Instrucciones:
1. Proveer **1 opción** más barata dentro del ZIP {zip_code}, indicando **nombre de la clínica/hospital y dirección exacta**.
2. Proveer **3 opciones en el mismo condado** o en el mismo estado, indicando **nombre de la clínica/hospital y dirección exacta**.
3. Proveer **3-6 opciones fuera del estado**, indicando **nombre de la clínica/hospital y dirección exacta**.
4. Explicar cuánto se ahorra al negociar con el proveedor usando estos datos.
5. Hacer un resumen de la mejor opción y su ahorro.
6. BLINDAJE LEGAL: "Aura by May Roga LLC es una Agencia Informativa de Mercado. No ofrecemos servicios médicos ni seguros. Proveemos inteligencia de precios y estimados de costos para que el cliente pueda negociar y ahorrar dinero de manera informada."
7. Mencionar que estos datos sirven para **negociar precios reales**, no es consulta médica ni seguro.

Formato de salida en HTML con saltos de línea claros (<br>).
"""

    try:
        # Intentar generar con Gemini
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        respuesta = response.text
    except Exception as e:
        # Respaldo OpenAI si Gemini falla
        try:
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            res = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
            respuesta = res.choices[0].message.content
        except Exception as e2:
            respuesta = "Aura está procesando altos volúmenes de datos. Por favor, refresque y reintente."

    return {"estimado": f"<strong>ACCESO CONCEDIDO: {tiempo}</strong><br><br>{respuesta.replace(chr(10), '<br>')}"}

@app.post("/create-checkout-session")
async def create_checkout_session(
    amount: float = Form(...), 
    description: str = Form("Donación a Aura by May Roga LLC")
):
    try:
        # Donaciones directas sin Price ID
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": description
                    },
                    "unit_amount": int(amount * 100),  # Convertir a cents
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
