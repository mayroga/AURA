import os
import sqlite3
from dentist_codes import dentist_codes, national_fbi_codes

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_LOCAL = os.path.join(BASE_DIR, "cost_estimates.db")
DB_FBI = os.path.join(BASE_DIR, "fbi_national.db")

def crear_y_poblar(db_path, table_name, data_list):
    # 1. LIMPIEZA TOTAL: Borra el archivo físico si existe
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"🗑️ Eliminando base de datos antigua: {os.path.basename(db_path)}")

    # 2. CREACIÓN DESDE CERO
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute(f"""
        CREATE TABLE {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpt_code TEXT,
            description TEXT,
            state TEXT,
            zip_code TEXT,
            low_price REAL,
            high_price REAL
        )
    """)

    # 3. INSERCIÓN DE DATOS REALES
    cursor.executemany(f"""
        INSERT INTO {table_name} (cpt_code, description, state, zip_code, low_price, high_price)
        VALUES (?, ?, ?, ?, ?, ?)
    """, data_list)

    conn.commit()
    conn.close()
    print(f"✅ {os.path.basename(db_path)} creada y poblada con {len(data_list)} registros.")

if __name__ == "__main__":
    print("🚀 Iniciando motor de población de Aura...")
    
    # Poblar Local (Florida/Tu zona)
    crear_y_poblar(DB_LOCAL, "cost_estimates", dentist_codes)
    
    # Poblar Nacional (Estados baratos: TX, AL, MS, etc.)
    crear_y_poblar(DB_FBI, "fbi_cost_estimates", national_fbi_codes)
    
    print("\n[LISTO] Aura by Maroga LLC tiene sus bases de datos listas para el lanzamiento.")
