import os
import sqlite3
from dentist_codes import dentist_codes  # SOLO LOCAL

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_LOCAL = os.path.join(BASE_DIR, "cost_estimates.db")
DB_FBI = os.path.join(BASE_DIR, "fbi_national.db")

def crear_y_poblar(db_path, table_name, data_list):
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"🗑️ Eliminada DB antigua: {os.path.basename(db_path)}")

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
    cursor.executemany(f"""
        INSERT INTO {table_name} (cpt_code, description, state, zip_code, low_price, high_price)
        VALUES (?, ?, ?, ?, ?, ?)
    """, data_list)
    conn.commit()
    conn.close()
    print(f"✅ {os.path.basename(db_path)} creada con {len(data_list)} registros.")

if __name__ == "__main__":
    print("🚀 Inicializando bases de datos AURA...")

    # POBLAR LOCAL
    crear_y_poblar(DB_LOCAL, "cost_estimates", dentist_codes)

    # POBLAR NACIONAL: reutilizar dentist_codes como ejemplo
    crear_y_poblar(DB_FBI, "fbi_cost_estimates", dentist_codes)

    print("🎉 AURA LISTA PARA PRODUCCIÓN")
