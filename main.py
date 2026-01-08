from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# ==============================
# BASE DE DATOS SIMULADA (LEGAL)
# ==============================

CMS_BASE_FEES = {
    "99213": 92.47,    # Consulta médica
    "D1110": 95.00     # Limpieza dental
}

GPCI_BY_STATE = {
    "FL": 1.02, "TX": 0.98, "CA": 1.15, "NY": 1.20,
    "AZ": 1.00, "NV": 1.05, "GA": 0.99, "NC": 1.01
}

# Proveedores / Marketplace
PROVIDERS = [
    {"id":1, "name":"Smile Dental", "state":"FL", "zip":"33160", "specialty":"Dental", "in_network":True},
    {"id":2, "name":"HealthFirst Clinic", "state":"TX", "zip":"75001", "specialty":"Medical", "in_network":False},
    {"id":3, "name":"Bright Smile Dental", "state":"CA", "zip":"90001", "specialty":"Dental", "in_network":True},
    {"id":4, "name":"WellCare Clinic", "state":"NY", "zip":"10001", "specialty":"Medical", "in_network":False}
]

# ==============================
# MODELOS
# ==============================
class EstimateRequest(BaseModel):
    state: str
    zip: str
    code: str
    insured: bool = False
    plan_type: str = "BASIC"

class ProviderRequest(BaseModel):
    state: str
    zip: str
    specialty: str = None

# ==============================
# ENDPOINT: ESTIMADOS
# ==============================
@app.post("/estimate")
def estimate(req: EstimateRequest):
    base_fee = CMS_BASE_FEES.get(req.code, 120)
    gpci = GPCI_BY_STATE.get(req.state, 1.0)

    # Factores insured/uninsured
    if req.insured:
        min_estimate = base_fee * gpci * 0.8
        max_estimate = base_fee * gpci * 1.2
    else:
        min_estimate = base_fee * gpci * 1.6
        max_estimate = base_fee * gpci * 2.4

    # Ajuste Premium
    if req.plan_type == "PREMIUM":
        min_estimate *= 0.95
        max_estimate *= 1.05

    return {
        "min": round(min_estimate, 2),
        "max": round(max_estimate, 2),
        "insured": req.insured,
        "plan_type": req.plan_type,
        "disclaimer": "Estimated cost only. Not a bill or guarantee.",
        "source": "CMS public data + regional adjustment + historical ranges"
    }

# ==============================
# ENDPOINT: PROVIDERS / MARKETPLACE
# ==============================
@app.post("/providers")
def get_providers(req: ProviderRequest):
    results = [
        p for p in PROVIDERS
        if p["state"] == req.state and (p["zip"] == req.zip or req.specialty is None)
    ]
    return results
