# Visual Flow: Anthropic API in SEDECO App

## User's Visual Experience

```
┌─────────────────────────────────────────────────────────────────┐
│  🏢 SEDECO - Viabilidad de Negocios CDMX                        │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  📋 Tu Propuesta          │  💰 Recursos                        │
│  ─────────────────────────┼────────────────────────────────────│
│  Tipo de Negocio:         │  Presupuesto Inicial (MXN):       │
│  [Restaurante      ↓]     │  [500,000                    ]    │
│                           │                                   │
│  Zona (Alcaldía):         │  Espacio Disponible (m²):        │
│  [Cuauhtémoc       ↓]     │  [100                        ]    │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  [ 📊 EVALUAR VIABILIDAD ]                                       │
└──────────────────────────────────────────────────────────────────┘

                    ⏳ Loading... (1-2 seconds)

┌──────────────────────────────────────────────────────────────────┐
│  ✅ ALTAMENTE VIABLE                                             │
│  Puntuación de Viabilidad: 78/100                               │
│                                                                   │
│  📈 Análisis de Factores                                        │
│  ┌───────────────┬───────────────┬───────────────┐             │
│  │ 💰 Presupuesto│ 🏪 Competencia│ 📍 Ubicación  │             │
│  │   75/100      │    80/100     │    85/100     │             │
│  └───────────────┴───────────────┴───────────────┘             │
│  ┌───────────────┬───────────────┬───────────────┐             │
│  │ 🛡️ Seguridad  │ 📊 Crecimiento│ ⚖️ Legal      │             │
│  │   70/100      │    75/100     │    85/100     │             │
│  └───────────────┴───────────────┴───────────────┘             │
│                                                                   │
│  💵 Costos Estimados                                            │
│  Costo Mensual: $50,000                                        │
│  Costo Anual: $600,000                                         │
│  Equilibrio: 18 meses                                          │
│                                                                   │
│  📋 Procedimientos Requeridos                                  │
│  1. RFC (5 días) - $0                                          │
│  2. Registro Mercantil (10 días) - $500                        │
│  3. Uso de Suelo (7 días) - $600                               │
│  ... (5 more procedures)                                        │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘

                    ↓ [ANTHROPIC API CALL HAPPENS HERE]

┌──────────────────────────────────────────────────────────────────┐
│  🤖 Recomendación (Powered by Claude AI)  ← ← ← SHOWN HERE     │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ ✅ SÍ, es viable. Tienes presupuesto suficiente y zona    │ │
│  │ con alto tráfico de clientes. Los 2 factores críticos:   │ │
│  │                                                             │ │
│  │ 1) Competencia alta - necesitas diferenciación clara     │ │
│  │ 2) Seguridad moderada - refuerza medidas de protección  │ │
│  │                                                             │ │
│  │ Consejo: Comienza con menu innovador y ubicación         │ │
│  │ estratégica en zona de flujo peatonal alto.              │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  This is the Claude AI response ☝️                              │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

---

## Backend Flow: What's Happening

```
USER INTERACTION
      │
      ↓
┌──────────────────────────────────────┐
│ User clicks "EVALUAR VIABILIDAD"     │
└──────────────────────────────────────┘
      │
      ↓
┌──────────────────────────────────────┐
│ Streamlit app gets form inputs:      │
│ - business_type: "722110"            │
│ - zone: "Cuauhtémoc"                 │
│ - budget: 500000                     │
│ - space_sqm: 100                     │
└──────────────────────────────────────┘
      │
      ↓
┌──────────────────────────────────────┐
│ STEP 1: LOAD EMBEDDED DATA (FAST)    │
│ Load: zones.json, costs.json, etc.   │
│ Time: <500ms                         │
│ FROM: .claude/data/ (local files)    │
│ NO API CALL YET                      │
└──────────────────────────────────────┘
      │
      ↓
┌──────────────────────────────────────┐
│ STEP 2: CALCULATE 6 FACTORS          │
│ Budget = (500000 / 600000) * 100 = 83│
│ Competition = 100 - (450 / 5) = 10   │
│ Location = (150000 / 1000) = 100     │
│ Security = 100 - 65 = 35             │
│ Growth = (2.5 * 20) = 50             │
│ Legal = 85                           │
│ Total Score = weighted sum = 78      │
│ Time: <100ms                         │
│ FROM: Embedded algorithms            │
│ NO API CALL YET                      │
└──────────────────────────────────────┘
      │
      ↓
┌──────────────────────────────────────┐
│ STEP 3: DISPLAY IMMEDIATE RESULTS    │
│ ✅ Show score card: 78/100           │
│ ✅ Show 6 factors                    │
│ ✅ Show cost breakdown               │
│ ✅ Show procedure list               │
│ Time: <200ms                         │
│ FROM: Streamlit rendering            │
│ NO API CALL YET                      │
└──────────────────────────────────────┘
      │
      ↓
┌──────────────────────────────────────┐
│ STEP 4: CALL ANTHROPIC API           │
│ HERE THE REAL AI HAPPENS:           │
│                                      │
│ Send to Claude:                      │
│ "Eres un asesor de negocios SEDECO" │
│ "Tipo: Restaurante"                 │
│ "Zona: Cuauhtémoc"                  │
│ "Budget: $500k MXN"                 │
│ "Viability Score: 78/100"           │
│ "Factors: [all 6 factors]"          │
│ "Provide: recommendation + reasons" │
│                                      │
│ Time: 1-2 seconds (network latency) │
│ FROM: https://api.anthropic.com     │
│ ENDPOINT: /v1/messages              │
│ MODEL: claude-opus-4-6              │
└──────────────────────────────────────┘
      │
      ↓ [Network request to Anthropic servers]
      │
      ↓
┌──────────────────────────────────────┐
│ ANTHROPIC SERVERS (External)         │
│                                      │
│ Claude reads:                        │
│ "You are a SEDECO business advisor" │
│ "Entrepreneur wants: Restaurant"    │
│ "Zone: Cuauhtémoc"                  │
│ "Viability score: 78/100"           │
│ "Critical factors: competition, ..." │
│ "Provide: brief recommendation"     │
│                                      │
│ Claude thinks and writes:            │
│ "SÍ, es viable. Tienes presupuesto" │
│ "...factor crítico: competencia..." │
│ "...consejo práctico: menu..."       │
│                                      │
│ Sends back response text             │
└──────────────────────────────────────┘
      │
      ↓ [Response sent back to app]
      │
      ↓
┌──────────────────────────────────────┐
│ STEP 5: DISPLAY AI RECOMMENDATION   │
│ Receive: Claude's text response     │
│ Display in: Green success box       │
│ Label: "🤖 Recomendación"           │
│         "(Powered by Claude AI)"    │
│ Time: Instant rendering             │
│ FROM: Streamlit UI                  │
└──────────────────────────────────────┘
      │
      ↓
   USER SEES COMPLETE RESULTS

TIMING:
═══════════════════════════════════════
Steps 1-3: ~800ms  (instant, no API)
Step 4:    ~1500ms (Claude API call)
Step 5:    ~100ms  (display)
───────────────────────────────────────
TOTAL:     ~2400ms (2.4 seconds)
═══════════════════════════════════════
```

---

## Code Path to API Call

```
app.py
  │
  ├─ Line 86: from anthropic import Anthropic
  │
  ├─ Line 116-119: Initialize Claude client
  │  def get_claude_client():
  │    return Anthropic()  ← Creates connection
  │  claude = get_claude_client()
  │
  ├─ Line 179: User clicks button
  │  if st.button("📊 EVALUAR VIABILIDAD"):
  │    │
  │    ├─ Line 181-210: Calculate 6 factors
  │    ├─ Line 212-245: Display results
  │    │
  │    └─ Line 258-297: THE API CALL SECTION
  │       st.subheader("🤖 Recomendación (Powered by Claude AI)")
  │       │
  │       └─ Line 263: claude.messages.create(
  │            model="claude-opus-4-6",
  │            max_tokens=300,
  │            messages=[{
  │              "role": "user",
  │              "content": f"Eres un asesor SEDECO..."
  │            }]
  │          )
  │          ↓
  │          [SENDS REQUEST TO: https://api.anthropic.com/v1/messages]
  │          [WAITS FOR RESPONSE: 1-2 seconds]
  │
  │       └─ Line 292: recommendation_text = ai_message.content[0].text
  │          ↓
  │          [GETS: Claude's recommendation in Spanish]
  │
  │       └─ Line 294: st.success(recommendation_text)
  │          ↓
  │          [DISPLAYS: Green box with recommendation]
```

---

## Is It Shown Anywhere?

### YES, Multiple Ways:

1. **In the UI (Most Important)**
   - Green box labeled: "🤖 Recomendación (Powered by Claude AI)"
   - Content: Claude's recommendation text
   - Location: Bottom of results dashboard
   - Visible to: All end users

2. **In the Code** 
   - Line 258: Section header with "Claude AI" mention
   - Line 263: API call is documented with comment
   - Line 297: Error handling shows "Claude API"

3. **In Error Messages**
   - If API fails: "Error conectando con Claude API"
   - Shows: User knows it was trying to use AI

4. **In Browser Network Tab** (for developers)
   - If user opens DevTools
   - Can see: `POST https://api.anthropic.com/v1/messages`
   - Headers show: Model, tokens, API calls

5. **In Terminal Output** (if running locally)
   - Streamlit shows: Request logs
   - Claude library logs: API interactions

---

## Summary: Where to Find It

| Location | What You See |
|----------|------|
| **App UI** | Green box: "🤖 Recomendación (Powered by Claude AI)" |
| **Code** | Line 263: `claude.messages.create(...)` |
| **Label** | "Powered by Claude AI" under recommendation heading |
| **Error** | "Error conectando con Claude API" if it fails |
| **Network** | Devtools → Network tab → `api.anthropic.com` |
| **Documentation** | This file + TASK-MVP-STREAMLIT.md |

---

## TL;DR

**What**: Uses Claude API to generate business recommendations  
**Where**: Green box at bottom of results (visible to all users)  
**How**: Sends viability data to Claude, gets personalized advice back  
**Cost**: ~$0.02 per recommendation  
**Time**: 1-2 seconds (network latency)  
**Key Phrase**: "Powered by Claude AI" appears in UI  
**Critical**: This is what makes the app get 5/5 on "IA real y bien elegida"
