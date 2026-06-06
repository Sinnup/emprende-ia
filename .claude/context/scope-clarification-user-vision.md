# Scope Clarification: User Vision vs. Challenge Description

## User's Proposed Solution

### Core Capabilities
1. **Business Success Probability** (1-year forecast)
   - ML model: Will this business survive 12 months?
   - Based on: location, business type, competition, capital

2. **Monthly Cost Breakdown** (itemized)
   - Fixed costs: rent, utilities, permits, insurance, taxes
   - Variable costs: inventory, labor, marketing
   - Aggregated by month × 12

3. **Budget Feasibility Assessment**
   - Compare: User's capital vs. first-year total costs
   - Cash flow projection: month-by-month
   - Break-even analysis

4. **Business Recommendation Engine**
   - Input: "I have $X budget, I prefer zone Y, I have skills Z"
   - Output: "You can succeed with these 3 business ideas in these 5 locations"
   - Based on: historic success rates, competition, costs

5. **Location Recommendation**
   - "Restaurant would succeed best in these zones"
   - Ranked by success probability, cost, competition

---

## Original Challenge Description

### Stated Requirements
"Tu trabajo: Construir una herramienta que permita a los emprendedores o inversionistas saber si su negocio puede ser viable; conocer los pasos que debe seguir desde su constitución como sociedad o actuación como persona física; afluencia en la zona, competencia, los trámites y permisos que debe obtener, la forma de participar en programas de emprendimiento de la CDMX, entre otros."

**Translation**: Build a tool that allows entrepreneurs/investors to:
1. Know if their business **can be viable** ✓ (vague on "viability")
2. Know the steps for constitution (individual vs. corporate) ✓
3. View zone metrics (foot traffic, competition) ✓
4. Learn procedures & permits ✓
5. Discover CDMX entrepreneurship programs ✓
6. "Among others" (open-ended)

### Original MVP Interpretation (My Analysis)
- Business type + location → Viability Yes/No
- Show required procedures in order
- Display zone metrics (competition count)
- Registration process guide
- Links to CDMX programs

---

## Comparison: Original vs. User Vision

### Scope Dimensions

| Dimension | Original Challenge | User Vision | Difference |
|-----------|-------------------|-------------|-----------|
| **Viability Definition** | Zone compatibility + legal compliance | Success probability + financial feasibility | Major |
| **Data Needed** | Business type, location, zoning rules | Historic business outcomes + cost data | Major |
| **Output** | Yes/No + procedures | Success %, costs, recommendations, locations | Major |
| **Complexity** | Deterministic logic | ML/statistical models | Major |
| **User Input** | Business type + location | Budget, capital, skills, preferences | Major |
| **Economic Analysis** | None | Monthly costs + cash flow + break-even | Major |

### Feature Mapping

#### In Original Challenge ✓
- Zone viability (location compatibility)
- Procedural guidance
- Competition metrics
- Registration process
- CDMX programs

#### In User Vision (NOT in Challenge) ✗
- **1-year success forecasting** (no historical data mentioned)
- **Monthly cost breakdown** (no cost data sources mentioned)
- **Budget feasibility** (no financial modeling)
- **Business recommendation engine** (inverse: given budget, recommend businesses)
- **Location recommendation** (ranking zones by success)
- **Cash flow projections** (12-month timeline)
- **Break-even analysis** (financial metrics)

---

## Data Availability Analysis

### Original Challenge Data Sources
- ✓ RETYS (procedures)
- ✓ SEDUVI (zoning)
- ✓ DENUE (competition count)
- ✓ SIAPEM (environmental permits)
- ✗ Historic business outcomes (NOT provided)
- ✗ Costs per business type (NOT provided)
- ✗ Success rates by zone (NOT provided)
- ✗ Monthly expense templates (NOT provided)

### User Vision Data Needs
- **Success rates**: Where do restaurants succeed? 60% in Centro, 40% in Industrial?
- **Cost templates**: Restaurant fixed costs = $3K-5K/month?
- **Historic outcomes**: 500 restaurants opened 2022-2024, 350 survived 1 year?
- **Competitive pressure**: High competition = lower margins = higher failure rate?
- **Market saturation**: Zone X has 50 restaurants per 10k people (saturated)?

**Problem**: User vision requires data that's NOT available in hackathon brief

---

## Viability Assessment: Two Interpretations

### Interpretation 1: LEGAL/PROCEDURAL Viability (Original Challenge)
```
Question: Can I legally open a restaurant here?
Answer: Yes, because:
  ✓ Land use zoning allows restaurants in Centro
  ✓ You have no criminal record (assumed)
  ✓ You can follow the 8-step registration process
  ✓ You can obtain required permits

Time: Instant (rules-based logic)
Requires: Zoning rules, legal framework (available)
```

### Interpretation 2: FINANCIAL Viability (User Vision)
```
Question: Will my $100K restaurant in Centro succeed in 1 year?
Answer: 65% success probability, because:
  ✓ Centro has high foot traffic (good)
  ✓ 42 restaurants per 10k people (competitive)
  ✓ Your estimated costs: $45K first year
  ✓ Your estimated revenue: $180K first year
  ✓ You have 12-month runway (adequate capital)
  ✗ BUT competition is high (forces lower margins)
  → Viability = MEDIUM (doable, but risky)

Time: 5 minutes (data lookup + model prediction)
Requires: Historic data, cost templates, ML model (NOT available)
```

---

## Hackathon Reality Check

### Challenge: No Financial Data Provided

The hackathon brief mentions:
- RETYS (procedures) ✓
- SEDUVI (zoning) ✓
- DENUE (competition) ✓
- SIAPEM (environmental) ✓

But does NOT mention:
- Historic business outcomes ✗
- Cost data ✗
- Success rate benchmarks ✗
- Financial templates ✗

### Challenge Solution: Synthetic Data

The brief explicitly states:
> "Los datos sobre los trámites pueden obtenerse del RETYS, de la Ley de Establecimientos Mercantiles y de su Reglamento o de búsqueda libre en internet. Tú inventas datos sintéticos plausibles y construyes sobre eso."

**Translation**: "Procedure data comes from RETYS and law. YOU INVENT PLAUSIBLE SYNTHETIC DATA and build on that."

**Implication**: Creating synthetic cost + success data is ALLOWED for hackathon

---

## Scope Decision Matrix

### Option A: Original Challenge (Procedural Viability)
**Modules**:
1. Zone viability check (legal/zoning)
2. Procedural roadmap
3. Competition analysis
4. Registration guide
5. CDMX programs

**Effort**: 3-4 hours  
**Data**: All available (RETYS, SEDUVI, DENUE)  
**Hackathon Fit**: Perfect (matches original challenge)  
**Scoring Risk**: Low (clear requirements)

### Option B: User Vision (Financial Viability)
**Modules**:
1. Zone viability (legal + financial)
2. Cost breakdown (12-month, itemized)
3. Success probability model
4. Budget feasibility
5. Business recommendation engine
6. Location recommendation

**Effort**: 6-8 hours  
**Data**: 50% available (competition), 50% synthetic (costs, outcomes)  
**Hackathon Fit**: Good (extends original challenge with "entre otros")  
**Scoring Risk**: Medium (goes beyond stated requirements, but "among others" allows it)

### Option C: Hybrid MVP (Best of Both)
**Core MVP (3-4 hours)**:
1. Zone viability (legal checks)
2. Procedural roadmap
3. Compete analysis

**Extended (add 2-3 hours)**:
4. Monthly cost breakdown (synthetic)
5. Success probability (synthetic model)
6. Budget feasibility

**Effort**: 5-6 hours total  
**Data**: 70% available, 30% synthetic  
**Hackathon Fit**: Excellent (matches original + adds financial layer)  
**Scoring Risk**: Low (clearly more complete than original)

---

## Scoring Impact Analysis

### Criterion A: Quality & Solution Fit

**Option A (Original)**: 
- Meets challenge requirements exactly
- User gets procedural guidance (useful)
- **Score**: 3-4/5 (adequate but basic)

**Option B (User Vision)**:
- Goes beyond challenge requirements
- User gets financial guidance + recommendations
- More valuable to actual entrepreneur
- **Score**: 4-5/5 (excellent but risky if incomplete)

**Option C (Hybrid)**:
- Core meets requirements, extended adds value
- User gets both procedural + financial guidance
- Risk-managed (core is solid, extensions are bonus)
- **Score**: 5/5 (complete solution)

### Criterion B: Technical Execution

**Option A**: Simple (rule-based, deterministic)  
**Option B**: Complex (ML model, synthetic data) → Risk  
**Option C**: Moderate (rule-based core + simple model) → Manageable

### Criterion C: SEDECO Operational Fit

**Option A**: Fits SEDECO's procedural knowledge  
**Option B**: Requires financial modeling (beyond SEDECO's normal scope)  
**Option C**: Hybrid approach (procedures from SEDECO + finance as extension)

---

## My Recommendation

### Go with Option C: Hybrid MVP

**Rationale**:

1. **Meets Challenge**: Original requirements + "entre otros"
2. **Adds Value**: Financial feasibility (what user actually needs)
3. **Risk-Managed**: Core is solid, extensions are bonus
4. **Time-Efficient**: 5-6 hours fits 8-hour sprint
5. **Scoring**: Likely 4.5-5/5 (exceeds original but still verifiable)

### Module Sequence

#### Tier 1: Core MVP (3-4 hours) - MUST DO
```
Module 1: Zone Viability Check
  - Legal/zoning compatibility
  - Competition count
  - Foot traffic estimate

Module 2: Regulatory Roadmap
  - Procedures in order
  - Documents needed
  - Timeline

Module 3: Registration Guide
  - Individual vs. Corporate
  - Steps + documents
```

#### Tier 2: Extended Features (2-3 hours) - SHOULD DO
```
Module 4: Cost Breakdown
  - Monthly fixed costs (synthetic)
  - Monthly variable costs (synthetic)
  - 12-month total + monthly cash flow

Module 5: Success Probability
  - Simple model: Zone + Competition + Capital → Success %
  - Based on synthetic benchmarks
  - Caveats clearly stated (hackathon data)

Module 6: Business Recommendation (IF TIME)
  - "Given $X budget + zone preference, here are viable businesses"
  - With estimated costs + success rate
```

### Data Strategy

#### Available (Use Real Data)
- Zoning rules (synthetic, but based on real SEDUVI structure)
- Procedures (manual extraction from RETYS)
- Competition counts (synthetic DENUE sample)

#### Synthetic but Plausible (Hackathon-Valid)
- Monthly costs by business type
  - Restaurant: $3K-5K fixed, $0.5-1K per $1K revenue variable
  - Tienda: $2K-3K fixed, $0.2-0.4K per $1K revenue variable
  - Oficina: $1.5K-2K fixed, $0.1-0.2K per $1K revenue variable
- Success rates by zone + competition level
  - Centro high-traffic: 70% success (competitive)
  - Industrial medium-traffic: 60% success
  - Residential low-traffic: 50% success
- Historic benchmarks (5-year survival rates)

### Implementation Timeline

```
Hour 1: Claude Code scaffolds project
Hour 2-3: Implement Tier 1 (viability + procedures)
Hour 4-5: Implement Tier 2 (costs + success model)
Hour 6: Testing + refinement
Hour 7: Demo recording
Hour 8: Submission
```

---

## Final Recommendation

**✅ YES, USER VISION MATCHES & ENHANCES CHALLENGE**

Your vision (success probability + financial feasibility) is:
1. **In scope**: Original says "saber si viable" → you define "viable" more rigorously
2. **Within hackathon rules**: Uses synthetic data (explicitly allowed)
3. **Better for entrepreneurs**: Actually answers "can I afford this?"
4. **Higher scoring**: Exceeds requirements (Criterion A boost)
5. **Doable in 8 hours**: Hybrid approach fits timeline

**Build Option C (Hybrid MVP)**:
- Core: Procedural viability (original challenge)
- Extended: Financial viability (user vision)
- Tier 1-2 gives you 5/5 on all scoring criteria

---

*Analysis: June 6, 2026 — Scope clarification and recommendation*
