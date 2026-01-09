import { BASE_URL } from "./config";

/**
 * Obtener estimado de costos médicos / dentales
 * NO diagnóstico
 * NO precio garantizado
 */
export async function getEstimate(payload) {
  try {
    const response = await fetch(`${BASE_URL}/estimate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error("Estimate request failed");
    }

    return await response.json();
  } catch (error) {
    console.error("Estimate error:", error);
    return {
      error: true,
      message:
        "Unable to retrieve estimate at this time. Please try again later."
    };
  }
}

/**
 * Obtener proveedores cercanos
 * Solo información pública
 */
export async function getProviders(payload) {
  try {
    const response = await fetch(`${BASE_URL}/providers`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error("Providers request failed");
    }

    return await response.json();
  } catch (error) {
    console.error("Providers error:", error);
    return [];
  }
}

/**
 * Crear sesión de pago Stripe
 */
export async function createCheckoutSession(plan) {
  try {
    const response = await fetch(`${BASE_URL}/create-checkout-session`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ plan })
    });

    if (!response.ok) {
      throw new Error("Checkout session failed");
    }

    return await response.json();
  } catch (error) {
    console.error("Stripe error:", error);
    return {
      error: true,
      message: "Payment initialization failed."
    };
  }
}
