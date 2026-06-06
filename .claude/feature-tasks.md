# Feature Tasks & Sprint Breakdown

**Status**: Phase 1 Complete ✅, Phase 2 In Progress 🔄

---

## Phase 1: Pre-Processing (✅ COMPLETED)

All tasks completed successfully on June 6, 2026 (20:05).

### Tasks 1-7: Data Foundation
- [x] Task 1: Create SCIAN taxonomy (business-types.json)
- [x] Task 2: Create CDMX zones database (zones.json)
- [x] Task 3: Create procedures database (procedures.json)
- [x] Task 4: Create cost models (costs.json)
- [x] Task 5: Create crime index (crime-index.json)
- [x] Task 6: Create viability model (viability-model.json)
- [x] Task 7: Extract critical PDFs (Ley, Reglamento, Cenproin)

### Tasks 8-10: Integration Prep
- [x] Task 8: Create query index (query-index.json)
- [x] Task 9: Verify data consistency (10 files, 52 KB, 0 errors)
- [x] Task 10: Prepare Claude Code handoff (3 agents + 2 modules)

**Phase 1 Output**: 10 data files (52 KB) + complete context documentation

---

## Phase 2: Backend Development (🔄 IN PROGRESS)

Estimated: 2.5-3.5 hours remaining

### Task #11: FastAPI Backend with 4 Endpoints (🔄 IN PROGRESS)

**Status**: 🔄 In Progress  
**Estimated Duration**: 2-3 hours  
**Effort**: HIGH  

**Requirements**:
- [ ] Create Python FastAPI application
- [ ] Load all 10 data files at startup (startup_cache)
- [ ] Implement 4 REST endpoints
- [ ] Add request/response validation (Pydantic models)
- [ ] Return structured JSON responses
- [ ] Handle errors gracefully

**Endpoint 1: POST /api/viability-check**
```
Input:
{
  "business_type": "722110",  # SCIAN code
  "location": "Cuauhtémoc",   # Zone name
  "budget": 500000,            # MXN
  "space_sqm": 100,           # Square meters
  "entity_type": "Persona Física"
}

Output:
{
  "viability_score": 78,
  "interpretation": "Viable",
  "factors": {
    "budget": 75,
    "competition": 80,
    "location": 85,
    "security": 70,
    "growth": 75,
    "legal": 80
  },
  "costs": {
    "monthly": 15000,
    "annual": 180000,
    "first_year": 250000,
    "break_even_months": 18
  },
  "risks": ["High competition", "Location costs", "Permit delays"],
  "recommendation": "Suitable for experienced restaurateur"
}
```

**Endpoint 2: GET /api/cost-estimate/{scian}/{zone}/{sqm}**
```
Example: /api/cost-estimate/722110/Cuauhtémoc/100

Output:
{
  "monthly_costs": 15000,
  "annual_costs": 180000,
  "first_year_total": 250000,
  "break_even_months": 18,
  "cost_breakdown": {
    "rent": 5000,
    "utilities": 2000,
    "permits": 1000,
    "insurance": 500,
    "labor": 5000,
    "supplies": 1500
  }
}
```

**Endpoint 3: GET /api/procedures/{business_type}**
```
Example: /api/procedures/722110

Output:
{
  "procedures": [
    {
      "order": 1,
      "code": "TRM001",
      "name": "RFC (Registro Federal de Contribuyentes)",
      "timeline_days": 5,
      "cost_mxn": 0,
      "blocking": [],
      "documents": ["Identificación", "Comprobante domicilio"]
    },
    ... (10 procedures total)
  ],
  "total_days": 45,
  "total_cost": 8500
}
```

**Endpoint 4: GET /api/zone/{zone_code}**
```
Example: /api/zone/Cuauhtémoc

Output:
{
  "name": "Cuauhtémoc",
  "population": 520000,
  "foot_traffic_daily": 150000,
  "vehicular_traffic_daily": 200000,
  "rental_cost_sqm_annual": 1200,
  "crime_index": 65,
  "business_density_per_10k": 450,
  "parking_requirement": 1,
  "expansion_rate": 2.5
}
```

**Implementation Steps**:
1. Set up FastAPI project structure
2. Implement data loading functions from data-loaders.md
3. Create Pydantic models for request/response validation
4. Implement each endpoint with data lookups
5. Add error handling and validation
6. Test with sample requests
7. Optimize for performance (<100ms response)

---

### Task #12: Viability Scoring Algorithm (⏳ PENDING)

**Status**: ⏳ Pending  
**Estimated Duration**: 30 mins - 1 hour  
**Effort**: MEDIUM  
**Dependencies**: Task #11 (needs endpoint structure)

**Requirements**:
- [ ] Implement 6-factor scoring function
- [ ] Load viability-model.json weights
- [ ] Calculate each factor (Budget, Competition, Location, Security, Growth, Legal)
- [ ] Apply weights and normalize to 0-100 scale
- [ ] Generate interpretation text based on score
- [ ] Add risk assessment logic

**Scoring Algorithm**:
```python
def calculate_viability_score(factors_dict):
    weights = load_viability_model()["weights"]
    
    # Normalize each factor to 0-100
    score = sum(
        factors_dict[factor] * weights[factor]
        for factor in weights.keys()
    )
    
    # Interpret result
    if score >= 80:
        interpretation = "Highly Viable"
    elif score >= 65:
        interpretation = "Viable"
    elif score >= 50:
        interpretation = "Marginal"
    else:
        interpretation = "Not Recommended"
    
    return {"score": score, "interpretation": interpretation}
```

**Factor Calculation Logic**:
1. **Budget Factor** = (user_budget / estimated_annual_costs) * 100
2. **Competition Factor** = (available_market_size / current_competitors) * 100
3. **Location Factor** = (foot_traffic * zone_compatibility) / 100
4. **Security Factor** = (100 - crime_index_for_zone)
5. **Growth Factor** = (population_growth_rate * expansion_rate) * 100
6. **Legal Factor** = (100 - procedure_complexity_score)

---

### Task #13: React/HTML Frontend (⏳ PENDING)

**Status**: ⏳ Pending  
**Estimated Duration**: 2-3 hours  
**Effort**: HIGH  
**Dependencies**: Task #11 (API must be ready)

**Requirements**:
- [ ] Create React application (or HTML + vanilla JS)
- [ ] Build input form component (business type, location, budget, space)
- [ ] Build output dashboard component
- [ ] Implement API client for FastAPI calls
- [ ] Add error handling and loading states
- [ ] Responsive design (mobile + desktop)

**UI Components**:

**Component 1: Input Form**
- Dropdown: Business Type (lookup from business-types.json)
- Dropdown: Zone (16 CDMX boroughs)
- Input: Budget (MXN, numeric)
- Input: Space Size (sqm, numeric)
- Radio: Entity Type (Persona Física vs Moral)
- Button: "Assess Viability"

**Component 2: Viability Dashboard**
- Large score card (0-100, color-coded)
- 6-factor breakdown (bar chart or table)
- Cost summary (monthly, annual, break-even)
- Risk assessment (top 3 risks as cards)
- Recommendation text (large, prominent)

**Component 3: Procedure Timeline**
- Ordered list of procedures
- Timeline visualization (days per procedure)
- Cumulative cost tracker
- Expandable procedure details (documents, agency, blocking info)

**Component 4: Zone Information**
- Zone metrics (population, traffic, crime, rental cost)
- Business density visualization
- Market context

**Implementation**:
```
src/
├── App.jsx or index.html
├── components/
│   ├── ViabilityForm.jsx
│   ├── ViabilityDashboard.jsx
│   ├── ProcedureTimeline.jsx
│   └── ZoneInfo.jsx
├── api/
│   └── client.js (fetch wrapper for /api/*)
├── styles/
│   └── main.css (TailwindCSS or vanilla CSS)
└── data/
    └── (symlink to ../../.claude/data/)
```

---

## Phase 3: Polish & Launch (⏳ PENDING)

Estimated: 1.5-2.5 hours remaining

### Task #14: Styling, Testing & Polish (⏳ PENDING)

**Status**: ⏳ Pending  
**Estimated Duration**: 1-1.5 hours  
**Effort**: MEDIUM  

**Requirements**:
- [ ] Add responsive CSS (mobile-first design)
- [ ] Implement loading states (spinners during API calls)
- [ ] Add error handling (invalid inputs, API failures)
- [ ] Test all 4 endpoints with sample data
- [ ] Verify mobile responsiveness
- [ ] Add accessibility features (ARIA labels, color contrast)
- [ ] Optimize performance (CSS/JS minification)

**Testing Checklist**:
- [ ] Form validation (empty fields, invalid budgets)
- [ ] API error handling (missing data, timeouts)
- [ ] Dashboard rendering (all 6 factors visible)
- [ ] Procedure timeline (correct order, accurate costs)
- [ ] Mobile layout (buttons clickable, text readable)
- [ ] Loading states (spinner shows during request)
- [ ] Response time (<100ms per request)

---

### Task #15: Deploy to GitHub (⏳ PENDING)

**Status**: ⏳ Pending  
**Estimated Duration**: 30 mins  
**Effort**: LOW  

**Requirements**:
- [ ] Initialize GitHub repository (public)
- [ ] Create proper folder structure
- [ ] Write comprehensive README.md
- [ ] Write SETUP.md (5-min setup instructions)
- [ ] Commit all code with atomic messages
- [ ] Push to main branch before 17:00

**GitHub Structure**:
```
repo/
├── README.md (Problem, user, how-to-run, stack, limitations)
├── SETUP.md (5-min quick start)
├── src/ (FastAPI + React code)
├── .claude/ (All data files + context)
├── data/ (Sample data, if applicable)
├── .github/workflows/ (CI/CD, optional)
├── docs/ (Architecture, API docs)
└── .gitignore (Python/Node standards)
```

---

### Task #16: Record Demo Video (⏳ PENDING)

**Status**: ⏳ Pending  
**Estimated Duration**: 20-30 mins  
**Effort**: LOW  
**Critical**: Must be single continuous recording, no cuts

**Video Structure** (3 minutes max):
- **0:00-0:20**: Problem statement + target user
  - "SMEs/entrepreneurs in CDMX need to assess business viability before opening"
  - "This tool provides instant assessment + regulatory roadmap"

- **0:20-2:20**: Live product demo (functional walkthrough)
  - Fill form: Restaurant, Cuauhtémoc, 500k budget, 100 sqm
  - Click "Assess Viability"
  - Show viability score + 6 factors
  - Show cost breakdown
  - Show procedure timeline
  - Show recommendation text

- **2:20-3:00**: What was built + gaps + learnings
  - "Built viability assessment + cost estimator + procedure guide"
  - "Key achievement: 100% legal-compliant data from Ley de Establecimientos"
  - "Future: Add SEDUVI land use verification, DENUE competitor analysis"

**Critical Rules**:
- ❌ NO CUTS OR EDITS
- ❌ NO "IMAGINE X WORKS" STATEMENTS
- ❌ NO SLIDES OR WIREFRAMES
- ✓ REAL PRODUCT, REAL DATA, REAL RESPONSE TIME

---

### Task #17: Submit to Hackathon (⏳ PENDING)

**Status**: ⏳ Pending  
**Window**: 16:00-17:00 (absolute deadline)  
**Effort**: 5 mins  

**Submission Form Fields**:
- Team name + members
- Reto chosen: "Reto 2 - Viabilidad de Negocios CDMX"
- GitHub repo link (must be public)
- Demo video link (Loom or uploaded)
- Live product link (GitHub Pages, Vercel, or Railway)

**Critical**: Form closes at 17:00, auto-closed, no exceptions

---

## Timeline Summary

| Phase | Tasks | Status | Time |
|-------|-------|--------|------|
| Pre-Processing | 1-10 | ✅ Complete | 0h (done) |
| Backend | 11-12 | 🔄 In Progress | 2.5-3.5h remaining |
| Frontend | 13 | ⏳ Pending | 2-3h |
| Polish/Launch | 14-17 | ⏳ Pending | 1.5-2.5h |
| **TOTAL** | **1-17** | **🔄 60%** | **~7h remaining** |

**Freeze Time**: 17:00 (absolute)  
**Current Time**: 20:05 (June 6, 2026)  

---

## Success Criteria

**Minimum (MVP)**:
- ✓ Input form works
- ✓ Viability score calculated
- ✓ 6 factors displayed
- ✓ Procedures listed in order
- ✓ <100ms response time

**Target (Score 5/5)**:
- ✓ User can operate without help
- ✓ Logic matches CDMX legal reality
- ✓ Clean, well-documented code
- ✓ AI used appropriately (not decorative)
- ✓ SEDECO could adopt as-is

---

*Last Updated: June 6, 2026 20:05 — Phase 1 Complete, Phase 2 In Progress* 🚀

---

## Language Specification

**UI Language**: 🇲🇽 SPANISH ONLY (Visually)

**Requirement**: 
- All user-facing text in Spanish
- All visible output in Spanish
- Claude API prompts in Spanish
- Claude API responses in Spanish (already configured)

**What this means**:
✅ Form labels in Spanish
✅ Button text in Spanish
✅ Error messages in Spanish
✅ Metrics/numbers with Spanish labels
✅ Procedure names in Spanish (from data)
✅ Recommendation text in Spanish (from Claude)

✅ Internal code comments can be English
✅ Variable names can be English
✅ Logic code can be English

**Verification**: 
- Run app and look at UI
- No English text should be visible except in browser chrome
- All form fields, buttons, results in Spanish

