// ==============================
// CONFIGURACIÓN DE LA APP
// ==============================

// Planes y precios
export const PLANS = {
  BASIC: {
    price: 7.00,       // Mensual
    zipOnly: true      // Solo estimado básico por ZIP
  },
  PAY_PER_USE: {
    price: 4.99        // Por uso
  },
  PREMIUM: {
    price: 19.99,      // Acceso completo
    insuranceAware: true,   // Estimados ajustados según seguro
    historicalRanges: true, // Rango más preciso
    priorityMarketplace: true
  }
};

// URL del backend (FastAPI)
export const API_URL = "http://localhost:8000";
