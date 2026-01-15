import os
import sqlite3
from dentist_codes import dentist_codes

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_LOCAL = os.path.join(BASE_DIR, "cost_estimates.db")
DB_FBI = os.path.join(BASE_DIR, "fbi_national.db")


def crear_y_poblar(db_path, table_name, data_list):
    """
    Crea una base de datos SQLite desde cero y la puebla
    usando datos públicos estimados (uso informativo).
    """

    # 1️⃣ LIMPIEZA TOTAL
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"🗑️ Eliminando base de datos antigua: {os.path.basename(db_path)}")

    # 2️⃣ CREACIÓN
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

    # 3️⃣ INSERCIÓN
    cursor.executemany(f"""
        INSERT INTO {table_name}
        (cpt_code, description, state, city, zip_code, low_price, high_price)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, data_list)

    conn.commit()
    conn.close()

    print(f"✅ {os.path.basename(db_path)} creada con {len(data_list)} registros.")


if __name__ == "__main__":
    print("🚀 Iniciando motor de población de Aura...")

    # 🔹 Base LOCAL (se filtra luego por ZIP / estado)
    crear_y_poblar(
        DB_LOCAL,
        "cost_estimates",
        dentist_codes
    )

    # 🔹 Base NACIONAL (misma data, distinto contexto analítico)
    crear_y_poblar(
        DB_FBI,
        "fbi_cost_estimates",
        dentist_codes
    )

    print("\n✅ [LISTO] Aura by May Roga LLC tiene sus bases de datos creadas correctamente.")
    print("🛡️ Uso informativo, datos públicos estimados, sin nombres reales de clínicas.")
