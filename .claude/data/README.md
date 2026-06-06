# Pre-Processed Data Files for SME Viability Platform

All files are JSON format, optimized for <1ms lookup performance.

## File Structure

### business-types.json
- **Purpose**: SCIAN taxonomy of business types
- **Records**: 9 main types (expandable to 100+)
- **Fields**: startup capital, monthly costs, success rates, procedure timelines
- **Lookup**: By SCIAN 6-digit code or category

### zones.json
- **Purpose**: All 16 CDMX boroughs with characteristics
- **Records**: 16 zones
- **Fields**: population, growth, foot traffic, rental costs, crime index, expansion rate, parking rules
- **Lookup**: By zone code or name

### procedures.json
- **Purpose**: Complete RETYS procedure catalog
- **Records**: 8 core procedures (expandable to 30+)
- **Fields**: timeline, cost, required documents, agency, blocking dependencies
- **Lookup**: By procedure code or business type

### costs.json
- **Purpose**: Detailed cost breakdown by business type
- **Records**: 7 business types with monthly/annual projections
- **Fields**: procedure costs, monthly fixed costs, variable ratios, break-even analysis
- **Lookup**: By SCIAN code

### crime-index.json
- **Purpose**: Security risk by zone and business type
- **Records**: 16 zones × crime categories + 9 business-specific risks
- **Fields**: robbery, theft, assault, vandalism scores (0-100)
- **Lookup**: By zone code or business type

### viability-model.json
- **Purpose**: 6-factor scoring algorithm
- **Records**: 6 factors with weights, thresholds, interpretation
- **Fields**: weight, scoring rules, logic, interpretation guide
- **Lookup**: Algorithms are pre-computed

### query-index.json
- **Purpose**: Fast reverse lookups for complex queries
- **Records**: Multiple indices (business→procedures, zone→type, etc.)
- **Fields**: Indexed mappings
- **Lookup**: Cross-reference queries

## API Contract for Claude Code

```python
# Backend will expose these endpoints:
GET    /api/business-type/{scian_code}          → business details
GET    /api/zone/{zone_code}                     → zone characteristics
GET    /api/procedures/{business_type}           → required procedures
GET    /api/cost-estimate/{scian}/{zone}/{sqm}  → cost projection
GET    /api/crime-risk/{zone}/{business_type}   → security assessment
POST   /api/viability-check                      → complete assessment
```

## Data Update Frequency

- **business-types.json**: Quarterly (INEGI updates)
- **zones.json**: Annual (demographic data)
- **procedures.json**: Real-time (RETYS website scraping recommended)
- **costs.json**: Quarterly (market data)
- **crime-index.json**: Monthly (CDMX security reports)
- **viability-model.json**: As needed (algorithm tuning)

## Sources & Validation

- SCIAN codes: https://www.inegi.org.mx/app/scian/
- Zone data: INEGI Census 2020 + CDMX statistics
- Procedures: RETYS (https://www.registrodetramitesyservicios.cdmx.gob.mx/)
- Costs: Industry averages + CDMX government publications
- Crime: INEGI + CDMX Secretaría de Seguridad
- Model: Expert estimation based on hackathon requirements

## Notes for Claude Code

1. All data is denormalized (some duplication) for performance
2. No external API calls needed at runtime (fully embedded)
3. Response time target: <100ms for any query
4. All timestamps in ISO 8601 format
5. All costs in MXN (Mexican Pesos)
6. All distances/areas in meters and square meters

