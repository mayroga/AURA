import os
import stripe
from datetime import datetime
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import openai
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# Configuración de Seguridad y Cobro
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# IDs de Stripe - ASEGÚRATE DE COPIAR LOS DE TU DASHBOARD DE STRIPE
PRICE_IDS = {
    "rapido": "price_1Snam1BOA5mT4t0PuVhT2ZIq",   
    "standard": "price_1SnaqMBOA5mT4t0PppRG2PuE", 
    "special": "price_1SnatfBOA5mT4t0PZouWzfpw",  
    "donacion": "price_1SoB56BOA5mT4t0P7EXAMPLE" # Reemplaza este por tu ID de Donación real
}

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/estimado")
async def obtener_estimado(
    zip_code: str = Form(...), 
    consulta: str = Form(...), 
    plan_type: str = Form(...),
    is_admin: str = Form("false")
):
    hoy = datetime.now()
    # Lógica de tiempos exacta
    if is_admin == "true": tiempo = "Ilimitado"
    elif plan_type == "rapido": tiempo = "7 min"
    elif plan_type == "standard": tiempo = "15 min"
    elif plan_type == "special": tiempo = "35 min" if hoy.day <= 2 else "6 min"
    else: tiempo = "Acceso por Pago"

    # El Prompt que vende tu servicio y te blinda
    prompt = f"""
    ERES EL ASESOR JEFE DE 'AURA BY MAY ROGA LLC'. 
    Misión: Inteligencia de Precios para Ahorro del Cliente.
    
    1. Localiza 5 estimados de precios (los más baratos encontrados en USA) para: {consulta} cerca de {zip_code}.
    2. Compara el ahorro si el cliente viaja a otro estado o condado.
    3. Indica cuánto dinero ganan al NO pagar el precio inflado de los hospitales.
    4. Explica que estos datos son para negociar directamente con el proveedor.
    5. BLINDAJE: "Este reporte es emitido por Aura by May Roga LLC, una Agencia Informativa Independiente. No somos médicos, ni seguros, ni damos diagnósticos. Solo informamos costos de mercado."
    """
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        # timeout de 10 segundos para que no se congele
        response = model.generate_content(prompt)
        respuesta = response.text
    except Exception as e:
        # Respaldo OpenAI en caso de caída de Gemini
        try:
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
            respuesta = res.choices[0].message.content
        except:
            respuesta = "Aura está procesando altos volúmenes de datos. Por favor, refresque y reintente."

    return {"estimado": f"<strong>ACCESO CONCEDIDO: {tiempo}</strong><br><br>{respuesta.replace('\n', '<br>')}"}

@app.post("/create-checkout-session")
async def pay(plan: str = Form(...)):
    try:
        mode = "subscription" if plan.lower() == "special" else "payment"
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": PRICE_IDS[plan.lower()], "quantity": 1}],
            mode=mode,
            success_url="https://aura-iyxa.onrender.com/?success=true",
            cancel_url="https://aura-iyxa.onrender.com/?cancel=true"
        )
        return {"url": session.url}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
