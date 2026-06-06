# ViabilidadMX — Evaluador de Viabilidad de Negocios CDMX

**Problema:** Los emprendedores que quieren abrir un negocio en CDMX no saben si su idea es viable en la zona elegida, ni qué trámites deben realizar ni en qué orden.

**Usuario objetivo:** Emprendedor o inversionista que quiere abrir un establecimiento comercial en Ciudad de México y necesita una evaluación rápida, confiable y basada en datos reales.

---

## ¿Cómo ejecutarlo? (5 minutos)

```bash
git clone <repo-url>
cd SEDECO
pip install -r requirements.txt
uvicorn src.main:app --reload --port 8000
```

Abre tu navegador en: **http://localhost:8000**

---

## Stack

| Capa | Tecnología |
|------|-----------|
| Backend | Python 3.11 + FastAPI |
| Frontend | HTML5 + Bootstrap 5 + Chart.js |
| Datos | JSON embebido (sin base de datos externa) |
| Despliegue | Uvicorn (compatible con Railway / Render / fly.io) |

---

## Qué hace

1. **Acepta**: tipo de negocio + alcaldía + capital disponible + superficie
2. **Calcula** un puntaje de viabilidad 0–100 con 6 factores ponderados:
   - Capital disponible (15%), Saturación de mercado (20%), Tráfico peatonal (20%),
     Seguridad de zona (15%), Crecimiento económico (15%), Factibilidad legal (15%)
3. **Muestra**:
   - Puntaje + etiqueta (Altamente Viable / Viable / Marginal / No Recomendado)
   - Desglose de costos de apertura + proyección 12 meses
   - Hoja de ruta de trámites en orden secuencial (RETYS)
   - Evaluación de riesgos con semáforo
   - Gráfica de flujo de caja proyectado

---

## Endpoints de la API

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/viability-check` | Evaluación completa de viabilidad |
| GET | `/api/procedures/{scian}` | Trámites requeridos por tipo de negocio |
| GET | `/api/cost-estimate/{scian}/{zone}/{sqm}` | Estimación de costos |
| GET | `/api/zone/{zone_code}` | Datos de la alcaldía |
| GET | `/api/business-types` | Catálogo de tipos de negocio |
| GET | `/api/zones` | Catálogo de alcaldías |

---

## Datos

Todos los datos están embebidos en archivos JSON en `data/` — sin llamadas a APIs externas en runtime:

| Archivo | Fuente | Contenido |
|---------|--------|-----------|
| `business-types.json` | INEGI SCIAN | 9 tipos de negocio |
| `zones.json` | INEGI + SEDUVI | 16 alcaldías CDMX |
| `procedures.json` | RETYS + Ley de Establecimientos | 8 trámites con secuencia |
| `costs.json` | Promedios industria | Costos por tipo de negocio |
| `crime-index.json` | INEGI + Secretaría de Seguridad | Índice de criminalidad por zona |
| `viability-model.json` | Modelo propio | Pesos y umbrales del scoring |

---

## Limitaciones conocidas

- **Datos de mercado sintéticos**: los indicadores de competencia y tráfico son estimaciones basadas en datos censales, no conteos en tiempo real.
- **Tipos sin costo detallado**: Galería de arte (711120) y Hotel (721110) usan estimaciones generales, no datos específicos de costos.
- **SEDUVI**: La compatibilidad de uso de suelo por dirección exacta requiere integración con el servidor de SEDUVI (intermitente); actualmente se usa el nivel alcaldía.
- **Cobertura legal**: Basado en Ley de Establecimientos Mercantiles 2024 y RETYS CDMX. Trámites federales (COFEPRIS, etc.) no incluidos.
