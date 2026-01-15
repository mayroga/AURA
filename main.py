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

# ==============================
# 1️⃣ Configuración Stripe y motores IA
# ==============================
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
client_gemini = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
openai.api_key = os.getenv("OPENAI_API_KEY")

# ==============================
# 2️⃣ Precios y enlace de donación
# ==============================
PRICE_IDS = {
    "rapido": "price_1Snam1BOA5mT4t0PuVhT2ZIq",
    "standard": "price_1SnaqMBOA5mT4t0PppRG2PuE",
    "special": "price_1SnatfBOA5mT4t0PZouWzfpw"
}
LINK_DONACION = "https://buy.stripe.com/28E00igMD8dR00v5vl7Vm0h"

# ==============================
# 3️⃣ Middleware CORS
# ==============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ==============================
# 4️⃣ Función para consultar SQL
# ==============================
def query_sql(termino):
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, 'cost_estimates.db')
        if not os.path.exists(db_path):
            return "SQL_OFFLINE"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        query = """
        SELECT cpt_code, procedure_name, state, zip_code, low_price, high_price, low_price_ins, high_price_ins, notes
        FROM cost_estimates
        WHERE procedure_name LIKE ? OR cpt_code LIKE ? OR zip_code LIKE ? OR state LIKE ?
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

# ==============================
# 5️⃣ Ruta principal (index.html)
# ==============================
@app.get("/", response_class=HTMLResponse)
async def read_index():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_dir, "index.html"), "r", encoding="utf-8") as f:
        return f.read()

# ==============================
# 6️⃣ Cálculo Fair Price matemático + validación legal
# ==============================
def calcular_fair_price(datos_sql):
    """
    Calcula el Fair Price matemáticamente:
    Fórmula simple auditada:
    FP = (promedio_low + promedio_high)/2 ajustado por insurance coverage
    """
    if not datos_sql or datos_sql in ["SQL_OFFLINE", "DATO_NO_SQL"]:
        return None

    total_low = total_high = total_ins_low = total_ins_high = 0
    count = 0

    for fila in datos_sql:
        _, _, _, _, low, high, ins_low, ins_high, _ = fila
        total_low += low
        total_high += high
        total_ins_low += ins_low
        total_ins_high += ins_high
        count += 1

    if count == 0:
        return None

    avg_low = total_low / count
    avg_high = total_high / count
    avg_ins_low = total_ins_low / count
    avg_ins_high = total_ins_high / count

    # Cálculo Fair Price: promedio mercado + ajuste seguro
    fair_price = round((avg_low + avg_high + avg_ins_low + avg_ins_high)/4, 2)
    return fair_price

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

    # ==============================
    # Calcular Fair Price matemáticamente
    # ==============================
    fair_price = calcular_fair_price(datos_sql)
    fair_price_txt = f"${fair_price}" if fair_price else "Estimado no disponible"

    # ==============================
    # Prompt legal para IA fallback (solo si SQL falla)
    # ==============================
    prompt = f"""
ERES AURA, MOTOR FINANCIERO MÉDICO DE MAY ROGA LLC.
SOLO PROPORCIONAS ESTIMADOS DE MERCADO, NUNCA DIAGNÓSTICOS NI RECOMENDACIONES MÉDICAS.
IDIOMA: {idioma_destino}
DATOS SQL ENCONTRADOS: {datos_sql}
CONSULTA ORIGINAL: {consulta}
ZIP DETECTADO: {zip_user}

────────────────────────────────────
BLINDAJE LEGAL:
"Este reporte es emitido por Aura by May Roga LLC, agencia de información independiente.
No somos médicos ni aseguradoras. Toda información es financiera y de mercado únicamente."
────────────────────────────────────
Fair Price calculado matemáticamente: {fair_price_txt}
────────────────────────────────────
"""

    # ⚡ Fallback IA solo si SQL falla
    if datos_sql in ["SQL_OFFLINE", "DATO_NO_SQL"]:
        motores = []
        try:
            modelos_gemini = client_gemini.models.list().data
            if modelos_gemini:
                motores.append(("gemini", modelos_gemini[0].name))
        except: pass
        try:
            motores.append(("openai", "gpt-4"))
        except: pass

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
            except: pass

        return {"resultado": "Estimado generado sin datos exactos SQL, Fair Price no disponible."}

    # ==============================
    # Construir reporte final
    # ==============================
    reporte = f"""
⚠️ BLINDAJE LEGAL:
Este reporte es emitido por Aura by May Roga LLC, agencia de información independiente.
No somos médicos ni aseguradoras. Información financiera de mercado únicamente.

💰 FAIR PRICE CALCULADO: {fair_price_txt}

📝 Opciones locales y nacionales encontradas (Top 5):
{datos_sql}

Este estimado es solo referencial y auditado, basado en precios reales de la base de datos CMS / PFS.
"""

    return {"resultado": reporte}

# ==============================
# 7️⃣ Crear sesión de pago
# ==============================
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

# ==============================
# 8️⃣ Login admin / acceso gratuito
# ==============================
@app.post("/login-admin")
async def login_admin(user: str = Form(...), pw: str = Form(...)):
    ADMIN_USER = os.getenv("ADMIN_USERNAME", "TU_USERNAME")
    ADMIN_PASS = os.getenv("ADMIN_PASSWORD", "TU_PASSWORD")
    if user == ADMIN_USER and pw == ADMIN_PASS:
        return {"status": "success", "access": "full"}
    return JSONResponse(status_code=401, content={"status": "error"})
