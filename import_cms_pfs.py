import requests
import sqlite3
from datetime import date

CMS_API = "https://data.cms.gov/data-api/v1/dataset/6fea9d79-0129-4e4c-b1b8-23cd86a4f435/data"

conn = sqlite3.connect("cost_estimates.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS medicare_pfs (
    cpt_code TEXT,
    description TEXT,
    locality TEXT,
    state TEXT,
    zip_code TEXT,
    facility_type TEXT,
    medicare_price REAL,
    national_price REAL,
    gpci_adjustment REAL,
    source_year INTEGER,
    last_updated DATE,
    PRIMARY KEY (cpt_code, locality, facility_type)
)
""")

params = {"size": 5000}
data = requests.get(CMS_API, params=params).json()

rows = []
for item in data:
    try:
        rows.append((
            item.get("hcpcs_code"),
            item.get("short_description"),
            item.get("locality_name", "NATIONAL"),
            item.get("state", "US"),
            None,
            item.get("facility_type", "non-facility"),
            float(item.get("payment_amount", 0)),
            float(item.get("national_payment_amount", 0)),
            float(item.get("gpci", 1)),
            2026,
            date.today().isoformat()
        ))
    except:
        continue

c.executemany("""
INSERT OR REPLACE INTO medicare_pfs VALUES (?,?,?,?,?,?,?,?,?,?,?)
""", rows)

conn.commit()
conn.close()

print("✅ CMS PFS IMPORTADO CORRECTAMENTE")
