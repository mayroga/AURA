import os
import sqlite3
import stripe
import asyncio
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# 1. Configuración de API Keys con validación
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# IDs de Stripe verificados
PRICE_IDS = {
    "rapido": "price_1Snam1BOA5mT4t0PuVhT2ZIq",
    "standard": "price_1SnaqMBOA5mT4t0PppRG2PuE",
    "special": "price_1SnatfBOA5mT4t0PZouWzfpw"
}

# Link Externo de Donación Directa
LINK_DONACION = "https://buy.stripe.com/28E00igMD8dR00v5vl7Vm0h"

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# 2. Motor SQL con Rutas Absolutas para Render
def query_sql(termino):
    try:
        # Esto asegura que encuentre el archivo .db sin importar la carpeta de Render
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

# 3. Función de Estimado con Soporte de Idiomas y Anti-Bloqueo
@app.post("/estimado")
async def obtener_estimado(consulta: str = Form(...), lang: str = Form("es")):
    datos_internos = query_sql(consulta)
    
    # Mapeo de idiomas para que la IA sepa en qué responder
    idiomas = {"es": "Español", "en": "English", "ht": "Kreyòl (Haitian Creole)"}
    idioma_destino = idiomas.get(lang, "Español")
    
    blindaje = "Este reporte es emitido por Aura by May Roga LLC, Agencia Informativa Independiente. No somos médicos, ni seguros, ni damos diagnósticos. Reportamos datos de mercado públicos para el ahorro del consumidor."

    prompt = f"""
    ERES EL ASESOR JEFE DE AURA BY MAY ROGA LLC. 
    RESPONDE ÚNICAMENTE EN IDIOMA: {idioma_destino}.
    
    DATOS REALES EN NUESTRO SQL: {datos_internos}
    
    INSTRUCCIÓN: 
    - Usa los datos del SQL como prioridad absoluta. 
    - Si los datos son 'SQL_OFFLINE' o 'DATO_NO_SQL', busca en CMS.gov 2026. ¡PROHIBIDO INVENTAR!
    - Estructura: Blindaje, Tesoro (Comparativa), Tu Ganancia Real, Triángulo de Decisión (Cercanía, Prestigio, Ahorro Vecino, Ruta Nacional), Derecho Legal (Self-pay rate), Fuente y Cierre.
    """

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        # Usamos asyncio.to_thread para que la IA no bloquee el servidor
        response = await asyncio.to_thread(model.generate_content, prompt)
        return {"resultado": response.text}
    except Exception as e:
        return {"resultado": "Aura está procesando su solicitud. Por favor, intente de nuevo en unos segundos."}

# 4. Gestión de Pagos (Donación vs Planes)
@app.post("/create-checkout-session")
async def pay(plan: str = Form(...)):
    if plan.lower() == "donacion":
        return {"url": LINK_DONACION}
    
    try:
        # Suscripción para 'special', pago único para el resto
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
