from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
import json
from pathlib import Path
from typing import Optional

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
FRONTEND_DIR = BASE_DIR / "src" / "frontend"

# ── Startup cache (loaded once, queried in <1ms) ─────────────────────────────
BUSINESS_TYPES: dict = {}
ZONES: dict = {}
PROCEDURES: dict = {}
COSTS: dict = {}
CRIME: dict = {}
VIABILITY_MODEL: dict = {}
REGULATORY_COSTS: dict = {}
CENPROIN: dict = {}

def _load():
    global BUSINESS_TYPES, ZONES, PROCEDURES, COSTS, CRIME
    global VIABILITY_MODEL, REGULATORY_COSTS, CENPROIN

    with open(DATA_DIR / "business-types.json") as f:
        raw = json.load(f)
        BUSINESS_TYPES = raw["business_types"]  # already keyed by SCIAN

    with open(DATA_DIR / "zones.json") as f:
        raw = json.load(f)
        ZONES = raw["zones"]  # keyed by zone_code

    with open(DATA_DIR / "procedures.json") as f:
        raw = json.load(f)
        PROCEDURES = {
            "by_code": raw["procedures"],
            "sequences": raw["procedure_sequences"],
        }

    with open(DATA_DIR / "costs.json") as f:
        COSTS = json.load(f)["costs"]

    with open(DATA_DIR / "crime-index.json") as f:
        CRIME = json.load(f)

    with open(DATA_DIR / "viability-model.json") as f:
        VIABILITY_MODEL = json.load(f)

    with open(DATA_DIR / "regulatory-costs.json") as f:
        REGULATORY_COSTS = json.load(f)["costs"]

    with open(DATA_DIR / "cenproin-training-context.json") as f:
        CENPROIN = json.load(f)["modules"]

_load()  # load immediately at import time (works with --reload)

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(title="ViabilidadMX API", version="1.0.0",
              description="Business Viability Assessment for CDMX Entrepreneurs — SEDECO SecretarIA Hackathon 2026")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Models ────────────────────────────────────────────────────────────────────
class ViabilityRequest(BaseModel):
    business_type: str
    zone: str
    user_budget_mxn: float
    space_sqm: float
    entity_type: str = "individual"

    @field_validator("user_budget_mxn")
    @classmethod
    def budget_positive(cls, v):
        if v <= 0:
            raise ValueError("El presupuesto debe ser mayor a 0")
        return v

    @field_validator("space_sqm")
    @classmethod
    def sqm_valid(cls, v):
        if v <= 0 or v > 10000:
            raise ValueError("La superficie debe estar entre 1 y 10,000 m²")
        return v


# ── Helpers ───────────────────────────────────────────────────────────────────
def _get_procedure_sequence(business_type: str) -> list[str]:
    """Map SCIAN code to procedure sequence key, then return ordered keys."""
    food_types = {"722110", "722210"}
    office_types = {"551020"}
    if business_type in food_types:
        seq_key = "restaurant"
    elif business_type in office_types:
        seq_key = "oficina"
    else:
        seq_key = "tienda_retail"
    return PROCEDURES["sequences"].get(seq_key, [])


def _build_procedures_list(business_type: str) -> tuple[list[dict], int, int]:
    """Return (procedures_list, total_days, total_cost)."""
    keys = _get_procedure_sequence(business_type)
    result = []
    total_cost = 0
    for i, key in enumerate(keys):
        p = PROCEDURES["by_code"].get(key, {})
        total_cost += p.get("cost_mxn", 0)
        result.append({
            "sequence": i + 1,
            "code": p.get("code", ""),
            "name": p.get("name_es", key),
            "description": p.get("description", ""),
            "timeline_days": p.get("timeline_days", 0),
            "cost_mxn": p.get("cost_mxn", 0),
            "agency": p.get("agency", ""),
            "documents": p.get("required_documents", []),
            "blocking": p.get("blocking", []),
            "status": "Requerido",
        })
    bt = BUSINESS_TYPES.get(business_type, {})
    total_days = bt.get("procedures_days", sum(p["timeline_days"] for p in result))
    return result, total_days, total_cost


def _calculate_viability(req: ViabilityRequest) -> dict:
    # ── Step 2: Load profiles ────────────────────────────────────────────────
    bt = BUSINESS_TYPES.get(req.business_type)
    z = ZONES.get(req.zone)
    if not bt:
        raise HTTPException(400, f"Tipo de negocio '{req.business_type}' no registrado en SCIAN")
    if not z:
        raise HTTPException(400, f"Zona '{req.zone}' no encontrada en CDMX")

    cost_template = COSTS.get(req.business_type)
    crime_zone = CRIME["crime_by_zone"].get(req.zone, {})
    model = VIABILITY_MODEL["factors"]

    # ── Step 3: Rental based on actual space_sqm (workflow spec) ─────────────
    rental_sqm_annual = z["rental_cost_sqm_annual"]
    rental_monthly = round((rental_sqm_annual * req.space_sqm) / 12)

    if cost_template:
        monthly_breakdown = dict(cost_template["monthly_fixed"])
        monthly_breakdown["rent"] = rental_monthly  # override with actual space cost
        monthly_fixed_total = sum(monthly_breakdown.values())
        first_year_total = monthly_fixed_total * 12 + cost_template["procedure_costs"] + cost_template["initial_setup"]
        procedure_costs = cost_template["procedure_costs"]
        initial_setup = cost_template["initial_setup"]
        break_even_months = cost_template["break_even_months"]
        rev_monthly = cost_template["estimated_revenue_monthly"]
    else:
        monthly_breakdown = {"rent": rental_monthly, "utilities": 300, "permits": 100, "insurance": 200, "labor_base": bt["monthly_fixed"], "supplies": 150}
        monthly_fixed_total = sum(monthly_breakdown.values())
        _, _, procedure_costs = _build_procedures_list(req.business_type)
        initial_setup = round(bt["startup_capital"] * 0.1)
        first_year_total = monthly_fixed_total * 12 + procedure_costs + initial_setup
        break_even_months = 8
        rev_monthly = monthly_fixed_total * 2

    # ── Step 4: Budget factor (vs first_year_total per workflow spec) ─────────
    if req.user_budget_mxn >= first_year_total:
        budget_score = model["budget"]["scoring"]["sufficient"]   # 15
        budget_status = "sufficient"
        budget_detail = f"Cubre el primer año completo (${first_year_total:,.0f})"
    elif req.user_budget_mxn >= first_year_total * 0.8:
        budget_score = model["budget"]["scoring"]["marginal"]     # 10
        budget_status = "marginal"
        budget_detail = f"Cubre 80%+ del primer año — margen ajustado"
    else:
        budget_score = model["budget"]["scoring"]["insufficient"]  # 3
        budget_status = "insufficient"
        pct = round(req.user_budget_mxn / first_year_total * 100)
        budget_detail = f"Solo cubre {pct}% del primer año (${first_year_total:,.0f} requerido)"

    # ── Step 5: Competition factor ────────────────────────────────────────────
    density = z["business_density_per_10k"]
    if density < 20:
        comp_score = model["competition"]["scoring"]["low"]       # 20
        comp_status = "low"
    elif density < 50:
        comp_score = model["competition"]["scoring"]["medium"]    # 15
        comp_status = "medium"
    elif density < 100:
        comp_score = model["competition"]["scoring"]["high"]      # 8
        comp_status = "high"
    else:
        comp_score = model["competition"]["scoring"]["very_high"] # 3
        comp_status = "very_high"

    # ── Step 6: Location factor ───────────────────────────────────────────────
    foot_traffic = z["foot_traffic_daily"]
    if foot_traffic > 5000:
        loc_score = model["location"]["scoring"]["high"]    # 20
        loc_status = "high"
    elif foot_traffic > 2000:
        loc_score = model["location"]["scoring"]["medium"]  # 15
        loc_status = "medium"
    else:
        loc_score = model["location"]["scoring"]["low"]     # 8
        loc_status = "low"

    # ── Step 7: Security factor ───────────────────────────────────────────────
    crime_overall = crime_zone.get("overall", 50)
    if crime_overall < 40:
        sec_score = model["security"]["scoring"]["low"]     # 15
        sec_status = "low"
    elif crime_overall < 70:
        sec_score = model["security"]["scoring"]["medium"]  # 10
        sec_status = "medium"
    else:
        sec_score = model["security"]["scoring"]["high"]    # 3
        sec_status = "high"

    # ── Step 8: Growth factor (population_growth_annual per workflow spec) ────
    growth_rate = z["population_growth_annual"]
    if growth_rate > 0.02:
        grow_score = model["growth"]["scoring"]["growing"]   # 15
        grow_status = "growing"
    elif growth_rate > 0.01:
        grow_score = model["growth"]["scoring"]["stable"]    # 10
        grow_status = "stable"
    else:
        grow_score = model["growth"]["scoring"]["declining"] # 5
        grow_status = "declining"

    # ── Step 9: Legal factor ──────────────────────────────────────────────────
    procedures_list, total_proc_days, total_proc_cost = _build_procedures_list(req.business_type)
    legal_score = model["legal"]["scoring"]["all_attainable"]  # 15 — all RETYS procedures attainable
    legal_status = "all_attainable"

    # ── Step 10: Total score (factors already weighted 0-100 scale) ──────────
    total_score = budget_score + comp_score + loc_score + sec_score + grow_score + legal_score

    # ── Step 11: Interpretation ───────────────────────────────────────────────
    interp = VIABILITY_MODEL["interpretation"]
    if total_score >= 80:
        label = "Altamente Viable"
        recommendation = "Adelante con confianza. Indicadores sólidos en esta zona."
        rec_class = "alta"
    elif total_score >= 65:
        label = "Viable"
        recommendation = "Procede con monitoreo de riesgos. Alta probabilidad de éxito."
        rec_class = "viable"
    elif total_score >= 50:
        label = "Marginal"
        recommendation = "Requiere planeación cuidadosa. Considera alcaldías alternativas."
        rec_class = "marginal"
    else:
        label = "No Recomendado"
        recommendation = "Múltiples factores de riesgo. Reconsiderar zona o giro."
        rec_class = "no"

    # ── Risks ─────────────────────────────────────────────────────────────────
    risks = []
    risks.append({
        "category": "Seguridad",
        "level": "Alto" if crime_overall >= 70 else "Medio" if crime_overall >= 40 else "Bajo",
        "detail": f"Índice de criminalidad: {crime_overall}/100",
        "icon": "🔴" if crime_overall >= 70 else "🟡" if crime_overall >= 40 else "🟢",
    })
    risks.append({
        "category": "Competencia",
        "level": "Alto" if density >= 100 else "Medio" if density >= 50 else "Bajo",
        "detail": f"{density} negocios por 10,000 hab. en {z['name']}",
        "icon": "🔴" if density >= 100 else "🟡" if density >= 50 else "🟢",
    })
    cap_level = "Alto" if budget_status == "insufficient" else "Medio" if budget_status == "marginal" else "Bajo"
    risks.append({
        "category": "Capital",
        "level": cap_level,
        "detail": budget_detail,
        "icon": "🔴" if cap_level == "Alto" else "🟡" if cap_level == "Medio" else "🟢",
    })
    risks.append({
        "category": "Legal / Trámites",
        "level": "Bajo",
        "detail": f"{len(procedures_list)} trámites alcanzables en ~{total_proc_days} días hábiles",
        "icon": "🟢",
    })

    # ── 12-month cash flow projection ─────────────────────────────────────────
    monthly_cashflow = []
    cumulative = -(total_proc_cost + initial_setup)
    variable_ratio = bt.get("variable_ratio", 0.35)
    for month in range(1, 13):
        revenue = rev_monthly * (1 + 0.04 * (month - 1) / 12)
        monthly_costs = monthly_fixed_total + revenue * variable_ratio
        net = revenue - monthly_costs
        cumulative += net
        monthly_cashflow.append({
            "month": month,
            "revenue": round(revenue),
            "costs": round(monthly_costs),
            "net": round(net),
            "cumulative": round(cumulative),
        })

    runway_months = round(req.user_budget_mxn / monthly_fixed_total, 1) if monthly_fixed_total else 0

    return {
        "viability_score": total_score,
        "viability_label": label,
        "viability_class": rec_class,
        "recommendation": recommendation,
        "success_probability": bt.get("success_rate", 0.65),
        "entity_type": req.entity_type,
        # 6-factor detail
        "factors": {
            "budget": {
                "score": budget_score, "max": 15, "status": budget_status,
                "details": budget_detail,
            },
            "competition": {
                "score": comp_score, "max": 20, "status": comp_status,
                "details": f"{density} negocios/10k hab.",
            },
            "location": {
                "score": loc_score, "max": 20, "status": loc_status,
                "details": f"{foot_traffic:,} peatones/día",
            },
            "security": {
                "score": sec_score, "max": 15, "status": sec_status,
                "details": f"Criminalidad: {crime_overall}/100",
            },
            "growth": {
                "score": grow_score, "max": 15, "status": grow_status,
                "details": f"Crecimiento poblacional: {growth_rate*100:.1f}%/año",
            },
            "legal": {
                "score": legal_score, "max": 15, "status": legal_status,
                "details": f"{len(procedures_list)} trámites en ~{total_proc_days} días",
            },
        },
        # Cost breakdown
        "cost_breakdown": {
            "procedure_costs": total_proc_cost,
            "initial_setup": initial_setup,
            "monthly_fixed": monthly_fixed_total,
            "monthly_fixed_breakdown": monthly_breakdown,
            "first_year_total": round(first_year_total),
            "break_even_months": break_even_months,
            "runway_months": runway_months,
            "estimated_revenue_monthly": rev_monthly,
            "rental_calculated": rental_monthly,
            "space_sqm": req.space_sqm,
        },
        # Procedures
        "procedures_required": procedures_list,
        "total_procedure_days": total_proc_days,
        "total_procedure_cost": total_proc_cost,
        # Risk assessment
        "risks": risks,
        # Projections
        "estimated_monthly_revenue": rev_monthly,
        "monthly_cashflow": monthly_cashflow,
        # Zone summary
        "zone_summary": {
            "name": z["name"],
            "type": z.get("type", ""),
            "population": z["population"],
            "characteristics": z.get("characteristics", []),
            "rental_sqm_annual": rental_sqm_annual,
        },
        # Cenproin support programs
        "support_resources": {
            "constitution": CENPROIN.get("constitution", {}).get("key_points", []),
            "support_programs": CENPROIN.get("support_programs", {}).get("key_points", []),
        },
    }


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/")
async def serve_frontend():
    return FileResponse(str(FRONTEND_DIR / "index.html"))


@app.post("/api/viability-check")
async def viability_check(req: ViabilityRequest):
    """Full 6-factor viability assessment. Core endpoint for the demo."""
    return _calculate_viability(req)


@app.get("/api/cost-estimate/{scian}/{zone}/{sqm}")
async def cost_estimate(scian: str, zone: str, sqm: float):
    """Detailed cost breakdown for a given business type, zone, and space size."""
    bt = BUSINESS_TYPES.get(scian)
    z = ZONES.get(zone)
    if not bt:
        raise HTTPException(404, "Tipo de negocio no encontrado")
    if not z:
        raise HTTPException(404, "Zona no encontrada")

    rental_monthly = round((z["rental_cost_sqm_annual"] * sqm) / 12)
    costs = COSTS.get(scian)

    if costs:
        breakdown = dict(costs["monthly_fixed"])
        breakdown["rent"] = rental_monthly
        monthly_total = sum(breakdown.values())
        first_year = monthly_total * 12 + costs["procedure_costs"] + costs["initial_setup"]
        return {
            "business_type": costs["name"],
            "location": z["name"],
            "space_sqm": sqm,
            "monthly_costs": {**breakdown, "total_fixed": monthly_total},
            "procedure_costs": costs["procedure_costs"],
            "setup_costs": costs["initial_setup"],
            "first_year_projection": {
                "total_costs": round(first_year),
                "estimated_revenue": costs["estimated_revenue_monthly"] * 12,
                "profit_year_1": round(costs["estimated_revenue_monthly"] * 12 - first_year),
                "break_even_month": costs["break_even_months"],
            },
        }
    else:
        monthly_total = rental_monthly + bt["monthly_fixed"] + 300
        _, _, proc_cost = _build_procedures_list(scian)
        return {
            "business_type": bt["name_es"],
            "location": z["name"],
            "space_sqm": sqm,
            "note": "Estimación basada en promedios de industria",
            "monthly_costs": {"rent": rental_monthly, "other": bt["monthly_fixed"], "total_fixed": monthly_total},
            "procedure_costs": proc_cost,
            "setup_costs": round(bt["startup_capital"] * 0.1),
            "first_year_projection": {
                "total_costs": monthly_total * 12 + proc_cost,
                "estimated_revenue": monthly_total * 24,
                "break_even_month": 8,
            },
        }


@app.get("/api/procedures/{business_type}")
async def get_procedures(business_type: str):
    """Ordered RETYS procedure roadmap for a given business type."""
    bt = BUSINESS_TYPES.get(business_type)
    if not bt:
        raise HTTPException(404, "Tipo de negocio no encontrado")
    procs, total_days, total_cost = _build_procedures_list(business_type)
    return {
        "business_type": bt["name_es"],
        "entity_type_note": "Los trámites varían entre Persona Física y Moral en el RFC y Registro Mercantil.",
        "total_timeline_days": total_days,
        "total_cost_mxn": total_cost,
        "critical_path": ["rfc_business", "uso_de_suelo", "licencia_municipal"],
        "procedures": procs,
    }


@app.get("/api/zone/{zone_code}")
async def get_zone(zone_code: str):
    """Complete zone profile with characteristics, costs, and crime data."""
    z = ZONES.get(zone_code)
    if not z:
        raise HTTPException(404, "Zona no encontrada")
    crime = CRIME["crime_by_zone"].get(zone_code, {})
    return {
        "zone_code": zone_code,
        "name": z["name"],
        "type": z.get("type", ""),
        "characteristics": {
            "population": z["population"],
            "foot_traffic_daily": z["foot_traffic_daily"],
            "vehicular_traffic_daily": z["vehicular_traffic_daily"],
            "crime_index": z["crime_index"],
            "business_density_per_10k": z["business_density_per_10k"],
            "zone_tags": z.get("characteristics", []),
        },
        "costs": {
            "rental_sqm_annual_mxn": z["rental_cost_sqm_annual"],
            "rental_monthly_per_100sqm": round(z["rental_cost_sqm_annual"] * 100 / 12),
        },
        "growth": {
            "population_annual_pct": z["population_growth_annual"],
            "expansion_rate": z["expansion_rate"],
        },
        "regulations": {
            "parking_restaurant": z.get("parking_requirement_restaurant", ""),
            "zone_type": z.get("type", ""),
        },
        "crime_detail": crime,
    }


@app.get("/api/business-types")
async def list_business_types():
    """Full catalog of supported SCIAN business types."""
    return BUSINESS_TYPES


@app.get("/api/zones")
async def list_zones():
    """All 16 CDMX boroughs with key metrics."""
    return {
        k: {
            "name": v["name"],
            "type": v.get("type", ""),
            "foot_traffic_daily": v["foot_traffic_daily"],
            "crime_index": v["crime_index"],
            "rental_sqm_annual": v["rental_cost_sqm_annual"],
        }
        for k, v in ZONES.items()
    }
