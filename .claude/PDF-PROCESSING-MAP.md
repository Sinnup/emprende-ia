# PDF Information Processing Flow

## 📁 Stage 1: Raw PDFs (Source)
**Location**: `context/SecretarIA/` and `context/Listado de Mercados Públicos/`

### Hackathon PDFs (Used for context)
```
context/SecretarIA/
├── Brief_Hackathon_SEDECO.pdf           (240 KB) - Challenge briefs, rules, timeline
├── CheatSheet_NVIDIA_Hackathon.pdf      (1.6 MB) - Tech stack recommendations
├── Hackathon_SEDECO_Como_se_califica.pdf (66 KB) - Scoring criteria
└── Presentacion.pdf                     (11 MB) - Event presentation
```

### Problem Description
```
context/
└── Problemas H.pdf                      - All 3 Reto descriptions
```

### Market Data (Not used for MVP)
```
context/Listado de Mercados Públicos/
├── 160415 Listado de Mercados Públicos.pdf
├── 190421 - Primer Aviso...pdf
├── 220222 - Segundo Aviso...pdf
├── 240323 - Tercer Aviso...pdf
└── 03092024 - QUINTO AVISO...pdf
```

---

## 📋 Stage 2: Extracted & Structured Summaries
**Location**: `.claude/legal/`

### Legal Framework Extracted
```
.claude/legal/
├── ley-establecimientos-summary.md     (5.1 KB)
│   └── Extracted from: Ley de Establecimientos Mercantiles
│       Content:
│       - Definiciones clave
│       - Requisitos de funcionamiento
│       - Procedimientos prohibidos/restringidos
│       - Sanciones por incumplimiento
│
└── retys-procedures-summary.md         (3.8 KB)
    └── Extracted from: RETYS (Registro de Trámites y Servicios)
        Content:
        - 6 core procedures (RFC, Registro Mercantil, etc.)
        - Timeline per procedure (1-20 days)
        - Required documents per step
        - Chronogram for different business types
```

**How Extracted**: Manual extraction from PDF briefs + CDMX official sources
- Parsed regulatory text
- Summarized key points
- Structured as markdown for easy reference

---

## 🔄 Stage 3: Data Transformation
**Location**: `.claude/data/`

### Procedures → JSON
```
procedures.json ← RETYS procedures summary
├── 8 core procedures extracted
├── Timeline estimates (days)
├── Cost data (MXN)
├── Required documents
├── Agency responsible
└── Blocking dependencies
```

### Legal Info → Cost Models
```
costs.json ← Legal framework summaries
├── Procedure costs extracted from RETYS
├── Monthly cost templates (from industry data)
├── First-year projections
└── Break-even calculations
```

### Business Types → Taxonomy
```
business-types.json ← Hackathon brief + INEGI SCIAN codes
├── 9 SCIAN codes
├── Startup capital per type
├── Monthly costs per type
├── Success rates (synthetic)
└── Procedure timeline per type
```

### Zone Data → Characteristics
```
zones.json ← INEGI Census + CDMX statistics
├── 16 CDMX boroughs
├── Population and growth
├── Foot traffic estimates
├── Crime indices
└── Rental cost estimates
```

---

## 💾 Stage 4: Embedded Data Files (Used by Claude Code)
**Location**: `.claude/data/` (7 files, 64 KB total)

```
.claude/data/
├── business-types.json        ← Business profiles
├── zones.json                 ← Zone characteristics
├── procedures.json            ← RETYS procedures
├── costs.json                 ← Cost breakdowns
├── crime-index.json           ← Security risk data
├── viability-model.json       ← 6-factor scoring algorithm
└── query-index.json           ← Fast lookup indices
```

**How Used by Claude Code**:
- Loaded at startup (Python script in `.claude/tools/data-loaders.md`)
- All data in memory (sub-millisecond access)
- No runtime PDF parsing needed
- Zero network dependencies

---

## 📖 Stage 5: Context & Reference Documents
**Location**: `.claude/`

### Agent Definitions
```
.claude/agents/
├── viability-assessment-agent.md      ← Uses procedures.json, zones.json, costs.json
├── cost-estimator-agent.md            ← Uses costs.json, zones.json
└── procedure-guide-agent.md           ← Uses procedures.json
```

### Module Instructions
```
.claude/instructions/
├── module-1-viability.md              ← Combines all 7 JSON files
└── module-2-roadmap.md                ← Uses procedures.json
```

### Workflows
```
.claude/workflows/
└── viability-check-workflow.md        ← 13-step process using all data
```

### Tools
```
.claude/tools/
└── data-loaders.md                    ← How to load all 7 JSON files
```

---

## 🔗 Information Flow Summary

```
Raw PDFs (context/)
    ↓
Manual Extraction & Summarization
    ↓
Markdown Summaries (.claude/legal/)
    ↓
Data Transformation & Structuring
    ↓
JSON Data Files (.claude/data/) ← PRODUCTION DATA
    ↓
Claude Code at Runtime
    ├→ Load all 7 JSON files
    ├→ Index in memory
    └→ Query for < 1ms response
```

---

## 🎯 What Claude Code Never Does

❌ Parse PDFs at runtime  
❌ Make network calls to download data  
❌ Extract text dynamically  
❌ Load raw PDF files  

✅ Load pre-processed JSON  
✅ Query in-memory indices  
✅ Return results in <100ms  

---

## 📊 Data Quality Assurance

### Validation Done
- ✅ All 7 JSON files valid (0 syntax errors)
- ✅ 16 zones with complete metrics
- ✅ 8 procedures with full timelines
- ✅ 9 business types with costs
- ✅ Cross-reference consistency checks
- ✅ Performance testing (<1ms queries)

### No Runtime Processing Needed
- Legal framework already extracted → markdown
- Procedures already structured → JSON
- Costs already calculated → JSON
- Zones already characterized → JSON

---

## 📌 Files for Reference Only

Not loaded at runtime, but available for Claude Code reference:
- `.claude/legal/ley-establecimientos-summary.md` - Legal reference
- `.claude/legal/retys-procedures-summary.md` - Procedure reference
- `.claude/processed/CLAUDE-CODE-INTEGRATION.md` - API spec

---

**Bottom Line**: All PDF information has been pre-processed into 7 compact, indexed JSON files. Claude Code loads them once at startup and queries them in <1ms. Zero runtime PDF processing.

