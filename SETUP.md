# SETUP — ViabilidadMX

## Requisitos

- Python 3.10 o superior
- pip
- Navegador web moderno

## Instalación y ejecución

```bash
# 1. Clona el repositorio
git clone <repo-url>
cd SEDECO

# 2. (Opcional) Crea un entorno virtual
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# 3. Instala dependencias
pip install -r requirements.txt

# 4. Ejecuta el servidor
uvicorn src.main:app --reload --port 8000

# 5. Abre en el navegador
open http://localhost:8000   # macOS
# o navega manualmente a http://localhost:8000
```

## Verificación

El servidor está listo cuando ves:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

Visita `http://localhost:8000/docs` para ver la documentación interactiva de la API (Swagger UI).

## Estructura del proyecto

```
SEDECO/
├── src/
│   ├── main.py              # FastAPI backend — 4 endpoints + scoring
│   └── frontend/
│       └── index.html       # SPA — formulario + dashboard de resultados
├── data/                    # JSON embebido (cargado en memoria al iniciar)
│   ├── business-types.json
│   ├── zones.json
│   ├── procedures.json
│   ├── costs.json
│   ├── crime-index.json
│   ├── viability-model.json
│   └── query-index.json
├── requirements.txt
├── README.md
└── SETUP.md
```

## Variables de entorno (opcionales)

Ninguna requerida. La aplicación corre sin configuración adicional.

## Despliegue en Railway / Render

```bash
# Procfile para Railway
web: uvicorn src.main:app --host 0.0.0.0 --port $PORT
```

El startup time es < 1 segundo (todos los datos se cargan en memoria).
