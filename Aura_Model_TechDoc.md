# AURA – MODELO DE PRECIOS MÉDICOS Y DENTALES

## Principio Central
Aura NO estima precios individuales de hospitales.
Aura calcula el valor justo basado en **datos federales oficiales**, escalables y reproducibles.

## 1️⃣ Fuentes de Datos
1. **CMS – Medicare Physician & Hospital Payment Data**
   - CPT / HCPCS
   - Pagos reales por Medicare
   - Mediana, promedio y percentiles
   - Datos por estado y tipo de proveedor

2. **OPPS & ASC Datasets**
   - Hospital Outpatient Prospective Payment System
   - Ambulatory Surgical Centers
   - Tarifas ajustadas anualmente
   - Ajustes regionales y por tipo de centro

3. **GPCI – Geographic Practice Cost Index**
   - Ajuste por costo de vida médico
   - Diferencia entre estados
   - Legalmente validado para precios locales

4. **Percentiles CMS**
   - Calcula Premium Price (p85)  
   - Benchmark para comparaciones objetivas

## 2️⃣ Procesamiento
- Descarga automática de datasets federales
- Normalización de columnas
- Agrupación por CPT/Estado/ZIP
- Cálculo:
  - Fair Price = Mediana CMS
  - Local Price = Fair Price × GPCI
  - Premium Price = Percentil 85
- Inserción y actualización automática en Postgres

## 3️⃣ API / Endpoint Aura Verdict
- Entrada: CPT/CDT + ZIP + Estado + precio cotizado (opcional)
- Salida:
  - Fair Price, Local Price, Premium Price
  - Comparación con precio cotizado
  - Estimación de ahorro
  - Fuente y nota legal
- Tiempo de respuesta < 100 ms

## 4️⃣ Compliance / Legal
- ✔ No uso de datos privados
- ✔ No scraping de hospitales
- ✔ No PHI
- ✔ Datos 100% públicos
- ✔ Cumplimiento CMS, GAO y FTC
- ✔ Reproducible y auditado

## 5️⃣ Automatización Operativa
- Ejecución programada (cron o GitHub Actions)
- Actualización de tablas SQL mensual o trimestral
- Calculo automático de medianas, percentiles y ajustes geográficos
- Escalable 50 estados

## 6️⃣ Impacto
- Clínicas respetan métricas objetivas
- Brokers confían en valores defendibles
- Pacientes reciben información clara
- Abogados no tienen base para disputa

## 7️⃣ Frase institucional
**“Aura no estima precios. Aura calcula el valor justo basado en datos federales reales.”**

---

**Autor:** Maykel Rodríguez García – Aura by May Roga LLC  
**Fecha:** Enero 2026  
**Versión:** 1.0
