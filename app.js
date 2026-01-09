const BASE_URL = "https://aura-iyxa.onrender.com";

const priceIds = {
    "TRIAL": "price_1SnYkMBOA5mT4t0P2Ra3NpYy",
    "BASIC": "price_1SnYuABOA5mT4t0Pv706amhC",
    "PREMIUM": "price_1SnZ0eBOA5mT4t0Phwt58d4k"
};

let selectedPlan = "TRIAL";

// Cambio de idioma
document.getElementById("langSelector").addEventListener("change", (e) => {
    const lang = e.target.value;
    const title = document.getElementById("title");
    const ad = document.getElementById("autopropaganda");

    if (lang === "es") {
        title.innerText = "Bienvenido a SmartCargo";
        ad.innerText = "Protege tu dinero y tu carga 🚛";
    } else if (lang === "en") {
        title.innerText = "Welcome to SmartCargo";
        ad.innerText = "Protect your money and cargo 🚛";
    } else {
        title.innerText = "Byenveni nan SmartCargo";
        ad.innerText = "Pwoteje lajan ou ak chaj ou 🚛";
    }
});

// Selección de plan
document.querySelectorAll(".planBtn").forEach(btn => {
    btn.addEventListener("click", () => {
        selectedPlan = btn.dataset.plan;
        alert("Plan seleccionado: " + selectedPlan);
    });
});

// Botón de donación / compra plan
document.getElementById("donateBtn").addEventListener("click", async () => {
    try {
        const priceId = priceIds[selectedPlan];
        if (!priceId) {
            alert("Plan no válido");
            return;
        }

        // Llamamos a nuestro endpoint en main.py que crea la sesión de Stripe
        const data = new FormData();
        data.append("price_id", priceId);

        const resp = await fetch(`${BASE_URL}/create-checkout-session`, {
            method: "POST",
            body: data
        });

        const session = await resp.json();

        if (session.url) {
            window.location.href = session.url; // Redirige al checkout
        } else {
            alert("Error al crear sesión de pago.");
        }
    } catch (err) {
        console.error(err);
        alert("Ocurrió un error en el pago.");
    }
});
