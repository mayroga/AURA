import os
import sqlite3
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

# Configuración de Llaves desde Render
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
client_openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# IDs de Stripe para los 3 Planes de Acceso
PRICE_IDS = {
    "rapido": "price_1Snam1BOA5mT4t0PuVhT2ZIq",
    "standard": "price_1SnaqMBOA5mT4t0PppRG2PuE",
    "special": "price_1SnatfBOA5mT4t0PZouWzfpw"  # El ID propio del plan Especial
}

# Link Externo EXCLUSIVO para Donaciones
LINK_DONACION = "https://buy.stripe.com/28E00igMD8dR00v5vl7Vm0h"

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

def query_sql(termino):
    try:
        conn = sqlite3.connect('aura_data.db')
        cursor = conn.cursor()
        query = "SELECT cpt_code, description, state, low_price, high_price FROM cost_estimates WHERE description LIKE ? OR cpt_code LIKE ?"
        cursor.execute(query, (f"%{termino}%", f"%{termino}%"))
        results = cursor.fetchall()
        conn.close()
        return results if results else "Dato no en SQL"
    except:
        return "Error SQL"

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
async def obtener_estimado(consulta: str = Form(...)):
    datos_internos = query_sql(consulta)
    blindaje = "Este reporte es emitido por Aura by May Roga LLC, Agencia Informativa Independiente. No somos médicos, ni seguros, ni damos diagnósticos. Reportamos datos de mercado públicos para el ahorro del consumidor."

    prompt = f"""
    ERES EL ASESOR JEFE DE AURA BY MAY ROGA LLC.
    DATOS REALES EN NUESTRO SQL: {datos_internos}
    
    INSTRUCCIÓN: 
    - Usa los datos del SQL como prioridad absoluta. 
    - Si no están en SQL, busca en CMS.gov y datos públicos oficiales. NO INVENTES.
    - Estructura: Blindaje, Tesoro (Comparativa), Tu Ganancia Real, Triángulo de Decisión, Derecho Legal (Self-pay), Fuente y Cierre con Blindaje.
    """

    async def call_gemini():
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model.generate_content(prompt).text

    try:
        res_text = await asyncio.wait_for(call_gemini(), timeout=12.0)
        return {"resultado": res_text}
    except:
        return {"resultado": "Aura consultando fuentes oficiales. Reintente."}

@app.post("/create-checkout-session")
async def pay(plan: str = Form(...)):
    # Lógica de separación: Donación va al link externo, Planes van por API
    if plan.lower() == "donacion":
        return {"url": LINK_DONACION}
    
    try:
        # El plan especial se procesa como suscripción, los otros como pago único
        mode = "subscription" if plan.lower() == "special" else "payment"
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": PRICE_IDS[plan.lower()], "quantity": 1}],
            mode=mode,
            success_url="https://aura-iyxa.onrender.com/?success=true",
            cancel_url="https://aura-iyxa.onrender.com/"
        )
        return {"url": session.url}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
