import os
import sqlite3
import stripe
from datetime import datetime
from fastapi import FastAPI, Form, Depends, HTTPException, status
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import openai
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="Aura by May Roga LLC")

# Configuración Dual IA
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
openai.api_key = os.getenv("OPENAI_API_KEY")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Credenciales ocultas de Render para el Dueño
ADMIN_USER = os.getenv("ADMIN_USERNAME")
ADMIN_PASS = os.getenv("ADMIN_PASSWORD")

# Los 3 Precios Acordados vinculados a tus IDs de Stripe
PRICE_IDS = {
    "rapido": "price_1Snam1BOA5mT4t0PuVhT2ZIq",   # $5.99
    "standard": "price_1SnaqMBOA5mT4t0PppRG2PuE", # $9.99
    "special": "price_1SnatfBOA5mT4t0PZouWzfpw"   # $19.99
}

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

def init_db():
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    if os.path.exists('cost_estimates.sql'):
        with open('cost_estimates.sql', 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
    return conn

db_conn = init_db()

def dual_ia_expert(query, zip_code):
    """Función de respaldo: Si Gemini falla, entra OpenAI"""
    prompt = f"Estimate US healthcare cost for '{query}' in ZIP {zip_code}. Provide a range based on CPT/CDT. Format: 'Estimated Range: $X - $Y'."
    try:
        model = genai.GenerativeModel('gemini-pro')
        return model.generate_content(prompt).text
    except:
        try:
            res = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
            return res.choices[0].message.content
        except:
            return "Información técnica en proceso. Intente en unos minutos."

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/login-owner")
async def login_owner(username: str = Form(...), password: str = Form(...)):
    if username == ADMIN_USER and password == ADMIN_PASS:
        return {"status": "success", "message": "Bienvenida, May Roga LLC"}
    raise HTTPException(status_code=401, detail="No autorizado")

@app.post("/estimado")
async def obtener_estimado(
    zip_code: str = Form(...), 
    consulta: str = Form(...), 
    plan_type: str = Form(...),
    is_admin: str = Form("false")
):
    # Lógica de tiempos basada en el plan seleccionado
    dia = datetime.now().day
    if is_admin == "true": 
        tiempo = "Acceso Ilimitado (Dueño)"
    elif plan_type == "rapido": tiempo = "7 minutos"
    elif plan_type == "standard": tiempo = "15 minutos"
    elif plan_type == "special": tiempo = "35 min" if dia <= 2 else "6 min"
    else: tiempo = "Consulta de cortesía"

    cursor = db_conn.cursor()
    # 1. Buscar en el Storage
    sql = "SELECT * FROM cost_estimates WHERE (description LIKE ? OR cpt_code = ?) AND zip_code = ? LIMIT 1"
    cursor.execute(sql, (f'%{consulta}%', consulta.upper(), zip_code))
    row = cursor.fetchone()

    if row:
        resultado = f"Servicio Identificado: {row[2]} (Código {row[1]}) - Rango Estimado: ${row[5]} - ${row[6]}"
        fuente = "Storage Interno Aura"
    else:
        # 2. Si no está en storage, usar Dual IA
        resultado = dual_ia_expert(consulta, zip_code)
        fuente = "Dual IA (Real-Time)"

    return {
        "estimado": f"{resultado}<br><small>Tiempo de acceso concedido: {tiempo}</small>",
        "fuente": fuente,
        "empresa": "May Roga LLC"
    }

@app.post("/create-checkout-session")
async def pay(plan: str = Form(...)):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": PRICE_IDS[plan.lower()], "quantity": 1}],
            mode="subscription" if plan.lower() == "special" else "payment",
            success_url="https://aura-iyxa.onrender.com/?success=true",
            cancel_url="https://aura-iyxa.onrender.com/?cancel=true"
        )
        return {"url": session.url}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
