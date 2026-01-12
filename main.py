import os
import stripe
import smtplib
import asyncio
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from email.mime.text import MIMEText
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
client_openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# IDs de Stripe proporcionados
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

@app.post("/estimado")
async def obtener_estimado(consulta: str = Form(...), lang: str = Form("es")):
    # BLINDAJE LEGAL IMPENETRABLE EXACTO
    blindaje_exacto = "Este reporte es emitido por Aura by May Roga LLC, Agencia Informativa Independiente. No somos médicos, ni seguros, ni damos diagnósticos. Reportamos datos de mercado públicos para el ahorro del consumidor."
    
    prompt = f"""
    ERES EL ASESOR JEFE DE AURA BY MAY ROGA LLC. 
    (PROHIBIDO usar la palabra 'IA' o 'Inteligencia Artificial').
    
    OBJETIVO: Transparencia total para: 
    1. Quienes no tienen seguro.
    2. Quienes tienen seguro pero les cubre poco.
    3. Quienes buscan lo mejor (Excelencia y Prestigio).
    
    Consulta: "{consulta}" | Idioma: "{lang}"

    ESTRUCTURA DE RESPUESTA (BANDEJA DE PLATA):
    1. BLINDAJE LEGAL: "{blindaje_exacto}"
    2. GANANCIA ESTIMADA: Cuánto dinero gana el cliente al no pagar precios inflados.
    3. PILAR 1 - TU ZONA: 2 opciones locales más baratas.
    4. PILAR 2 - EXCELENCIA Y PRESTIGIO: La mejor opción en reputación del estado.
    5. PILAR 3 - GANANCIA POR DISTANCIA: 3 opciones en condados vecinos.
    6. PILAR 4 - RUTA NACIONAL: Los 6 mejores precios en los 50 estados de USA.
    7. CIERRE: Repetir Blindaje Legal.
    """

    async def call_gemini():
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model.generate_content(prompt).text

    async def call_openai():
        response = client_openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "Eres el Asesor de Aura by May Roga LLC."}, {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    try:
        try:
            res_text = await asyncio.wait_for(call_gemini(), timeout=12.0)
        except:
            res_text = await call_openai()
        
        return {"resultado": res_text}
    except:
        return {"resultado": "El Asesor de Aura está procesando sus datos. Por favor reintente."}

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
