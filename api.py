from fastapi import FastAPI, Query
import psycopg2
import os

app = FastAPI()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=5432
)

@app.get("/price/cpt")
def get_cpt_price(
    cpt: str = Query(...),
    zip: str = Query(...),
    state: str = Query(...)
):
    cur = conn.cursor()

    # 1️⃣ ZIP exacto
    cur.execute("""
        SELECT avg_price, min_price, max_price
        FROM prices_cpt
        WHERE cpt=%s AND zip=%s
        LIMIT 1
    """, (cpt, zip))

    row = cur.fetchone()

    # 2️⃣ Estado
    if not row:
        cur.execute("""
            SELECT AVG(avg_price), MIN(min_price), MAX(max_price)
            FROM prices_cpt
            WHERE cpt=%s AND state=%s
        """, (cpt, state))
        row = cur.fetchone()

    # 3️⃣ Nacional
    if not row or row[0] is None:
        cur.execute("""
            SELECT AVG(avg_price), MIN(min_price), MAX(max_price)
            FROM prices_cpt
            WHERE cpt=%s
        """, (cpt,))
        row = cur.fetchone()

    cur.close()

    return {
        "cpt": cpt,
        "zip": zip,
        "state": state,
        "average": float(row[0]),
        "min": float(row[1]),
        "max": float(row[2]),
        "source": "CMS + Internal Model"
    }
