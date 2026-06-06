# Comprehensive SME Viability Platform for CDMX

Detailed scope analysis: 17 success factors, data sources, PDF integration, hackathon feasibility.

---

## Your 17 Success Factors: Complete Data Mapping

### Factor 1-3: BUSINESS FUNDAMENTALS

#### 1. Budget (User Input)
- **What**: Entrepreneur's available capital in MXN
- **Source**: User enters amount
- **Data Type**: Numeric input
- **Complexity**: Trivial
- **Example**: "I have $150,000"

#### 2. Business Type (User Input + INEGI Classification)
- **What**: Industry sector (restaurant, tienda, oficina, etc.)
- **Source**: User selects from dropdown (INEGI SCIAN codes)
- **Data Type**: Categorical
- **Reference**: INEGI SCIAN (Sistema de Clasificación Industrial de América del Norte)
- **Complexity**: Low (taxonomy)
- **URL**: https://www.inegi.org.mx/app/scian/
- **Example**: SCIAN 722110 (Full-service restaurants)

#### 3. Location (User Input + Geocoding)
- **What**: Specific address or zone in CDMX
- **Source**: User enters, tool geocodes to coordinates
- **Data Type**: Geographic (lat/lon)
- **Tools**: Google Maps API or CDMX geocoder
- **Complexity**: Low (geolocation)
- **Example**: "Paseo de la Reforma 505, Cuauhtémoc"

---

### Factor 4-5: REAL ESTATE & INFRASTRUCTURE

#### 4. Rental Cost (Market Data + Zone Analysis)
- **What**: Monthly rent in MXN per m²
- **Source**: Real estate market data by zone
- **Data Type**: Numeric
- **Availability**: Partial (needs research/synthesis)
- **Complexity**: Medium (varies by zone, building type)
- **Challenge**: Real-time rental data not freely available
- **Workaround**: INEGI provides median rental estimates by borough
- **URL**: https://www.inegi.org.mx/ (Encuesta Nacional de Ocupación y Empleo)
- **Synthetic Approach**: Zone-based averages
  - Centro: $500-800/m² annually
  - Polanco: $800-1500/m² annually
  - Industrial zones: $200-400/m² annually
- **Example**: Centro restaurant (100m²) = $50-80K/year

#### 5. Size - Square Meters (User Input)
- **What**: Physical space size in m²
- **Source**: User enters or selected from building options
- **Data Type**: Numeric
- **Complexity**: Trivial
- **Impact**: Scales rental costs, labor requirements, capacity
- **Example**: "100 square meters"

---

### Factor 6-8: LEGAL & PROCEDURAL FRAMEWORK

#### 6. Costs of Procedures (PDF + RETYS + Ley)
- **What**: Total MXN for all required registrations, permits, licenses
- **Source**: Extract from PDFs + RETYS procedures
- **Data Type**: Numeric
- **Required PDFs**:
  - ✓ Ley de Establecimientos Mercantiles
  - ✓ Reglamento de la Ley
  - ✓ RETYS procedure catalog
  - ? Cost breakdowns (may not exist in public docs)
- **Procedures to Track**:
  - Registro Mercantil (CDMX Commerce Registry)
  - Licencia Municipal (Municipal License)
  - Uso de Suelo (Land Use Certificate)
  - SIAPEM (Environmental Permit if applicable)
  - Sanitario (Health Permit if food)
  - Others by business type
- **Complexity**: High (multi-step, variable by type)
- **Synthetic Estimate**: 
  - Restaurant: $3K-5K in procedure costs
  - Tienda: $1.5K-2.5K
  - Oficina: $1K-2K
- **PDF Extraction**: Yes (must extract procedure names, timelines)

#### 7. Legal Procedures (PDF)
- **What**: Step-by-step process, timeline, required documents
- **Source**: Extract from Ley + Reglamento + RETYS
- **Data Type**: Structured (procedure → steps[] → documents[])
- **Complexity**: High (legal text parsing)
- **PDF Files**:
  - Ley de Establecimientos Mercantiles.pdf (primary)
  - Reglamento.pdf (implementation)
  - RETYS procedures (web export)
- **Extraction Method**: Manual + Claude AI for semantic parsing
- **Example Output**:
  ```json
  {
    "procedure": "Licencia Municipal",
    "steps": [
      {"step": 1, "name": "Solicitud CCDMX", "documents": ["RFC", "ID"], "days": 5},
      {"step": 2, "name": "Inspección", "documents": [], "days": 3},
      {"step": 3, "name": "Licencia Expedida", "documents": ["Comprobante"], "days": 2}
    ]
  }
  ```

#### 8. Competition (DENUE API + Aggregation)
- **What**: Count of same business type in zone + distance distribution
- **Source**: INEGI DENUE API
- **Data Type**: Numeric + spatial
- **API**: https://www.inegi.org.mx/servicios/api_denue.html
- **Complexity**: Medium (API integration + analysis)
- **What to Extract**:
  - Count of restaurants within 500m of location
  - Count within 1km, 2km
  - Market saturation index (businesses per 10k people)
  - Nearest competitor distance
- **Example**: "There are 47 restaurants within 1km (high competition)"

---

### Factor 9-11: MARKET & DEMOGRAPHIC FACTORS

#### 9. Insecurity Index (INEGI + CDMX Data)
- **What**: Crime rate specific to business type in zone
- **Source**: INEGI crime statistics + CDMX security reports
- **Data Type**: Risk score (0-100)
- **Availability**: INEGI provides by zone/crime type
- **Complexity**: High (complex data, requires normalization)
- **Data Sources**:
  - INEGI Encuesta Nacional de Victimización
  - CDMX Secretaría de Seguridad reports (by zone)
  - Crime classification by business type (e.g., robbery risk for retail)
- **URLs**:
  - https://www.inegi.org.mx/temas/incidencias/
  - https://www.datos.cdmx.gob.mx/dataset/incidentes-delictivos
- **Synthetic Model**: 
  - Robbery risk (retail): High in Centro, Low in residential
  - Assault risk (nightlife): High in Garibaldi, Low in Polanco
  - Vandalism: Zone-dependent
- **Example**: "Centro retail: 45/100 robbery risk (moderate-high)"

#### 10. Business Turnover Rate (INEGI + DENUE)
- **What**: % of businesses that survive 1 year in zone by type
- **Source**: INEGI business survival statistics + DENUE historical
- **Data Type**: Percentage (0-100)
- **Availability**: LIMITED (no official 1-year survival rates by zone)
- **Complexity**: Very High (requires longitudinal DENUE data)
- **Approximation**:
  - Use INEGI Encuesta Nacional de Ocupación y Empleo (ENOE) for sector-wide survival
  - Combine with zone economic health (growth rate)
- **Synthetic Model**:
  - Restaurants: 65% survive 1 year nationally
  - Zone multiplier: Centro (stable) = 1.0x, Emerging = 0.8x
  - Adjusted: Centro restaurant = 65% baseline
- **Example**: "Restaurant in Centro: 65% estimated 1-year survival"

#### 11. Pedestrian Flow (INEGI Census + Inference)
- **What**: Estimated daily foot traffic at location
- **Source**: INEGI economic census data + zone classification
- **Data Type**: Numeric (estimated people/day)
- **Availability**: Census-level only (not street-level)
- **Complexity**: High (requires inference from zone type)
- **Data Sources**:
  - INEGI Censo Económico (establishes foot traffic proxies)
  - Zone classification (commercial vs. residential vs. mixed)
  - Population density in 500m radius
- **Synthetic Model**:
  - Centro commercial: 5K-10K people/day
  - Polanco high-end: 2K-4K (but high purchasing power)
  - Residential: 500-1.5K people/day
- **Example**: "Paseo de la Reforma (Centro): ~8K pedestrians/day"

---

### Factor 12-14: INFRASTRUCTURE & PHYSICAL CONSTRAINTS

#### 12. Vehicular Flow (INEGI Transport Data)
- **What**: Estimated daily vehicle traffic on street
- **Source**: INEGI transport surveys + zone routing
- **Data Type**: Numeric (vehicles/day)
- **Availability**: Zone-level aggregate
- **Complexity**: High (not street-level granular data)
- **Data Sources**:
  - INEGI Encuesta Origen-Destino de Viajes (EODV)
  - CDMX traffic patterns by avenue
- **Synthetic Model**:
  - Major avenues (Paseo de la Reforma): 50K+ vehicles/day
  - Secondary streets: 5K-20K vehicles/day
  - Residential: <5K vehicles/day
- **Example**: "Calle local in Coyoacán: ~3K vehicles/day"

#### 13. Parking Spaces (CDMX Regulation + Building Data)
- **What**: Available parking spaces required/provided by CDMX law
- **Source**: CDMX building codes + lot data
- **Data Type**: Count + regulation requirement
- **Availability**: Partial (regulations published, actual spaces vary)
- **Complexity**: Medium (regulatory logic + site-specific)
- **CDMX Regulations**:
  - Restaurants 100m²: Minimum 1 space per 100m² OR 1 per 20 seats (varies by borough)
  - Retail/Tiendas: 1 space per 200m² (typical)
  - Offices: 1 space per 100m²
  - Rules vary by CDMX entity (Cuauhtémoc vs. Gustavo A. Madero, etc.)
- **PDF Reference**: CDMX Reglamento de Zonificación
- **Example**: "Your 100m² restaurant needs 1 space (not available in building) = BARRIER"

#### 14. Building Age (Real Estate Data)
- **What**: Year built, impacts suitability for food/health services
- **Source**: Real estate records, building registries, owner input
- **Data Type**: Year, or age category (new <5yr, old >30yr)
- **Availability**: Partial (official building registry not fully public)
- **Complexity**: Medium (sourcing + analysis)
- **Impact Rules**:
  - Food business in >50yr old building without renovation = HIGH RISK (plumbing, electrical)
  - Retail in well-maintained building = LOW RISK
  - Historic zone (Centro) = older buildings OK if regulated
- **Example**: "Building built 1950, no recent renovation = not suitable for food business"

---

### Factor 15-17: GROWTH & EXPANSION METRICS

#### 15. Growth by Buildings (Construction/Development Rate)
- **What**: New construction rate in zone (buildings/year)
- **Source**: CDMX SEDUVI + construction permits
- **Data Type**: Numeric (new permits/year)
- **Availability**: Published by SEDUVI
- **Complexity**: Low (aggregate statistic)
- **URL**: http://ciudadmx.cdmx.gob.mx:8080/seduvi/
- **Implication**: High construction = gentrification/rising rents
- **Example**: "Centro: 15 new buildings/year (rising rents, opportunity?)"

#### 16. Growth by People (Population Growth Rate)
- **What**: % population growth in zone per year
- **Source**: INEGI Census data + estimates
- **Data Type**: Percentage
- **Availability**: INEGI publishes estimates
- **Complexity**: Low (aggregate statistic)
- **Data Sources**:
  - INEGI Censo de Población y Vivienda (2020)
  - INEGI population projections
- **Implication**: Growing population = more customers, but also more competition
- **Example**: "Cuauhtémoc: 1.2% annual growth (slow)"

#### 17. Expansion Rate (Economic Activity Index)
- **What**: Overall economic growth in zone (% annual)
- **Source**: INEGI Índice de Volumen Físico del Sector Servicios + zone metrics
- **Data Type**: Percentage
- **Availability**: Sectoral level (not zone-specific)
- **Complexity**: High (requires synthesis)
- **Indicator**: Proxy = growth in establishment count (DENUE year-over-year)
- **Example**: "Centro services sector: 2.5% annual expansion"

---

## PDF Integration Requirements

### PDFs to Extract & Parse

#### 1. Ley de Establecimientos Mercantiles (PRIMARY)
- **File**: `/context/SecretarIA/Ley_Establecimientos_Mercantiles.pdf`
- **Extract**:
  - Definition of SME vs. large business
  - Legal classifications (individual, partnership, corporation)
  - Permit requirements by business type
  - Procedure steps and timeline
  - Cost implications
- **Method**: PDF → Text extraction (pdfplumber) → Claude AI semantic parsing
- **Output**: Structured JSON with procedures, requirements, definitions

#### 2. Reglamento de la Ley (SECONDARY)
- **File**: `/context/SecretarIA/Reglamento_Ley_Establecimientos.pdf`
- **Extract**:
  - Implementation details
  - Specific cost breakdowns
  - Zone-specific variations
  - Entity-specific rules (Cuauhtémoc vs. other boroughs)
  - Building code implications (parking, electrical, plumbing)
- **Method**: PDF parsing → Cross-reference with Ley
- **Output**: Detailed implementation guide per entity

#### 3. RETYS Procedure Catalog (WEB + PDF EXPORT)
- **Source**: https://www.registrodetramitesyservicios.cdmx.gob.mx/
- **Extract**:
  - Complete procedure list for "Mercantile Establishments"
  - Steps, documents, costs, timelines
  - Required agencies/windows
- **Method**: Web scraping or PDF export → Structured data
- **Output**: Procedure database indexed by business type

#### 4. SIAPEM Environmental Procedures (IF APPLICABLE)
- **Source**: https://siapem.cdmx.gob.mx/
- **Extract**: Environmental permit requirements by sector
- **Method**: Document review + classification
- **Output**: Conditional environmental requirements

---

## Data Availability Assessment

### Tier 1: Available Data (Use Real Sources)
- ✓ Legal framework (PDFs available)
- ✓ Procedures (RETYS + PDFs)
- ✓ Competition (DENUE API)
- ✓ Zoning rules (SEDUVI)
- ✓ Population/census (INEGI public)
- ✓ Parking regulations (CDMX published)

### Tier 2: Partially Available (Research + Synthesis)
- ~ Rental costs (estimates by zone available)
- ~ Crime statistics (INEGI by zone, must map to business type)
- ~ Building ages (real estate platforms have samples)
- ~ Traffic patterns (INEGI EODV provides zone estimates)
- ~ Growth rates (INEGI sector-level, extrapolate to zones)

### Tier 3: Not Available (Synthetic Data Required)
- ✗ Business turnover rates by zone (synthesize from national + zone health)
- ✗ Street-level foot traffic (synthesize from zone type + population)
- ✗ Success factors correlation weights (expert estimation)
- ✗ Cost templates by business type (industry averages + synthesis)

---

## Success Factor Correlation Model

### Simplified Viability Score (Hackathon-Feasible)

```
Viability_Score (0-100) = Weighted Sum

Budget_Factor (15 points)
  - ✓ Budget >= setup + 12mo costs: +15
  - ~ Budget 80-100% of needed: +10
  - ✗ Budget < 80% of needed: +3

Competition_Factor (20 points)
  - Low (<20 competitors per 10k): +20
  - Medium (20-50 per 10k): +15
  - High (50-100 per 10k): +8
  - Very High (>100 per 10k): +3

Location_Factor (20 points)
  - High foot traffic (>5k/day): +20
  - Medium (2k-5k/day): +15
  - Low (<2k/day): +8

Security_Factor (15 points)
  - Low crime (score <40): +15
  - Medium (40-70): +10
  - High (>70): +3

Growth_Factor (15 points)
  - Growing zone (>2% annual): +15
  - Stable (1-2%): +10
  - Declining (<1%): +5

Legal_Factor (15 points)
  - All procedures attainable (no blockers): +15
  - Minor blockers (solvable): +10
  - Major blockers (expensive fixes): +3

Total: 0-100 (below 50 = not viable, 70+ = viable)

Result Interpretation:
  - 80-100: Highly viable, likely success
  - 65-79: Viable, moderate risk
  - 50-64: Marginal, high risk
  - <50: Not recommended
```

---

## Hackathon Feasibility Assessment

### MVP Scope (5-6 hours) — Core Viability

**MUST BUILD**:
1. ✓ PDF extraction (Ley + Reglamento)
2. ✓ Procedure list from PDFs
3. ✓ Business type input + SCIAN classification
4. ✓ Location input + geocoding
5. ✓ Basic competition analysis (DENUE API)
6. ✓ Legal procedures display
7. ✓ Cost estimation (procedure + rental estimate)
8. ✓ Viability score (6-factor model)

**DATA**:
- Real: Legal PDFs, DENUE API, INEGI census
- Synthetic: Rental costs, crime mapping, success rates

**TIME BUDGET**:
- Claude Code scaffolding: 1 hour
- PDF extraction + parsing: 1.5 hours
- Procedure logic: 1 hour
- Viability scoring: 1 hour
- Testing + UI: 1 hour
- **Total: 5.5 hours**

### Extended Scope (7-8 hours) — Add Recommendation Engine

**COULD ADD** (if time):
- Business recommendation (inverse query)
- Location ranking by success probability
- Detailed cash flow projections
- Risk visualization (radar charts)

**TIME**: +1.5-2 hours

---

## Recommended Approach: Multi-Phase

### Phase 1: Hackathon MVP (5-6 hours)
```
Input: Business type + Location + Budget
Output: 
  - Viability score (0-100)
  - Cost breakdown (procedures + rent estimate)
  - Competition analysis
  - Regulatory requirements
  - Risk factors
  - Success probability estimate
```

### Phase 2: Post-Hackathon Enhancement
```
Add:
  - Real-time rental data (Inmuebles24 API)
  - Advanced ML model (historic DENUE data)
  - Business recommendation engine
  - Location heat maps
  - Monthly projection with scenarios
```

---

## Critical Questions Before Implementation

1. **PDF Parsing**: Use Claude AI to parse legal PDFs into structured data?
2. **DENUE API**: Real-time API calls during hackathon, or cached sample data?
3. **Crime Data**: INEGI raw data, or curated dataset?
4. **Viability Weights**: Use proposed 6-factor model, or different weighting?
5. **SCIAN Codes**: How detailed (3-digit, 6-digit)?
6. **Zone Granularity**: CDMX boroughs, neighborhoods, or specific addresses?

---

*Analysis: June 6, 2026 — Comprehensive SME viability platform specification*
