import os
import sqlite3
import stripe
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from google import genai
import openai
from dotenv import load_dotenv
import urllib.parse

# ===============================
# CARGA DE ENTORNO
# ===============================
load_dotenv()
app = FastAPI()

# ===============================
# STRIPE & IA
# ===============================
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
client_gemini = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
openai.api_key = os.getenv("OPENAI_API_KEY")

PRICE_IDS = {
    "rapido": "price_1Snam1BOA5mT4t0PuVhT2ZIq",
    "standard": "price_1SnaqMBOA5mT4t0PppRG2PuE",
    "special": "price_1SnatfBOA5mT4t0PZouWzfpw"
}

LINK_DONACION = "https://buy.stripe.com/28E00igMD8dR00v5vl7Vm0h"

# ===============================
# CORS (RENDER SAFE)
# ===============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ===============================
# SQL DUAL: LOCAL + NACIONAL
# ===============================
def query_sql_dual(termino: str):
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        busqueda = f"%{termino.strip().upper()}%"
        data = {"local": [], "nacional": []}

        # ----- LOCAL -----
        db_local = os.path.join(base_dir, "cost_estimates.db")
        if os.path.exists(db_local):
            conn = sqlite3.connect(db_local)
            cur = conn.cursor()
            cur.execute("""
                SELECT cpt_code, description, state, city, zip_code, low_price, high_price
                FROM cost_estimates
                WHERE description LIKE ? OR cpt_code LIKE ? OR zip_code LIKE ?
                ORDER BY low_price ASC LIMIT 5
            """, (busqueda, busqueda, busqueda))
            data["local"] = cur.fetchall()
            conn.close()

        # ----- NACIONAL -----
        db_nat = os.path.join(base_dir, "fbi_national.db")
        if os.path.exists(db_nat):
            conn = sqlite3.connect(db_nat)
            cur = conn.cursor()
            cur.execute("""
                SELECT cpt_code, description, state, city, zip_code, low_price, high_price
                FROM fbi_cost_estimates
                WHERE description LIKE ? OR cpt_code LIKE ?
                ORDER BY low_price ASC LIMIT 5
            """, (busqueda, busqueda))
            data["nacional"] = cur.fetchall()
            conn.close()

        return data if data["local"] or data["nacional"] else "NO_SQL_DATA"

    except Exception as e:
        return f"SQL_ERROR: {str(e)}"

# ===============================
# GOOGLE MAPS (LEGAL SAFE)
# ===============================
def google_maps_links(query: str, zip_user: str = None):
    base = "https://www.google.com/maps/search/"
    local_q = f"{query} {zip_user}" if zip_user else f"{query} near me"
    national_q = f"{query} USA"

    return {
        "local_maps": base + urllib.parse.quote(local_q),
        "national_maps": base + urllib.parse.quote(national_q)
    }

# ===============================
# INDEX
# ===============================
@app.get("/", response_class=HTMLResponse)
async def index():
    path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>AURA by May Roga LLC</h1>"

# ===============================
# ESTIMADOR AURA
# ===============================
@app.post("/estimado")
async def estimado(
    consulta: str = Form(...),
    lang: str = Form("es"),
    zip_user: str = Form(None)
):
    termino = zip_user if zip_user and len(consulta.strip()) < 5 else consulta
    datos = query_sql_dual(termino)
    maps = google_maps_links(consulta, zip_user)

    idiomas = {"es": "Español", "en": "English", "ht": "Haitian Creole"}
    idioma = idiomas.get(lang, "Español")

    prompt = f"""
ERES AURA, SISTEMA DE INTELIGENCIA FINANCIERA MÉDICA.
OPERAS COMO AGENCIA INFORMATIVA INDEPENDIENTE.

IDIOMA: {idioma}
CONSULTA: {consulta}
ZIP USUARIO: {zip_user}

DATOS SQL:
{datos}

REGLAS LEGALES:
- No diagnóstico
- No recomendaciones médicas
- Datos públicos y federales
- Uso educativo e informativo

FORMATO:
1️⃣ BLINDAJE LEGAL CLARO
2️⃣ OPCIONES LOCALES (Top 3)
3️⃣ OPCIONES NACIONALES (Top 5)
4️⃣ PRECIO JUSTO
5️⃣ AHORRO REAL
6️⃣ CASH VS SEGURO
7️⃣ MENSAJE FINAL DE NEGOCIACIÓN
"""

    try:
        r = client_gemini.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        texto = r.text
    except Exception:
        r = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        texto = r.choices[0].message.content

    texto += f"""

🔗 VER OPCIONES REALES EN GOOGLE MAPS
Locales: {maps['local_maps']}
Nacionales: {maps['national_maps']}

⚠️ AURA NO CONTROLA NI MODIFICA DATOS DE GOOGLE MAPS.
"""

    return {"resultado": texto}

# ===============================
# STRIPE
# ===============================
@app.post("/create-checkout-session")
async def checkout(plan: str = Form(...)):
    if plan == "donacion":
        return {"url": LINK_DONACION}
    try:
        mode = "subscription" if plan == "special" else "payment"
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": PRICE_IDS[plan], "quantity": 1}],
            mode=mode,
            success_url="https://aura-iyxa.onrender.com/?success=true",
            cancel_url="https://aura-iyxa.onrender.com/"
        )
        return {"url": session.url}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# ===============================
# ADMIN
# ===============================
@app.post("/login-admin")
async def login_admin(user: str = Form(...), pw: str = Form(...)):
    if user == os.getenv("ADMIN_USERNAME") and pw == os.getenv("ADMIN_PASSWORD"):
        return {"status": "success"}
    return JSONResponse(status_code=401, content={"status": "denied"})
