import os, sqlite3, stripe, json, requests
from fastapi import FastAPI, Form, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from google import genai
import openai
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# ================== CONFIG ==================
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

PRICE_IDS = {
    "rapido": os.getenv("PRICE_RAPIDO"),
    "standard": os.getenv("PRICE_STANDARD"),
    "special": os.getenv("PRICE_SPECIAL")
}
LINK_DONACION = os.getenv("LINK_DONACION")

ADMIN_USER = os.getenv("ADMIN_USERNAME")
ADMIN_PASS = os.getenv("ADMIN_PASSWORD")

gemini = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
openai.api_key = os.getenv("OPENAI_API_KEY")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "aura_data.db")

# ================== GEO IP ==================
def ip_to_zip(ip):
    try:
        r = requests.get(f"https://ipapi.co/{ip}/json/").json()
        return r.get("postal"), r.get("region"), r.get("country_name")
    except:
        return None, None, None

# ================== SQL ==================
def query_prices(term, zip_code=None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    term = f"%{term.upper()}%"

    if zip_code:
        cur.execute("""
        SELECT description, cpt_code, icd_code, county, state, zip_code, low_price, high_price
        FROM cost_estimates
        WHERE zip_code = ?
        AND (description LIKE ? OR cpt_code LIKE ? OR icd_code LIKE ?)
        ORDER BY low_price ASC LIMIT 5
        """,(zip_code,term,term,term))
        rows = cur.fetchall()
        if rows:
            conn.close()
            return rows

    cur.execute("""
    SELECT description, cpt_code, icd_code, county, state, zip_code, low_price, high_price
    FROM cost_estimates
    WHERE description LIKE ? OR cpt_code LIKE ? OR icd_code LIKE ?
    ORDER BY low_price ASC LIMIT 10
    """,(term,term,term))
    rows = cur.fetchall()
    conn.close()
    return rows

# ================== INDEX ==================
@app.get("/", response_class=HTMLResponse)
async def index():
    with open(os.path.join(BASE_DIR,"index.html"),"r",encoding="utf-8") as f:
        return f.read()

# ================== ESTIMADOR ==================
@app.post("/estimado")
async def estimado(request: Request, consulta: str = Form(...), lang: str = Form("es"), zip_user: str = Form(None)):
    ip = request.client.host
    ip_zip, ip_state, _ = ip_to_zip(ip)

    zip_final = zip_user or ip_zip or "USA"

    sql = query_prices(consulta, zip_final)

    idioma = {"es":"Spanish","en":"English","ht":"Haitian Creole"}.get(lang,"Spanish")

    legal = {
        "es":"Los precios pueden variar por proveedor, ubicación y complejidad. Estos son rangos estimados de mercado. Aura no ofrece servicios médicos ni de seguros.",
        "en":"Prices may vary by provider, location and complexity. These are estimated market ranges. Aura does not provide medical or insurance services.",
        "ht":"Pri yo ka varye selon founisè ak kote. Sa yo se estimasyon mache. Aura pa bay sèvis medikal ni asirans."
    }[lang]

    prompt = f"""
Aura by May Roga LLC is a medical price intelligence system.
Never provide medical or insurance advice.

User: {consulta}
ZIP: {zip_final}
SQL DATA: {sql}

Respond in {idioma}.

Format:
Simple explanation first.
Then structured finance:

Procedure:
CPT/ICD:
Location:
Market Price Range:
Estimated Fair Price:
Typical Overcharge:

End with this disclaimer:
{legal}
"""

    try:
        r = gemini.responses.create(model="gemini-2.5", input=prompt, temperature=0.2, max_output_tokens=700)
        text = r.output_text
    except:
        try:
            c = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role":"user","content":prompt}],
                temperature=0.2,
                max_tokens=700
            )
            text = c.choices[0].message.content
        except:
            text = legal

    return {"resultado": text}

# ================== PAY ==================
@app.post("/create-checkout-session")
async def pay(plan: str = Form(...)):
    if plan=="donacion":
        return {"url": LINK_DONACION}
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": PRICE_IDS[plan], "quantity": 1}],
            mode="payment",
            success_url="https://yourdomain.com/?success=true",
            cancel_url="https://yourdomain.com/"
        )
        return {"url": session.url}
    except Exception as e:
        return JSONResponse(status_code=500,content={"error":str(e)})

# ================== ADMIN ==================
@app.post("/login-admin")
async def admin(user: str = Form(...), pw: str = Form(...)):
    if user==ADMIN_USER and pw==ADMIN_PASS:
        return {"status":"success","access":"full"}
    return JSONResponse(status_code=401,content={"status":"error"})
