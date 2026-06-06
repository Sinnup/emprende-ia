# Setup Guide — ViabilidadMX

**Tiempo**: ~5 minutos  
**Requisitos**: Python 3.11+, pip

---

## 1. Clonar Repositorio

```bash
git clone https://github.com/your-username/SEDECO.git
cd SEDECO
```

---

## 2. Crear Entorno Virtual (Recomendado)

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

---

## 3. Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 4. Ejecutar la Aplicación

```bash
streamlit run app.py
```

Abre tu navegador en: http://localhost:8501

---

## ✅ Quick Test

1. Select: Restaurante + Cuauhtémoc + Centro + $500k + 100m²
2. Click "Evaluar Viabilidad"
3. Should see: Viability score, costs breakdown, procedures, risk chart, competitor map

---

## Data Files (Auto-loaded)

All data is embedded in `.claude/data/`:
- business-types.json (9 SCIAN types)
- zones.json (16 CDMX alcaldías)
- procedures.json (10 RETYS procedures)
- costs.json (cost estimates)
- crime-index.json (security data)
- viability-model.json (6-factor scoring)
- competitors.json (100+ synthetic competitors)
- colonias.json (120+ neighborhoods)

---

**Ready to go.** 🚀
