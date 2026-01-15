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

# 4️⃣ Función para consultar SQL actualizada con respaldo FBI
def query_sql(termino):
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        resultados = []
        busqueda = f"%{termino.strip().upper()}%"

        # 1️⃣ Buscar en DB local
        db_local = os.path.join(base_dir, 'cost_estimates.db')
        if os.path.exists(db_local):
            conn = sqlite3.connect(db_local)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT cpt_code, description, state, zip_code, low_price, high_price
                FROM cost_estimates
                WHERE description LIKE ? OR cpt_code LIKE ? OR zip_code LIKE ? OR state LIKE ?
                ORDER BY low_price ASC
                LIMIT 5
            """, (busqueda, busqueda, busqueda, busqueda))
            resultados = cursor.fetchall()
            conn.close()
            if resultados:
                return resultados  # si hay resultados locales, ya los devolvemos

        # 2️⃣ Buscar en DB nacional del FBI si local no tiene
        db_fbi = os.path.join(base_dir, 'fbi_national.db')
        if os.path.exists(db_fbi):
            conn = sqlite3.connect(db_fbi)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT cpt_code, description, state, zip_code, low_price, high_price
                FROM fbi_cost_estimates
                WHERE description LIKE ? OR cpt_code LIKE ?
                ORDER BY low_price ASC
                LIMIT 5
            """, (busqueda, busqueda))
            resultados_nacional = cursor.fetchall()
            conn.close()
            if resultados_nacional:
                return resultados_nacional

        return "DATO_NO_SQL"  # si no hay en ninguna DB

    except Exception as e:
        print(f"[ERROR SQL] {e}")
        return f"ERROR_SQL: {str(e)}"

# 5️⃣ Ruta principal (index.html)
@app.get("/", response_class=HTMLResponse)
async def read_index():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_dir, "index.html"), "r", encoding="utf-8") as f:
        return f.read()

# 6️⃣ Obtener estimado con análisis estratégico completo
@app.post("/estimado")
async def obtener_estimado(
    consulta: str = Form(...),
    lang: str = Form("es"),
    zip_user: str = Form(None)
):
    # Determinar término final para SQL
    termino_final = zip_user if (zip_user and len(consulta.strip()) < 5) else consulta
    datos_sql = query_sql(termino_final)

    idiomas = {"es": "Español", "en": "English", "ht": "Kreyòl (Haitian Creole)"}
    idioma_destino = idiomas.get(lang, "Español")

    # Prompt base para IA
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
       * Condado + ZIP:
       * Opciones locales más baratas (Top 3):
       * Opciones nacionales más baratas (Top 5):
       * Opción premium/cara:
       * Comparación cash price vs insurance:
       * Notas clínicas:
       * Precio Justo (Fair Price):
       * Ahorro Real vs Premium:
       * Diagnóstico de Mercado:
       * Cálculo de Eficiencia:
4) ACTIVACIÓN CONSULTA DE DUDAS:
   "He analizado 150 puntos de datos para este presupuesto. Tienes tiempo disponible en tu suscripción: 
    ¿Quieres que te explique cómo usar estos precios para negociar con tu clínica o por qué la opción de otro estado es más barata?"
5) CIERRE:
   "Estos son estimados de mercado basados en datos SQL locales e inteligencia comparativa nacional. Aura by Maroga LLC no es un proveedor médico ni aseguradora; somos tu radar de transparencia financiera en salud. No damos consejos médicos, damos poder de ahorro."
"""

    # ⚡ Fallback automático usando motores disponibles
    motores = []

    # 1️⃣ Gemini
    try:
        modelos_gemini = client_gemini.models.list().data
        if modelos_gemini:
            motores.append(("gemini", modelos_gemini[0].name))
    except Exception as e:
        print(f"[ERROR GEMINI LIST] {e}")

    # 2️⃣ OpenAI
    try:
        motores.append(("openai", "gpt-4"))
    except Exception as e:
        print(f"[ERROR OPENAI LIST] {e}")

    # 3️⃣ Intento de fallback en orden
    for motor, modelo in motores:
        try:
            if motor == "gemini":
                response = client_gemini.models.generate_content(model=modelo, contents=prompt)
                return {"resultado": response.text}
            elif motor == "openai":
                response = openai.chat.completions.create(
                    model=modelo,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5,
                )
                return {"resultado": response.choices[0].message.content}
        except Exception as e:
            print(f"[ERROR {motor.upper()} con modelo {modelo}] {e}, intentando siguiente motor...")

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
# 9️⃣ Función para poblar la DB con dentist_codes.py
def populate_dentist_codes():
    import dentist_codes  # nuestro módulo con todos los códigos

    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_local = os.path.join(base_dir, 'cost_estimates.db')
    conn = sqlite3.connect(db_local)
    cursor = conn.cursor()

    # Crear tabla si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cost_estimates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpt_code TEXT,
            description TEXT,
            state TEXT,
            zip_code TEXT,
            low_price REAL,
            high_price REAL
        )
    """)

    # Insertar códigos
    for code in dentist_codes.dentist_codes:
        cursor.execute("""
            INSERT INTO cost_estimates (cpt_code, description, state, zip_code, low_price, high_price)
            VALUES (?, ?, ?, ?, ?, ?)
        """, code)

    conn.commit()
    conn.close()
    print("[INFO] Base de datos poblada con códigos de odontología.")

# ⚡ Llamada automática al iniciar main.py (opcional, solo si quieres poblar al inicio)
# populate_dentist_codes()
