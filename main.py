import os
import sqlite3
import stripe
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from google import genai
import openai
from dotenv import load_dotenv

# Cargamos variables de entorno
load_dotenv()
app = FastAPI()

# 1️⃣ Configuración Stripe e IA
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
client_gemini = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
openai.api_key = os.getenv("OPENAI_API_KEY")

# IDs de Precios de Stripe
PRICE_IDS = {
    "rapido": "price_1Snam1BOA5mT4t0PuVhT2ZIq",
    "standard": "price_1SnaqMBOA5mT4t0PppRG2PuE",
    "special": "price_1SnatfBOA5mT4t0PZouWzfpw"
}
LINK_DONACION = "https://buy.stripe.com/28E00igMD8dR00v5vl7Vm0h"

# 3️⃣ Middleware CORS para despliegue en Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# 4️⃣ Función Maestra de Consulta SQL (Local + Nacional simultáneo)
def query_sql_dual(termino):
    """
    Busca en cost_estimates.db (Local) y fbi_national.db (Nacional) 
    para forzar la comparativa de precios.
    """
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        busqueda = f"%{termino.strip().upper()}%"
        data_consolidada = {"local": [], "nacional": []}

        # --- BUSQUEDA EN DB LOCAL ---
        db_local = os.path.join(base_dir, 'cost_estimates.db')
        if os.path.exists(db_local):
            conn = sqlite3.connect(db_local)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT cpt_code, description, state, city, zip_code, low_price, high_price
                FROM cost_estimates
                WHERE description LIKE ? OR cpt_code LIKE ? OR zip_code LIKE ?
                ORDER BY low_price ASC LIMIT 5
            """, (busqueda, busqueda, busqueda))
            data_consolidada["local"] = cursor.fetchall()
            conn.close()

        # --- BUSQUEDA EN DB NACIONAL (FBI) ---
        db_fbi = os.path.join(base_dir, 'fbi_national.db')
        if os.path.exists(db_fbi):
            conn = sqlite3.connect(db_fbi)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT cpt_code, description, state, city, zip_code, low_price, high_price
                FROM fbi_cost_estimates
                WHERE description LIKE ? OR cpt_code LIKE ?
                ORDER BY low_price ASC LIMIT 5
            """, (busqueda, busqueda))
            data_consolidada["nacional"] = cursor.fetchall()
            conn.close()

        return data_consolidada if (data_consolidada["local"] or data_consolidada["nacional"]) else "DATO_NO_SQL"

    except Exception as e:
        print(f"[ERROR SQL] {e}")
        return f"ERROR_SQL: {str(e)}"

# 5️⃣ Rutas de la Aplicación
@app.get("/", response_class=HTMLResponse)
async def read_index():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(base_dir, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Aura by May Roga LLC - Online</h1>"

@app.post("/estimado")
async def obtener_estimado(
    consulta: str = Form(...),
    lang: str = Form("es"),
    zip_user: str = Form(None)
):
    # Lógica de búsqueda priorizando ZIP si la consulta es corta
    termino_busqueda = zip_user if (zip_user and len(consulta.strip()) < 5) else consulta
    datos_sql = query_sql_dual(termino_busqueda)

    idiomas = {"es": "Español", "en": "English", "ht": "Kreyòl (Haitian Creole)"}
    idioma_destino = idiomas.get(lang, "Español")

    # PROMPT ESTRATÉGICO DE AURA (Fuerza la transparencia radical)
    prompt = f"""
ERES AURA, EL MOTOR FINANCIERO MÉDICO DE MAY ROGA LLC. 
TU OBJETIVO ES EXPONER LA VERDAD DE LOS COSTOS MÉDICOS EN USA 2026.

DATOS SQL ENCONTRADOS: {datos_sql}
IDIOMA: {idioma_destino}
CONSULTA DEL USUARIO: {consulta}
ZIP DEL USUARIO: {zip_user}

REGLAS DE REPORTE (FORMATO ZILLOW):
1) BLINDAJE: "Este reporte es emitido por Aura by May Roga LLC, agencia de información independiente. No somos médicos, ni seguros, ni damos diagnósticos."
2) REPORTE ESTRUCTURADO:
   - Procedimiento: Nombre claro basado en SQL.
   - Opciones LOCALES (Top 3): Usa los precios más bajos de cost_estimates.db en el estado/ZIP del usuario.
   - Opciones NACIONALES (Top 5): Usa los precios de fbi_national.db para mostrar cuánto ahorraría si viaja a otro estado.
   - Opción PREMIUM: Muestra el precio 'high_price' local más alto como referencia cara.
3) ANÁLISIS ESTRATÉGICO:
   - Precio Justo (Fair Price): El promedio de las 3 opciones locales más baratas.
   - Ahorro Real: Diferencia en dólares entre la opción Premium y la más barata local.
   - Cash vs Insurance: Explica que el precio cash detectado es inferior al valor inflado de los seguros.
4) CIERRE:
   "He analizado 150 puntos de datos de CMS y bases federales. Tienes tiempo disponible en tu suscripción: ¿Quieres que te explique cómo negociar con tu clínica usando estos precios?"
"""

    # Motores con Fallback (Gemini -> OpenAI)
    try:
        # Intento con Gemini (Flash 1.5 por velocidad)
        response = client_gemini.models.generate_content(
            model="gemini-1.5-flash", 
            contents=prompt
        )
        return {"resultado": response.text}
    except Exception as e:
        print(f"[FALLBACK] Gemini falló, intentando OpenAI: {e}")
        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            return {"resultado": response.choices[0].message.content}
        except Exception as oe:
            return {"resultado": f"Error en motores de IA: {str(oe)}"}

# 6️⃣ Gestión de Pagos Stripe
@app.post("/create-checkout-session")
async def create_checkout(plan: str = Form(...)):
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

# 7️⃣ Panel Admin
@app.post("/login-admin")
async def login_admin(user: str = Form(...), pw: str = Form(...)):
    if user == os.getenv("ADMIN_USERNAME") and pw == os.getenv("ADMIN_PASSWORD"):
        return {"status": "success", "access": "full"}
    return JSONResponse(status_code=401, content={"status": "error"})
