# SEDECO - Reto 2: Viabilidad de Negocios CDMX

## Project Overview

**Event:** Hackathon SecretarIA - June 6, 2026 (8:00-18:00)  
**Organizers:** SEDECO + Saptiva AI  
**Location:** Av. Cuauhtémoc 898, Narvarte Poniente, Benito Juárez, CDMX, Piso 2  
**Focus:** Reto 2 - Business Viability Assessment Tool  
**User Email:** constantlearning.91@gmail.com

---

## Problem Statement

**Double Barrier Problem**  
Entrepreneurs/investors wanting to open a business in Mexico City face:

1. **Viability Uncertainty**: Don't know if their business idea is viable in their chosen location
2. **Procedural Complexity**: Don't know what documents are needed, which government windows to visit, or what order to follow

**Consequences**
- Unnecessary delays
- Unexpected costs
- Business closures
- Legal sanctions

---

## Solution Deliverable

Build a tool that enables entrepreneurs/investors to:

### Core Capabilities
1. **Assess business viability** in a specific zone/location
2. **Understand constitutional/registration process** (individual vs. corporate entity)
3. **View zone metrics**: foot traffic, competition, regulations
4. **Learn required permits and procedures** in correct order
5. **Discover CDMX entrepreneurship programs**
6. **Understand compliance and legal requirements**

---

## Scope Definition

### In Scope ✓
- Business viability assessment (location + business type)
- Regulatory compliance pathway (permits, procedures, sequential order)
- Zone metrics (competition analysis, land use compatibility)
- Business registration process (both entity types)
- Environmental permits (SIAPEM integration)
- Applicable laws and regulations

### Out of Scope ✗
- Territorial/geographic data analysis (Reto 1)
- Economic impact of events (Reto 3)
- Detailed financial modeling or business planning
- Real-time market data beyond local regulations

---

## Core Modules to Build

### Module 1: Zone Viability Checker
- **Input**: Business type + Location/Postal code
- **Output**: Viability assessment (Yes/No + detailed reasons)
- **Data Source**: Land use compatibility (SEDUVI), zoning restrictions, regulations

### Module 2: Regulatory Roadmap
- **Output**: Step-by-step procedure list in correct sequential order
- **Details**: Time estimates per step, required documents, responsible agency
- **Source**: RETYS, Ley de Establecimientos Mercantiles

### Module 3: Business Registration Guide
- **Comparison**: Individual vs. Corporate entity
- **Process**: Step-by-step constitution procedures
- **Requirements**: Required documentation by entity type

### Module 4: Permit & Compliance Tracker
- **Environmental Permits**: SIAPEM workflow
- **Commercial Permits**: RETYS procedures
- **Dependencies**: Timeline and sequential requirements

### Module 5: Competition & Market Context
- **Data**: Similar businesses in zone (DENUE data)
- **Zone Characteristics**: Foot traffic potential, regulation intensity
- **Market Analysis**: Local business ecosystem

---

## Data Sources & APIs

### Primary Sources

#### 1. RETYS (Registro de Trámites y Servicios)
- **URL**: https://www.registrodetramitesyservicios.cdmx.gob.mx/
- **Search**: https://www.cdmx.gob.mx/public/resultadoBuscador.xhtml
- **Purpose**: Complete procedure catalog with steps, documents, timelines
- **Status**: Production data, always current

#### 2. SIAPEM (Environmental Permits)
- **URL**: https://siapem.cdmx.gob.mx/
- **Guide**: https://docs.google.com/document/d/1v1AHsCjUrBnBAWEWFPwTzEHrGAGLgjAJ/edit?usp=drive_link
- **Purpose**: Environmental impact assessment and permits
- **Relevance**: Required for most commercial establishments

#### 3. SEDUVI (Land Use Zoning)
- **URL**: http://ciudadmx.cdmx.gob.mx:8080/seduvi/
- **Purpose**: Verify land use compatibility for business type
- **Critical Note**: Server intermittent, download during setup phase

#### 4. Land Use Certificate (Certificado de Uso de Suelo)
- **URL**: https://www.cdmx.gob.mx/public/InformacionTramite.xhtml?idTramite=806
- **Purpose**: Official certificate required in registration process
- **Process**: Part of regulatory roadmap

#### 5. Legal Framework

**Ley de Establecimientos Mercantiles (Commercial Establishments Law)**
- **URL**: https://prontuario.cdmx.gob.mx/pdf/Ley%20Establecimientos%20Mercantiles%2024122025.pdf
- **Content**: Rules for commercial activities, entity types, requirements
- **Critical**: Source of procedural truth (don't invent logic)

**Reglamento (Regulation)**
- **URL**: https://prontuario.cdmx.gob.mx/pdf/e69b_REGLAMENTO%20DE%20LA%20LEY%20DE%20ESTABLECIMIENTOS%20MERCANTILES%20PARA%20LA%20CIUDAD%20DE%20M%C3%89XICO25092024.pdf
- **Content**: Implementation details, specific requirements, sanctions

**NotebookLM Reference**
- **URL**: https://notebooklm.google.com/notebook/83b692ed-ac65-46c7-972c-4b785cc5149d
- **Purpose**: Structured Q&A reference for law details

#### 6. DENUE (Commercial Establishments Database)
- **URL**: https://www.inegi.org.mx/servicios/api_denue.html
- **Purpose**: Competitor/market analysis in zone
- **Data**: Business type distribution, density, categories

---

## Data Approach & Strategy

### Synthetic Data Requirement
- **Law & Procedures**: MUST use actual RETYS and legal framework (NOT invented)
- **Market Data**: Use plausible synthetic data (5-20 realistic examples)
- **Demo Validity**: 100% acceptable to use synthetic market data
- **Critical Rule**: Procedure logic must match legal reality

### Pre-Download Strategy (Token & Network Savings)
⚠️ **Important**: Download heavy data sources before event start to avoid network saturation

1. **Download immediately**:
   - Ley de Establecimientos Mercantiles (PDF)
   - Reglamento (PDF)
   - RETYS procedure catalog (export from web interface)
   - DENUE sample data (CSV from INEGI)

2. **Cache locations**: Store in `.claude/context/legal/` and `.claude/context/data/`

3. **Network-sensitive**: SEDUVI land use server often overloaded

---

## Evaluation Criteria

### Disqualifiers (Binary - Must Pass)
❌ Auto-fail if:
- Repository is not public OR last commit after 17:00
- Submission form not sent between 16:00-17:00
- Repository contains no real code (README-only)

### Gate 1: Functional Test (Binary - Must Pass)
Single question: **Does the video show end-to-end product functioning on a real use case, without manual intervention?**
- ✓ Pass → enters ranking
- ✗ Fail → disqualified regardless of quality

### Gate 2: Scoring (3 Criteria, Equal Weight, 1-5 Scale Each)

#### Criterion A: Quality & Solution Fit
| Score | Standard |
|-------|----------|
| **1** | Output incoherent, flow doesn't solve problem |
| **3** | Solves halfway, user would hesitate |
| **5** | User would use without help, clean flow |

#### Criterion B: Technical Execution
| Score | Standard |
|-------|----------|
| **1** | Messy code, useless README, AI decorative |
| **3** | Reasonable structure, README adequate, AI generic |
| **5** | Clean code, complete README, AI well-chosen |

#### Criterion C: SEDECO Operational Fit
| Score | Standard |
|-------|----------|
| **1** | Invents legal/procedure logic incorrectly |
| **3** | Partially fits, SEDECO could fix with adjustments |
| **5** | Matches CDMX operations, adoptable as-is |

**Scoring Tiebreaker**: Criterion C (Encaje) weight increases

---

## Deliverables Checklist

### 1. Public GitHub Repository
**Structure Required**:
```
repo/
├── README.md              # Problem, user, how-to-run, stack, limitations
├── SETUP.md              # Proven 5-minute setup instructions
├── src/                  # Complete source code
├── data/                 # Demo data used
├── .github/workflows/    # CI/CD (optional but recommended)
└── docs/                 # Architecture, module docs
```

**README Order** (Non-negotiable):
1. Problem statement (one sentence)
2. Target user (specific persona, not "citizens")
3. How to run (clone + run in 5 min)
4. Stack used
5. Known limitations

### 2. Demo Video
**Format**: Single continuous screen recording, no cuts/edits, max 3 minutes

**Structure**:
- 0:00-0:20: Problem + target user
- 0:20-2:20: Live product demo (end-to-end)
- 2:20-3:00: What built, gaps, learnings

**Tools**: Loom or native screen recorder

**Critical Rules**:
- ❌ NO edited video (disqualifies)
- ❌ NO "imagine X works" statements
- ❌ NO slides/wireframes
- ✓ Show actual functioning product

### 3. Submission Form
**Open**: 16:00  
**Closes**: 17:00 (auto-close, no exceptions)

**Fields**:
- Team name + members
- Reto chosen
- GitHub repo link (must be public)
- Video link
- Live product link (if applicable)

---

## Tech Stack

### Recommended (Based on Hackathon Guidance)

**NVIDIA Stack Option** (CheatSheet provided):
- **Model Inference**: Nemotron (llama-3.2-nemoretriever, llama-3.1-nemoguard)
- **RAG**: NeMo Retriever + Blueprint over Ley + RETYS
- **OCR**: nemotron-ocr-v1 + nemotron-page-elements-v3
- **Validation**: cuSpatial for land use compatibility
- **API**: https://integrate.api.nvidia.com/v1 (OpenAI-compatible)

**Agnostic Approach** ✓
- NVIDIA, Saptiva AI, Anthropic, OpenAI, or combinations
- **Stack is not weighted in scoring** — use what solves best
- Bring API keys for your chosen stack on event day

**Requirements**:
- API keys pre-configured
- Screen recording tool ready (Loom or native)
- GitHub account ready
- Dev environment tested locally

---

## Hackathon Rules

### What's Allowed ✓
- Any stack/AI tools combination
- Starting with public open-source code (cited in README)
- External libraries, APIs, SaaS
- Mentors available for help
- Reto change before 17:00

### What's Forbidden ✗
- Working on project before June 6
- Teams >5 people
- Repository modifications after 17:00
- Submitting slides/wireframes as deliverable
- Edited/cut video instead of continuous recording

### Timeline (June 6, 2026)
| Time | Event |
|------|-------|
| 08:00-08:30 | Arrival, coffee, registration |
| 08:30-09:00 | Intro, team formation, reto selection |
| 09:00-17:00 | Build (8 hours) |
| 16:00 | Submission form opens |
| 17:00 | **FREEZE** — Code in main, video sent, form submitted |
| 17:00-17:45 | Judges review videos + AI reports |
| 17:45-18:00 | Awards + closing |

**Hard Rules**: 17:00 is absolute deadline. No exceptions, no reopening.

---

## Team Composition

**Requirements**:
- Minimum 3 people
- Maximum 5 people
- Recommended mix: 2 technical + 1 product/design + 1 domain expert

**Solo/Pair**:
- Matched with others in first 30 minutes

---

## Panel of Judges

- **Manola Zabalza Aldama** — SEDECO Secretary
- **Angel Cisneros** — Saptiva AI Founder/CEO
- **Pablo Pruneda Gross** — UNAM (Law & AI Research)
- **Ricardo Lira de la Vega** — Anthropic Ambassador
- **Carlos Daniel Reyes Morales** — CIDE (Academic)
- **Miguel González Mendoza** — Tecnológico de Monterrey
- **Andrés Molano** — IBERO (Additional judge)

---

## Success Criteria Summary

### MVP Minimum
A tool that demonstrates:
1. ✓ Accepts business type + location
2. ✓ Returns viability assessment with reasons
3. ✓ Shows required procedures in order
4. ✓ Lists required documents
5. ✓ Runs end-to-end in <10 seconds

### Quality Bar (Score 5/5)
1. User can operate without help
2. Logic matches CDMX legal reality
3. Clean, well-documented code
4. Sensible AI usage (not decorative)
5. Could be adopted by SEDECO with minimal changes

---

## Known Challenges & Mitigation

| Challenge | Impact | Mitigation |
|-----------|--------|-----------|
| SEDUVI server intermittent | Land use lookup fails | Download polygon data beforehand |
| RETYS data dispersed | Procedure gathering slow | Extract + cache procedures day-of |
| Legal complexity | Procedure logic hard | Use law PDFs, don't invent logic |
| 8-hour constraint | Scope creep risk | Focus on 1-2 modules, not all 5 |
| Network saturation | API/download delays | Pre-download all large files |

---

## File Organization Strategy

### .claude/ Folder Structure

```
.claude/
├── context/
│   ├── legal/              # Law PDFs, RETYS exports
│   ├── data/               # Synthetic data samples
│   ├── references/         # API docs, NotebookLM links
│   └── hackathon/          # Brief, scoring, rules
├── agents/                 # Agent definitions (prompt templates)
├── instructions/           # System instructions per module
├── tasks/                  # Feature tasks, sprints
├── tools/                  # Tool definitions (API wrappers)
├── workflows/              # Workflow orchestration (multi-step processes)
└── changelog.md            # All changes, atomic commits
```

---

## Next Steps

1. **Before Event**:
   - [ ] Download legal PDFs to `.claude/context/legal/`
   - [ ] Export RETYS procedures to `.claude/context/data/`
   - [ ] Create synthetic market data samples
   - [ ] Test API keys for chosen stack
   - [ ] Prepare screen recording tool
   - [ ] Set up GitHub repo structure

2. **Day Of (09:00 start)**:
   - [ ] Form team (3-5 people)
   - [ ] Choose Reto 2
   - [ ] Define MVP scope (modules 1-2 core)
   - [ ] Set up git workflow (atomic commits)
   - [ ] Divide work: legal/data, UI/logic, demo

3. **Before 17:00**:
   - [ ] Code in main branch
   - [ ] Record demo video
   - [ ] Submit form (16:00-17:00 window)
   - [ ] Push final commit before 17:00

---

## Scoring Tiebreaker

If two teams score equally:
1. Higher score on Criterion C (Encaje/Fit) wins
2. If still tied, SEDECO Secretary decides

---

*Last Updated: June 6, 2026 — Ready for hackathon* 🚀
