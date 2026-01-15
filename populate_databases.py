import os
import sqlite3
from dentist_codes import dentist_codes, fbi_codes  # Asegúrate que dentist_codes.py tenga ambas listas

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_LOCAL = os.path.join(BASE_DIR, "cost_estimates.db")
DB_FBI = os.path.join(BASE_DIR, "fbi_national.db")

def crear_y_poblar(db_path, table_name, data_list):
    # 1️⃣ Elimina la DB anterior si existe
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"🗑️ Eliminando base de datos antigua: {os.path.basename(db_path)}")

    # 2️⃣ Crea la DB desde cero
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(f"""
        CREATE TABLE {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpt_code TEXT,
            description TEXT,
            state TEXT,
            city TEXT,
            zip_code TEXT,
            low_price REAL,
            high_price REAL
        )
    """)

    # 3️⃣ Inserta los datos
    for record in data_list:
        if len(record) == 7:
            cursor.execute(f"""
                INSERT INTO {table_name} 
                (cpt_code, description, state, city, zip_code, low_price, high_price)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, record)
        else:
            print(f"[WARN] Registro ignorado por formato incorrecto: {record}")

    conn.commit()
    conn.close()
    print(f"✅ {os.path.basename(db_path)} creada y poblada con {len(data_list)} registros.")

if __name__ == "__main__":
    print("🚀 Iniciando población de bases de datos Aura...")

    # Local
    crear_y_poblar(DB_LOCAL, "cost_estimates", dentist_codes)

    # Nacional
    crear_y_poblar(DB_FBI, "fbi_cost_estimates", fbi_codes)

    print("\n[LISTO] Bases de datos listas para el lanzamiento de Aura.")
