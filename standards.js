/**
 * STANDARDS & LEGAL GUARDRAILS
 * Este archivo protege legalmente la app
 * NO tocar sin asesoría
 */

// ===============================
// ESTADOS DONDE ES PERMITIDO
// (Estimaciones de costos basadas en datos públicos)
// ===============================
export const ALLOWED_STATES = [
  "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA",
  "HI","ID","IL","IN","IA","KS","KY","LA","ME","MD",
  "MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ",
  "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC",
  "SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"
];

// ===============================
// CÓDIGOS ACEPTADOS
// ===============================
export const CODE_TYPES = {
  MEDICAL: ["CPT", "HCPCS"],
  DENTAL: ["CDT"],
  GOVERNMENT: ["DRG"]
};

// ===============================
// DISCLAIMER CORTO (pantalla resultados)
// ===============================
export const DISCLAIMER_SHORT = `
Estimates only. Not medical advice. 
No price guarantees. 
Data based on public fee schedules.
`;

// ===============================
// DISCLAIMER COMPLETO
// ===============================
export const DISCLAIMER_FULL = `
This application provides healthcare and dental cost estimates only.

It does NOT:
- Provide medical, dental, or insurance advice
- Diagnose conditions
- Recommend treatments
- Guarantee prices or coverage
- Act as a healthcare provider or insurer

All estimates are informational and based on publicly available data,
historical ranges, geographic factors, and standard coding systems
(CPT, CDT, HCPCS, DRG).

Actual prices may vary significantly depending on provider, facility,
insurance contracts, and individual circumstances.

Users are solely responsible for contacting providers directly to
confirm prices, coverage, and services.

This platform does not require medical licensure and does not engage
in regulated medical activities.
`;

// ===============================
// CHECKBOX LEGAL (APP MÓVIL)
// ===============================
export const CHECKBOX_TEXT = `
I understand this app provides cost estimates only.
I acknowledge no medical or financial advice is given.
I agree prices are not guaranteed.
`;

// ===============================
// REGLAS DE NEGOCIO (BLINDAJE)
// ===============================
export const BUSINESS_RULES = {
  NO_DIAGNOSIS: true,
  NO_BILLING: true,
  NO_NEGOTIATION: true,
  NO_MEDICAL_ADVICE: true,
  ESTIMATES_ONLY: true
};

// ===============================
// VISIBILIDAD LEGAL OBLIGATORIA
// ===============================
export const LEGAL_VISIBILITY = {
  SHOW_ON_FIRST_USE: true,
  SHOW_ON_RESULTS: true,
  REQUIRE_ACCEPTANCE: true
};
