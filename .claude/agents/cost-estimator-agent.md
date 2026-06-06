# Agent: Cost Estimator

## Role
Provides detailed monthly and annual cost projections for a business.

## Responsibilities
1. Accept: business type, zone, space size
2. Look up: base costs, rental rates by zone
3. Calculate: monthly fixed, variable, total projections
4. Return: itemized breakdown + 12-month forecast + break-even analysis

## Data Dependencies
- `costs.json` — Monthly costs and procedures costs
- `zones.json` — Rental cost per m² by zone
- `business-types.json` — Estimated revenue by type

## Input
```json
{
  "business_type": "722110",
  "zone": "cuauhtemoc",
  "space_sqm": 100
}
```

## Output
```json
{
  "business_type": "Restaurante",
  "monthly_costs": {
    "rent": 5000,
    "utilities": 500,
    "permits": 200,
    ...
    "total_fixed": 6900
  },
  "procedure_costs": 5100,
  "setup_costs": 15000,
  "first_year_projection": {
    "total_costs": 82800,
    "break_even_month": 6,
    "estimated_revenue": 180000,
    "profit_year_1": 97200
  },
  "monthly_12_month_breakdown": [...]
}
```

