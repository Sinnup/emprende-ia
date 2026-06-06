# Claude Code Integration Guide

## Pre-Processed Data Ready

All data is now in JSON format, fully denormalized, cached in memory at startup.

### Data Files Location
```
/mnt/SEDECO/.claude/data/
├── business-types.json       (1.8 KB)
├── zones.json               (8.6 KB)
├── procedures.json          (4.2 KB)
├── costs.json               (3.0 KB)
├── crime-index.json         (2.7 KB)
├── viability-model.json     (2.4 KB)
└── query-index.json         (1.5 KB)
```

**Total**: ~24 KB (fits entirely in memory, <1ms access)

---

## Backend API Specification

### Endpoint 1: `/api/viability-check` (POST)

**Request**:
```json
{
  "business_type": "722110",
  "location": "Paseo de la Reforma 505, Cuauhtémoc",
  "user_budget_mxn": 250000,
  "space_sqm": 100,
  "entity_type": "individual"
}
```

**Response**:
```json
{
  "viability_score": 72,
  "viability_label": "Viable",
  "recommendation": "Proceed, monitor risks",
  "factors": {
    "budget": {"score": 15, "status": "sufficient", "details": "Budget covers first 8 months"},
    "competition": {"score": 15, "status": "medium", "count": 35, "per_10k": 45},
    "location": {"score": 20, "status": "high", "foot_traffic": 8500},
    "security": {"score": 10, "status": "medium", "crime_index": 65},
    "growth": {"score": 15, "status": "growing", "rate": 0.025},
    "legal": {"score": 15, "status": "all_attainable", "procedure_days": 25}
  },
  "cost_breakdown": {
    "procedures_total": 5100,
    "first_year_total": 82800,
    "monthly_fixed": 6900,
    "monthly_variable_avg": 5250,
    "break_even_months": 6,
    "runway_months": 8
  },
  "procedures_required": [
    {"name": "RFC", "timeline_days": 1, "cost_mxn": 0},
    {"name": "Registro Mercantil", "timeline_days": 3, "cost_mxn": 500},
    {"name": "Uso de Suelo", "timeline_days": 10, "cost_mxn": 600},
    {"name": "Licencia Municipal", "timeline_days": 5, "cost_mxn": 800},
    {"name": "SIAPEM", "timeline_days": 20, "cost_mxn": 2000},
    {"name": "Sanitario", "timeline_days": 10, "cost_mxn": 1200}
  ],
  "risks": [
    {"category": "Security", "level": "Medium", "detail": "Crime index 65 (moderate-high)"},
    {"category": "Competition", "level": "Medium", "detail": "35 restaurants per 10k population"},
    {"category": "Legal", "level": "Low", "detail": "All procedures attainable"}
  ],
  "success_probability": 0.65,
  "estimated_monthly_revenue": 15000
}
```

---

### Endpoint 2: `/api/cost-estimate/{scian}/{zone}/{sqm}` (GET)

**Request**:
```
GET /api/cost-estimate/722110/cuauhtemoc/100
```

**Response**:
```json
{
  "business_type": "Restaurante de servicio completo",
  "location": "Cuauhtémoc",
  "space_sqm": 100,
  "monthly_costs": {
    "rent": 4000,
    "utilities": 500,
    "permits": 200,
    "insurance": 400,
    "labor_base": 1500,
    "supplies": 300,
    "total_fixed": 6900
  },
  "procedure_costs": 5100,
  "setup_costs": 15000,
  "first_year_projection": {
    "total_costs": 82800,
    "estimated_revenue": 180000,
    "profit_year_1": 97200,
    "break_even_month": 6
  }
}
```

---

### Endpoint 3: `/api/procedures/{business_type}` (GET)

**Request**:
```
GET /api/procedures/722110
```

**Response**:
```json
{
  "business_type": "Restaurante",
  "total_timeline_days": 25,
  "total_cost_mxn": 5100,
  "procedures": [
    {
      "sequence": 1,
      "code": "TRM007",
      "name": "RFC",
      "timeline_days": 1,
      "cost_mxn": 0,
      "documents": ["ID", "Proof of address"],
      "blocking": [],
      "status": "Required"
    },
    {
      "sequence": 2,
      "code": "TRM001",
      "name": "Registro Mercantil",
      "timeline_days": 3,
      "cost_mxn": 500,
      "documents": ["RFC", "ID", "Proof of address"],
      "blocking": [],
      "status": "Required"
    }
    // ... more procedures
  ]
}
```

---

### Endpoint 4: `/api/zone/{zone_code}` (GET)

**Request**:
```
GET /api/zone/cuauhtemoc
```

**Response**:
```json
{
  "zone_code": "cuauhtemoc",
  "name": "Cuauhtémoc",
  "characteristics": {
    "population": 520000,
    "foot_traffic_daily": 8500,
    "vehicular_traffic_daily": 45000,
    "crime_index": 65,
    "business_density_per_10k": 280
  },
  "costs": {
    "rental_sqm_annual_mxn": 600
  },
  "growth": {
    "population_annual_percent": 0.012,
    "expansion_rate": 0.025
  },
  "regulations": {
    "parking_restaurant": "1 space per 100 sqm OR 1 per 20 seats",
    "type": "commercial_historic"
  }
}
```

---

## Frontend Requirements

### Input Form
```
Business Type Dropdown       → SCIAN codes from business-types.json
Location Search             → Zone names from zones.json  
Available Budget (MXN)      → Numeric input
Space Size (m²)            → Numeric input
Entity Type (Individual/Corp) → Radio buttons
```

### Output Dashboard
```
1. Viability Score (0-100)       → Numeric + color code
2. 6-Factor Breakdown           → Radar chart or bar chart
3. Cost Summary (12-month)       → Costs table
4. Monthly Projection           → Line chart showing cash flow
5. Procedures List              → Expandable cards with timeline
6. Risk Assessment              → Traffic light system
7. Recommendation Statement     → Text + next steps
```

---

## Load-Time Performance

All data pre-loaded at server startup:

```python
# startup.py
with open('.claude/data/business-types.json') as f:
    BUSINESS_TYPES = json.load(f)
with open('.claude/data/zones.json') as f:
    ZONES = json.load(f)
with open('.claude/data/procedures.json') as f:
    PROCEDURES = json.load(f)
# ... load other files

# Queries: <1ms guaranteed (dictionary lookups)
```

---

## 3-Minute Demo Walkthrough

**0:00-0:20**: Problem statement + introduce user
- "María wants to open a restaurant in Centro but doesn't know if it's viable"

**0:20-2:20**: Live product walkthrough (no cuts)
1. (0:20-0:30) Click on app, select "Restaurante"
2. (0:30-0:45) Enter location "Paseo de la Reforma, Cuauhtémoc"
3. (0:45-1:00) Enter budget: $200,000 MXN
4. (1:00-1:15) Enter space: 100 m²
5. (1:15-1:30) Click "Check Viability"
6. (1:30-1:45) Show results: Viability score 72%, cost breakdown, procedures
7. (1:45-2:00) Show procedures list with timeline
8. (2:00-2:15) Show risk assessment and recommendation
9. (2:15-2:20) Show cash flow projection

**2:20-3:00**: Learnings + what's next
- "Built in X hours, used real CDMX data, ready for SEDECO"

---

## Key Implementation Notes

1. **No Runtime API Calls**: All data embedded
2. **Sub-Second Responses**: All queries <100ms
3. **Full CDMX Coverage**: 16 zones, 9 business types, 8 procedures
4. **Real Legal Framework**: Based on actual CDMX regulations
5. **Modular Data**: Easy to update individual JSON files

