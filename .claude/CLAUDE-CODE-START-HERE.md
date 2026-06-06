# Claude Code Start Here - Quick Build Guide

**Status**: ✅ All pre-processing complete. Ready to build backend.

---

## What's Ready for You

### Data (100% Embedded - No PDFs to Load)
```
.claude/data/
├── business-types.json (1.8 KB) → 9 SCIAN business types
├── zones.json (8.6 KB) → 16 CDMX boroughs + metrics
├── procedures.json (5.8 KB) → 10 RETYS procedures from Ley
├── costs.json (3.0 KB) → Cost models by type
├── crime-index.json (2.7 KB) → Crime/security by zone
├── viability-model.json (2.4 KB) → 6-factor algorithm
├── query-index.json (1.4 KB) → Fast lookups
├── regulatory-costs.json (811 B) → Official costs from Ley
├── cenproin-training-context.json (1.3 KB) → Training modules
└── README.md (3.4 KB) → Data guide
```
**Total**: 52 KB, all JSON, zero syntax errors ✅

### Specifications Ready
```
.claude/agents/
├── viability-assessment-agent.md → Main scoring logic
├── cost-estimator-agent.md → Cost calculations
└── procedure-guide-agent.md → Procedure sequencing

.claude/instructions/
├── module-1-viability.md → UI/UX specs (form + dashboard)
└── module-2-roadmap.md → Procedure display logic

.claude/tools/
└── data-loaders.md → 6 Python functions ready to implement

.claude/workflows/
└── viability-check-workflow.md → 13-step process (85ms total)
```

---

## 4-Step Build Plan (Remaining Tasks)

### Step 1: Task #11 - FastAPI Backend (2-3 hours)
**Goal**: Create 4 REST endpoints with embedded data

**Implementation**:
```python
# .claude/tools/data-loaders.md → Use these functions
from .data_loaders import (
    load_business_types,
    load_zones,
    load_procedures,
    load_costs,
    load_crime_index,
    load_viability_model,
    startup_cache
)

# FastAPI routes to create:
POST /api/viability-check
  Input: { business_type, location, budget, space_sqm, entity_type }
  Output: { viability_score, factors, costs, risks, recommendation }

GET /api/cost-estimate/{scian}/{zone}/{sqm}
  Output: { monthly, annual, first_year, break_even }

GET /api/procedures/{business_type}
  Output: { procedures[], timeline[], costs[] }

GET /api/zone/{zone_code}
  Output: { population, traffic, rental, crime, business_density }
```

**Performance Target**: <100ms per request, sub-1ms lookups

---

### Step 2: Task #12 - Viability Scoring (30 mins - 1 hour)
**Goal**: Implement 6-factor algorithm

**From viability-model.json**:
```json
{
  "weights": {
    "budget": 0.15,
    "competition": 0.20,
    "location": 0.20,
    "security": 0.15,
    "growth": 0.15,
    "legal": 0.15
  },
  "interpretation": {
    "80-100": "Highly Viable",
    "65-79": "Viable",
    "50-64": "Marginal",
    "<50": "Not Recommended"
  }
}
```

**Calculate**:
1. Budget factor = (user_budget / estimated_costs) * 100
2. Competition factor = (available_market / competitors) * 100
3. Location factor = (foot_traffic * zone_compatibility) * 100
4. Security factor = (100 - crime_index) * 100
5. Growth factor = (expansion_rate * population_growth) * 100
6. Legal factor = (procedures_complexity_inverse) * 100

**Weighted Score** = Σ(factor × weight)

---

### Step 3: Task #13 - React/HTML Frontend (2-3 hours)
**Goal**: Build input form + output dashboard

**Frontend Structure**:
```
src/
├── App.jsx (main component)
├── components/
│   ├── ViabilityForm.jsx (input form)
│   ├── ViabilityDashboard.jsx (output results)
│   └── ProcedureTimeline.jsx (procedure timeline)
├── api/
│   └── client.js (FastAPI calls)
└── styles/
    └── main.css (responsive design)
```

**Form Inputs**:
- Dropdown: Business Type (SCIAN lookup)
- Dropdown: Zone (16 CDMX boroughs)
- Input: Budget (MXN)
- Input: Space Size (sqm)

**Dashboard Outputs**:
- Large viability score card (0-100)
- 6-factor breakdown (bar chart)
- Cost summary (monthly, annual, break-even)
- Risk assessment (top 3 risks)
- Procedures timeline (step-by-step list)
- Recommendation text

---

### Step 4: Task #14-17 - Polish & Demo (2 hours)
**Goal**: Styling, test, record 3-min video, submit

**Polish Checklist**:
- [ ] Responsive design (mobile + desktop)
- [ ] Error handling (invalid inputs, data missing)
- [ ] Loading states (API calls)
- [ ] Accessibility (colors, fonts, buttons)

**Demo Script** (3 minutes max):
1. 0:00-0:20 → Problem + user intro
2. 0:20-2:20 → Live demo (end-to-end functionality)
3. 2:20-3:00 → What built, gaps, learnings

**Critical**: No cuts, no "imagine" statements, real product only

---

## Files You Have

### Context Files
- CLAUDE.md → Full hackathon requirements + evaluation criteria
- data-extraction-plan.md → What was extracted from PDFs
- PRE-PROCESSING-SUMMARY.md → Pre-processing checklist (all done)
- changelog.md → Complete commit log
- feature-tasks.md → Original task breakdown

### Configuration
- settings.local.json → Permissions (no prompts, allow any commit/execution)
- .gitignore → Standard Python/Node excludes

### Legal References
- .claude/legal/ley-establecimientos-summary.md → Extracted law
- .claude/legal/retys-procedures-summary.md → Procedure guide

---

## Performance Targets

| Metric | Target | Status |
|--------|--------|--------|
| Startup cache load | <100ms | Ready (all data indexed) |
| Single lookup | <1ms | Ready (JSON flat structure) |
| Full viability check | <100ms | Ready (6 lightweight calculations) |
| Frontend render | <500ms | TBD (React optimization) |

---

## Legal Compliance Notes

✅ All procedures extracted from actual Ley de Establecimientos (NOT invented)
✅ All costs validated against regulatory documents
✅ All requirements match CDMX official regulations
✅ No fabricated legal logic

---

## Quick Commands

```bash
# Load all data at startup
python
from .data_loaders import startup_cache
startup_cache()

# Example: Get zones
zones = load_zones()
print(zones["16"])  # Cuauhtémoc

# Example: Get procedures for business type
procs = load_procedures()
print(procs["722110"])  # Restaurante procedures
```

---

## Success = 

- ✅ Input form works (dropdown/inputs valid)
- ✅ API calls complete in <100ms
- ✅ Dashboard displays 6 factors + recommendation
- ✅ Procedures timeline shows correct order
- ✅ 3-min demo shows end-to-end flow
- ✅ Code pushed before 17:00
- ✅ Form submitted 16:00-17:00 window

---

**Timeline**: ~7 hours remaining (freeze at 17:00)  
**Data Ready**: YES ✅  
**Specifications Ready**: YES ✅  
**Legal Compliance**: YES ✅  

**Start with FastAPI backend. Go.** 🚀

---

## Language Requirement

**🇲🇽 UI MUST BE 100% SPANISH**

All visible text to users must be in Spanish:
- Form labels
- Button text
- Metrics/results display
- Error messages
- Claude API responses

**Internal code** (comments, variable names) can be English.

This is already configured in the provided app.py code. Ensure NO English text appears in the UI.

