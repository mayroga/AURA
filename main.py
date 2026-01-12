import os
import stripe
import smtplib
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from email.mime.text import MIMEText
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# Configuración de Llaves y Seguridad
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# IDs de Stripe proporcionados
PRICE_IDS = {
    "rapido": "price_1Snam1BOA5mT4t0PuVhT2ZIq",
    "standard": "price_1SnaqMBOA5mT4t0PppRG2PuE",
    "special": "price_1SnatfBOA5mT4t0PZouWzfpw",
    "donacion": "price_1SoB56BOA5mT4t0P7EXAMPLE"
}

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/estimado")
async def obtener_estimado(consulta: str = Form(...), lang: str = Form("es")):
    prompt = f"""
    ERES EL ASESOR JEFE DE AURA BY MAY ROGA LLC. 
    OBJETIVO: TRANSPARENCIA TOTAL PARA SIN SEGURO, POCO SEGURO Y BUSCADORES DE PRESTIGIO.
    CONSULTA: "{consulta}" | IDIOMA: "{lang}"

    REGLA DE ORO: EL REPORTE DEBE COMENZAR Y TERMINAR CON ESTE BLINDAJE:
    "ESTE REPORTE ES EMITIDO POR AURA BY MAY ROGA LLC, AGENCIA INFORMATIVA INDEPENDIENTE. NO SOMOS MÉDICOS, NI SEGUROS, NI DAMOS DIAGNÓSTICOS. REPORTAMOS DATOS PÚBLICOS DE MERCADO PARA AHORRO DEL CONSUMIDOR."

    ORDEN DEL REPORTE:
    1. GANANCIA ESTIMADA (Dinero que el cliente deja de perder hoy).
    2. ZONA DE CONFORT: 2 opciones locales en su área.
    3. PRESTIGIO: La mejor opción por fama y reputación del estado.
    4. AHORRO VECINO: 3 opciones en condados cercanos.
    5. RUTA NACIONAL: Los 6 mejores precios de los 50 estados.
    
    ESTILO: Peras y manzanas. Usa: DINERO, GANANCIA, CONTROL.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(prompt)
        return {"resultado": res.text}
    except:
        return {"resultado": "Error en Aura. Reintente."}

@app.post("/enviar-email")
async def enviar_email(destinatario: str = Form(...), contenido: str = Form(...)):
    try:
        msg = MIMEText(contenido)
        msg['Subject'] = 'REPORTE BLINDADO DE AHORRO - AURA BY MAY ROGA LLC'
        msg['From'] = os.getenv("SENDER_EMAIL")
        msg['To'] = destinatario
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(os.getenv("SENDER_EMAIL"), os.getenv("EMAIL_API_KEY"))
            server.sendmail(os.getenv("SENDER_EMAIL"), destinatario, msg.as_string())
        return {"status": "Enviado"}
    except:
        return JSONResponse(content={"error": "Error al enviar"}, status_code=500)

@app.post("/create-checkout-session")
async def pay(plan: str = Form(...)):
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
        return JSONResponse(content={"error": str(e)}, status_code=500)
