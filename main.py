# main.py
import os
import time
from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from datetime import datetime
import stripe
import httpx
import openai
import asyncio

# -------------------------------
# VARIABLES DE ENTORNO
# -------------------------------
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
DATABASE_URI = os.environ.get("DATABASE_URI")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")

# -------------------------------
# CONFIGURACIÓN
# -------------------------------
stripe.api_key = STRIPE_SECRET_KEY
app = FastAPI(title="Asesor de Costos AURA by May Roga LLC")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# DB SIMPLIFICADA
# -------------------------------
cost_estimates_db = {}
usage_tokens_db = {}

# -------------------------------
# PLANES Y TIEMPO DE USO
# -------------------------------
PLANES = {
    "trial": {"precio": 1.99, "tiempo_seg": 40, "consultas": 1},
    "basic": {"precio": 7.99, "tiempo_seg": 2400, "consultas": 5},       # 40 min
    "special": {"precio": 14.99, "tiempo_seg": 3600, "consultas": 10},   # 1 hora
    "subscription": {"precio": 8.99, "tiempo_seg": 3600, "consultas": 10},  # 1 hora/día
    "loyalty": {"precio": 0.99, "tiempo_seg": 2400, "consultas": 5},
}

# -------------------------------
# PRICE_ID DE STRIPE (CAMBIAR AQUÍ)
# -------------------------------
PRICE_IDS = {
    "trial": "price_XXXXXXXXXXXX",
    "basic": "price_XXXXXXXXXXXX",
    "special": "price_XXXXXXXXXXXX",
    "subscription": "price_XXXXXXXXXXXX",
    "loyalty": "price_XXXXXXXXXXXX",
}

# -------------------------------
# DETECCIÓN DE IDIOMA
# -------------------------------
def detectar_idioma(texto):
    texto = texto.lower()
    if any(word in texto for word in ["hello","hi","thanks"]):
        return "en"
    elif any(word in texto for word in ["bonjou","mèsi"]):
        return "creole"
    else:
        return "es"

# -------------------------------
# FUNCIÓN PARA LLAMAR A IA
# -------------------------------
async def consulta_ia(prompt):
    # Intentar OpenAI
    try:
        openai.api_key = OPENAI_API_KEY
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"user","content":prompt}],
            temperature=0.7,
            timeout=50
        )
        return resp.choices[0].message.content
    except Exception:
        # Fallback Gemini
        async with httpx.AsyncClient(timeout=50) as client:
            data = {"input": prompt}
            headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}
            resp = await client.post("https://api.gemini.ai/generate", json=data, headers=headers)
            return resp.json().get("output", "No se pudo generar estimado")

# -------------------------------
# CONTROL DE USO POR PLAN
# -------------------------------
def validar_acceso(usuario_id, plan):
    if usuario_id not in usage_tokens_db:
        usage_tokens_db[usuario_id] = {}
    if plan not in usage_tokens_db[usuario_id]:
        usage_tokens_db[usuario_id][plan] = {"inicio": datetime.utcnow(), "consultas": 0}

    datos = usage_tokens_db[usuario_id][plan]
    plan_info = PLANES[plan]
    tiempo_transcurrido = (datetime.utcnow() - datos["inicio"]).total_seconds()

    if tiempo_transcurrido > plan_info["tiempo_seg"] or datos["consultas"] >= plan_info["consultas"]:
        raise HTTPException(status_code=403, detail="Tiempo de uso o consultas agotadas")
    datos["consultas"] += 1
    return True

# -------------------------------
# ENDPOINT ADMIN (gratis total)
# -------------------------------
@app.post("/admin/estimado")
async def admin_estimado(usuario: str = Form(...), clave: str = Form(...), prompt: str = Form(...)):
    if usuario != ADMIN_USERNAME or clave != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    respuesta = await consulta_ia(prompt)
    return JSONResponse({"estimado": respuesta})

# -------------------------------
# ENDPOINT CLIENTE
# -------------------------------
@app.post("/estimado")
async def obtener_estimado(usuario_id: str = Form(...), plan: str = Form(...), prompt: str = Form(...)):
    if plan not in PLANES:
        raise HTTPException(status_code=400, detail="Plan inválido")
    validar_acceso(usuario_id, plan)
    idioma = detectar_idioma(prompt)
    respuesta = await consulta_ia(prompt)
    return JSONResponse({"estimado": respuesta, "idioma": idioma})

# -------------------------------
# ENDPOINT STRIPE
# -------------------------------
@app.post("/create-checkout-session")
async def crear_pago(plan: str = Form(...)):
    if plan not in PRICE_IDS:
        raise HTTPException(status_code=400, detail="Plan inválido")
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price": PRICE_IDS[plan], "quantity":1}],
        mode="payment",
        success_url="https://aura-iyxa.onrender.com/success",
        cancel_url="https://aura-iyxa.onrender.com/cancel"
    )
    return {"url": session.url}

# -------------------------------
# ENDPOINT DONACIÓN
# -------------------------------
@app.post("/donacion")
async def donacion(cantidad: float = Form(...)):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data":{
                "currency":"usd",
                "product_data":{"name":"Donación"},
                "unit_amount":int(cantidad*100)
            },
            "quantity":1
        }],
        mode="payment",
        success_url="https://aura-iyxa.onrender.com/success",
        cancel_url="https://aura-iyxa.onrender.com/cancel"
    )
    return {"url": session.url}

# -------------------------------
# AUTOPROPAGANDA
# -------------------------------
AUTOPROPAGANDA = """
<div style='background-color:#007BFF;color:white;padding:10px;margin:10px;text-align:center;animation:marquee 15s linear infinite;'>
AURA by May Roga LLC - Asesor de Costos Dentales y Médicos | Calcula precios reales según tu zona y seguro | Beneficios: ahorro, transparencia y confianza
</div>
<style>
@keyframes marquee {0%{transform:translateX(100%);}100%{transform:translateX(-100%);}}
</style>
"""

@app.get("/autopropaganda")
async def propaganda():
    return HTMLResponse(content=AUTOPROPAGANDA)

# -------------------------------
# RUN APP
# -------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT",8000)), reload=True)
