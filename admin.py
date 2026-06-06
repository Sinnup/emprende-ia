"""
ViabilidadMX — Panel de Control Admin (SEDECO)
Analytics dashboard — cargado desde app.py
"""

import json
import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path

BASE = Path(__file__).parent

# ── Load / persist analytics ──────────────────────────────────────────────────
_ANALYTICS_PATH = BASE / "data" / "analytics-tracker.json"

@st.cache_resource
def _load_analytics():
    return json.loads(_ANALYTICS_PATH.read_text(encoding="utf-8"))

def get_analytics():
    return st.session_state.get("_analytics", _load_analytics())

def save_analytics(data):
    st.session_state["_analytics"] = data
    try:
        _ANALYTICS_PATH.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    except Exception:
        pass  # non-fatal if write fails

# ── Tracking helpers ──────────────────────────────────────────────────────────
def get_viability_label(score):
    if score >= 80: return "Altamente Viable"
    if score >= 65: return "Viable"
    if score >= 50: return "Marginal"
    return "No Recomendado"

def identify_blocking_factor(factors: dict):
    ordered = [("Capital", factors.get("budget",{}).get("score",15)),
               ("Competencia", factors.get("competition",{}).get("score",20)),
               ("Ubicación", factors.get("location",{}).get("score",20)),
               ("Seguridad", factors.get("security",{}).get("score",15)),
               ("Crecimiento", factors.get("growth",{}).get("score",15)),
               ("Legal", factors.get("legal",{}).get("score",15))]
    worst_name, worst_score = min(ordered, key=lambda x: x[1])
    return worst_name if worst_score <= 3 else None

def track_request(business_type_name: str, zone_name: str, colonia_name: str,
                  budget: float, sqm: float, score: int, factors: dict):
    data = get_analytics()
    req = {
        "request_id":        f"req_{len(data['requests'])+1:05d}",
        "timestamp":         datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "business_type":     business_type_name,
        "alcaldia":          zone_name,
        "colonia":           colonia_name or "",
        "budget":            budget,
        "space_sqm":         sqm,
        "viability_score":   score,
        "viability_label":   get_viability_label(score),
        "capital_score":     factors.get("budget",{}).get("score", 0),
        "competition_score": factors.get("competition",{}).get("score", 0),
        "location_score":    factors.get("location",{}).get("score", 0),
        "security_score":    factors.get("security",{}).get("score", 0),
        "growth_score":      factors.get("growth",{}).get("score", 0),
        "legal_score":       factors.get("legal",{}).get("score", 0),
        "blocking_factor":   identify_blocking_factor(factors),
    }
    data["requests"].append(req)
    data["metadata"]["total_requests"] = len(data["requests"])
    save_analytics(data)

# ── Dashboard helpers ─────────────────────────────────────────────────────────
def _success_rate(requests):
    if not requests: return 0
    return round(sum(1 for r in requests if r["viability_score"] >= 65) / len(requests) * 100)

def _avg_score(requests):
    if not requests: return 0
    return round(sum(r["viability_score"] for r in requests) / len(requests), 1)

TEAL    = "#104C42"
MAGENTA = "#88185B"
GOLD    = "#BC955C"
COLORS  = [TEAL, MAGENTA, GOLD, "#2E7D32", "#1565C0", "#6A1B9A", "#E65100", "#C62828", "#37474F"]

# ── Main dashboard ────────────────────────────────────────────────────────────
def render_admin_dashboard():
    data = get_analytics()
    reqs = data["requests"]

    st.markdown("""
    <style>
    .kpi-card { background:#fff; border-radius:12px; padding:1.1rem 1.4rem;
                box-shadow:0 2px 10px rgba(0,0,0,.08); text-align:center; }
    .kpi-val  { font-size:2.2rem; font-weight:900; color:#104C42; }
    .kpi-lbl  { font-size:.8rem; color:#6b7280; font-weight:600; text-transform:uppercase;
                letter-spacing:.5px; margin-top:.2rem; }
    .sec-title{ font-size:.75rem; font-weight:700; text-transform:uppercase;
                letter-spacing:1px; color:#88185B; margin:.5rem 0 .8rem; }
    </style>""", unsafe_allow_html=True)

    st.markdown("## 📊 Panel de Control — SEDECO ViabilidadMX")
    st.caption(f"Período: {data['metadata'].get('date_range','')} · "
               f"Actualizado: {data['metadata'].get('last_updated','')[:10]}")
    st.divider()

    # ── 1. KPI cards ──────────────────────────────────────────────────────────
    st.markdown('<div class="sec-title">Métricas de uso</div>', unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    today = datetime.date.today().isoformat()
    today_count = sum(1 for r in reqs if r["timestamp"][:10] == today)

    with k1: st.markdown(f'<div class="kpi-card"><div class="kpi-val">{len(reqs)}</div><div class="kpi-lbl">Evaluaciones totales</div></div>', unsafe_allow_html=True)
    with k2: st.markdown(f'<div class="kpi-card"><div class="kpi-val">{today_count}</div><div class="kpi-lbl">Hoy</div></div>', unsafe_allow_html=True)
    with k3: st.markdown(f'<div class="kpi-card"><div class="kpi-val">{_success_rate(reqs)}%</div><div class="kpi-lbl">Tasa de éxito (≥65)</div></div>', unsafe_allow_html=True)
    with k4: st.markdown(f'<div class="kpi-card"><div class="kpi-val">{_avg_score(reqs)}</div><div class="kpi-lbl">Viabilidad promedio</div></div>', unsafe_allow_html=True)

    st.divider()

    # ── 2. Geographic ─────────────────────────────────────────────────────────
    st.markdown('<div class="sec-title">📍 Análisis geográfico</div>', unsafe_allow_html=True)
    g1, g2 = st.columns(2)

    agg_alc = data["aggregates"]["by_alcaldia"]
    df_alc  = pd.DataFrame([
        {"Alcaldía": k, "Solicitudes": v["count"], "Éxito (%)": v["success_rate"]}
        for k, v in sorted(agg_alc.items(), key=lambda x: x[1]["count"], reverse=True)[:8]
    ])
    with g1:
        fig = px.bar(df_alc, x="Solicitudes", y="Alcaldía", orientation="h",
                     color="Éxito (%)", color_continuous_scale="RdYlGn",
                     title="Top alcaldías por solicitudes")
        fig.update_layout(height=320, margin=dict(l=5,r=5,t=35,b=5),
                          plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

    agg_col = data["aggregates"]["by_colonia"]
    df_col  = pd.DataFrame([
        {"Colonia": k, "Solicitudes": v["count"], "Éxito (%)": v["success_rate"]}
        for k, v in sorted(agg_col.items(), key=lambda x: x[1]["count"], reverse=True)[:10]
    ])
    with g2:
        fig = px.bar(df_col, x="Solicitudes", y="Colonia", orientation="h",
                     color="Éxito (%)", color_continuous_scale="RdYlGn",
                     title="Top colonias por solicitudes")
        fig.update_layout(height=320, margin=dict(l=5,r=5,t=35,b=5),
                          plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ── 3. Business type analytics ────────────────────────────────────────────
    st.markdown('<div class="sec-title">🏢 Análisis por giro comercial</div>', unsafe_allow_html=True)
    b1, b2 = st.columns(2)

    agg_bt = data["aggregates"]["by_business_type"]
    df_bt  = pd.DataFrame([
        {"Giro": k, "Solicitudes": v["count"], "Éxito (%)": v["success_rate"],
         "Puntaje promedio": v.get("avg_score", 0)}
        for k, v in agg_bt.items()
    ])
    with b1:
        fig = px.pie(df_bt, values="Solicitudes", names="Giro",
                     color_discrete_sequence=COLORS,
                     title="Distribución de solicitudes por giro")
        fig.update_layout(height=320, margin=dict(l=5,r=5,t=35,b=5))
        st.plotly_chart(fig, use_container_width=True)

    df_suc = df_bt.sort_values("Éxito (%)", ascending=True)
    with b2:
        fig = px.bar(df_suc, x="Éxito (%)", y="Giro", orientation="h",
                     color="Éxito (%)", color_continuous_scale="RdYlGn",
                     title="Tasa de éxito por giro (mayor = mejor)")
        fig.update_layout(height=320, margin=dict(l=5,r=5,t=35,b=5),
                          plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ── 4. Blocking factors ───────────────────────────────────────────────────
    st.markdown('<div class="sec-title">⚠️ Principales obstáculos</div>', unsafe_allow_html=True)
    bl1, bl2 = st.columns(2)

    blocking = data["aggregates"]["blocking_factors"]
    df_block = pd.DataFrame([
        {"Factor": k, "Frecuencia": v}
        for k, v in sorted(blocking.items(), key=lambda x: x[1])
    ])
    with bl1:
        fig = px.bar(df_block, x="Frecuencia", y="Factor", orientation="h",
                     color="Frecuencia", color_continuous_scale="Reds",
                     title="Factores que bloquean la viabilidad")
        fig.update_layout(height=280, margin=dict(l=5,r=5,t=35,b=5),
                          plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

    with bl2:
        st.markdown("**Principales desafíos por giro**")
        for giro, gdata in sorted(agg_bt.items(), key=lambda x: x[1]["count"], reverse=True)[:6]:
            challenges = gdata.get("top_challenges", [])
            if challenges:
                st.markdown(f"**{giro}**: {', '.join(challenges)}")
            else:
                st.markdown(f"**{giro}**: Sin bloqueos frecuentes")

    st.divider()

    # ── 5. Trends ─────────────────────────────────────────────────────────────
    st.markdown('<div class="sec-title">📈 Tendencias diarias</div>', unsafe_allow_html=True)
    t1, t2 = st.columns(2)

    df_daily = pd.DataFrame(data["daily_stats"])
    df_daily["date"] = pd.to_datetime(df_daily["date"])

    with t1:
        fig = px.line(df_daily, x="date", y="requests", markers=True,
                      title="Solicitudes por día",
                      labels={"date": "Fecha", "requests": "Solicitudes"},
                      color_discrete_sequence=[TEAL])
        fig.update_layout(height=280, margin=dict(l=5,r=5,t=35,b=5),
                          plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        fig = go.Figure()
        fig.add_scatter(x=df_daily["date"], y=df_daily["avg_viability"],
                        mode="lines+markers", name="Viabilidad promedio",
                        line=dict(color=GOLD, width=2.5), marker=dict(size=6))
        fig.add_hline(y=65, line_dash="dot", line_color="#dc2626",
                      annotation_text="Umbral viable (65)", annotation_position="right")
        fig.update_layout(height=280, margin=dict(l=5,r=5,t=35,b=5),
                          plot_bgcolor="white", paper_bgcolor="white",
                          title="Viabilidad promedio por día",
                          yaxis=dict(range=[40, 100]))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ── 6. Insights ───────────────────────────────────────────────────────────
    st.markdown('<div class="sec-title">💡 Insights y recomendaciones para SEDECO</div>', unsafe_allow_html=True)
    ins = data.get("insights", {})
    i1, i2, i3 = st.columns(3)

    with i1:
        lines = "\n".join(
            f"• **{b['type']}**: {b['success_rate']}%<br>{b['recommendation']}"
            for b in ins.get("top_success_businesses", [])
        )
        st.success(f"**🎯 Giros de mayor éxito**\n\n" +
                   "\n\n".join(f"• **{b['type']}**: {b['success_rate']}% éxito  \n{b['recommendation']}"
                               for b in ins.get("top_success_businesses", [])))

    with i2:
        st.error("**🚨 Zonas de mayor riesgo**\n\n" +
                 "\n\n".join(f"• **{z['alcaldia']}**: {z['success_rate']}% éxito  \n{z['recommendation']}"
                             for z in ins.get("highest_risk_zones", [])))

    with i3:
        st.info("**✨ Zonas de oportunidad**\n\n" +
                "\n\n".join(f"• **{z['alcaldia']}**: crecimiento {z['growth_rate']}%  \n{z['recommendation']}"
                            for z in ins.get("opportunity_zones", [])))

    st.divider()

    # ── 7. Export ─────────────────────────────────────────────────────────────
    st.markdown('<div class="sec-title">📥 Exportar datos</div>', unsafe_allow_html=True)
    e1, e2 = st.columns(2)

    with e1:
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        st.download_button("📊 Descargar análisis completo (JSON)", data=json_str,
                           file_name="analytics_sedeco.json", mime="application/json",
                           use_container_width=True)
    with e2:
        df_exp = pd.DataFrame(reqs)
        st.download_button("📋 Descargar solicitudes (CSV)", data=df_exp.to_csv(index=False),
                           file_name="solicitudes_sedeco.csv", mime="text/csv",
                           use_container_width=True)
