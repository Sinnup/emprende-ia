# Workflow: Complete Viability Check

## Trigger
User submits form with: business_type, location, budget, space_sqm

## Steps

### Step 1: Input Validation (5ms)
```
Validate business_type exists in BUSINESS_TYPES
Validate location exists in ZONES
Validate budget > 0
Validate space_sqm > 0 and < 10000
→ If invalid: return 400 error with message
```

### Step 2: Load Profiles (10ms)
```
business_profile = BUSINESS_TYPES[business_type]
zone_profile = ZONES[location]
cost_template = COSTS[business_type]
crime_data = CRIME['by_zone'][location]
```

### Step 3: Calculate Rental Cost (5ms)
```
rental_sqm_annual = zone_profile['rental_cost_sqm_annual']
rental_monthly = (rental_sqm_annual * space_sqm) / 12
→ Adjust cost_template['monthly_fixed']['rent']
```

### Step 4: Calculate Budget Factor (5ms)
```
first_year_total = cost_template['first_year_total']
if user_budget >= first_year_total:
    budget_score = 15
elif user_budget >= first_year_total * 0.8:
    budget_score = 10
else:
    budget_score = 3
```

### Step 5: Calculate Competition Factor (5ms)
```
business_density = zone_profile['business_density_per_10k']
if business_density < 20:
    competition_score = 20
elif business_density < 50:
    competition_score = 15
elif business_density < 100:
    competition_score = 8
else:
    competition_score = 3
```

### Step 6: Calculate Location Factor (5ms)
```
foot_traffic = zone_profile['foot_traffic_daily']
if foot_traffic > 5000:
    location_score = 20
elif foot_traffic > 2000:
    location_score = 15
else:
    location_score = 8
```

### Step 7: Calculate Security Factor (5ms)
```
crime_index = crime_data[business_category]['overall']
if crime_index < 40:
    security_score = 15
elif crime_index < 70:
    security_score = 10
else:
    security_score = 3
```

### Step 8: Calculate Growth Factor (5ms)
```
growth_rate = zone_profile['population_growth_annual']
if growth_rate > 0.02:
    growth_score = 15
elif growth_rate > 0.01:
    growth_score = 10
else:
    growth_score = 5
```

### Step 9: Calculate Legal Factor (5ms)
```
Check if all required procedures attainable
Check if any blockers
legal_score = 15 (if all attainable) OR 10 OR 3
```

### Step 10: Calculate Total Score (5ms)
```
score = (
    budget_score * 0.15 +
    competition_score * 0.20 +
    location_score * 0.20 +
    security_score * 0.15 +
    growth_score * 0.15 +
    legal_score * 0.15
)
→ Round to nearest integer
```

### Step 11: Get Interpretation (5ms)
```
if score >= 80:
    label = "Highly Viable"
    recommendation = "Strong indicators, proceed"
elif score >= 65:
    label = "Viable"
    recommendation = "Proceed, monitor risks"
elif score >= 50:
    label = "Marginal"
    recommendation = "High risk, needs careful planning"
else:
    label = "Not Recommended"
    recommendation = "Multiple red flags, reconsider"
```

### Step 12: Get Procedures (5ms)
```
procedures = PROCEDURES['by_type'][business_type]
for each procedure:
    - Add timeline
    - Add cost
    - Add documents
    - Add blocking dependencies
```

### Step 13: Compile Response (5ms)
```
response = {
    viability_score: score,
    factors: {budget, competition, location, security, growth, legal},
    cost_breakdown: {...},
    procedures: [...],
    risks: [...],
    recommendation: "..."
}
→ Return JSON
```

## Total Time: ~85ms (well under 100ms target)

## Error Handling
- Invalid input → 400 Bad Request
- Missing data → 404 Not Found
- Calculation error → 500 Internal Server Error

