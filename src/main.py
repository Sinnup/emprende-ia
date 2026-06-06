from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
FRONTEND_DIR = BASE_DIR / "src" / "frontend"

with open(DATA_DIR / "business-types.json") as f:
    BUSINESS_TYPES = json.load(f)
with open(DATA_DIR / "zones.json") as f:
    ZONES = json.load(f)
with open(DATA_DIR / "procedures.json") as f:
    PROCEDURES = json.load(f)
with open(DATA_DIR / "costs.json") as f:
    COSTS = json.load(f)
with open(DATA_DIR / "crime-index.json") as f:
    CRIME_INDEX = json.load(f)
with open(DATA_DIR / "viability-model.json") as f:
    VIABILITY_MODEL = json.load(f)

app = FastAPI(title="ViabilidadMX API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ViabilityRequest(BaseModel):
    business_type: str
    zone: str
    user_budget_mxn: float
    space_sqm: float
    entity_type: str = "individual"


def get_procedure_sequence(business_type: str) -> list:
    food_types = {"722110", "722210"}
    office_types = {"551020"}
    if business_type in food_types:
        return PROCEDURES["procedure_sequences"]["restaurant"]
    elif business_type in office_types:
        return PROCEDURES["procedure_sequences"]["oficina"]
    else:
        return PROCEDURES["procedure_sequences"]["tienda_retail"]


def calculate_viability(req: ViabilityRequest) -> dict:
    bt = BUSINESS_TYPES["business_types"].get(req.business_type)
    z = ZONES["zones"].get(req.zone)
    costs = COSTS["costs"].get(req.business_type)
    crime = CRIME_INDEX["crime_by_zone"].get(req.zone)
    model = VIABILITY_MODEL

    if not bt:
        raise HTTPException(status_code=404, detail=f"Tipo de negocio '{req.business_type}' no encontrado")
    if not z:
        raise HTTPException(status_code=404, detail=f"Zona '{req.zone}' no encontrada")

    monthly_fixed = costs["monthly_fixed_total"] if costs else bt["monthly_fixed"]
    runway = req.user_budget_mxn / monthly_fixed if monthly_fixed > 0 else 0

    # 1. Budget factor
    if runway >= 12:
        budget_score = model["factors"]["budget"]["scoring"]["sufficient"]
        budget_status = "sufficient"
    elif runway >= 6:
        budget_score = model["factors"]["budget"]["scoring"]["marginal"]
        budget_status = "marginal"
    else:
        budget_score = model["factors"]["budget"]["scoring"]["insufficient"]
        budget_status = "insufficient"

    # 2. Competition factor
    density = z["business_density_per_10k"]
    if density < 20:
        comp_score = model["factors"]["competition"]["scoring"]["low"]
        comp_status = "low"
    elif density < 50:
        comp_score = model["factors"]["competition"]["scoring"]["medium"]
        comp_status = "medium"
    elif density < 100:
        comp_score = model["factors"]["competition"]["scoring"]["high"]
        comp_status = "high"
    else:
        comp_score = model["factors"]["competition"]["scoring"]["very_high"]
        comp_status = "very_high"

    # 3. Location factor
    foot_traffic = z["foot_traffic_daily"]
    if foot_traffic > 5000:
        loc_score = model["factors"]["location"]["scoring"]["high"]
        loc_status = "high"
    elif foot_traffic > 2000:
        loc_score = model["factors"]["location"]["scoring"]["medium"]
        loc_status = "medium"
    else:
        loc_score = model["factors"]["location"]["scoring"]["low"]
        loc_status = "low"

    # 4. Security factor
    crime_overall = crime["overall"] if crime else 50
    if crime_overall < 40:
        sec_score = model["factors"]["security"]["scoring"]["low"]
        sec_status = "low"
    elif crime_overall < 70:
        sec_score = model["factors"]["security"]["scoring"]["medium"]
        sec_status = "medium"
    else:
        sec_score = model["factors"]["security"]["scoring"]["high"]
        sec_status = "high"

    # 5. Growth factor
    growth = z["expansion_rate"]
    if growth > 0.02:
        grow_score = model["factors"]["growth"]["scoring"]["growing"]
        grow_status = "growing"
    elif growth > 0.01:
        grow_score = model["factors"]["growth"]["scoring"]["stable"]
        grow_status = "stable"
    else:
        grow_score = model["factors"]["growth"]["scoring"]["declining"]
        grow_status = "declining"

    # 6. Legal factor (all procedures are attainable via RETYS)
    legal_score = model["factors"]["legal"]["scoring"]["all_attainable"]
    legal_status = "all_attainable"

    total_score = budget_score + comp_score + loc_score + sec_score + grow_score + legal_score

    if total_score >= 80:
        label = "Altamente Viable"
        recommendation = "Adelante con confianza. Base solida para el exito en esta zona."
    elif total_score >= 65:
        label = "Viable"
        recommendation = "Procede con monitoreo de riesgos. Alta probabilidad de exito."
    elif total_score >= 50:
        label = "Marginal"
        recommendation = "Requiere planeacion cuidadosa. Considera alternativas de zona o tipo de negocio."
    else:
        label = "No Recomendado"
        recommendation = "Reconsiderar ubicacion o tipo de negocio. Multiples factores de alto riesgo."

    # Procedures
    procedure_keys = get_procedure_sequence(req.business_type)
    procedures_list = []
    for i, key in enumerate(procedure_keys):
        p = PROCEDURES["procedures"].get(key, {})
        procedures_list.append({
            "sequence": i + 1,
            "code": p.get("code", ""),
            "name": p.get("name_es", key),
            "description": p.get("description", ""),
            "timeline_days": p.get("timeline_days", 0),
            "cost_mxn": p.get("cost_mxn", 0),
            "agency": p.get("agency", ""),
            "documents": p.get("required_documents", []),
            "blocking": p.get("blocking", []),
        })

    total_proc_days = bt.get("procedures_days", sum(p["timeline_days"] for p in procedures_list))
    total_proc_cost = sum(p["cost_mxn"] for p in procedures_list)

    # Costs
    if costs:
        cost_data = {
            "procedures_total": costs["procedure_costs"],
            "initial_setup": costs["initial_setup"],
            "first_year_total": costs["first_year_total"],
            "monthly_fixed": costs["monthly_fixed_total"],
            "monthly_fixed_breakdown": costs["monthly_fixed"],
            "break_even_months": costs["break_even_months"],
            "runway_months": round(runway, 1),
            "estimated_revenue_monthly": costs["estimated_revenue_monthly"],
        }
        rev_monthly = costs["estimated_revenue_monthly"]
    else:
        cost_data = {
            "procedures_total": total_proc_cost,
            "initial_setup": round(bt["startup_capital"] * 0.1),
            "first_year_total": round(monthly_fixed * 12 + total_proc_cost),
            "monthly_fixed": monthly_fixed,
            "monthly_fixed_breakdown": {},
            "break_even_months": 8,
            "runway_months": round(runway, 1),
            "estimated_revenue_monthly": monthly_fixed * 2,
        }
        rev_monthly = monthly_fixed * 2

    # Risks
    risks = []
    sec_level = "Alto" if crime_overall >= 70 else "Medio" if crime_overall >= 40 else "Bajo"
    risks.append({"category": "Seguridad", "level": sec_level,
                  "detail": f"Indice de criminalidad: {crime_overall}/100"})

    comp_level = "Alto" if density >= 100 else "Medio" if density >= 50 else "Bajo"
    risks.append({"category": "Competencia", "level": comp_level,
                  "detail": f"{density} negocios por 10k habitantes"})

    cap_level = "Alto" if budget_status == "insufficient" else "Medio" if budget_status == "marginal" else "Bajo"
    risks.append({"category": "Capital", "level": cap_level,
                  "detail": f"Capital cubre {round(runway, 1)} meses de operacion"})

    risks.append({"category": "Legal", "level": "Bajo",
                  "detail": f"{len(procedures_list)} tramites alcanzables en ~{total_proc_days} dias"})

    # 12-month cash flow projection
    monthly_cashflow = []
    cumulative = -(cost_data["procedures_total"] + cost_data.get("initial_setup", 0))
    variable_ratio = bt.get("variable_ratio", 0.35)
    for month in range(1, 13):
        revenue = rev_monthly * (1 + 0.04 * (month - 1) / 12)
        monthly_costs = monthly_fixed + revenue * variable_ratio
        net = revenue - monthly_costs
        cumulative += net
        monthly_cashflow.append({
            "month": month,
            "revenue": round(revenue),
            "costs": round(monthly_costs),
            "net": round(net),
            "cumulative": round(cumulative),
        })

    return {
        "viability_score": total_score,
        "viability_label": label,
        "recommendation": recommendation,
        "success_probability": bt.get("success_rate", 0.65),
        "factors": {
            "budget": {"score": budget_score, "max": 15, "status": budget_status,
                       "details": f"Capital cubre {round(runway, 1)} meses"},
            "competition": {"score": comp_score, "max": 20, "status": comp_status,
                            "details": f"{density} negocios/10k hab."},
            "location": {"score": loc_score, "max": 20, "status": loc_status,
                         "details": f"{foot_traffic:,} peatones/dia"},
            "security": {"score": sec_score, "max": 15, "status": sec_status,
                         "details": f"Criminalidad: {crime_overall}/100"},
            "growth": {"score": grow_score, "max": 15, "status": grow_status,
                       "details": f"Crecimiento: {growth * 100:.1f}%/anio"},
            "legal": {"score": legal_score, "max": 15, "status": legal_status,
                      "details": f"{len(procedures_list)} tramites en ~{total_proc_days} dias"},
        },
        "cost_breakdown": cost_data,
        "procedures_required": procedures_list,
        "risks": risks,
        "estimated_monthly_revenue": rev_monthly,
        "monthly_cashflow": monthly_cashflow,
    }


@app.get("/")
async def serve_frontend():
    return FileResponse(str(FRONTEND_DIR / "index.html"))


@app.post("/api/viability-check")
async def viability_check(req: ViabilityRequest):
    return calculate_viability(req)


@app.get("/api/cost-estimate/{scian}/{zone}/{sqm}")
async def cost_estimate(scian: str, zone: str, sqm: float):
    costs = COSTS["costs"].get(scian)
    z = ZONES["zones"].get(zone)
    bt = BUSINESS_TYPES["business_types"].get(scian)
    if not z:
        raise HTTPException(status_code=404, detail="Zona no encontrada")
    if not bt:
        raise HTTPException(status_code=404, detail="Tipo de negocio no encontrado")
    if not costs:
        return {
            "business_type": bt["name_es"], "location": z["name"], "space_sqm": sqm,
            "note": "Estimacion basada en promedios de industria",
            "monthly_costs": {"total_fixed": bt["monthly_fixed"]},
            "procedure_costs": 2000,
            "setup_costs": round(bt["startup_capital"] * 0.1),
            "first_year_projection": {
                "total_costs": bt["monthly_fixed"] * 12 + 2000,
                "estimated_revenue": bt["monthly_fixed"] * 24,
                "break_even_month": 8,
            },
        }
    return {
        "business_type": costs["name"], "location": z["name"], "space_sqm": sqm,
        "monthly_costs": {**costs["monthly_fixed"], "total_fixed": costs["monthly_fixed_total"]},
        "procedure_costs": costs["procedure_costs"],
        "setup_costs": costs["initial_setup"],
        "first_year_projection": {
            "total_costs": costs["first_year_total"],
            "estimated_revenue": costs["estimated_revenue_monthly"] * 12,
            "profit_year_1": costs["estimated_revenue_monthly"] * 12 - costs["first_year_total"],
            "break_even_month": costs["break_even_months"],
        },
    }


@app.get("/api/procedures/{business_type}")
async def get_procedures(business_type: str):
    bt = BUSINESS_TYPES["business_types"].get(business_type)
    if not bt:
        raise HTTPException(status_code=404, detail="Tipo de negocio no encontrado")
    keys = get_procedure_sequence(business_type)
    procs = []
    total_cost = 0
    for i, key in enumerate(keys):
        p = PROCEDURES["procedures"].get(key, {})
        total_cost += p.get("cost_mxn", 0)
        procs.append({
            "sequence": i + 1, "code": p.get("code", ""),
            "name": p.get("name_es", key), "description": p.get("description", ""),
            "timeline_days": p.get("timeline_days", 0), "cost_mxn": p.get("cost_mxn", 0),
            "agency": p.get("agency", ""), "documents": p.get("required_documents", []),
            "blocking": p.get("blocking", []),
        })
    return {
        "business_type": bt["name_es"],
        "total_timeline_days": bt.get("procedures_days", sum(p["timeline_days"] for p in procs)),
        "total_cost_mxn": total_cost,
        "procedures": procs,
    }


@app.get("/api/zone/{zone_code}")
async def get_zone(zone_code: str):
    z = ZONES["zones"].get(zone_code)
    if not z:
        raise HTTPException(status_code=404, detail="Zona no encontrada")
    crime = CRIME_INDEX["crime_by_zone"].get(zone_code, {})
    return {
        "zone_code": zone_code, "name": z["name"], "type": z.get("type", ""),
        "characteristics": {
            "population": z["population"],
            "foot_traffic_daily": z["foot_traffic_daily"],
            "vehicular_traffic_daily": z["vehicular_traffic_daily"],
            "crime_index": z["crime_index"],
            "business_density_per_10k": z["business_density_per_10k"],
            "zone_characteristics": z.get("characteristics", []),
        },
        "costs": {"rental_sqm_annual_mxn": z["rental_cost_sqm_annual"]},
        "growth": {"population_annual_percent": z["population_growth_annual"], "expansion_rate": z["expansion_rate"]},
        "regulations": {"parking_restaurant": z.get("parking_requirement_restaurant", ""), "type": z.get("type", "")},
        "crime_detail": crime,
    }


@app.get("/api/business-types")
async def list_business_types():
    return BUSINESS_TYPES["business_types"]


@app.get("/api/zones")
async def list_zones():
    return {k: {"name": v["name"], "type": v.get("type", "")} for k, v in ZONES["zones"].items()}
