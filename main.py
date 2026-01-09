import os
import sqlite3
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# VARIABLES DE RENDER
ADMIN_USER = os.getenv("ADMIN_USERNAME")
ADMIN_PASS = os.getenv("ADMIN_PASSWORD")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

def init_db():
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    if os.path.exists('cost_estimates.sql'):
        with open('cost_estimates.sql', 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
    return conn

db_conn = init_db()

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/login-owner")
async def login_owner(username: str = Form(...), password: str = Form(...)):
    if username == ADMIN_USER and password == ADMIN_PASS:
        return {"status": "success"}
    raise HTTPException(status_code=401)

@app.post("/estimado")
async def obtener_estimado(zip_code: str = Form(...), consulta: str = Form(...), is_admin: str = Form(...)):
    # Aquí la lógica de búsqueda en Storage + Dual IA
    # ...
    return {"estimado": "Estimado Informativo Generado"}
