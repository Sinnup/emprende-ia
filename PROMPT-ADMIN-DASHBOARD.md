# SEDECO MVP: Admin Dashboard Implementation

## Objective
Add a **password-protected Admin Dashboard** to track analytics:
- Request volume & trends
- Geographic distribution (Alcaldías, Colonias)
- Business types (Giros) performance
- Success factors & main blockers
- Actionable insights for SEDECO policy

---

## 📋 Task Checklist

- [ ] Load analytics-tracker.json data
- [ ] Add admin login page (password)
- [ ] Create admin sidebar toggle (User App ↔ Admin)
- [ ] Build Overview metrics (KPI cards)
- [ ] Build Geographic analysis (Alcaldías + Colonias)
- [ ] Build Business type analytics (Giros performance)
- [ ] Build Blocking factors analysis (Why businesses fail)
- [ ] Build Trends visualization (Daily requests, viability over time)
- [ ] Build Insights panel (Actionable recommendations)
- [ ] Add CSV export functionality
- [ ] Integrate tracking in user app (log every request)
- [ ] Test with 3 admin scenarios
- [ ] No performance impact on user app

---

## 🚀 Implementation Steps

### STEP 1: Load Analytics Data (2 mins)

In `app.py`, add to data loading section:

```python
# Load analytics tracker
with open(".claude/data/analytics-tracker.json") as f:
    ANALYTICS = json.load(f)
```

---

### STEP 2: Create Admin Login Page (5 mins)

After the initial title/header, add sidebar for app mode selection:

```python
# Sidebar app mode selection
st.sidebar.markdown("---")
st.sidebar.title("🔐 Control de Acceso")
app_mode = st.sidebar.radio(
    "Selecciona el modo",
    ["Evaluar Viabilidad", "Panel de Control (Admin)"]
)

if app_mode == "Panel de Control (Admin)":
    # Check if logged in
    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False
    
    if not st.session_state.admin_logged_in:
        st.warning("⚠️ Acceso restringido. Ingresa contraseña.")
        password = st.text_input("Contraseña de Admin", type="password")
        if st.button("Ingresar"):
            if password == "sedeco2026":  # Change this password
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("❌ Contraseña incorrecta")
        st.stop()
    
    # Admin dashboard code goes here (STEP 3+)
    admin_dashboard()

else:
    # Original user app code (existing)
    user_app()
```

---

### STEP 3: Restructure App into Functions (5 mins)

Wrap existing user app code in function:

```python
def user_app():
    """Original viability evaluation app"""
    # All existing code from current app.py
    # (form, viability check, results, heatmap, etc.)
    pass

def admin_dashboard():
    """Admin analytics dashboard"""
    # All admin code (steps 4-9)
    pass
```

---

### STEP 4: Build Overview Metrics (5 mins)

At top of `admin_dashboard()` function:

```python
st.title("📊 Panel de Control SEDECO")
st.subheader("Analytics de Evaluaciones de Viabilidad")

# KPI Metrics
col1, col2, col3, col4 = st.columns(4)

total_requests = ANALYTICS["metadata"]["total_requests"]
requests_today = ANALYTICS["metadata"]["requests_today"]
success_rate = calculate_success_rate()  # See helper functions below
avg_viability = calculate_avg_viability()

col1.metric("Total Evaluaciones", total_requests)
col2.metric("Hoy", requests_today)
col3.metric("Tasa de Éxito", f"{success_rate}%")
col4.metric("Viabilidad Promedio", f"{avg_viability:.1f}/100")

st.markdown("---")
```

---

### STEP 5: Geographic Analysis (8 mins)

```python
# Geographic Analysis
st.subheader("📍 Análisis Geográfico")

col1, col2 = st.columns(2)

with col1:
    st.write("**Top Alcaldías por Solicitudes**")
    alcaldias_data = ANALYTICS["aggregates"]["by_alcaldia"]
    
    # Sort by count descending
    top_alcaldias = sorted(
        [(k, v["count"], v["success_rate"]) for k, v in alcaldias_data.items()],
        key=lambda x: x[1],
        reverse=True
    )[:5]
    
    # Create dataframe for chart
    df_alcaldias = pd.DataFrame(
        top_alcaldias,
        columns=["Alcaldía", "Solicitudes", "Tasa de Éxito (%)"]
    )
    
    fig = px.bar(
        df_alcaldias,
        x="Solicitudes",
        y="Alcaldía",
        orientation="h",
        color="Tasa de Éxito (%)",
        color_continuous_scale="RdYlGn",
        title="Top 5 Alcaldías"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.write("**Top Colonias por Solicitudes**")
    colonias_data = ANALYTICS["aggregates"]["by_colonia"]
    
    top_colonias = sorted(
        [(k, v["count"], v["success_rate"]) for k, v in colonias_data.items()],
        key=lambda x: x[1],
        reverse=True
    )[:10]
    
    df_colonias = pd.DataFrame(
        top_colonias,
        columns=["Colonia", "Solicitudes", "Tasa de Éxito (%)"]
    )
    
    fig = px.bar(
        df_colonias,
        x="Solicitudes",
        y="Colonia",
        orientation="h",
        color="Tasa de Éxito (%)",
        color_continuous_scale="RdYlGn",
        title="Top 10 Colonias"
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
```

---

### STEP 6: Business Type Analytics (8 mins)

```python
st.subheader("🏢 Análisis de Giros Comerciales")

col1, col2 = st.columns(2)

with col1:
    st.write("**Volumen de Solicitudes por Giro**")
    business_data = ANALYTICS["aggregates"]["by_business_type"]
    
    top_businesses = sorted(
        [(k, v["count"]) for k, v in business_data.items()],
        key=lambda x: x[1],
        reverse=True
    )
    
    df_business = pd.DataFrame(
        top_businesses,
        columns=["Giro", "Solicitudes"]
    )
    
    fig = px.pie(
        df_business,
        values="Solicitudes",
        names="Giro",
        title="Distribución por Giro"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.write("**Tasa de Éxito por Giro (% ≥ 65)**")
    
    success_by_business = sorted(
        [(k, v["success_rate"]) for k, v in business_data.items()],
        key=lambda x: x[1],
        reverse=True
    )
    
    df_success = pd.DataFrame(
        success_by_business,
        columns=["Giro", "Tasa de Éxito (%)"]
    )
    
    fig = px.barh(
        df_success,
        x="Tasa de Éxito (%)",
        y="Giro",
        color="Tasa de Éxito (%)",
        color_continuous_scale="RdYlGn",
        title="Éxito por Giro (Mayor = Mejor)"
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
```

---

### STEP 7: Blocking Factors Analysis (5 mins)

```python
st.subheader("⚠️ Principales Obstáculos")

col1, col2 = st.columns(2)

with col1:
    st.write("**Factores Bloqueadores más Comunes**")
    blocking_data = ANALYTICS["aggregates"]["blocking_factors"]
    
    df_blocking = pd.DataFrame(
        [(k, v) for k, v in blocking_data.items()],
        columns=["Factor", "Frecuencia"]
    ).sort_values("Frecuencia", ascending=True)
    
    fig = px.barh(
        df_blocking,
        x="Frecuencia",
        y="Factor",
        color="Frecuencia",
        color_continuous_scale="Reds",
        title="Obstáculos que Impiden Viabilidad"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.write("**Desafíos Principales por Giro**")
    
    challenges_text = ""
    for giro, data in sorted(
        business_data.items(),
        key=lambda x: x[1]["count"],
        reverse=True
    )[:5]:
        if data["top_challenges"]:
            challenges = ", ".join(data["top_challenges"])
            challenges_text += f"**{giro}**: {challenges}\n\n"
    
    st.markdown(challenges_text)

st.markdown("---")
```

---

### STEP 8: Trends & Time Series (5 mins)

```python
st.subheader("📈 Tendencias")

col1, col2 = st.columns(2)

with col1:
    st.write("**Solicitudes Diarias (Últimos 7 días)**")
    daily_stats = ANALYTICS["daily_stats"]
    
    df_daily = pd.DataFrame(daily_stats)
    df_daily["date"] = pd.to_datetime(df_daily["date"])
    
    fig = px.line(
        df_daily,
        x="date",
        y="requests",
        markers=True,
        title="Volumen de Solicitudes",
        labels={"date": "Fecha", "requests": "Solicitudes"}
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.write("**Viabilidad Promedio (Últimos 7 días)**")
    
    fig = px.line(
        df_daily,
        x="date",
        y="avg_viability",
        markers=True,
        title="Viabilidad Promedio",
        labels={"date": "Fecha", "avg_viability": "Puntaje Promedio"}
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
```

---

### STEP 9: Actionable Insights (5 mins)

```python
st.subheader("💡 Insights y Recomendaciones para SEDECO")

insights = ANALYTICS["insights"]

col1, col2, col3 = st.columns(3)

with col1:
    st.info("### 🎯 Giros de Mayor Éxito\n" +
            "\n".join([f"• {b['type']}: {b['success_rate']}% - {b['recommendation']}"
                      for b in insights["top_success_businesses"]]))

with col2:
    st.error("### 🚨 Zonas de Mayor Riesgo\n" +
             "\n".join([f"• {z['alcaldia']}: {z['success_rate']}% - {z['recommendation']}"
                       for z in insights["highest_risk_zones"]]))

with col3:
    st.success("### ✨ Zonas de Oportunidad\n" +
               "\n".join([f"• {z['alcaldia']}: Crecimiento {z['growth_rate']}% - {z['recommendation']}"
                         for z in insights["opportunity_zones"]]))

st.markdown("---")
```

---

### STEP 10: Add CSV Export (3 mins)

```python
st.subheader("📥 Exportar Datos")

col1, col2 = st.columns(2)

with col1:
    if st.button("📊 Descargar Análisis Completo (JSON)"):
        json_str = json.dumps(ANALYTICS, indent=2, ensure_ascii=False)
        st.download_button(
            label="Descargar JSON",
            data=json_str,
            file_name="analytics_sedeco.json",
            mime="application/json"
        )

with col2:
    if st.button("📋 Descargar Solicitudes (CSV)"):
        df_requests = pd.DataFrame(ANALYTICS["requests"])
        csv = df_requests.to_csv(index=False)
        st.download_button(
            label="Descargar CSV",
            data=csv,
            file_name="solicitudes_sedeco.csv",
            mime="text/csv"
        )
```

---

### STEP 11: Add Request Tracking (5 mins)

In the `calculate()` function (where viability is computed), add tracking:

```python
# After calculating viability, before displaying results:
def track_request(business_type, zone_key, colonia_name, budget, space, viability_score, factors):
    """Log request to analytics tracker"""
    request = {
        "request_id": f"req_{len(ANALYTICS['requests']) + 1:05d}",
        "timestamp": datetime.datetime.now().isoformat() + "Z",
        "business_type": business_type,
        "alcaldia": zone_key,
        "colonia": colonia_name,
        "budget": budget,
        "space_sqm": space,
        "viability_score": int(viability_score),
        "viability_label": get_viability_label(viability_score),
        "capital_score": factors["capital"],
        "competition_score": factors["competition"],
        "location_score": factors["location"],
        "security_score": factors["security"],
        "growth_score": factors["growth"],
        "legal_score": factors["legal"],
        "blocking_factor": identify_blocking_factor(factors)
    }
    
    # Append to tracker
    ANALYTICS["requests"].append(request)
    ANALYTICS["metadata"]["total_requests"] += 1
    
    # Optional: save to file for persistence
    with open(".claude/data/analytics-tracker.json", "w") as f:
        json.dump(ANALYTICS, f, indent=2, ensure_ascii=False)
```

---

### STEP 12: Helper Functions (5 mins)

Add these functions outside main code:

```python
def calculate_success_rate():
    """Calculate % of evaluations with score ≥ 65"""
    if not ANALYTICS["requests"]:
        return 0
    successful = sum(1 for r in ANALYTICS["requests"] if r["viability_score"] >= 65)
    return round((successful / len(ANALYTICS["requests"])) * 100)

def calculate_avg_viability():
    """Calculate average viability score"""
    if not ANALYTICS["requests"]:
        return 0
    return sum(r["viability_score"] for r in ANALYTICS["requests"]) / len(ANALYTICS["requests"])

def identify_blocking_factor(factors):
    """Identify main blocker (lowest scoring factor)"""
    factor_names = ["Capital", "Competencia", "Ubicación", "Seguridad", "Crecimiento", "Legal"]
    factor_scores = [factors["capital"], factors["competition"], factors["location"],
                     factors["security"], factors["growth"], factors["legal"]]
    min_factor = min(factor_scores)
    if min_factor <= 3:
        return factor_names[factor_scores.index(min_factor)]
    return None

def get_viability_label(score):
    """Get label for viability score"""
    if score >= 80:
        return "Altamente Viable"
    elif score >= 65:
        return "Viable"
    elif score >= 50:
        return "Marginal"
    else:
        return "No Recomendado"
```

---

## 🧪 Testing (10 mins)

### Test 1: Admin Login
```
- Go to app
- Select "Panel de Control (Admin)"
- Try wrong password → should show error
- Try correct password (sedeco2026) → should show dashboard
```

### Test 2: Dashboard Displays Correctly
```
- Verify KPI cards show numbers
- Verify all 6 sections display (geographic, business, blocking, trends, insights, export)
- Verify charts render without errors
```

### Test 3: Request Tracking
```
- Go to "Evaluar Viabilidad"
- Make a request (Centro, Cuauhtémoc, Restaurante)
- Return to admin panel
- Verify total requests incremented
- Verify new request appears in data
```

---

## ✅ Success Criteria

After implementation:
- [ ] Admin login works (password protected)
- [ ] Overview metrics display (4 KPI cards)
- [ ] Geographic charts render (alcaldías + colonias)
- [ ] Business type analytics show (giros, success rates)
- [ ] Blocking factors chart displays
- [ ] Trends show over time (daily requests, avg viability)
- [ ] Insights panel with recommendations displays
- [ ] CSV/JSON export works
- [ ] Request tracking logs each user evaluation
- [ ] No errors in console
- [ ] Performance: Admin dashboard loads <2 seconds

---

## 📝 Notes

- Admin password is hardcoded (change in production)
- Analytics data persists in `.claude/data/analytics-tracker.json`
- All text is in Spanish (matches user app)
- Charts use Plotly (interactive)
- CSS/styling inherited from Streamlit defaults

---

## ⏱️ Time Estimate

- Admin login: 5 mins
- Overview metrics: 5 mins
- Geographic analysis: 8 mins
- Business analytics: 8 mins
- Blocking factors: 5 mins
- Trends: 5 mins
- Insights: 5 mins
- CSV export: 3 mins
- Request tracking: 5 mins
- Helper functions: 5 mins
- Testing: 10 mins
- **Total: 65 minutes**

---

Ready to implement? Copy this prompt and run it in Claude Code! 🚀

