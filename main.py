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

# Configuración de seguridad y Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# IDs de Stripe para planes
PRICE_IDS = {
    "rapido": os.getenv("PRICE_RAPIDO"),   
    "standard": os.getenv("PRICE_STANDARD"), 
    "special": os.getenv("PRICE_SPECIAL"),  
    "donacion": os.getenv("PRICE_DONACION")
}

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

# Endpoint de estimado
@app.post("/estimado")
async def obtener_estimado(
    zip_code: str = Form(...), 
    consulta: str = Form(...), 
    plan_type: str = Form(...),
    is_admin: str = Form("false")
):
    hoy = datetime.now()
    # Definir tiempo de acceso según plan
    if is_admin.lower() == "true":
        tiempo = "Ilimitado"
    elif plan_type.lower() == "rapido":
        tiempo = "7 min"
    elif plan_type.lower() == "standard":
        tiempo = "15 min"
    elif plan_type.lower() == "special":
        tiempo = "35 min"
    else:
        tiempo = "Acceso por Pago"

    # Prompt principal para generar estimados con nombre de clínica, dirección y precios
    prompt = f"""
    ERES EL ASESOR JEFE DE 'AURA BY MAY ROGA LLC'.
    Misión: Inteligencia de Precios para Ahorro del Cliente.
    
    Para la solicitud: {consulta} en ZIP {zip_code}:
    1. Localiza 1 opción en el mismo ZIP con nombre de clínica, dirección y estimado de precio.
    2. Localiza 3 opciones adicionales en el mismo condado o en el mismo estado (especificar ZIP, ciudad, dirección y precio).
    3. Localiza de 3 a 6 opciones fuera del estado (nombre de clínica, dirección, precio, ciudad y estado).
    4. Para cada opción, calcula el ahorro aproximado si el cliente viaja por avión, tren, auto o barco.
    5. Escribe todo en formato amigable para mostrar en la app.
    6. Agrega un aviso: "BLINDAJE: Este reporte es emitido por Aura by May Roga LLC, una Agencia Informativa Independiente. No somos médicos ni seguros. Solo informamos costos de mercado."
    """

    try:
        # Primero intentar con Gemini
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        respuesta = response.text
    except Exception as e:
        # Respaldo OpenAI
        try:
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            res = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
            respuesta = res.choices[0].message.content
        except:
            respuesta = "Aura está procesando altos volúmenes de datos. Por favor, refresque y reintente."

    return {"estimado": f"<strong>ACCESO CONCEDIDO: {tiempo}</strong><br><br>{respuesta.replace('\n', '<br>')}"}


# Endpoint de pago para planes
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


# Endpoint de donación directa
@app.post("/create-donation-session")
async def donation(amount: str = Form(...)):
    try:
        amount_float = float(amount)
        if amount_float <= 0:
            raise HTTPException(status_code=400, detail="Monto inválido")

        # Creamos un PaymentIntent directo para donación
        intent = stripe.PaymentIntent.create(
            amount=int(amount_float * 100),  # Stripe usa centavos
            currency="usd",
            payment_method_types=["card"],
            description="Donación a Aura by May Roga LLC"
        )
        return {"url": intent.client_secret}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
