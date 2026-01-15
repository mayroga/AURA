AURA by May Roga LLC – Estimador de Precios Médicos en USA
📌 Descripción General

AURA es un sistema profesional para consultar estimados de precios médicos y dentales en Estados Unidos, usando datos reales de CMS / PFS.
El objetivo principal es brindar transparencia total de mercado para consumidores y empresas, sin dar diagnósticos ni reemplazar seguros o médicos.

La aplicación está diseñada para ser:

Automática: la base de datos se actualiza mensual desde CMS/PFS.

Auditada: cada actualización queda registrada en GitHub.

Legalmente blindada: disclaimers, datos y cálculos cumplen regulaciones de salud y privacidad.

100% transparente y reproducible: sin datos inventados ni randomización.

🗂️ Estructura del Repositorio
.
├─ main.py                  # Backend FastAPI + lógica de estimados
├─ import_cms_pfs.py        # Script que descarga y normaliza datos CMS/PFS
├─ cost_estimates.db        # Base de datos SQLite con precios y ZIP/condado/estado
├─ index.html               # Frontend, interfaz de usuario
├─ requirements.txt         # Dependencias Python
└─ .github/
   └─ workflows/
       └─ cms_job.yml      # Job automático para actualizar DB mensual

⚙️ Funcionamiento del Sistema

Actualización de datos (CMS/PFS)

import_cms_pfs.py descarga los archivos oficiales de CMS/PFS, los normaliza y llena la base de datos SQLite cost_estimates.db.

Este proceso se ejecuta automáticamente el día 1 de cada mes vía .github/workflows/cms_job.yml.

Cada actualización queda registrada y versionada en GitHub para auditoría.

Backend y Cálculo de Fair Price

main.py maneja la ruta /estimado para consultas de precios.

Calcula automáticamente el Fair Price matemático usando precios locales y nacionales, sin IA ni inferencias subjetivas.

Incluye disclaimers y blindaje legal, protegiendo a la empresa frente a hospitales, aseguradoras y reguladores.

Los resultados se presentan de manera estructurada, clara y auditada.

Frontend / Interfaz de usuario

index.html permite al usuario ingresar procedimiento, código, síntoma o ubicación.

El sistema detecta el ZIP automáticamente (opcional).

Muestra los resultados con opciones de PDF, WhatsApp y lectura en voz alta.

Incluye botones de pago o acceso gratuito para usuarios admin, sin afectar la seguridad de los datos.

🔐 Blindaje Legal y Disclaimer

Toda la información generada incluye:

Mensajes claros: “No somos médicos ni seguros, solo información de mercado.”

Datos basados en CMS/PFS oficiales 2026.

Cálculo de Fair Price auditado y reproducible.

Registro de cambios y trazabilidad en GitHub Actions.

Esto protege a AURA by May Roga LLC frente a reguladores, hospitales y aseguradoras.

📊 Automatización & Auditoría

Job GitHub Actions: .github/workflows/cms_job.yml

Frecuencia: mensual (día 1 a las 03:00 AM UTC)

Acciones:

Clona el repositorio

Instala dependencias (requirements.txt)

Ejecuta import_cms_pfs.py → actualiza cost_estimates.db

Commit automático solo si hay cambios

Mensaje de auditoría: "Automated CMS/PFS data refresh - legally audited"

🛠️ Dependencias

Archivo requirements.txt:

fastapi
uvicorn[standard]
stripe
python-dotenv
python-multipart
google-genai
openai
httpx
pandas
requests

🚀 Cómo Ejecutar Localmente

Clonar el repositorio:

git clone <repo-url>
cd aura


Crear entorno virtual:

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows


Instalar dependencias:

pip install -r requirements.txt


Ejecutar servidor FastAPI:

uvicorn main:app --reload


Abrir navegador en:

http://127.0.0.1:8000/

📌 Nota Final

Toda la información es de uso exclusivo de transparencia de precios, no sustituye consejo médico ni seguros.

El sistema está auditado, legalmente blindado y listo para producción.

Cualquier actualización futura se realizará mediante el job automático CMS/PFS, manteniendo la trazabilidad.
