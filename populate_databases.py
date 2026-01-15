# populate_databases.py
import sqlite3
import os
from dentist_codes import dentist_codes

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_LOCAL = os.path.join(BASE_DIR, "cost_estimates.db")
DB_FBI = os.path.join(BASE_DIR, "fbi_national.db")

def create_and_populate(db_path, table_name):
    # Eliminar archivo si está corrupto
    if os.path.exists(db_path):
        try:
            sqlite3.connect(db_path).execute("SELECT 1")
        except:
            os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpt_code TEXT NOT NULL,
            description TEXT NOT NULL,
            state TEXT NOT NULL,
            zip_code TEXT NOT NULL,
            low_price REAL,
            high_price REAL
        )
    """)

    cursor.execute(f"DELETE FROM {table_name}")

    for code in dentist_codes:
        cursor.execute(f"""
            INSERT INTO {table_name}
            (cpt_code, description, state, zip_code, low_price, high_price)
            VALUES (?, ?, ?, ?, ?, ?)
        """, code)

    conn.commit()
    conn.close()
    print(f"[OK] {db_path} creada y poblada correctamente")

if __name__ == "__main__":
    create_and_populate(DB_LOCAL, "cost_estimates")
    create_and_populate(DB_FBI, "fbi_cost_estimates")
    print("[LISTO] Bases LOCAL y NACIONAL creadas sin errores")
