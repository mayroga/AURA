const BASE_URL = "https://aura-iyxa.onrender.com";

export async function createCheckoutSession(plan) {
    const data = new FormData();
    data.append("plan", plan);
    const resp = await fetch(`${BASE_URL}/create-checkout-session`, {
        method: "POST",
        body: data
    });
    return await resp.json();
}

export async function getEstimate(state, zip, code, insured, plan_type) {
    const data = new FormData();
    data.append("state", state);
    data.append("zip", zip);
    data.append("code", code);
    data.append("insured", insured);
    data.append("plan_type", plan_type);

    const resp = await fetch(`${BASE_URL}/estimado`, { method: "POST", body: data });
    return await resp.json();
}

export async function donate(amount) {
    const data = new FormData();
    data.append("amount", amount);
    const resp = await fetch(`${BASE_URL}/donacion`, { method: "POST", body: data });
    return await resp.json();
}
