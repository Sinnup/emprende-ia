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

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ViabilidadMX — SEDECO CDMX",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CDMX brand CSS ────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Brand colours */
    :root { --teal:#104C42; --magenta:#88185B; --gold:#BC955C; }

    .stApp { background:#F5F0F3; }

    /* Hero banner */
    .hero {
        background: linear-gradient(135deg, #104C42 0%, #235B4E 100%);
        border-radius: 16px; padding: 2rem 2.5rem; margin-bottom: 1.5rem; color: #fff;
    }
    .hero h1 { font-size:2rem; font-weight:900; margin:0 0 .5rem; }
    .hero p  { opacity:.85; margin:0; font-size:.97rem; }

    /* Score banner */
    .score-alta     { background:linear-gradient(135deg,#14532d,#16a34a); }
    .score-viable   { background:linear-gradient(135deg,#631135,#88185B); }
    .score-marginal { background:linear-gradient(135deg,#7c2d12,#ea580c); }
    .score-no       { background:linear-gradient(135deg,#7f1d1d,#dc2626); }
    .score-box {
        border-radius:16px; padding:1.5rem 2rem; color:#fff;
        margin-bottom:1rem; display:flex; align-items:center; gap:2rem;
    }
    .score-num  { font-size:4rem; font-weight:900; line-height:1; }
    .score-info { flex:1; }
    .score-label { font-size:1.3rem; font-weight:700; }
    .score-rec   { font-size:.9rem; opacity:.85; margin-top:.3rem; }
    .score-prob  { font-size:.78rem; opacity:.65; margin-top:.4rem; }

    /* Cards */
    .card {
        background:#fff; border-radius:14px; padding:1.25rem 1.4rem;
        box-shadow:0 2px 12px rgba(0,0,0,.07); margin-bottom:1rem;
    }
    .card-title {
        font-size:.72rem; font-weight:700; text-transform:uppercase;
        letter-spacing:1px; color:#88185B; margin-bottom:.9rem;
    }

    /* Factor bar */
    .factor-row { margin-bottom:.65rem; }
    .factor-header { display:flex; justify-content:space-between; font-size:.82rem; margin-bottom:3px; }
    .factor-name { font-weight:600; }
    .factor-score { color:#6b7280; }
    .bar-bg { height:8px; background:#e5e7eb; border-radius:4px; overflow:hidden; }
    .bar-fill { height:100%; border-radius:4px; }

    /* Risk badges */
    .risk-alto  { background:#fee2e2; color:#991b1b; border-radius:6px; padding:2px 10px; font-size:.78rem; font-weight:600; }
    .risk-medio { background:#fef3c7; color:#92400e; border-radius:6px; padding:2px 10px; font-size:.78rem; font-weight:600; }
    .risk-bajo  { background:#d1fae5; color:#065f46; border-radius:6px; padding:2px 10px; font-size:.78rem; font-weight:600; }

    /* Procedure step */
    .proc-step { display:flex; gap:.9rem; margin-bottom:.9rem; align-items:flex-start; }
    .proc-dot  {
        width:30px; height:30px; border-radius:50%; color:#fff; font-weight:800;
        display:flex; align-items:center; justify-content:center; flex-shrink:0;
        font-size:.82rem;
    }
    .proc-body { flex:1; }
    .proc-name { font-weight:700; font-size:.88rem; margin-bottom:.15rem; }
    .proc-meta { font-size:.76rem; color:#6b7280; }

    /* Agency colours */
    .ag-sat       { background:#1565C0; }
    .ag-comercio  { background:#6A1B9A; }
    .ag-seduvi    { background:#2E7D32; }
    .ag-ventanilla{ background:#E65100; }
    .ag-sedema    { background:#00695C; }
    .ag-salud     { background:#C62828; }
    .ag-imss      { background:#1B5E20; }
    .ag-seguro    { background:#37474F; }

    /* Cost table */
    .cost-row { display:flex; justify-content:space-between; padding:.35rem 0; border-bottom:1px solid #f3f4f6; font-size:.84rem; }
    .cost-row:last-child { border:none; }
    .cost-val { font-weight:700; }
    .cost-sec { font-size:.68rem; font-weight:700; text-transform:uppercase; letter-spacing:.8px; color:#88185B; margin:.7rem 0 .2rem; }

    /* Zone tag */
    .zone-tag { display:inline-block; background:#EDE0E8; color:#104C42; border-radius:20px; padding:2px 10px; font-size:.7rem; font-weight:600; margin:2px; }
    .zone-row { display:flex; gap:.5rem; align-items:center; padding:.38rem 0; border-bottom:1px solid #f3f4f6; font-size:.82rem; }
    .zone-row:last-child { border:none; }
    .zm-lbl { color:#6b7280; flex:1; }
    .zm-val { font-weight:700; }

    /* AI section */
    .ai-box { background:#fdf0f6; border-left:4px solid #88185B; border-radius:12px; padding:1.1rem 1.25rem; }

    /* Hide streamlit chrome */
    #MainMenu, footer, header { visibility:hidden; }
    .block-container { padding-top:1.5rem !important; max-width:1100px; }
    div[data-testid="stDecoration"] { display:none; }
</style>
""", unsafe_allow_html=True)

# ── Data loading ──────────────────────────────────────────────────────────────
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
    }

@st.cache_resource
def get_claude():
    return Anthropic()

DATA = load_data()
claude = get_claude()

# ── Scoring helpers (matches src/main.py logic) ───────────────────────────────
def get_procedure_sequence(btype):
    food   = {"722110", "722210"}
    office = {"551020"}
    seqs   = DATA["procedures"]["procedure_sequences"]
    if btype in food:   return seqs["restaurant"]
    if btype in office: return seqs["oficina"]
    return seqs["tienda_retail"]

def agency_class(agency):
    MAP = {
        "SAT": "sat", "Cámara": "comercio", "SEDUVI": "seduvi",
        "Delegación": "ventanilla", "Ventanilla": "ventanilla",
        "SIAPEM": "sedema", "Secretaría de Salud": "salud",
        "IMSS": "imss",
    }
    for k, v in MAP.items():
        if k in agency:
            return v
    return "seguro"

def score_color(pct):
    if pct >= 75: return "#16a34a"
    if pct >= 50: return "#d97706"
    return "#dc2626"

def calculate(btype, zone_key, budget, sqm):
    bt = DATA["business_types"][btype]
    z  = DATA["zones"][zone_key]
    costs = DATA["costs"].get(btype)
    crime = DATA["crime"]["crime_by_zone"].get(zone_key, {})
    m = DATA["model"]["factors"]

    # Rental
    rental_monthly = round(z["rental_cost_sqm_annual"] * sqm / 12)

    if costs:
        bkdown = dict(costs["monthly_fixed"])
        bkdown["rent"] = rental_monthly
        monthly_fixed = sum(bkdown.values())
        first_year = monthly_fixed * 12 + costs["procedure_costs"] + costs["initial_setup"]
        proc_costs = costs["procedure_costs"]
        initial_setup = costs["initial_setup"]
        break_even = costs["break_even_months"]
        rev_monthly = costs["estimated_revenue_monthly"]
    else:
        bkdown = {"rent": rental_monthly, "utilities": 300, "permits": 100, "insurance": 200, "labor_base": bt["monthly_fixed"], "supplies": 150}
        monthly_fixed = sum(bkdown.values())
        proc_costs = 2500
        initial_setup = round(bt["startup_capital"] * 0.1)
        first_year = monthly_fixed * 12 + proc_costs + initial_setup
        break_even = 8
        rev_monthly = monthly_fixed * 2

    # 6 factors
    if budget >= first_year:         bs, bst = m["budget"]["scoring"]["sufficient"], "Suficiente"
    elif budget >= first_year * 0.8: bs, bst = m["budget"]["scoring"]["marginal"],   "Marginal"
    else:                             bs, bst = m["budget"]["scoring"]["insufficient"],"Insuficiente"

    dens = z["business_density_per_10k"]
    if dens < 20:   cs, cst = m["competition"]["scoring"]["low"],      "Baja"
    elif dens < 50: cs, cst = m["competition"]["scoring"]["medium"],   "Media"
    elif dens < 100:cs, cst = m["competition"]["scoring"]["high"],     "Alta"
    else:           cs, cst = m["competition"]["scoring"]["very_high"],"Muy Alta"

    ft = z["foot_traffic_daily"]
    if ft > 5000:   ls, lst = m["location"]["scoring"]["high"],   "Alto"
    elif ft > 2000: ls, lst = m["location"]["scoring"]["medium"], "Medio"
    else:           ls, lst = m["location"]["scoring"]["low"],    "Bajo"

    ci = crime.get("overall", 50)
    if ci < 40:   ss, sst = m["security"]["scoring"]["low"],    "Bajo"
    elif ci < 70: ss, sst = m["security"]["scoring"]["medium"], "Medio"
    else:         ss, sst = m["security"]["scoring"]["high"],   "Alto"

    gr = z["population_growth_annual"]
    if gr > 0.02:  gs, gst = m["growth"]["scoring"]["growing"],  "Creciendo"
    elif gr > 0.01:gs, gst = m["growth"]["scoring"]["stable"],   "Estable"
    else:          gs, gst = m["growth"]["scoring"]["declining"],"Declive"

    legal, lst2 = m["legal"]["scoring"]["all_attainable"], "Alcanzable"

    total = bs + cs + ls + ss + gs + legal

    # Procedures
    procs = []
    for key in get_procedure_sequence(btype):
        p = DATA["procedures"]["procedures"].get(key, {})
        procs.append(p)
    total_proc_days  = bt.get("procedures_days", sum(p.get("timeline_days", 0) for p in procs))
    total_proc_cost  = sum(p.get("cost_mxn", 0) for p in procs)

    # Cashflow
    cashflow = []
    cumul = -(proc_costs + initial_setup)
    vr = bt.get("variable_ratio", 0.35)
    for mo in range(1, 13):
        rev  = rev_monthly * (1 + 0.04 * (mo-1) / 12)
        cost = monthly_fixed + rev * vr
        net  = rev - cost
        cumul += net
        cashflow.append({"month": mo, "revenue": round(rev), "costs": round(cost), "net": round(net), "cumulative": round(cumul)})

    return {
        "score": total,
        "label": ("Altamente Viable" if total>=80 else "Viable" if total>=65 else "Marginal" if total>=50 else "No Recomendado"),
        "cls":   ("alta"             if total>=80 else "viable" if total>=65 else "marginal" if total>=50 else "no"),
        "rec":   ("Adelante con confianza — base sólida." if total>=80
                  else "Procede monitoreando riesgos." if total>=65
                  else "Requiere planeación cuidadosa." if total>=50
                  else "Reconsiderar zona o giro."),
        "success_prob": bt.get("success_rate", 0.65),
        "factors": {
            "budget":      {"score":bs, "max":15, "status":bst, "detail":f"${budget:,.0f} vs ${first_year:,.0f} año 1"},
            "competition": {"score":cs, "max":20, "status":cst, "detail":f"{dens} negocios/10k hab."},
            "location":    {"score":ls, "max":20, "status":lst, "detail":f"{ft:,} peatones/día"},
            "security":    {"score":ss, "max":15, "status":sst, "detail":f"Criminalidad {ci}/100"},
            "growth":      {"score":gs, "max":15, "status":gst, "detail":f"Crecimiento {gr*100:.1f}%/año"},
            "legal":       {"score":legal,"max":15,"status":lst2,"detail":f"{len(procs)} trámites ~{total_proc_days} días"},
        },
        "costs": {
            "proc_costs": proc_costs, "initial_setup": initial_setup,
            "monthly_fixed": monthly_fixed, "breakdown": bkdown,
            "first_year": round(first_year), "break_even": break_even,
            "runway": round(budget / monthly_fixed, 1),
            "revenue_monthly": rev_monthly,
            "rental_monthly": rental_monthly, "sqm": sqm,
        },
        "procedures": procs,
        "total_proc_days": total_proc_days,
        "total_proc_cost": total_proc_cost,
        "zone": z, "zone_key": zone_key,
        "cashflow": cashflow,
    }

# ── UI ─────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🏙️ ViabilidadMX — SEDECO CDMX</h1>
    <p>Evalúa en segundos la viabilidad de tu negocio en la Ciudad de México.<br>
    Basado en datos reales del RETYS y la Ley de Establecimientos Mercantiles 2024.</p>
</div>
""", unsafe_allow_html=True)

# ── Form ───────────────────────────────────────────────────────────────────────
BTYPE_OPTS = {k: f"{v['name_es']}" for k, v in DATA["business_types"].items()}
ZONE_OPTS  = {k: v["name"] for k, v in DATA["zones"].items()}

FACTOR_NAMES = {
    "budget":      "💰 Capital Disponible",
    "competition": "🏪 Saturación de Mercado",
    "location":    "📍 Tráfico Peatonal",
    "security":    "🛡️ Seguridad de Zona",
    "growth":      "📈 Crecimiento Económico",
    "legal":       "⚖️ Factibilidad Regulatoria",
}
COST_LABELS = {
    "rent":"Renta", "utilities":"Servicios", "permits":"Permisos",
    "insurance":"Seguro", "labor_base":"Nómina base", "supplies":"Insumos",
}

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("#### 🏢 Tipo de negocio y zona")
    btype = st.selectbox("Giro SCIAN", options=list(BTYPE_OPTS.keys()),
                         format_func=lambda k: BTYPE_OPTS[k])
    zone_key = st.selectbox("Alcaldía", options=list(ZONE_OPTS.keys()),
                             format_func=lambda k: ZONE_OPTS[k])

with col2:
    st.markdown("#### 💰 Recursos disponibles")
    budget = st.number_input("Capital disponible (MXN)", value=200_000, step=10_000, min_value=10_000,
                              format="%d")
    sqm    = st.number_input("Superficie del local (m²)", value=80, step=5, min_value=5, max_value=9999)
    entity = st.radio("Tipo de persona", ["Persona Física", "Persona Moral (S.A./S. de R.L.)"],
                      horizontal=True)

st.divider()
evaluar = st.button("🔍 Evaluar Viabilidad del Negocio", use_container_width=True, type="primary")

# ── Results ────────────────────────────────────────────────────────────────────
if evaluar:
    with st.spinner("Calculando viabilidad con datos del RETYS y SEDUVI…"):
        R = calculate(btype, zone_key, budget, sqm)

    # Score banner
    fmt_score = f"""
    <div class="score-box score-{R['cls']}">
        <div class="score-num">{R['score']}</div>
        <div class="score-info">
            <div class="score-label">{R['label']}</div>
            <div class="score-rec">{R['rec']}</div>
            <div class="score-prob">Tasa histórica de éxito del giro: {round(R['success_prob']*100)}% · {entity}</div>
        </div>
        <div style="font-size:1.1rem;opacity:.7;">/100 pts</div>
    </div>"""
    st.markdown(fmt_score, unsafe_allow_html=True)

    # ── Factors + Costs ───────────────────────────────────────────────────────
    fc, cc = st.columns([3, 2], gap="large")

    with fc:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Factores de viabilidad — 6 dimensiones</div>', unsafe_allow_html=True)
        for key, f in R["factors"].items():
            pct = round(f["score"] / f["max"] * 100)
            color = score_color(pct)
            st.markdown(f"""
            <div class="factor-row">
                <div class="factor-header">
                    <span class="factor-name">{FACTOR_NAMES[key]}</span>
                    <span class="factor-score">{f['score']}/{f['max']} · {f['status']}</span>
                </div>
                <div class="bar-bg"><div class="bar-fill" style="width:{pct}%;background:{color};"></div></div>
                <div style="font-size:.71rem;color:#9ca3af;margin-top:2px;">{f['detail']}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with cc:
        c = R["costs"]
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Desglose de costos</div>', unsafe_allow_html=True)

        bk_rows = "".join(
            f'<div class="cost-row"><span style="color:#6b7280;">{COST_LABELS.get(k,k)}</span><span class="cost-val">${v:,.0f}</span></div>'
            for k, v in c["breakdown"].items()
        )
        run_color = "green" if c["runway"] >= 12 else ("inherit" if c["runway"] >= 6 else "red")
        st.markdown(f"""
        <div class="cost-sec">Apertura (única vez)</div>
        <div class="cost-row"><span>Trámites regulatorios</span><span class="cost-val">${c['proc_costs']:,.0f}</span></div>
        <div class="cost-row"><span>Instalación y acondicionamiento</span><span class="cost-val">${c['initial_setup']:,.0f}</span></div>
        <div class="cost-sec">Mensual fijo — {c['sqm']} m² / renta ${c['rental_monthly']:,.0f}/mes</div>
        {bk_rows}
        <div class="cost-row" style="border-top:2px solid #EDE0E8;margin-top:2px;">
            <span><strong>Total mensual</strong></span><span class="cost-val">${c['monthly_fixed']:,.0f}</span></div>
        <div class="cost-sec">Proyección primer año</div>
        <div class="cost-row"><span><strong>Total año 1</strong></span><span class="cost-val">${c['first_year']:,.0f}</span></div>
        <div class="cost-row"><span>Ingreso mensual estimado</span><span class="cost-val" style="color:#16a34a;">${c['revenue_monthly']:,.0f}</span></div>
        <div class="cost-row"><span>Punto de equilibrio</span><span class="cost-val">{c['break_even']} meses</span></div>
        <div class="cost-row"><span>Runway con tu capital</span><span class="cost-val" style="color:{run_color};">{c['runway']} meses</span></div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Cash flow chart ───────────────────────────────────────────────────────
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Proyección financiera — 12 meses</div>', unsafe_allow_html=True)

    import pandas as pd
    cf_df = pd.DataFrame(R["cashflow"])
    cf_df = cf_df.set_index("month").rename(columns={
        "revenue": "Ingresos", "costs": "Costos", "net": "Utilidad neta"
    })
    st.bar_chart(cf_df[["Ingresos", "Costos"]], color=["#104C42", "#88185B"])
    st.line_chart(cf_df[["Utilidad neta"]], color=["#BC955C"])
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Zone + Procedures ─────────────────────────────────────────────────────
    zc, pc = st.columns([2, 3], gap="large")

    with zc:
        z = R["zone"]
        crime_color = "#dc2626" if z["crime_index"]>=70 else "#d97706" if z["crime_index"]>=40 else "#16a34a"
        tags = "".join(f'<span class="zone-tag">{c}</span>' for c in z.get("characteristics", []))
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Perfil de alcaldía</div>
            <div style="font-weight:700;margin-bottom:.7rem;">{z['name']} <span style="font-size:.75rem;color:#6b7280;font-weight:400;">· {z.get('type','')}</span></div>
            <div class="zone-row"><span class="zm-lbl">👥 Población</span><span class="zm-val">{z['population']:,} hab.</span></div>
            <div class="zone-row"><span class="zm-lbl">🚶 Tráfico peatonal/día</span><span class="zm-val">{z['foot_traffic_daily']:,}</span></div>
            <div class="zone-row"><span class="zm-lbl">🏪 Densidad comercial</span><span class="zm-val">{z['business_density_per_10k']} neg./10k</span></div>
            <div class="zone-row"><span class="zm-lbl">🛡️ Índice de criminalidad</span><span class="zm-val" style="color:{crime_color};">{z['crime_index']}/100</span></div>
            <div class="zone-row"><span class="zm-lbl">💰 Renta comercial</span><span class="zm-val">${z['rental_cost_sqm_annual']:,}/m²/año</span></div>
            <div class="zone-row"><span class="zm-lbl">📈 Crecimiento anual</span><span class="zm-val">{z['expansion_rate']*100:.1f}%</span></div>
            <div style="margin-top:.7rem;">{tags}</div>
        </div>
        """, unsafe_allow_html=True)

    with pc:
        AGENCY_COLORS = {
            "sat":"#1565C0","comercio":"#6A1B9A","seduvi":"#2E7D32",
            "ventanilla":"#E65100","sedema":"#00695C","salud":"#C62828",
            "imss":"#1B5E20","seguro":"#37474F",
        }
        steps_html = ""
        for i, p in enumerate(R["procedures"], 1):
            ak  = agency_class(p.get("agency",""))
            col = AGENCY_COLORS.get(ak, "#37474F")
            docs = " · ".join(p.get("required_documents", [])[:3])
            cost_str = f"${p.get('cost_mxn',0):,}" if p.get("cost_mxn",0)>0 else "Gratuito"
            steps_html += f"""
            <div class="proc-step">
                <div class="proc-dot" style="background:{col};">{i}</div>
                <div class="proc-body">
                    <div class="proc-name" style="color:{col};">{p.get('name_es','')}</div>
                    <div class="proc-meta">{p.get('description','')} · ⏱ {p.get('timeline_days',0)} días · {cost_str}</div>
                    <div class="proc-meta" style="margin-top:2px;">📄 {docs}</div>
                </div>
            </div>"""

        st.markdown(f"""
        <div class="card">
            <div class="card-title">Hoja de ruta regulatoria — {len(R['procedures'])} trámites RETYS · {R['total_proc_days']} días · ${R['total_proc_cost']:,}</div>
            {steps_html}
        </div>
        """, unsafe_allow_html=True)

    # ── Claude AI recommendation ──────────────────────────────────────────────
    st.divider()
    st.markdown("### 🤖 Recomendación personalizada (Claude AI)")

    factors_txt = "\n".join(
        f"- {FACTOR_NAMES[k]}: {f['score']}/{f['max']} ({f['status']}) — {f['detail']}"
        for k, f in R["factors"].items()
    )
    prompt = f"""Eres un asesor especialista de SEDECO Ciudad de México.

Un emprendedor evalúa abrir:
- Giro: {BTYPE_OPTS[btype]}
- Alcaldía: {ZONE_OPTS[zone_key]}
- Capital disponible: ${budget:,} MXN
- Superficie: {sqm} m²
- Tipo de persona: {entity}

Resultado del modelo de viabilidad: {R['score']}/100 — {R['label']}

Factores evaluados:
{factors_txt}

Costo total primer año estimado: ${R['costs']['first_year']:,} MXN
Punto de equilibrio: {R['costs']['break_even']} meses
Trámites requeridos: {len(R['procedures'])} ({R['total_proc_days']} días hábiles, ${R['total_proc_cost']:,} MXN)

Proporciona en español mexicano (máx. 180 palabras):
1. **Veredicto** (1 frase directa: SÍ / CON PRECAUCIÓN / NO)
2. **Fortalezas** del caso (máx. 2 puntos)
3. **Riesgos principales** a atender (máx. 2 puntos)
4. **Próximo paso concreto** que debe tomar HOY

Sé directo, práctico y usa contexto real de la Ciudad de México."""

    with st.spinner("Claude está analizando tu caso específico…"):
        try:
            resp = claude.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=400,
                messages=[{"role":"user","content":prompt}],
            )
            ai_text = resp.content[0].text
            st.markdown(f'<div class="ai-box">{ai_text}</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error al conectar con Claude API: {e}")
            st.info("Configura ANTHROPIC_API_KEY en tus variables de entorno para activar las recomendaciones IA.")

    # ── Footer ────────────────────────────────────────────────────────────────
    st.divider()
    st.caption("📊 Datos: Ley de Establecimientos Mercantiles CDMX 2024 · RETYS · SEDUVI · INEGI  |  Hackathon SecretarIA 2026 · SEDECO")
