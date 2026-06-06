# Admin Dashboard — Contexto Completo

**Feature**: Analytics & Admin Control Panel  
**Complexity**: Medium (45 minutes)  
**Impact**: Operational insights for SEDECO  
**Data**: Real-time tracking de consultas  

---

## 🎯 Objective

Provide SEDECO administrators with:
1. **Usage Metrics**: Total requests, trend over time
2. **Geographic Hotspots**: Alcaldías + Colonias más consultadas
3. **Business Analytics**: Giros (business types) más buscados
4. **Success Metrics**: Líneas de negocio que tienen mejor viabilidad
5. **Risk Analysis**: Principales obstáculos de emprendedores
6. **Actionable Insights**: Recomendaciones para política pública

---

## 📋 Admin Dashboard Sections

### 1. Overview Metrics (Top of Dashboard)

```
┌─────────────────┬─────────────────┬─────────────────┐
│  Total Requests │  Today Requests │  Success Rate   │
│       1,247     │       182       │      68%        │
└─────────────────┴─────────────────┴─────────────────┘

┌─────────────────┬─────────────────┬─────────────────┐
│ Avg Viability   │  High Viability │  Low Viability  │
│     68/100      │      34%        │      18%        │
└─────────────────┴─────────────────┴─────────────────┘
```

### 2. Geographic Analysis

**Top 5 Alcaldías by Requests**
```
Cuauhtémoc      ████████████ 35%
Benito Juárez   ████████ 24%
Miguel Hidalgo  █████ 15%
Coyoacán        ████ 12%
Álvaro Obregón  ███ 8%
```

**Top 10 Colonias by Requests**
```
Centro (Cuauhtémoc)      ████████ 12%
Polanco (Miguel Hidalgo) ██████ 9%
Roma Norte (Cuauhtémoc)  █████ 8%
Narvarte (Benito Juárez) ████ 6%
Pedregal (Álvaro Obregón) ███ 5%
... (top 10 list)
```

### 3. Business Type Analytics

**Top Giros by Request Volume**
```
Restaurante         ██████████ 25%
Consultoría         ███████ 18%
Tienda Retail       ██████ 15%
Café/Bar            █████ 12%
Servicios Tech      ████ 10%
Galería de Arte     ██ 8%
Hotel               ██ 7%
Farmacia            ██ 5%
```

**Success Rate by Giro** (% scoring 65+)
```
Servicios Tech      ██████████ 92%
Consultoría         █████████ 88%
Galería de Arte     ████████ 82%
Café/Bar            ███████ 78%
Restaurante         ██████ 68%
Farmacia            █████ 65%
Tienda Retail       ████ 52%
Hotel               ███ 45%
```

### 4. Success Factors Analysis

**Most Common Blockers for Failed Viability** (score <50)
```
Capital Insuficiente      ████████ 35%
Zona Muy Saturada         ███████ 28%
Seguridad Baja            █████ 18%
Tráfico Peatonal Bajo     ████ 12%
Incompatibilidad Legal    ███ 7%
```

**Success Factors** (score 65+)
```
Buen Capital               ████████ 38%
Tráfico Peatonal Alto      ███████ 32%
Baja Competencia           ██████ 28%
Seguridad Alta             █████ 24%
Zona en Crecimiento        ████ 19%
```

### 5. Trends Over Time

**Daily Requests (Last 7 Days)**
```
Monday:    240 requests
Tuesday:   268 requests
Wednesday: 251 requests
Thursday:  275 requests
Friday:    289 requests
Saturday:  185 requests
Sunday:    156 requests
```

**Viability Score Trend**
```
Week 1: Avg 66/100
Week 2: Avg 68/100
Week 3: Avg 71/100
Week 4: Avg 70/100
Trend: ↑ Improving
```

### 6. Actionable Insights Panel

**For SEDECO Policy**:
- "Iztapalapa has 18% of total requests but 32% failure rate → target subsidies"
- "Tech consulting: 92% success → promote in incubators"
- "Retail: most blocked by competition → suggest differentiation training"
- "Polanco saturated: 450 competitors/10k → consider zoning alternatives"

---

## 📊 Data Structure: analytics-tracker.json

```json
{
  "metadata": {
    "version": "1.0",
    "last_updated": "2026-06-06T18:45:00Z",
    "total_requests": 1247,
    "tracking_start": "2026-06-06T08:00:00Z"
  },
  "requests": [
    {
      "request_id": "req_001",
      "timestamp": "2026-06-06T09:15:30Z",
      "business_type": "Restaurante",
      "alcaldia": "Cuauhtémoc",
      "colonia": "Centro",
      "budget": 500000,
      "space_sqm": 100,
      "viability_score": 78,
      "viability_label": "Viable",
      "capital_score": 15,
      "competition_score": 3,
      "location_score": 20,
      "security_score": 10,
      "growth_score": 15,
      "legal_score": 15,
      "blocking_factor": null
    }
  ],
  "aggregates": {
    "by_alcaldia": {
      "Cuauhtémoc": {
        "count": 435,
        "pct": 34.8,
        "avg_viability": 71.2,
        "success_rate": 72.0
      },
      "Benito Juárez": {
        "count": 299,
        "pct": 23.9,
        "avg_viability": 69.5,
        "success_rate": 68.0
      }
    },
    "by_colonia": {
      "Centro (Cuauhtémoc)": {
        "count": 149,
        "pct": 11.9,
        "avg_viability": 74.8,
        "success_rate": 76.0
      }
    },
    "by_business_type": {
      "Restaurante": {
        "count": 311,
        "pct": 24.9,
        "avg_viability": 66.8,
        "success_rate": 68.0,
        "top_challenges": ["Competencia", "Capital", "Tráfico bajo"]
      },
      "Consultoría": {
        "count": 224,
        "pct": 17.9,
        "avg_viability": 81.5,
        "success_rate": 88.0
      }
    },
    "blocking_factors": {
      "Capital Insuficiente": 437,
      "Zona Saturada": 349,
      "Seguridad Baja": 224,
      "Tráfico Bajo": 149,
      "Legal": 88
    }
  },
  "insights": {
    "top_success_businesses": [
      {"type": "Servicios Tech", "success_rate": 92},
      {"type": "Consultoría", "success_rate": 88},
      {"type": "Galería de Arte", "success_rate": 82}
    ],
    "highest_risk": [
      {"alcaldia": "Iztapalapa", "risk_score": 85},
      {"alcaldia": "Gustavo A. Madero", "risk_score": 72}
    ],
    "opportunity_zones": [
      {"alcaldia": "Benito Juárez", "growth_potential": 85},
      {"alcaldia": "Coyoacán", "growth_potential": 78}
    ]
  }
}
```

---

## 🔧 Implementation Plan

### Phase 1: Data Collection (5 mins)
- Add tracking to each viability check
- Store request in `analytics_tracker` data structure
- Capture all 6 factor scores + blocking factors

### Phase 2: Admin Page (20 mins)
1. Create `/admin` route in Streamlit
2. Add authentication (simple password)
3. Add sidebar to toggle between "User App" and "Admin"
4. Display 6 sections (metrics, geography, business, success, trends, insights)

### Phase 3: Charts & Visualization (15 mins)
1. Implement Plotly charts for trends
2. Add Folium heatmap for geographic distribution
3. Create metric cards (KPIs)
4. Build downloadable CSV export

### Phase 4: Polish (5 mins)
- Error handling
- Real-time refresh
- Responsive design

---

## 🔐 Admin Authentication

```python
# Simple password-based access
ADMIN_PASSWORD = "sedeco_admin_2026"

if st.session_state.get("admin_logged_in"):
    # Show admin dashboard
else:
    password = st.text_input("Admin Password", type="password")
    if st.button("Login"):
        if password == ADMIN_PASSWORD:
            st.session_state.admin_logged_in = True
        else:
            st.error("Contraseña incorrecta")
```

---

## 📈 Key Metrics to Display

### KPI Cards
- **Total Requests**: Cumulative count
- **Today**: Requests in last 24h
- **Success Rate**: % scoring 65+
- **Avg Viability**: Mean score across all requests
- **Peak Alcaldía**: Most requested zone
- **Peak Giro**: Most requested business type

### Charts
1. **Requests by Alcaldía** — Horizontal bar chart
2. **Viability by Giro** — Success rate ranking
3. **Blocking Factors** — Pie chart of why businesses fail
4. **Trend** — Line chart of daily avg viability
5. **Geographic Heatmap** — Folium map colored by request density
6. **Time Series** — Requests over time (daily/hourly)

---

## 💾 Data Persistence

**Option 1: In-Memory** (current session only)
```python
if "analytics" not in st.session_state:
    st.session_state.analytics = load_analytics_from_json()
```

**Option 2: File-Based** (persistent across sessions)
```python
with open(".claude/data/analytics-tracker.json", "a") as f:
    json.dump(request_record, f)
```

**Recommendation**: File-based (more valuable for SEDECO long-term tracking)

---

## 🎯 Success Criteria

After implementation:
- ✅ Admin can log in with password
- ✅ See total requests + today's count
- ✅ View top 5 alcaldías + colonias
- ✅ See success rate by business type
- ✅ Identify main blockers
- ✅ See trend of viability scores
- ✅ Generate insights (policy recommendations)
- ✅ Export data as CSV
- ✅ No performance degradation on user app

---

## ⏱️ Time Estimate

- Data collection: 5 mins
- Admin page setup: 20 mins
- Charts/visualization: 15 mins
- Polish: 5 mins
- **Total: 45 minutes**

---

## 📝 Notes for Claude Code

- Admin dashboard should be separate page (not mixed with user app)
- Use same data as user app (don't duplicate)
- Authentication should be simple (this is hackathon, not production)
- Charts should be interactive (Plotly for clicking/filtering)
- CSV export for SEDECO to analyze offline

---

*Ready for implementation in Claude Code* 🚀

