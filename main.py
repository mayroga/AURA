import os
import sqlite3
import stripe
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# ==============================
# STRIPE
# ==============================
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")  # desde Render

PRICE_IDS = {
    "rapido": "price_1Snam1BOA5mT4t0PuVhT2ZIq",
    "standard": "price_1SnaqMBOA5mT4t0PppRG2PuE",
    "special": "price_1SnatfBOA5mT4t0PZouWzfpw"
}
LINK_DONACION = "https://buy.stripe.com/28E00igMD8dR00v5vl7Vm0h"

# ==============================
# CORS
# ==============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ==============================
# FUNCIONES SQL
# ==============================
def query_sql(termino):
    try:
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cost_estimates.db')
        if not os.path.exists(db_path):
            return "SQL_OFFLINE"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        query = """
        SELECT cpt_code, procedure_name, state, county, zip_code, low_price, high_price, low_price_ins, high_price_ins, notes
        FROM cost_estimates
        WHERE procedure_name LIKE ? OR cpt_code LIKE ? OR zip_code LIKE ? OR state LIKE ?
        ORDER BY low_price ASC
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
# RUTA PRINCIPAL
# ==============================
@app.get("/", response_class=HTMLResponse)
async def read_index():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_dir, "index.html"), "r", encoding="utf-8") as f:
        return f.read()

# ==============================
# OBTENER ESTIMADO
# ==============================
@app.post("/estimado")
async def obtener_estimado(
    consulta: str = Form(...),
    lang: str = Form("es"),
    zip_user: str = Form(None)
):
    termino_final = zip_user if (zip_user and len(consulta.strip()) < 5) else consulta
    datos_sql = query_sql(termino_final)

    idioma_map = {"es": "Español", "en": "English", "ht": "Kreyòl (Haitian Creole)"}
    idioma_destino = idioma_map.get(lang, "Español")

    # ==============================
    # Reporte básico con SQL
    # ==============================
    if datos_sql in ["SQL_OFFLINE", "DATO_NO_SQL"]:
        return {"resultado": f"⚠ No se encontraron datos locales. Intentar otra búsqueda o usar Google Maps opcional."}

    resultado = f"🔹 ESTIMADO DE MERCADO ({idioma_destino})\n"
    for r in datos_sql[:10]:  # mostrar max 10 resultados
        cpt, proc, state, county, zip_code, low, high, low_ins, high_ins, notes = r
        resultado += (
            f"\nProcedimiento: {proc}\nCPT: {cpt}\nUbicación: {state}, {county}\nZIP: {zip_code}\n"
            f"Precio Cash: ${low} - ${high}\nPrecio Insurance: ${low_ins} - ${high_ins}\nNotas: {notes}\n"
        )

    # ==============================
    # Google Maps opcional
    # ==============================
    if zip_user:
        resultado += f"\n📍 Ver en Google Maps: https://www.google.com/maps/search/?api=1&query={zip_user}"

    return {"resultado": resultado}

# ==============================
# CREAR CHECKOUT STRIPE
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
# LOGIN ADMIN / ACCESO GRATUITO
# ==============================
@app.post("/login-admin")
async def login_admin(user: str = Form(...), pw: str = Form(...)):
    ADMIN_USER = os.getenv("ADMIN_USERNAME", "TU_USERNAME")
    ADMIN_PASS = os.getenv("ADMIN_PASSWORD", "TU_PASSWORD")
    if user == ADMIN_USER and pw == ADMIN_PASS:
        return {"status": "success", "access": "full"}
    return JSONResponse(status_code=401, content={"status": "error"})
