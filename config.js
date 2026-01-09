/**
 * CONFIGURACIÓN GLOBAL FRONTEND
 * Todo lo que el cliente puede ver (nunca secretos)
 */

// ===============================
// BACKEND (Render)
// ===============================
export const BASE_URL = process.env.BASE_URL || "https://TU-APP.onrender.com";

// ===============================
// STRIPE (PUBLIC)
// ===============================
export const STRIPE_PUBLISHABLE_KEY =
  process.env.STRIPE_PUBLISHABLE_KEY || "pk_live_REEMPLAZAR";

// ===============================
// PLANES & PRICE_ID (Stripe)
// ===============================
export const PLANS = {
  BASIC_MONTHLY: {
    name: "Basic Monthly",
    price: "$7.00 / month",
    price_id: "price_BASIC_MONTHLY_ID"
  },
  BASIC_DAILY: {
    name: "Pay Per Use",
    price: "$4.99 / use",
    price_id: "price_BASIC_DAILY_ID"
  },
  PREMIUM_MONTHLY: {
    name: "Premium Monthly",
    price: "$19.99 / month",
    price_id: "price_PREMIUM_MONTHLY_ID"
  }
};

// ===============================
// APP METADATA
// ===============================
export const APP_NAME = "US Healthcare Cost Transparency";
export const LEGAL_VERSION =
  process.env.LEGAL_VERSION || "2026-01-08-v1";

// ===============================
// FEATURE FLAGS
// ===============================
export const FEATURES = {
  ESTIMATES_ENABLED: true,
  PROVIDER_SEARCH: true,
  STRIPE_PAYMENTS: true,
  AI_EXPLANATIONS: true
};
