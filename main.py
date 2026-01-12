import os
import sqlite3
import stripe
import asyncio
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# 1. Configuración de API Keys
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
# Usamos el cliente nuevo que pide tu requirements
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

PRICE_IDS = {
    "rapido": "price_1Snam1BOA5mT4t0PuVhT2ZIq",
    "standard": "price_1SnaqMBOA5mT4t0PppRG2PuE",
    "special": "price_1SnatfBOA5mT4t0PZouWzfpw"
}

LINK_DONACION = "https://buy.stripe.com/28E00igMD8dR00v5vl7Vm0h"

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

def query_sql(termino):
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, 'aura_data.db')
        if not os.path.exists(db_path):
            return "SQL_OFFLINE"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        query = "SELECT cpt_code, description, state, low_price, high_price FROM cost_estimates WHERE description LIKE ? OR cpt_code LIKE ?"
        cursor.execute(query, (f"%{termino}%", f"%{termino}%"))
        results = cursor.fetchall()
        conn.close()
        return results if results else "DATO_NO_SQL"
    except Exception as e:
        return f"ERROR_SQL: {str(e)}"

@app.get("/", response_class=HTMLResponse)
async def read_index():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_dir, "index.html"), "r", encoding="utf-8") as f:
        return f.read()

@app.post("/estimado")
async def obtener_estimado(consulta: str = Form(...), lang: str = Form("es")):
    datos_internos = query_sql(consulta)
    idiomas = {"es": "Español", "en": "English", "ht": "Kreyòl (Haitian Creole)"}
    idioma_destino = idiomas.get(lang, "Español")
    
    blindaje = "Este reporte es emitido por Aura by May Roga LLC, Agencia Informativa Independiente. No somos médicos, ni seguros, ni damos diagnósticos. Reportamos datos de mercado públicos para el ahorro del consumidor."

    prompt = f"""
    ERES EL ASESOR JEFE DE AURA BY MAY ROGA LLC. 
    RESPONDE ÚNICAMENTE EN IDIOMA: {idioma_destino}.
    DATOS REALES EN NUESTRO SQL: {datos_internos}
    
    INSTRUCCIÓN: 
    - Usa los datos del SQL como prioridad absoluta. 
    - Si los datos son 'SQL_OFFLINE' o 'DATO_NO_SQL', busca en CMS.gov 2026.
    - Estructura: Blindaje, El Tesoro, Tu Ganancia Real, Triángulo de Decisión, Derecho Legal, Fuente y Cierre.
    """

    try:
        # Llamada con la nueva librería google-genai
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        return {"resultado": response.text}
    except Exception as e:
        return {"resultado": "Aura está procesando su solicitud. Por favor, intente de nuevo en unos segundos."}

@app.post("/create-checkout-session")
async def pay(plan: str = Form(...)):
    if plan.lower() == "donacion":
        return {"url": LINK_DONACION}
    try:
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
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/login-admin")
async def login_admin(user: str = Form(...), pw: str = Form(...)):
    if user == os.getenv("ADMIN_USERNAME") and pw == os.getenv("ADMIN_PASSWORD"):
        return {"status": "success"}
    return JSONResponse(status_code=401, content={"status": "error"})
