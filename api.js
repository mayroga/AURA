import { API_URL } from "./config";

// FETCH ESTIMATE
export async function getEstimate({ state, zip, code, insured = false, plan_type = "BASIC" }) {
  try {
    const res = await fetch(`${API_URL}/estimate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ state, zip, code, insured, plan_type })
    });

    if (!res.ok) {
      throw new Error("Failed to fetch estimate");
    }

    const data = await res.json();
    return data;

  } catch (err) {
    console.error("Error fetching estimate:", err);
    return {
      min: 0,
      max: 0,
      plan_type,
      insured,
      disclaimer: "Error fetching estimate. Try again later."
    };
  }
}

// FETCH PROVIDERS / MARKETPLACE
export async function getProviders({ state, zip, specialty = null }) {
  try {
    const res = await fetch(`${API_URL}/providers`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ state, zip, specialty })
    });

    if (!res.ok) {
      throw new Error("Failed to fetch providers");
    }

    const data = await res.json();
    return data;

  } catch (err) {
    console.error("Error fetching providers:", err);
    return [];
  }
}
