const BASE_URL = "https://aura-iyxa.onrender.com";

let language = navigator.language.startsWith("en") ? "en" :
               navigator.language.startsWith("ht") ? "ht" : "es";

const translations = {
    es: {
        "Bienvenido": "Bienvenido a Aura! Obtén estimados de salud rápidos y confiables.",
        "title": "Aura - Estimados de Salud",
        "estado": "Estado (ej: FL)",
        "zip": "Código ZIP",
        "code": "Código de procedimiento",
        "plan": ["Básico", "Prueba", "Premium"],
        "button": "Obtener Estimado",
        "result_error": "Error: "
    },
    en: {
        "Bienvenido": "Welcome to Aura! Get quick and reliable health estimates.",
        "title": "Aura - Health Estimates",
        "estado": "State (ex: FL)",
        "zip": "ZIP Code",
        "code": "Procedure Code",
        "plan": ["Basic","Trial","Premium"],
        "button": "Get Estimate",
        "result_error": "Error: "
    },
    ht: {
        "Bienvenido": "Byenveni nan Aura! Jwenn evalyasyon sante rapid ak serye.",
        "title": "Aura - Evalyasyon Sante",
        "estado": "Eta (eg: FL)",
        "zip": "Kòd ZIP",
        "code": "Kòd Pwosedi",
        "plan": ["Debaz","Esè","Premium"],
        "button": "Jwenn Evalyasyon",
        "result_error": "Erè: "
    }
};

// Cambiar idioma manualmente
function setLanguage(lang) {
    language = lang;
    updateText();
}

// Actualiza textos según idioma
function updateText() {
    const t = translations[language];
    document.getElementById("title").innerText = t.title;
    document.getElementById("state").placeholder = t.estado;
    document.getElementById("zip").placeholder = t.zip;
    document.getElementById("code").placeholder = t.code;
    document.getElementById("plan").options[0].text = t.plan[0];
    document.getElementById("plan").options[1].text = t.plan[1];
    document.getElementById("plan").options[2].text = t.plan[2];
}

// Llamada al backend para obtener estimado
async function getEstimate() {
    const state = document.getElementById("state").value;
    const zip = document.getElementById("zip").value;
    const code = document.getElementById("code").value;
    const plan = document.getElementById("plan").value;

    if(!state || !zip || !code){
        alert("Completa todos los campos!");
        return;
    }

    const formData = new FormData();
    formData.append("state", state);
    formData.append("zip", zip);
    formData.append("code", code);
    formData.append("plan_type", plan);

    try {
        const res = await fetch(`${BASE_URL}/estimate`, {
            method: "POST",
            body: formData
        });
        const data = await res.json();
        const resultDiv = document.getElementById("result");
        resultDiv.style.display = "block";
        if(data.error){
            resultDiv.innerText = translations[language].result_error + data.message;
        } else {
            resultDiv.innerText = data.estimate;
        }
    } catch(e){
        alert("Error al obtener estimado. Intenta más tarde.");
    }
}

// Inicializa textos al cargar
updateText();
