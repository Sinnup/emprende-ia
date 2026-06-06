# Agent: Viability Assessment

## Role
Determines if a business will succeed in a specific CDMX location based on 6 factors.

## Responsibilities
1. Accept user input: business type, location, budget, space size
2. Look up business profile (startup capital, monthly costs, success rate baseline)
3. Look up zone characteristics (foot traffic, crime, growth, competition)
4. Calculate 6-factor viability score (0-100)
5. Return detailed assessment with risks and recommendations

## Data Dependencies
- `business-types.json` — Startup capital, monthly costs, baseline success rate
- `zones.json` — Foot traffic, crime index, growth rate, business density
- `costs.json` — Monthly/annual projections
- `crime-index.json` — Security risks by zone and business type
- `viability-model.json` — 6-factor weights and scoring logic

## Input Format
```json
{
  "business_type": "722110",
  "location": "cuauhtemoc",
  "user_budget_mxn": 250000,
  "space_sqm": 100,
  "entity_type": "individual"
}
```

## Output Format
```json
{
  "viability_score": 72,
  "viability_label": "Viable",
  "recommendation": "Proceed, monitor risks",
  "factors": {
    "budget": {...},
    "competition": {...},
    "location": {...},
    "security": {...},
    "growth": {...},
    "legal": {...}
  },
  "risks": [...]
}
```

## Workflow
1. Validate inputs (business type exists, zone exists, budget >0)
2. Load business profile from `business-types.json`
3. Load zone characteristics from `zones.json`
4. Calculate each factor:
   - Budget: Compare user_budget to first-year costs
   - Competition: Look up businesses per 10k in zone
   - Location: Get foot traffic for zone
   - Security: Look up crime index for business type in zone
   - Growth: Get zone growth rate
   - Legal: Check if all procedures attainable
5. Apply weights from `viability-model.json`
6. Return interpreted score with recommendations

## Error Handling
- If business type not found: Return 400 "Business type not supported"
- If zone not found: Return 400 "Location not found"
- If budget < minimum: Return advisory "Insufficient capital"

