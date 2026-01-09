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

# Configuración Dual IA (Gemini + OpenAI)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
openai.api_key = os.getenv("OPENAI_API_KEY")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

PRICE_IDS = {
    "rapido": "price_1Snam1BOA5mT4t0PuVhT2ZIq",
    "standard": "price_1SnaqMBOA5mT4t0PppRG2PuE",
    "special": "price_1SnatfBOA5mT4t0PZouWzfpw"
}

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

def init_db():
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    try:
        if os.path.exists('cost_estimates.sql'):
            with open('cost_estimates.sql', 'r', encoding='utf-8') as f:
                conn.executescript(f.read())
            print("Storage Aura Operativo.")
    except Exception as e:
        print(f"Error Storage: {e}")
    return conn

db_conn = init_db()

def dual_ia_estimator(query, zip_code, facility):
    prompt = f"Estimate healthcare cost for '{query}' in ZIP {zip_code} ({facility}). Provide a market range (Low/High) based on CPT/CDT. Response: 'Code: [ID], Estimated Range: $X - $Y'."
    try:
        model = genai.GenerativeModel('gemini-pro')
        return model.generate_content(prompt).text
    except:
        try:
            res = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
            return res.choices[0].message.content
        except:
            return "Estimado en procesamiento..."

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/estimado")
async def obtener_estimado(zip_code: str = Form(...), consulta: str = Form(...), facility: str = Form(...), plan_type: str = Form(...)):
    cursor = db_conn.cursor()
    # Prioridad 1: Storage Interno (Datos Históricos/Públicos)
    sql = "SELECT * FROM cost_estimates WHERE (description LIKE ? OR cpt_code = ?) AND zip_code = ? LIMIT 1"
    cursor.execute(sql, (f'%{consulta}%', consulta.upper(), zip_code))
    row = cursor.fetchone()

    if row:
        low, high = row[5], row[6]
        if facility.lower() == "hospital":
            low *= 1.35; high *= 1.35 # Ajuste por complejidad hospitalaria
        resultado = f"Cód: {row[1]} | Rango Estimado: ${round(low,2)} - ${round(high,2)}"
        fuente = "Base de Datos Aura"
    else:
        # Prioridad 2: Dual IA Experta
        resultado = dual_ia_estimator(consulta, zip_code, facility)
        fuente = "Inteligencia de Mercado Real-Time"

    return {
        "empresa": "Aura by May Roga LLC",
        "estimado": resultado,
        "fuente": fuente,
        "mensaje": "Usa este estimado para comparar proveedores y elegir la opción más económica."
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
