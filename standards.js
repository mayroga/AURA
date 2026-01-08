// ==============================
// CÓDIGOS Y LEGALIDAD
// ==============================

// Estados permitidos para estimados y marketplace
export const ALLOWED_STATES = [
  "FL","TX","CA","NY","AZ","NV","GA","NC","WA","IL"
];

// Sistemas de códigos válidos
export const CODE_SYSTEMS = {
  MEDICAL: ["CPT","HCPCS","ICD-10"],
  DENTAL: ["CDT"]
};

// DISCLAIMER GENERAL
export const DISCLAIMER =
  "This platform provides cost estimates only. It does NOT provide medical advice, insurance advice, billing, or price guarantees. Estimates are based on public data and historical averages. Always confirm directly with provider.";

// VERSIÓN CORTA PARA PANTALLA DE RESULTADOS
export const DISCLAIMER_SHORT =
  "Estimates only. Not a bill or guarantee.";
