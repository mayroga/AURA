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

# --- Configuración de Stripe ---
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
PRICE_IDS = {
    "rapido": os.getenv("PRICE_RAPIDO"),
    "standard": os.getenv("PRICE_STANDARD"),
    "special": os.getenv("PRICE_SPECIAL")
}
LINK_DONACION = os.getenv("LINK_DONACION")

# --- Configuración de Gemini ---
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# --- Configuración OpenAI fallback ---
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- Middleware CORS ---
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# --- Función SQL para búsqueda ---
def query_sql(term):
    try:
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'aura_data.db')
        if not os.path.exists(db_path):
            return "SQL_OFFLINE"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        term_search = f"%{term.strip().upper()}%"
        query = """
        SELECT cpt_code, icd_code, state, zip_code, low_price, high_price
        FROM cost_estimates
        WHERE description LIKE ? OR cpt_code LIKE ? OR icd_code LIKE ? OR zip_code LIKE ? OR state LIKE ?
        ORDER BY low_price ASC
        LIMIT 5
        """
        cursor.execute(query, (term_search, term_search, term_search, term_search, term_search))
        results = cursor.fetchall()
        conn.close()
        return results if results else "DATO_NO_SQL"
    except Exception as e:
        print(f"[ERROR SQL] {e}")
        return f"ERROR_SQL: {str(e)}"

# --- Index ---
@app.get("/", response_class=HTMLResponse)
async def index():
    with open(os.path.join(os.path.dirname(__file__), "index.html"), "r", encoding="utf-8") as f:
        return f.read()

# --- Estimado de precios ---
@app.post("/estimado")
async def obtener_estimado(
    consulta: str = Form(...),
    lang: str = Form("es"),
    zip_user: str = Form(None)
):
    # Determinar término a buscar
    termino_final = zip_user if (zip_user and len(consulta.strip()) < 5) else consulta
    sql_results = query_sql(termino_final)

    # Prompt blindado legalmente para Gemini / OpenAI
    idioma_destino = {"es": "Español", "en": "English", "ht": "Kreyòl (Haitian Creole)"}.get(lang, "Español")
    prompt = f"""
Aura by May Roga LLC, a medical price intelligence system.
Do NOT provide medical advice, diagnosis, treatment or insurance guidance.
Only provide estimated market price ranges for medical and dental services in the United States.

User input: {consulta}
Detected ZIP: {zip_user}
SQL results: {sql_results}
Language: {idioma_destino}

Task:
1) Interpret user input (procedure, symptom, CPT, ICD-10, location)
2) Infer CPT/ICD if missing
3) Use SQL if available
4) If no SQL data, give national market range

Output format:
First: Simple explanation for users without medical knowledge
Then: Structured financial breakdown
- Procedure:
- CPT or ICD:
- Location:
- Market Price Range:
- Estimated Fair Price:
- Typical Overcharge:
- Legal disclaimer at the end:
Always include:
"Prices may vary by provider. These are market estimates, not medical or insurance advice."
"""

    # Intentar Gemini 2.5 primero
    try:
        response = gemini_client.responses.create(
            model="gemini-2.5",
            input=prompt,
            temperature=0.3,
            max_output_tokens=700
        )
        resultado = response.output_text or "Aura está procesando su solicitud. Intente nuevamente en unos segundos."
    except Exception as e:
        print(f"[ERROR GEMINI] {e}")
        # Fallback a OpenAI
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=700
            )
            resultado = completion.choices[0].message.content
        except Exception as ex:
            print(f"[ERROR OPENAI] {ex}")
            resultado = "Aura está procesando su solicitud. Intente nuevamente en unos segundos."

    return {"resultado": resultado}

# --- Crear sesión de pago ---
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
            success_url="http://localhost:8000/?success=true",
            cancel_url="http://localhost:8000/"
        )
        return {"url": session.url}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# --- Login Admin / acceso gratuito ---
@app.post("/login-admin")
async def login_admin(user: str = Form(...), pw: str = Form(...)):
    if user == os.getenv("ADMIN_USERNAME") and pw == os.getenv("ADMIN_PASSWORD"):
        return {"status": "success", "access": "full"}
    return JSONResponse(status_code=401, content={"status": "error"})

