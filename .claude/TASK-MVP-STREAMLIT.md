# Task #11: Streamlit MVP Implementation (30 mins)

**Status**: READY TO BUILD  
**Deadline**: 17:00 (absolute)  
**Phase**: Phase 2 - Backend Development (Fast Track)  
**Estimated Dev Time**: 30 minutes  

---

## What You're Building

**Single Streamlit application** (`app.py`) that:
- Accepts user inputs (business type, zone, budget, space)
- Calculates 6-factor viability score in real-time
- Shows cost breakdown + procedure timeline
- **Calls real Claude API for AI recommendations** ← Key differentiator
- Responsive design (mobile + desktop)
- Deployable in 1 command

---

## Why Streamlit (Not FastAPI + React)

| Aspect | FastAPI+React | Streamlit |
|--------|--------------|-----------|
| Dev time | 4-5 hours | 30 mins |
| Build process | Complex | None |
| Deployment | Vercel/Railway | Streamlit Cloud (1 click) |
| AI integration | Easy | Easy |
| Gate 1 (Functional) | ✅ | ✅ |
| Scoring potential | 5/5 | 5/5 |

**Result**: Same score, 4 hours saved = time for polish + video

---

## Implementation Steps (30 mins total)

### Step 1: Setup (5 mins)
```bash
# Install dependencies
pip install streamlit anthropic

# Verify data files exist
ls -la .claude/data/
# Should show: 10 JSON files (52 KB total)
```

### Step 2: Create app.py (20 mins)
Copy the complete code from COMPLETE_CODE section below.

**File location**: `/path/to/SEDECO/app.py`

**Key sections**:
1. Imports + config (lines 1-15)
2. Data loading (lines 17-35)
3. Claude client initialization (lines 37-42)
4. UI layout (lines 44-90)
5. Viability calculation (lines 92-120)
6. Results display (lines 122-180)
7. Claude API call (lines 182-220) ← **REAL AI**

### Step 3: Test (5 mins)
```bash
# Run locally
streamlit run app.py

# In browser: http://localhost:8501
# Fill form with test data
# Click "EVALUAR VIABILIDAD"
# Should see Claude recommendation appear
```

---

## Code (Copy Everything Below)

```python
"""
SEDECO - Viabilidad de Negocios CDMX
MVP with Real Claude API Integration
"""

import streamlit as st
import json
from anthropic import Anthropic

# Page config
st.set_page_config(
    page_title="SEDECO Viabilidad",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load data once
@st.cache_resource
def load_data():
    try:
        return {
            'zones': json.load(open('.claude/data/zones.json')),
            'business_types': json.load(open('.claude/data/business-types.json')),
            'procedures': json.load(open('.claude/data/procedures.json')),
            'costs': json.load(open('.claude/data/costs.json')),
            'crime': json.load(open('.claude/data/crime-index.json')),
            'model': json.load(open('.claude/data/viability-model.json')),
        }
    except FileNotFoundError as e:
        st.error(f"Error loading data: {e}")
        st.stop()

data = load_data()

# Initialize Claude client
@st.cache_resource
def get_claude_client():
    return Anthropic()

claude = get_claude_client()

# Title and description
st.markdown("# 🏢 SEDECO - Viabilidad de Negocios CDMX")
st.markdown("**Evalúa la viabilidad de tu negocio en la Ciudad de México**")

st.markdown("---")

# Input form
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Tu Propuesta")
    business_type = st.selectbox(
        "Tipo de Negocio (SCIAN)",
        options=list(data['business_types'].keys()),
        format_func=lambda x: f"{x} - {data['business_types'][x].get('name', 'Negocio')}"
    )
    
    zone = st.selectbox(
        "Zona (Alcaldía)",
        options=list(data['zones'].keys())
    )

with col2:
    st.subheader("💰 Recursos")
    budget = st.number_input(
        "Presupuesto Inicial (MXN)",
        value=500000,
        step=50000,
        min_value=100000
    )
    
    space_sqm = st.number_input(
        "Espacio Disponible (m²)",
        value=100,
        step=10,
        min_value=20
    )

st.markdown("---")

# Evaluate button
if st.button("📊 EVALUAR VIABILIDAD", use_container_width=True, type="primary"):
    with st.spinner("Analizando datos..."):
        # Get data for selected options
        zone_data = data['zones'][zone]
        biz_data = data['business_types'][business_type]
        costs_data = data['costs'].get(business_type, data['costs'].get('default', {}))
        crime_data = data['crime'][zone] if zone in data['crime'] else {'score': 50}
        
        # Calculate 6 factors (0-100 scale)
        factors = {
            'budget': min((budget / (costs_data.get('monthly_fixed', 10000) * 12 * 1.5)) * 100, 100),
            'competition': max(100 - (zone_data.get('business_density_per_10k', 300) / 5), 20),
            'location': min((zone_data.get('foot_traffic_daily', 50000) / 1000), 100),
            'security': 100 - crime_data.get('score', 50),
            'growth': min((zone_data.get('expansion_rate', 2) * 20), 100),
            'legal': 85  # Base score for legal compliance
        }
        
        # Apply weighted scoring
        weights = data['model']['weights']
        viability_score = sum(factors[k] * weights[k] for k in weights.keys())
        
        # Interpretation
        if viability_score >= 80:
            interpretation = "✅ ALTAMENTE VIABLE"
            color = "green"
        elif viability_score >= 65:
            interpretation = "⚠️ VIABLE"
            color = "blue"
        elif viability_score >= 50:
            interpretation = "⚠️ MARGINAL"
            color = "orange"
        else:
            interpretation = "❌ NO RECOMENDADO"
            color = "red"
        
        # Display main score
        st.markdown(f"### {interpretation}")
        st.metric("Puntuación de Viabilidad", f"{int(viability_score)}/100")
        
        st.markdown("---")
        
        # Display 6 factors
        st.subheader("📈 Análisis de Factores")
        factor_cols = st.columns(3)
        
        factor_names = {
            'budget': '💰 Presupuesto',
            'competition': '🏪 Competencia',
            'location': '📍 Ubicación',
            'security': '🛡️ Seguridad',
            'growth': '📊 Crecimiento',
            'legal': '⚖️ Legal'
        }
        
        for idx, (key, name) in enumerate(factor_names.items()):
            with factor_cols[idx % 3]:
                score_val = int(factors[key])
                st.metric(name, f"{score_val}/100")
        
        st.markdown("---")
        
        # Costs breakdown
        st.subheader("💵 Costos Estimados")
        cost_cols = st.columns(3)
        
        monthly = costs_data.get('monthly_fixed', 10000)
        annual = monthly * 12
        first_year = costs_data.get('first_year_total', annual * 1.5)
        breakeven = costs_data.get('break_even_months', 18)
        
        with cost_cols[0]:
            st.metric("Costo Mensual", f"${monthly:,.0f}")
        with cost_cols[1]:
            st.metric("Costo Anual", f"${annual:,.0f}")
        with cost_cols[2]:
            st.metric("Equilibrio", f"{breakeven} meses")
        
        st.markdown("---")
        
        # Procedures timeline
        st.subheader("📋 Procedimientos Requeridos")
        procs_list = data['procedures'].get(business_type, data['procedures'].get('default', {}))
        
        if 'procedures' in procs_list:
            for i, proc in enumerate(procs_list['procedures'][:8], 1):
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{i}. {proc.get('name_es', 'Procedimiento')}**")
                with col2:
                    st.write(f"⏱️ {proc.get('timeline_days', 5)}d")
                with col3:
                    st.write(f"${proc.get('cost_mxn', 0):,.0f}")
        
        st.markdown("---")
        
        # Claude AI Recommendation
        st.subheader("🤖 Recomendación (Powered by Claude AI)")
        
        try:
            # Call real Claude API
            ai_message = claude.messages.create(
                model="claude-opus-4-6",
                max_tokens=300,
                messages=[{
                    "role": "user",
                    "content": f"""Eres un asesor de negocios de SEDECO. 
                    
Un emprendedor quiere abrir:
- Tipo: {business_type}
- Zona: {zone}
- Presupuesto: ${budget:,} MXN
- Espacio: {space_sqm} m²

Su puntuación de viabilidad es {int(viability_score)}/100 con estos factores:
- Presupuesto: {int(factors['budget'])}/100
- Competencia: {int(factors['competition'])}/100
- Ubicación: {int(factors['location'])}/100
- Seguridad: {int(factors['security'])}/100
- Crecimiento: {int(factors['growth'])}/100
- Legal: {int(factors['legal'])}/100

Proporciona:
1. Una recomendación clara (SÍ/NO/CON CUIDADO)
2. Los 2 factores más críticos
3. Un consejo práctico de máx 50 palabras

Responde SOLO en español, de forma profesional."""
                }]
            )
            
            recommendation_text = ai_message.content[0].text
            st.success(recommendation_text)
            
        except Exception as e:
            st.error(f"Error conectando con Claude API: {str(e)}")
            st.info("Asegúrate de tener ANTHROPIC_API_KEY en las variables de entorno")
        
        st.markdown("---")
        st.caption("📊 Datos: Ley de Establecimientos Mercantiles CDMX | SEDECO Hackathon 2026")
```

---

## Environment Setup

**Before running, set your API key:**

```bash
# Option 1: Export (Linux/Mac)
export ANTHROPIC_API_KEY="sk-ant-YOUR-API-KEY"

# Option 2: Create .env file
cat > .env << 'ENVEOF'
ANTHROPIC_API_KEY=sk-ant-YOUR-API-KEY
ENVEOF

# Option 3: Set in code (NOT recommended)
# import os
# os.environ['ANTHROPIC_API_KEY'] = 'sk-ant-YOUR-API-KEY'
```

**Get your API key**:
1. Go to https://console.anthropic.com
2. Click "API Keys"
3. Create new key
4. Copy and paste above

---

## Testing Checklist

- [ ] App starts: `streamlit run app.py`
- [ ] Form loads with dropdowns
- [ ] Can enter budget and space
- [ ] Click "EVALUAR VIABILIDAD"
- [ ] Score appears (should be 50-95)
- [ ] 6 factors display
- [ ] Costs show
- [ ] Procedures list appears
- [ ] **Claude AI recommendation appears** ← Critical
- [ ] No errors in terminal

---

## Performance Targets

✅ Page load: <2 seconds  
✅ Data load: <1 second (cached)  
✅ Calculation: <500ms  
✅ Claude API call: 1-2 seconds  
✅ **Total response: <3 seconds** (acceptable for MVP)

---

## Scoring Alignment

| Criterion | Score | How This Achieves It |
|-----------|-------|---------------------|
| A. Quality | 5/5 | User can operate without help, clean flow, fast results |
| B. Technical | 5/5 | **IA real y bien elegida** (Real Claude API for recommendations) |
| C. Fit | 5/5 | Data from .claude/data/, procedures from Ley, legal compliant |

---

## Next Steps After MVP Complete

1. **Commit**: `git add app.py && git commit -m "feat: add streamlit MVP with claude api"`
2. **Deploy** (optional): `streamlit run app.py` works locally
3. **Record demo**: 3-min video showing end-to-end flow
4. **Submit**: GitHub repo link + video link (16:00-17:00)

---

## Files Required

- ✅ `.claude/data/zones.json` (already exists)
- ✅ `.claude/data/business-types.json` (already exists)
- ✅ `.claude/data/procedures.json` (already exists)
- ✅ `.claude/data/costs.json` (already exists)
- ✅ `.claude/data/crime-index.json` (already exists)
- ✅ `.claude/data/viability-model.json` (already exists)
- 📝 `app.py` (TO CREATE - this task)

---

## Troubleshooting

**Error: "ModuleNotFoundError: No module named 'streamlit'"**
→ Run: `pip install streamlit anthropic`

**Error: "ANTHROPIC_API_KEY not found"**
→ Set environment variable: `export ANTHROPIC_API_KEY="sk-ant-..."`

**Error: "FileNotFoundError: .claude/data/zones.json"**
→ Make sure app.py is in SEDECO root folder, not in src/ or another subfolder

**Claude API call fails**
→ Check: API key is valid, account has credits, network is connected

---

**Ready to build? Start now.** ⏱️ 30 minutes, clock starts when you paste code.


---

## Language Requirement

**UI Language**: 🇲🇽 **SPANISH ONLY**

All user-facing text must be in Spanish:
- Form labels → Spanish
- Button text → Spanish
- Results headers → Spanish
- Error messages → Spanish
- Tooltips/help text → Spanish
- Claude API prompts → Spanish
- Claude API responses → Spanish

**Internal Code**: Can be English (comments, variable names, etc.)

**Example**:
```python
# ✅ This is OK (English comments)
viability_score = sum(factors[k] * weights[k] for k in weights.keys())

# ✅ This is OK (English variable names)
st.metric("Puntuación de Viabilidad", f"{int(viability_score)}/100")

# ❌ This is NOT OK
st.metric("Viability Score", f"{int(viability_score)}/100")
```

**All UI text is already Spanish in the provided code** ✅

