import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def check_connection():
    print("🔍 Verificando conexión para Aura by May Roga LLC...")
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=5432
        )
        cur = conn.cursor()
        cur.execute("SELECT version();")
        record = cur.fetchone()
        print(f"✅ ¡Conexión Exitosa! Versión de DB: {record}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    check_connection()
