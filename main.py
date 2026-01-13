import os
import sqlite3
import stripe
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import openai
from google import genai  # Gemini 2.5

load_dotenv()
app = FastAPI()

# ===== CONFIGURACIONES =====
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
client_gemini = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
openai.api_key = os.getenv("OPENAI_API_KEY")

PRICE_IDS = {
    "rapido": "price_1Snam1BOA5mT4t0PuVhT2ZIq",
    "standard": "price_1SnaqMBOA5mT4t0PppRG2PuE",
    "special": "price_1SnatfBOA5mT4t0PZouWzfpw"
}

LINK_DONACION = "https://buy.stripe.com/28E00igMD8dR00v5vl7Vm0h"

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ===== FUNCIONES INTERNAS =====
def query_sql(termino):
    try:
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'aura_data.db')
        if not os.path.exists(db_path):
            return "SQL_OFFLINE"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        query = """
        SELECT cpt_code, description, state, zip_code, low_price, high_price
        FROM cost_estimates
        WHERE description LIKE ? OR cpt_code LIKE ? OR zip_code LIKE ? OR state LIKE ?
        ORDER BY low_price ASC
        LIMIT 5
        """
        busqueda = f"%{termino.strip().upper()}%"
        cursor.execute(query, (busqueda, busqueda, busqueda, busqueda))
        results = cursor.fetchall()
        conn.close()
        return results if results else "DATO_NO_SQL"
    except Exception as e:
        print(f"[ERROR SQL] {e}")
        return f"ERROR_SQL: {str(e)}"

def generar_prompt(consulta, datos_sql, zip_user, lang):
    idiomas = {"es": "Español", "en": "English", "ht": "Kreyòl (Haitian Creole)"}
    idioma_destino = idiomas.get(lang, "Español")
    return f"""
ERES AURA, MOTOR FINANCIERO MÉDICO DE MAY ROGA LLC. SOLO PROPORCIONAS ESTIMADOS DE MERCADO.
IDIOMA: {idioma_destino}
DATOS SQL ENCONTRADOS: {datos_sql}
CONSULTA ORIGINAL: {consulta}
ZIP DETECTADO: {zip_user}

REGLAS:
1) Usa los datos SQL si existen.
2) Si no hay datos exactos, genera un RANGO NACIONAL ESTIMADO basado en mercado USA 2026.
3) SALIDA ESTRUCTURADA:
   - BLINDAJE: "Este reporte es emitido por Aura by May Roga LLC, agencia de información independiente. No somos médicos, ni seguros, ni damos diagnósticos."
   - REPORTE:
       * Procedimiento/Síntoma:
       * CPT o ICD (si aplica):
       * Ubicación sugerida:
       * Rango de mercado:
       * Precio justo (Ahorro):
4) CIERRE: "Los precios pueden variar por proveedor. Estos son estimados de mercado, no precios garantizados ni asesoría médica."
"""

def generar_respuesta(consulta, lang="es", zip_user=None):
    datos_sql = query_sql(zip_user if zip_user and len(consulta.strip())<5 else consulta)
    prompt = generar_prompt(consulta, datos_sql, zip_user, lang)

    # ===== 1. Intentar Gemini 2.5 =====
    try:
        response = client_gemini.responses.create(
            model="gemini-2.5",
            input=prompt,
            temperature=0.3,
            max_output_tokens=700
        )
        resultado = response.output_text
        if resultado:
            return resultado
    except Exception as e:
        print(f"[ERROR GEMINI] {e}")

    # ===== 2. Fallback a OpenAI =====
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "Eres AURA, motor financiero de salud de May Roga LLC, solo estimados de precios en USA 2026."},
                      {"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=700
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"[ERROR OPENAI] {e}")

    # ===== 3. Si todo falla, usar datos internos 2026 =====
    if datos_sql != "DATO_NO_SQL" and datos_sql != "SQL_OFFLINE":
        base = "\n".join([f"{r[1]} ({r[0]}): {r[4]}-${r[5]} en {r[2]}, ZIP {r[3]}" for r in datos_sql])
        return f"BLINDAJE: Este reporte es emitido por Aura by May Roga LLC.\nREPORTE (Datos SQL internos 2026):\n{base}\nCierre: Los precios son estimados de mercado USA 2026."
    
    return "Aura no pudo procesar su solicitud, intente nuevamente en unos segundos."

# ===== RUTAS =====
@app.get("/", response_class=HTMLResponse)
async def read_index():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_dir, "index.html"), "r", encoding="utf-8") as f:
        return f.read()

@app.post("/estimado")
async def obtener_estimado(consulta: str = Form(...), lang: str = Form("es"), zip_user: str = Form(None)):
    resultado = generar_respuesta(consulta, lang, zip_user)
    return {"resultado": resultado}

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
            success_url=os.getenv("RENDER_APP_URL") + "/?success=true",
            cancel_url=os.getenv("RENDER_APP_URL") + "/"
        )
        return {"url": session.url}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/login-admin")
async def login_admin(user: str = Form(...), pw: str = Form(...)):
    if user == os.getenv("ADMIN_USERNAME") and pw == os.getenv("ADMIN_PASSWORD"):
        return {"status": "success"}
    return JSONResponse(status_code=401, content={"status": "error"})
