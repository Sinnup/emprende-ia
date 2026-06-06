"""
ViabilidadMX — SEDECO Reto 2
Evaluador de Viabilidad de Negocios para la Ciudad de México
Hackathon SecretarIA 2026
"""

import json
import os
from pathlib import Path
import streamlit as st
from anthropic import Anthropic
import markdown as md_lib
from admin import render_admin_dashboard, track_request, get_analytics

# Load API key from secrets.properties if not already in environment
def _load_secrets():
    secrets_path = Path(__file__).parent / ".claude" / "secrets.properties"
    if secrets_path.exists():
        for line in secrets_path.read_text().splitlines():
            if "=" in line and not line.strip().startswith("#"):
                _, value = line.split("=", 1)
                key = value.strip()
                if key.startswith("sk-ant-"):
                    os.environ.setdefault("ANTHROPIC_API_KEY", key)

_load_secrets()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ViabilidadMX — SEDECO CDMX",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""<style>
#MainMenu, footer, header { visibility: hidden; }
div[data-testid="stDecoration"] { display: none; }
.block-container { padding-top: 1.5rem !important; max-width: 1100px; }

/* Hero */
.hero {
    background: linear-gradient(135deg, #104C42 0%, #235B4E 100%);
    border-radius: 16px; padding: 2rem 2.5rem; margin-bottom: 1.5rem; color: #fff;
}
.hero h1 { font-size: 2rem; font-weight: 900; margin: 0 0 .5rem; line-height: 1.2; }
.hero p  { opacity: .85; margin: 0; font-size: .95rem; }

/* Score banner */
.score-box {
    border-radius: 16px; padding: 1.5rem 2rem; color: #fff;
    margin-bottom: 1.25rem; display: flex; align-items: center; gap: 2rem;
}
.score-alta     { background: linear-gradient(135deg,#14532d,#16a34a); }
.score-viable   { background: linear-gradient(135deg,#631135,#88185B); }
.score-marginal { background: linear-gradient(135deg,#7c2d12,#ea580c); }
.score-no       { background: linear-gradient(135deg,#7f1d1d,#dc2626); }
.score-num   { font-size: 4rem; font-weight: 900; line-height: 1; }
.score-info  { flex: 1; }
.score-label { font-size: 1.3rem; font-weight: 700; }
.score-rec   { font-size: .9rem; opacity: .85; margin-top: .3rem; }
.score-prob  { font-size: .78rem; opacity: .65; margin-top: .4rem; }

/* Cards — COMPLETE self-contained divs only */
.vx-card {
    background: #fff; border-radius: 14px; padding: 1.25rem 1.4rem;
    box-shadow: 0 2px 12px rgba(0,0,0,.08); margin-bottom: 1rem;
    color: #1f2937;
}
.vx-title {
    font-size: .72rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1px; color: #88185B; margin-bottom: 1rem;
    border-bottom: 1px solid #EDE0E8; padding-bottom: .5rem;
}

/* Factor bars */
.f-row   { margin-bottom: .7rem; }
.f-head  { display: flex; justify-content: space-between; font-size: .83rem; margin-bottom: 3px; }
.f-name  { font-weight: 600; color: #1f2937; }
.f-stat  { color: #6b7280; font-size: .78rem; }
.bar-bg  { height: 8px; background: #e5e7eb; border-radius: 4px; overflow: hidden; margin-bottom: 2px; }
.bar-fill{ height: 100%; border-radius: 4px; }
.f-det   { font-size: .71rem; color: #9ca3af; }

/* Cost rows */
.c-sec { font-size: .68rem; font-weight: 700; text-transform: uppercase;
         letter-spacing: .8px; color: #88185B; margin: .8rem 0 .3rem; }
.c-row { display: flex; justify-content: space-between; align-items: center;
         padding: .38rem 0; border-bottom: 1px solid #f3f4f6; font-size: .83rem;
         color: #1f2937; }
.c-row:last-child { border: none; }
.c-val { font-weight: 700; color: #1f2937; }

/* Zone rows */
.z-row { display: flex; align-items: center; gap: .5rem;
         padding: .38rem 0; border-bottom: 1px solid #f3f4f6; font-size: .82rem;
         color: #1f2937; }
.z-row:last-of-type { border: none; }
.z-lbl { color: #6b7280; flex: 1; }
.z-val { font-weight: 700; color: #1f2937; }
.z-tag { display: inline-block; background: #EDE0E8; color: #104C42;
         border-radius: 20px; padding: 2px 10px; font-size: .7rem;
         font-weight: 600; margin: 2px; }

/* Procedure steps */
.p-step { display: flex; gap: .9rem; margin-bottom: 1rem; align-items: flex-start; }
.p-dot  { width: 32px; height: 32px; border-radius: 50%; color: #fff;
          font-weight: 800; display: flex; align-items: center;
          justify-content: center; flex-shrink: 0; font-size: .82rem; }
.p-name { font-weight: 700; font-size: .88rem; margin-bottom: .15rem; }
.p-meta { font-size: .76rem; color: #6b7280; }

/* AI box */
.ai-box { background: #fdf0f6; border-left: 4px solid #88185B;
          border-radius: 12px; padding: 1.1rem 1.4rem; color: #1f2937;
          font-size: .9rem; line-height: 1.7; }
.ai-box h1, .ai-box h2, .ai-box h3 { color: #88185B; margin: .7rem 0 .3rem; font-size: 1rem; }
.ai-box strong { color: #631135; }
.ai-box ul, .ai-box ol { padding-left: 1.2rem; margin: .4rem 0; }
.ai-box li { margin-bottom: .25rem; }
.ai-box p  { margin: .4rem 0; }
</style>""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
BASE = Path(__file__).parent

@st.cache_resource
def load_data():
    d = BASE / "data"
    return {
        "business_types": json.loads((d / "business-types.json").read_text())["business_types"],
        "zones":          json.loads((d / "zones.json").read_text())["zones"],
        "procedures":     json.loads((d / "procedures.json").read_text()),
        "costs":          json.loads((d / "costs.json").read_text())["costs"],
        "crime":          json.loads((d / "crime-index.json").read_text()),
        "model":          json.loads((d / "viability-model.json").read_text()),
        "competitors":    json.loads((d / "competitors.json").read_text()),
        "colonias":       json.loads((d / "colonias.json").read_text()),
    }

@st.cache_resource
def get_claude():
    return Anthropic()

DATA  = load_data()
claude = get_claude()

# ── Constants ─────────────────────────────────────────────────────────────────
FACTOR_NAMES = {
    "budget":      "💰 Capital Disponible",
    "competition": "🏪 Saturación de Mercado",
    "location":    "📍 Tráfico Peatonal",
    "security":    "🛡️ Seguridad de Zona",
    "growth":      "📈 Crecimiento Económico",
    "legal":       "⚖️ Factibilidad Regulatoria",
}
COST_LABELS = {
    "rent": "Renta", "utilities": "Servicios", "permits": "Permisos",
    "insurance": "Seguro", "labor_base": "Nómina base", "supplies": "Insumos",
}
AGENCY_COLORS = {
    "sat": "#1565C0", "comercio": "#6A1B9A", "seduvi": "#2E7D32",
    "ventanilla": "#E65100", "sedema": "#00695C", "salud": "#C62828",
    "imss": "#1B5E20", "seguro": "#37474F",
}

# ── Helpers ───────────────────────────────────────────────────────────────────
def agency_key(agency):
    MAP = {"SAT": "sat", "Cámara": "comercio", "SEDUVI": "seduvi",
           "Delegación": "ventanilla", "Ventanilla": "ventanilla",
           "SIAPEM": "sedema", "Secretaría de Salud": "salud", "IMSS": "imss"}
    for k, v in MAP.items():
        if k in agency:
            return v
    return "seguro"

def bar_color(pct):
    return "#16a34a" if pct >= 75 else "#d97706" if pct >= 50 else "#dc2626"

def haversine_km(lat1, lon1, lat2, lon2):
    import math
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))

def get_sequence(btype):
    food, office = {"722110", "722210"}, {"551020"}
    seqs = DATA["procedures"]["procedure_sequences"]
    return seqs["restaurant"] if btype in food else seqs["oficina"] if btype in office else seqs["tienda_retail"]

# ── Scoring ───────────────────────────────────────────────────────────────────
def calculate(btype, zone_key, budget, sqm, colonia_data=None):
    bt    = DATA["business_types"][btype]
    z     = DATA["zones"][zone_key]
    costs = DATA["costs"].get(btype)
    crime = DATA["crime"]["crime_by_zone"].get(zone_key, {})
    m     = DATA["model"]["factors"]

    # Override zone-level metrics with colonia-specific data if available
    rental_sqm_annual = colonia_data["rental_cost_sqm_annual"] if colonia_data else z["rental_cost_sqm_annual"]
    foot_traffic_val  = colonia_data["foot_traffic_daily"]      if colonia_data else z["foot_traffic_daily"]
    crime_index_val   = colonia_data["crime_index"]             if colonia_data else crime.get("overall", 50)

    rental_monthly = round(rental_sqm_annual * sqm / 12)

    if costs:
        bkdown = dict(costs["monthly_fixed"])
        bkdown["rent"] = rental_monthly
        mf = sum(bkdown.values())
        fy = mf * 12 + costs["procedure_costs"] + costs["initial_setup"]
        pc, ins, be, rev = costs["procedure_costs"], costs["initial_setup"], costs["break_even_months"], costs["estimated_revenue_monthly"]
    else:
        bkdown = {"rent": rental_monthly, "utilities": 300, "permits": 100, "insurance": 200, "labor_base": bt["monthly_fixed"], "supplies": 150}
        mf = sum(bkdown.values())
        pc, ins = 2500, round(bt["startup_capital"] * 0.1)
        fy = mf * 12 + pc + ins
        be, rev = 8, mf * 2

    if budget >= fy:          bs, bst = m["budget"]["scoring"]["sufficient"],   "Suficiente"
    elif budget >= fy * 0.8:  bs, bst = m["budget"]["scoring"]["marginal"],     "Marginal"
    else:                      bs, bst = m["budget"]["scoring"]["insufficient"], "Insuficiente"

    # ENHANCEMENT: Space Adequacy Penalty
    space_penalty = 1.0
    if sqm < 50:    space_penalty = 0.80   # Too small: -20%
    elif sqm < 60:  space_penalty = 0.85   # Small: -15%
    elif sqm > 300: space_penalty = 0.70   # Too large: -30%
    elif sqm > 200: space_penalty = 0.80   # Large: -20%
    bs = round(bs * space_penalty)

    dens = z["business_density_per_10k"]
    if dens < 20:    cs, cst = m["competition"]["scoring"]["low"],       "Baja"
    elif dens < 50:  cs, cst = m["competition"]["scoring"]["medium"],    "Media"
    elif dens < 100: cs, cst = m["competition"]["scoring"]["high"],      "Alta"
    else:            cs, cst = m["competition"]["scoring"]["very_high"], "Muy Alta"

    ft = foot_traffic_val
    if ft > 5000:   ls, lst = m["location"]["scoring"]["high"],   "Alto"
    elif ft > 2000: ls, lst = m["location"]["scoring"]["medium"], "Medio"
    else:           ls, lst = m["location"]["scoring"]["low"],    "Bajo"

    ci = crime_index_val
    if ci < 40:   ss, sst = m["security"]["scoring"]["low"],    "Bajo"
    elif ci < 70: ss, sst = m["security"]["scoring"]["medium"], "Medio"
    else:         ss, sst = m["security"]["scoring"]["high"],   "Alto"

    gr = z["population_growth_annual"]
    if gr > 0.02:   gs, gst = m["growth"]["scoring"]["growing"],  "Creciendo"
    elif gr > 0.01: gs, gst = m["growth"]["scoring"]["stable"],   "Estable"
    else:           gs, gst = m["growth"]["scoring"]["declining"],"Declive"

    legal = m["legal"]["scoring"]["all_attainable"]

    procs = [DATA["procedures"]["procedures"].get(k, {}) for k in get_sequence(btype)]
    tdays = bt.get("procedures_days", sum(p.get("timeline_days", 0) for p in procs))
    tcost = sum(p.get("cost_mxn", 0) for p in procs)
    total = bs + cs + ls + ss + gs + legal

    cf, cumul, vr = [], -(pc + ins), bt.get("variable_ratio", 0.35)
    for mo in range(1, 13):
        r = rev * (1 + 0.04 * (mo-1) / 12)
        c = mf + r * vr
        cumul += r - c
        cf.append({"Mes": mo, "Ingresos": round(r), "Costos": round(c), "Saldo acumulado": round(cumul)})

    return {
        "score": total,
        "label": "Altamente Viable" if total>=80 else "Viable" if total>=65 else "Marginal" if total>=50 else "No Recomendado",
        "cls":   "alta"             if total>=80 else "viable" if total>=65 else "marginal" if total>=50 else "no",
        "rec":   ("Adelante con confianza — base sólida." if total>=80
                  else "Procede monitoreando riesgos." if total>=65
                  else "Requiere planeación cuidadosa." if total>=50
                  else "Reconsiderar zona o giro."),
        "prob":  bt.get("success_rate", 0.65),
        "factors": {
            "budget":      {"score": bs,    "max": 15, "status": bst,  "detail": f"${budget:,.0f} vs ${fy:,.0f} año 1"},
            "competition": {"score": cs,    "max": 20, "status": cst,  "detail": f"{dens} negocios/10k hab."},
            "location":    {"score": ls,    "max": 20, "status": lst,  "detail": f"{ft:,} peatones/día"},
            "security":    {"score": ss,    "max": 15, "status": sst,  "detail": f"Criminalidad {ci}/100"},
            "growth":      {"score": gs,    "max": 15, "status": gst,  "detail": f"Crecimiento {gr*100:.1f}%/año"},
            "legal":       {"score": legal, "max": 15, "status": "Alcanzable", "detail": f"{len(procs)} trámites ~{tdays} días"},
        },
        "costs": {"proc_costs": pc, "initial_setup": ins, "monthly_fixed": mf, "breakdown": bkdown,
                  "first_year": round(fy), "break_even": be, "runway": round(budget/mf, 1),
                  "revenue_monthly": rev, "rental_monthly": rental_monthly, "sqm": sqm},
        "procedures": procs, "tdays": tdays, "tcost": tcost,
        "zone": z, "cashflow": cf,
        "colonia": colonia_data,
    }

# ── Hero ──────────────────────────────────────────────────────────────────────
# ── Sidebar navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🏙️ ViabilidadMX")
    st.divider()
    app_mode = st.radio("Modo", ["🔍 Evaluar Viabilidad", "📊 Panel Admin"], label_visibility="collapsed")

    if app_mode == "📊 Panel Admin":
        if not st.session_state.get("admin_ok"):
            st.divider()
            pwd = st.text_input("Contraseña", type="password")
            if st.button("Ingresar", use_container_width=True):
                if pwd == "sedeco2026":
                    st.session_state["admin_ok"] = True
                    st.rerun()
                else:
                    st.error("Contraseña incorrecta")

# ── Admin mode ────────────────────────────────────────────────────────────────
if app_mode == "📊 Panel Admin":
    if not st.session_state.get("admin_ok"):
        st.warning("🔐 Ingresa la contraseña en el panel lateral para acceder.")
        st.stop()
    render_admin_dashboard()
    st.stop()

# ── User app ──────────────────────────────────────────────────────────────────
st.markdown("""<div class="hero">
    <h1>🏙️ ViabilidadMX — SEDECO CDMX</h1>
    <p>Evalúa en segundos la viabilidad de tu negocio en la Ciudad de México.<br>
       Basado en datos reales del RETYS y la Ley de Establecimientos Mercantiles 2024.</p>
</div>""", unsafe_allow_html=True)

# ── Form ──────────────────────────────────────────────────────────────────────
BTYPE_OPTS = {k: v["name_es"] for k, v in DATA["business_types"].items()}
ZONE_OPTS  = {k: v["name"]    for k, v in DATA["zones"].items()}

col1, col2 = st.columns(2, gap="large")
with col1:
    st.markdown("#### 🏢 Negocio y zona")
    btype    = st.selectbox("Giro SCIAN", list(BTYPE_OPTS), format_func=lambda k: BTYPE_OPTS[k])
    zone_key = st.selectbox("Alcaldía",   list(ZONE_OPTS),  format_func=lambda k: ZONE_OPTS[k])

    # Colonia selector — filtered by zone, resets when zone changes
    _zone_name     = ZONE_OPTS[zone_key]
    _colonias_list = DATA["colonias"].get(_zone_name, {}).get("colonias", [])
    _colonia_opts  = ["— Alcaldía completa —"] + [c["name"] for c in _colonias_list]
    colonia_label  = st.selectbox(
        "Colonia", options=_colonia_opts,
        key=f"colonia_{zone_key}",
        help="Datos específicos por colonia: renta, tráfico y criminalidad más precisos"
    )
    colonia_data = next((c for c in _colonias_list if c["name"] == colonia_label), None)
with col2:
    st.markdown("#### 💰 Recursos")
    budget = st.number_input("Capital disponible (MXN)", value=200_000, step=10_000, min_value=10_000, format="%d")
    sqm    = st.number_input("Superficie del local (m²)", value=80, step=5, min_value=5, max_value=9999)
    entity = st.radio("Tipo de persona", ["Persona Física", "Persona Moral (S.A./S. de R.L.)"], horizontal=True)

st.divider()
go = st.button("🔍 Evaluar Viabilidad del Negocio", use_container_width=True, type="primary")

# ── On button click: compute R immediately and cache (Claude called later) ─────
if go:
    with st.spinner("Calculando con datos del RETYS y SEDUVI…"):
        R = calculate(btype, zone_key, budget, sqm, colonia_data)
    st.session_state["R"]             = R
    st.session_state["claude_text"]   = None
    st.session_state["claude_error"]  = None
    st.session_state["needs_claude"]  = True
    st.session_state["entity"]        = entity
    st.session_state["btype"]         = btype
    st.session_state["zone_key"]      = zone_key
    st.session_state["budget"]        = budget
    st.session_state["colonia_label"] = colonia_label

    # Track this evaluation in the analytics log
    track_request(
        business_type_name = BTYPE_OPTS[btype],
        zone_name          = ZONE_OPTS[zone_key],
        colonia_name       = colonia_label if colonia_data else "",
        budget             = budget,
        sqm                = sqm,
        score              = R["score"],
        factors            = R["factors"],
    )

# ── Guard: nothing computed yet ───────────────────────────────────────────────
if "R" not in st.session_state:
    st.stop()

R        = st.session_state["R"]
entity   = st.session_state["entity"]
btype    = st.session_state["btype"]
zone_key = st.session_state["zone_key"]
budget   = st.session_state["budget"]

# ── Score banner ──────────────────────────────────────────────────────────────
st.markdown(f"""<div class="score-box score-{R['cls']}">
    <div class="score-num">{R['score']}</div>
    <div class="score-info">
        <div class="score-label">{R['label']}</div>
        <div class="score-rec">{R['rec']}</div>
        <div class="score-prob">Tasa histórica de éxito del giro: {round(R['prob']*100)}% · {entity}</div>
    </div>
    <div style="font-size:1.1rem;opacity:.7;">/100&nbsp;pts</div>
</div>""", unsafe_allow_html=True)

# ── Factors card (single HTML block) ─────────────────────────────────────────
factors_rows = ""
for key, f in R["factors"].items():
    pct   = round(f["score"] / f["max"] * 100)
    color = bar_color(pct)
    factors_rows += f"""<div class="f-row">
        <div class="f-head">
            <span class="f-name">{FACTOR_NAMES[key]}</span>
            <span class="f-stat">{f['score']}/{f['max']} · {f['status']}</span>
        </div>
        <div class="bar-bg"><div class="bar-fill" style="width:{pct}%;background:{color};"></div></div>
        <div class="f-det">{f['detail']}</div>
    </div>"""

# ── Costs card (single HTML block) ───────────────────────────────────────────
c = R["costs"]
bk_rows = "".join(
    f'<div class="c-row"><span style="color:#6b7280;">{COST_LABELS.get(k,k)}</span><span class="c-val">${v:,.0f}</span></div>'
    for k, v in c["breakdown"].items()
)
run_color = "#16a34a" if c["runway"] >= 12 else ("#d97706" if c["runway"] >= 6 else "#dc2626")
costs_card = f"""<div class="vx-card">
    <div class="vx-title">Desglose de costos</div>
    <div class="c-sec">Apertura (única vez)</div>
    <div class="c-row"><span>Trámites regulatorios</span><span class="c-val">${c['proc_costs']:,.0f}</span></div>
    <div class="c-row"><span>Instalación inicial</span><span class="c-val">${c['initial_setup']:,.0f}</span></div>
    <div class="c-sec">Mensual fijo — {c['sqm']} m² · renta ${c['rental_monthly']:,.0f}/mes</div>
    {bk_rows}
    <div class="c-row" style="border-top:2px solid #EDE0E8;margin-top:3px;">
        <span><strong>Total mensual</strong></span><span class="c-val">${c['monthly_fixed']:,.0f}</span>
    </div>
    <div class="c-sec">Proyección primer año</div>
    <div class="c-row"><span><strong>Total año 1</strong></span><span class="c-val">${c['first_year']:,.0f}</span></div>
    <div class="c-row"><span>Ingreso mensual estimado</span><span class="c-val" style="color:#16a34a;">${c['revenue_monthly']:,.0f}</span></div>
    <div class="c-row"><span>Punto de equilibrio</span><span class="c-val">{c['break_even']} meses</span></div>
    <div class="c-row"><span>Runway con tu capital</span><span class="c-val" style="color:{run_color};">{c['runway']} meses</span></div>
</div>"""

fc, cc = st.columns([3, 2], gap="large")
with fc:
    st.markdown(f'<div class="vx-card"><div class="vx-title">Factores de viabilidad — 6 dimensiones</div>{factors_rows}</div>', unsafe_allow_html=True)
with cc:
    st.markdown(costs_card, unsafe_allow_html=True)

# ── Cash flow chart ───────────────────────────────────────────────────────────
import plotly.graph_objects as go

cf   = R["cashflow"]
meses    = [f"Mes {m['Mes']}" for m in cf]
ingresos = [m["Ingresos"]   for m in cf]
costos   = [m["Costos"]     for m in cf]
utilidad = [m["Ingresos"] - m["Costos"] for m in cf]

fig = go.Figure()
fig.add_bar(name="Ingresos", x=meses, y=ingresos,
            marker_color="#104C42", opacity=0.85)
fig.add_bar(name="Costos",   x=meses, y=costos,
            marker_color="#88185B", opacity=0.85)
fig.add_scatter(name="Utilidad neta / mes", x=meses, y=utilidad,
                mode="lines+markers",
                line=dict(color="#BC955C", width=2.5),
                marker=dict(size=6, color="#BC955C"))

fig.update_layout(
    barmode="group",
    plot_bgcolor="white",
    paper_bgcolor="white",
    legend=dict(orientation="h", y=1.12, x=0),
    yaxis=dict(title="MXN", tickformat="$,.0f", gridcolor="#f0f0f0"),
    xaxis=dict(tickfont=dict(size=11)),
    margin=dict(l=10, r=10, t=40, b=10),
    height=360,
)
fig.add_hline(y=0, line_width=1, line_dash="dot", line_color="#aaa")

with st.container(border=True):
    st.markdown("**📈 Proyección financiera — 12 meses**")
    st.plotly_chart(fig, use_container_width=True)

# ── Zone card + Procedure roadmap ─────────────────────────────────────────────
zc, pc_col = st.columns([2, 3], gap="large")

with zc:
    z = R["zone"]
    ci_color = "#dc2626" if z["crime_index"]>=70 else "#d97706" if z["crime_index"]>=40 else "#16a34a"
    tags = "".join(f'<span class="z-tag">{c}</span>' for c in z.get("characteristics", []))
    st.markdown(f"""<div class="vx-card">
        <div class="vx-title">Perfil de alcaldía</div>
        <div style="font-weight:700;margin-bottom:.7rem;">{z['name']}
            <span style="font-size:.75rem;color:#6b7280;font-weight:400;"> · {z.get('type','')}</span>
        </div>
        <div class="z-row"><span class="z-lbl">👥 Población</span><span class="z-val">{z['population']:,} hab.</span></div>
        <div class="z-row"><span class="z-lbl">🚶 Tráfico peatonal/día</span><span class="z-val">{z['foot_traffic_daily']:,}</span></div>
        <div class="z-row"><span class="z-lbl">🏪 Densidad comercial</span><span class="z-val">{z['business_density_per_10k']} neg./10k</span></div>
        <div class="z-row"><span class="z-lbl">🛡️ Criminalidad</span><span class="z-val" style="color:{ci_color};">{z['crime_index']}/100</span></div>
        <div class="z-row"><span class="z-lbl">💰 Renta comercial</span><span class="z-val">${z['rental_cost_sqm_annual']:,}/m²/año</span></div>
        <div class="z-row"><span class="z-lbl">📈 Crecimiento</span><span class="z-val">{z['expansion_rate']*100:.1f}%/año</span></div>
        <div style="margin-top:.7rem;">{tags}</div>
    </div>""", unsafe_allow_html=True)

with pc_col:
    steps_html = ""
    for i, p in enumerate(R["procedures"], 1):
        ak    = agency_key(p.get("agency", ""))
        color = AGENCY_COLORS.get(ak, "#37474F")
        docs  = " · ".join(p.get("required_documents", [])[:3])
        cost  = f"${p.get('cost_mxn',0):,}" if p.get("cost_mxn", 0) > 0 else "Gratuito"
        steps_html += f"""<div class="p-step">
            <div class="p-dot" style="background:{color};">{i}</div>
            <div>
                <div class="p-name" style="color:{color};">{p.get('name_es','')}</div>
                <div class="p-meta">{p.get('description','')} · ⏱ {p.get('timeline_days',0)} días · {cost}</div>
                <div class="p-meta" style="margin-top:2px;">📄 {docs}</div>
            </div>
        </div>"""

    st.markdown(f"""<div class="vx-card">
        <div class="vx-title">Hoja de ruta regulatoria — {len(R['procedures'])} trámites RETYS · {R['tdays']} días · ${R['tcost']:,}</div>
        {steps_html}
    </div>""", unsafe_allow_html=True)

# ── Claude AI recommendation ──────────────────────────────────────────────────
# Results are already rendered above. Now call Claude (shown as spinner at
# bottom). On reruns (map pan, scroll) session_state has the cached response
# so the API is NOT called again.
st.divider()
st.markdown("### 🤖 Recomendación personalizada — Claude AI")

if st.session_state.get("needs_claude"):
    f_txt = "\n".join(
        f"- {FACTOR_NAMES[k]}: {f['score']}/{f['max']} ({f['status']}) — {f['detail']}"
        for k, f in R["factors"].items()
    )
    _prompt = f"""Eres un asesor especialista de SEDECO Ciudad de México.

Un emprendedor evalúa abrir:
- Giro: {BTYPE_OPTS[btype]}
- Alcaldía: {ZONE_OPTS[zone_key]}
- Capital disponible: ${budget:,} MXN
- Superficie: {sqm} m²
- Tipo de persona: {entity}

Resultado del modelo: {R['score']}/100 — {R['label']}

Factores:
{f_txt}

Costo total primer año: ${R['costs']['first_year']:,} MXN
Punto de equilibrio: {R['costs']['break_even']} meses
Trámites: {len(R['procedures'])} pasos ({R['tdays']} días, ${R['tcost']:,} MXN)

Responde en español mexicano (máx. 180 palabras):
1. **Veredicto** — SÍ / CON PRECAUCIÓN / NO (una frase directa)
2. **Fortalezas** del caso (máx. 2 puntos)
3. **Riesgos** a atender (máx. 2 puntos)
4. **Próximo paso concreto** que debe tomar HOY

Sé directo, usa contexto real de la Ciudad de México."""

    with st.spinner("Claude está analizando tu caso…"):
        try:
            _resp = claude.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=400,
                messages=[{"role": "user", "content": _prompt}],
            )
            st.session_state["claude_text"]  = _resp.content[0].text
            st.session_state["claude_error"] = None
        except Exception as e:
            st.session_state["claude_text"]  = None
            st.session_state["claude_error"] = str(e)
    st.session_state["needs_claude"] = False

if st.session_state.get("claude_text"):
    html_response = md_lib.markdown(st.session_state["claude_text"], extensions=["nl2br"])
    st.markdown(f'<div class="ai-box">{html_response}</div>', unsafe_allow_html=True)
elif st.session_state.get("claude_error"):
    st.error(f"Error al conectar con Claude API: {st.session_state['claude_error']}")

# ── Competitor heatmap ───────────────────────────────────────────────────────
st.divider()
st.markdown("### 🗺️ Mapa de Competidores en la Zona")

# Zone centres (CDMX approximate coordinates)
ZONE_COORDS = {
    "cuauhtemoc":                    (19.4326, -99.1332),
    "benito_juarez":                 (19.3984, -99.1572),
    "miguel_hidalgo":                (19.4270, -99.1961),
    "coyoacan":                      (19.3467, -99.1617),
    "alcaldia_alvaro_obregon":       (19.3608, -99.2003),
    "alcaldia_venustiano_carranza":  (19.4236, -99.0987),
    "alcaldia_iztacalco":            (19.3952, -99.0891),
    "gustavo_madero":                (19.4920, -99.1155),
    "iztapalapa":                    (19.3557, -99.0636),
    "alcaldia_tlahuac":              (19.2918, -99.0072),
    "alcaldia_xochimilco":           (19.2569, -99.1034),
    "alcaldia_milpa_alta":           (19.1893, -98.9697),
    "alcaldia_magdalena_contreras":  (19.3270, -99.2440),
    "alcaldia_azcapotzalco":         (19.4886, -99.1853),
    "alcaldia_la_paz":               (19.3635, -98.9567),
    "alcaldia_villa_gustavo_madero": (19.5004, -99.1275),
}

try:
    import folium
    from streamlit_folium import st_folium

    zone_name            = DATA["zones"][zone_key]["name"]
    competitors_for_type = DATA["competitors"].get(btype, {})
    all_zone_comps       = competitors_for_type.get(zone_name, [])
    colonia_info         = R.get("colonia")
    colonia_lbl          = st.session_state.get("colonia_label", "— Alcaldía completa —")

    # Centre map and filter competitors to colonia if selected
    if colonia_info:
        lat, lon = colonia_info["lat"], colonia_info["lon"]
        zone_competitors = [
            c for c in all_zone_comps
            if haversine_km(lat, lon, c["lat"], c["lon"]) <= 1.5
        ]
        map_title = f"{zone_name} · {colonia_lbl}"
    else:
        lat, lon = ZONE_COORDS.get(zone_key, (19.4326, -99.1332))
        zone_competitors = all_zone_comps
        map_title = zone_name

    fmap = folium.Map(location=[lat, lon], zoom_start=14, tiles="OpenStreetMap")

    # Competitor markers — colour by rating
    for comp in zone_competitors:
        if comp["rating"] >= 4.5:   color = "darkred"
        elif comp["rating"] >= 4.0: color = "red"
        elif comp["rating"] >= 3.5: color = "orange"
        else:                        color = "gray"
        folium.CircleMarker(
            location=[comp["lat"], comp["lon"]],
            radius=8,
            popup=f"<b>{comp['name']}</b><br>Rating: {comp['rating']}/5<br>Reseñas: {comp['reviews']:,}",
            color=color, fill=True, fillColor=color, fillOpacity=0.7, weight=2,
        ).add_to(fmap)

    # Your location
    folium.CircleMarker(
        location=[lat, lon], radius=12,
        popup="<b>Tu ubicación (aprox.)</b>",
        color="blue", fill=True, fillColor="blue", fillOpacity=0.85, weight=3,
    ).add_to(fmap)

    if zone_competitors:
        mc1, mc2 = st.columns([3, 1])
        with mc1:
            st_folium(fmap, width=700, height=500)
        with mc2:
            st.write("")
            st.metric("Total competidores", len(zone_competitors))
            avg_r = sum(c["rating"] for c in zone_competitors) / len(zone_competitors)
            st.metric("Rating promedio", f"{avg_r:.1f}/5")
            st.metric("Reseñas totales", f"{sum(c['reviews'] for c in zone_competitors):,}")
            high = len([c for c in zone_competitors if c["rating"] >= 4.5])
            st.metric("Bien calificados (≥4.5)", f"{high} ({100*high//len(zone_competitors)}%)")
        st.info(f"📊 {len(zone_competitors)} competidores directos en {map_title}" +
                (" (radio 1.5 km)" if colonia_info else ""))
    else:
        st_folium(fmap, width=700, height=400)
        st.info(f"📍 Sin datos de competidores directos para {map_title}")

except ImportError:
    st.warning("⚠️ Para ver el mapa instala: pip install folium streamlit-folium")

st.divider()
st.caption("📊 Datos: Ley de Establecimientos Mercantiles CDMX 2024 · RETYS · SEDUVI · INEGI  |  Hackathon SecretarIA 2026 · SEDECO")
