# Feature Tasks - Reto 2 Implementation

Breakdown of all features by module with task tracking, dependencies, and MVP priority.

## MVP Scope (8-hour sprint, 3-5 people)

**Priority**: Modules 1 & 2 only (Viability + Roadmap)  
**Reason**: Other modules are scope creep; focus on core deliverable

---

## Module 1: Zone Viability Checker ⭐ CORE MVP

**Purpose**: User inputs business type + location → Get viability assessment

### Task 1.1: Define Business Types & Categories
- [ ] Extract business types from RETYS
- [ ] Create taxonomy (50-100 types)
- [ ] Map to land use codes (SEDUVI)
- **Effort**: 30 min | **Owner**: Data specialist
- **Output**: `data/business-types.json`

### Task 1.2: Create Synthetic Zone Data
- [ ] Design 5-10 test zones (Mexico City locations)
- [ ] Synthetic data: traffic potential, competition count, regulations
- [ ] Make data realistic but plausible (hackathon requirement)
- **Effort**: 45 min | **Owner**: Data specialist
- **Output**: `data/test-zones.json`

### Task 1.3: Build Zone Viability Logic
- [ ] Input validation (business type + location)
- [ ] Land use compatibility check (SEDUVI rules)
- [ ] Competition analysis (DENUE count in zone)
- [ ] Output: Yes/No + 3-5 reasons
- **Effort**: 2 hours | **Owner**: Backend developer
- **Dependencies**: Tasks 1.1, 1.2
- **Output**: `src/modules/viability_checker.py`

### Task 1.4: API Endpoint for Viability Check
- [ ] REST endpoint: `POST /api/viability-check`
- [ ] Input schema: `{business_type, location}`
- [ ] Output schema: `{viable: bool, reasons: [], score: 0-100}`
- **Effort**: 1 hour | **Owner**: Backend developer
- **Dependencies**: Task 1.3
- **Output**: Endpoint fully tested

### Task 1.5: UI for Viability Input/Output
- [ ] Input form: business type dropdown, location search
- [ ] Results display: Viability status + visual indicators + reasons
- [ ] Responsive design (mobile-friendly for demo)
- **Effort**: 1.5 hours | **Owner**: Frontend developer
- **Output**: `/src/ui/viability-panel.tsx` or `.html`

**Module 1 Total Effort**: ~5.5 hours (✓ Achievable in 8-hour sprint)

---

## Module 2: Regulatory Roadmap ⭐ CORE MVP

**Purpose**: User gets step-by-step procedures in correct order based on business type + entity choice

### Task 2.1: Extract & Structure RETYS Procedures
- [ ] Download RETYS procedure catalog
- [ ] Extract for "business registration" + "permits"
- [ ] Structure: procedure_id, name, steps[], docs_required[], timeline
- [ ] Map procedures to business types
- **Effort**: 1.5 hours | **Owner**: Data specialist
- **Output**: `data/procedures.json`

### Task 2.2: Implement Procedure Sequencing Logic
- [ ] Business type → required procedures (array)
- [ ] Entity type (individual vs corporate) → variations
- [ ] Logical order (dependencies honored)
- [ ] Time estimates aggregated
- **Effort**: 1.5 hours | **Owner**: Backend developer
- **Dependencies**: Task 2.1
- **Output**: `src/modules/regulatory_roadmap.py`

### Task 2.3: Build Procedure Detail API
- [ ] Endpoint: `POST /api/regulatory-roadmap`
- [ ] Input: `{business_type, entity_type}`
- [ ] Output: `{procedures: [{name, steps[], docs[], timeline}]}`
- **Effort**: 1 hour | **Owner**: Backend developer
- **Dependencies**: Task 2.2
- **Output**: API fully tested

### Task 2.4: UI for Roadmap Display
- [ ] Timeline visualization (Gantt or sequential steps)
- [ ] Expandable procedure cards
- [ ] Document checklist per procedure
- [ ] Entity type selector (Individual / Corporate)
- **Effort**: 1.5 hours | **Owner**: Frontend developer
- **Output**: `/src/ui/roadmap-panel.tsx` or `.html`

**Module 2 Total Effort**: ~5.5 hours (✓ Achievable in 8-hour sprint)

---

## Module 3: Business Registration Guide 🔲 POST-MVP

**Purpose**: Step-by-step guide for entity constitution

### Task 3.1: Extraction of Registration Requirements
- [ ] Individual entity (Persona Física) requirements
- [ ] Corporate entity (Persona Moral) requirements  
- [ ] Documentation needed per type
- **Effort**: 1 hour | **Owner**: Legal specialist
- **Output**: `data/registration-requirements.json`

### Task 3.2: Registration Flow Implementation
- [ ] Decision tree: which entity type → what steps
- [ ] Document requirements list
- [ ] Timeline for each type
- **Effort**: 1.5 hours | **Owner**: Backend developer
- **Dependencies**: Task 3.1

### Task 3.3: Comparison UI (Individual vs Corporate)
- [ ] Side-by-side comparison table
- [ ] Pros/cons for each type
- [ ] Recommendation logic
- **Effort**: 1 hour | **Owner**: Frontend developer

**Module 3 Total Effort**: ~3.5 hours (⏸ Nice-to-have, skip if time short)

---

## Module 4: Permit & Compliance Tracker 🔲 POST-MVP

**Purpose**: Environmental permits + timeline dependencies

**Effort**: 4 hours (skip for MVP)

### Task 4.1: SIAPEM Integration
- [ ] Environmental impact assessment flow
- [ ] Required for most businesses
- [ ] Timeline integration

### Task 4.2: Permit Dependencies
- [ ] Which permits block others (sequencing)
- [ ] Timeline graphic

---

## Module 5: Competition & Market Context 🔲 POST-MVP

**Purpose**: Local market analysis

**Effort**: 3 hours (skip for MVP)

---

## Cross-Cutting Tasks

### Task C.1: Create `.gitignore`
- [ ] Standard Python ignore (venv, __pycache__, .env)
- [ ] Add node_modules, dist, build
- **Effort**: 15 min
- **Output**: `.gitignore`

### Task C.2: Set Up Demo Data
- [ ] 5-10 test zones with synthetic data
- [ ] 3-4 business types for demo walkthrough
- [ ] Sample output for edge cases
- **Effort**: 1 hour
- **Output**: `/data/demo-*.json`

### Task C.3: Create README.md
- [ ] Problem statement (one sentence)
- [ ] Target user (specific persona)
- [ ] How to run (5-minute setup)
- [ ] Stack used
- [ ] Known limitations
- **Effort**: 45 min
- **Output**: `README.md` (meets hackathon requirement)

### Task C.4: Create SETUP.md
- [ ] Step-by-step environment setup
- [ ] Dependency installation
- [ ] Verified to work in <5 minutes
- **Effort**: 30 min
- **Output**: `SETUP.md`

### Task C.5: Record Demo Video
- [ ] Screen recording (no cuts, continuous)
- [ ] 2-3 minute walkthrough
- [ ] Real product functioning
- **Effort**: 20 min
- **Output**: Video file (.mp4 or Loom link)

---

## Sprint Timeline (8 hours)

```
09:00-09:30  Team formation, reto choice, planning
09:30-11:30  Module 1: Viability Checker (2 hours)
11:30-13:30  Module 2: Regulatory Roadmap (2 hours)
13:30-14:00  Lunch / Break
14:00-15:30  Documentation + API testing (1.5 hours)
15:30-16:00  Demo prep + video recording (0.5 hours)
16:00-17:00  Submission: Form, final polishing (1 hour)
```

---

## Dependency Graph

```
Module 1 Viability:
├── Task 1.1: Business Types ──→ Task 1.3: Logic
├── Task 1.2: Synthetic Data ──→ Task 1.3: Logic
├── Task 1.3: Logic ──→ Task 1.4: API
└── Task 1.4: API ──→ Task 1.5: UI

Module 2 Roadmap:
├── Task 2.1: Extract Procedures ──→ Task 2.2: Logic
├── Task 2.2: Logic ──→ Task 2.3: API
└── Task 2.3: API ──→ Task 2.4: UI

Documentation:
├── Task C.1: .gitignore (independent)
├── Task C.2: Demo Data (after Module 1)
├── Task C.3: README (final, needs Stack info)
├── Task C.4: SETUP (final)
└── Task C.5: Video (last, before 17:00)
```

---

## Definition of Done

Each task is **complete** when:
1. ✓ Code/data created and committed
2. ✓ Tested (manual or automated)
3. ✓ Documented in code
4. ✓ Changelog entry added
5. ✓ Can be reviewed independently

---

*Updated: June 6, 2026 — Ready for team pickup*
