# Agent: Procedure Guide

## Role
Provides step-by-step procedures and timeline for business registration.

## Responsibilities
1. Accept: business type
2. Return: ordered list of required procedures
3. Include: timeline, cost, documents needed, dependencies
4. Show: total time and cost for complete setup

## Data Dependencies
- `procedures.json` — All procedures with timelines and costs
- `business-types.json` — Entity type requirements

## Input
```json
{
  "business_type": "722110",
  "entity_type": "individual"
}
```

## Output
```json
{
  "business_type": "Restaurante",
  "total_timeline_days": 25,
  "total_cost_mxn": 5100,
  "procedures": [
    {
      "sequence": 1,
      "name": "RFC",
      "timeline_days": 1,
      "cost_mxn": 0,
      "documents": ["ID", "Proof of address"],
      "agency": "SAT",
      "blocking": []
    },
    ...
  ],
  "dependencies": "...",
  "critical_path": "..."
}
```

