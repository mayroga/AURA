import os
import stripe
import asyncio
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# Configuración Profesional
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
client_openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# IDs de Stripe Aura
PRICE_IDS = {
    "rapido": "price_1Snam1BOA5mT4t0PuVhT2ZIq",
    "standard": "price_1SnaqMBOA5mT4t0PppRG2PuE",
    "special": "price_1SnatfBOA5mT4t0PZouWzfpw",
    "donacion": "price_1SoB56BOA5mT4t0P7EXAMPLE"
}

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/login-admin")
async def login_admin(user: str = Form(...), pw: str = Form(...)):
    if user == os.getenv("ADMIN_USERNAME") and pw == os.getenv("ADMIN_PASSWORD"):
        return {"status": "success"}
    return JSONResponse(status_code=401, content={"status": "error"})

@app.post("/estimado")
async def obtener_estimado(consulta: str = Form(...), lang: str = Form("es")):
    # BLINDAJE LEGAL IMPENETRABLE LEYENDO DE TU MEMORIA
    blindaje = "Este reporte es emitido por Aura by May Roga LLC, Agencia Informativa Independiente. No somos médicos, ni seguros, ni damos diagnósticos. Reportamos datos de mercado públicos para el ahorro del consumidor."
    
    fuente = "Fuente: CMS.gov / [Estado] Dept. of Health Data 2026."
    derecho = "Usted no necesita seguro para pagar este precio. Es su derecho legal preguntar por el 'Self-pay rate' (Tarifa de pago propio)."

    prompt = f"""
    ERES EL ASESOR JEFE DE AURA BY MAY ROGA LLC (No menciones IA).
    Misión: Inteligencia de Precios para Justicia Financiera.
    
    INSTRUCCIONES DE RESPUESTA (BANDEJA DE PLATA):
    1. BLINDAJE: {blindaje}
    2. EL TESORO LOCALIZADO: Compara el precio más bajo en su zona ($) vs Hospitales promedio ($).
    3. TU GANANCIA REAL: "Al usar Aura hoy, acabas de ganar $XXX que se quedan en tu bolsillo."
    4. TRIÁNGULO DE DECISIÓN:
       A. ZONA DE CONFORT (ZIP): 2 opciones de alta calidad cerca.
       B. OLIMPO DE LA SALUD (PRESTIGIO): La mejor opción del estado por reputación.
       C. OPERACIÓN AHORRO (VECINOS): 3 precios más bajos en condados cercanos.
       D. RUTA NACIONAL: Los 6 mejores precios en los 50 estados.
    5. ETIQUETA ORO: Si hay ahorro > $1000, añade "GANANCIA EXTREMA".
    6. DERECHO LEGAL: {derecho}
    7. FUENTE: {fuente}
    8. CIERRE: {blindaje}
    """

    async def call_gemini():
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model.generate_content(prompt).text

    async def call_openai():
        response = client_openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "Asesor de Aura"}, {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    try:
        try:
            res_text = await asyncio.wait_for(call_gemini(), timeout=12.0)
        except:
            res_text = await call_openai()
        return {"resultado": res_text}
    except:
        return {"resultado": "El Asesor de Aura está procesando los datos públicos. Reintente."}

@app.post("/create-checkout-session")
async def pay(plan: str = Form(...)):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": PRICE_IDS[plan.lower()], "quantity": 1}],
            mode="payment",
            success_url="https://aura-iyxa.onrender.com/?success=true",
            cancel_url="https://aura-iyxa.onrender.com/"
        )
        return {"url": session.url}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
