import os
import sqlite3
import stripe
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

try:
    from google import genai  # Gemini 2.5
except:
    genai = None

import openai

load_dotenv()
app = FastAPI()

# ---------------------------
# Configuración claves
# ---------------------------
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client_gemini = genai.Client(api_key=os.getenv("GEMINI_API_KEY")) if genai else None

PRICE_IDS = {
    "rapido": "price_1Snam1BOA5mT4t0PuVhT2ZIq",
    "standard": "price_1SnaqMBOA5mT4t0PppRG2PuE",
    "special": "price_1SnatfBOA5mT4t0PZouWzfpw"
}

LINK_DONACION = "https://buy.stripe.com/28E00igMD8dR00v5vl7Vm0h"

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ---------------------------
# Función SQL
# ---------------------------
def query_sql(termino):
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, "aura_data.db")
        if not os.path.exists(db_path):
            return "SQL_OFFLINE"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        query = """
        SELECT cpt_code, icd_code, state, zip_code, low_price, high_price
        FROM cost_estimates
        WHERE description LIKE ? OR cpt_code LIKE ? OR zip_code LIKE ? OR state LIKE ?
        ORDER BY low_price ASC
        LIMIT 10
        """
        busqueda = f"%{termino.strip().upper()}%"
        cursor.execute(query, (busqueda, busqueda, busqueda, busqueda))
        results = cursor.fetchall()
        conn.close()
        return results if results else "DATO_NO_SQL"
    except Exception as e:
        print(f"[ERROR SQL] {e}")
        return f"ERROR_SQL: {str(e)}"

# ---------------------------
# Página principal
# ---------------------------
@app.get("/", response_class=HTMLResponse)
async def read_index():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_dir, "index.html"), "r", encoding="utf-8") as f:
        return f.read()

# ---------------------------
# Estimado de precios
# ---------------------------
@app.post("/estimado")
async def obtener_estimado(consulta: str = Form(...), lang: str = Form("es"), zip_user: str = Form(None)):
    termino_final = zip_user if (zip_user and len(consulta.strip()) < 5) else consulta
    datos_sql = query_sql(termino_final)
    
    prompt = f"""
Aura by MY ROGA LLC, a medical price intelligence system.
Do NOT provide medical advice, diagnosis, treatment or insurance guidance.
Only provide estimated market price ranges for medical and dental services in the USA.

Task:
1) Interpret user input (procedure, symptom, CPT, ICD-10, location)
2) If CPT/ICD missing, infer most likely
3) Use SQL price data: {datos_sql}
4) If no SQL data, return national estimated market range

Output:
- First give a simple human explanation
- Then structured financial info:
Procedure:
CPT or ICD:
Location:
Market Price Range:
Estimated Fair Price:
Typical Overcharge:
Legal disclaimer: Prices may vary by provider. These are market estimates, not medical or insurance advice.
"""
    # ---------------------------
    # Intentar Gemini 2.5
    # ---------------------------
    if client_gemini:
        try:
            response = client_gemini.responses.create(
                model="gemini-2.5",
                input=prompt,
                temperature=0.3,
                max_output_tokens=700
            )
            resultado = response.output_text or "Aura está procesando su solicitud. Intente nuevamente."
            return {"resultado": resultado}
        except Exception as e:
            print(f"[ERROR GEMINI] {e}")
    
    # ---------------------------
    # Fallback OpenAI
    # ---------------------------
    try:
        import openai
        openai.api_key = OPENAI_API_KEY
        resp = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=700
        )
        return {"resultado": resp.choices[0].message.content}
    except Exception as e:
        print(f"[ERROR OPENAI] {e}")
        return {"resultado": "Aura está procesando su solicitud. Intente nuevamente."}

# ---------------------------
# Crear sesión de pago
# ---------------------------
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

# ---------------------------
# Login Admin
# ---------------------------
@app.post("/login-admin")
async def login_admin(user: str = Form(...), pw: str = Form(...)):
    if user == os.getenv("ADMIN_USERNAME") and pw == os.getenv("ADMIN_PASSWORD"):
        return {"status": "success"}
    return JSONResponse(status_code=401, content={"status": "error"})
