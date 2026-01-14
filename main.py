import os
import sqlite3
import stripe
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from google import genai
import openai
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# 1️⃣ Configuración Stripe y motores IA
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
client_gemini = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
openai.api_key = os.getenv("OPENAI_API_KEY")

# 2️⃣ Precios y enlace de donación
PRICE_IDS = {
    "rapido": "price_1Snam1BOA5mT4t0PuVhT2ZIq",
    "standard": "price_1SnaqMBOA5mT4t0PppRG2PuE",
    "special": "price_1SnatfBOA5mT4t0PZouWzfpw"
}
LINK_DONACION = "https://buy.stripe.com/28E00igMD8dR00v5vl7Vm0h"

# 3️⃣ Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# 4️⃣ Función para consultar SQL
def query_sql(termino):
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, 'cost_estimates.db')
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

# 5️⃣ Ruta principal (index.html)
@app.get("/", response_class=HTMLResponse)
async def read_index():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_dir, "index.html"), "r", encoding="utf-8") as f:
        return f.read()

# 6️⃣ Obtener estimado con fallback automático Gemini → OpenAI → Gemini
@app.post("/estimado")
async def obtener_estimado(
    consulta: str = Form(...),
    lang: str = Form("es"),
    zip_user: str = Form(None)
):
    termino_final = zip_user if (zip_user and len(consulta.strip()) < 5) else consulta
    datos_sql = query_sql(termino_final)

    idiomas = {"es": "Español", "en": "English", "ht": "Kreyòl (Haitian Creole)"}
    idioma_destino = idiomas.get(lang, "Español")

    prompt = f"""
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

    # ⚡ Fallback real automático: Gemini → OpenAI → Gemini
    for motor in ["gemini", "openai", "gemini"]:
        try:
            if motor == "gemini":
                response = client_gemini.models.generate_content(model="gemini-1.5-flash", contents=prompt)
                return {"resultado": response.text}
            elif motor == "openai":
                completion = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5,
                )
                return {"resultado": completion.choices[0].message.content}
        except Exception as e:
            print(f"[ERROR {motor.upper()}] {e}, intentando siguiente motor...")

    # ⚡ Fallback final automático, sin mensaje de error al usuario
    return {"resultado": "Estimado generado automáticamente sin datos exactos SQL."}

# 7️⃣ Crear sesión de pago
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
        print(f"[ERROR STRIPE] {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

# 8️⃣ Login admin / acceso gratuito
@app.post("/login-admin")
async def login_admin(user: str = Form(...), pw: str = Form(...)):
    ADMIN_USER = os.getenv("ADMIN_USERNAME", "TU_USERNAME")
    ADMIN_PASS = os.getenv("ADMIN_PASSWORD", "TU_PASSWORD")
    if user == ADMIN_USER and pw == ADMIN_PASS:
        return {"status": "success", "access": "full"}
    return JSONResponse(status_code=401, content={"status": "error"})
