# Token & Network Efficiency Strategy

Minimize token usage and network load during hackathon through strategic caching, lazy-loading, and chunking.

## Priority 1: Pre-Cache Legal Framework (DONE)

### Action: Extract PDFs to Markdown
- [ ] Download: Ley de Establecimientos Mercantiles (PDF)
- [ ] Extract text → markdown format
- [ ] Store in: `.claude/context/legal/ley-establecimientos.md`
- [ ] Saves tokens: ✓ Avoids re-reading PDF each time

### Action: Extract RETYS Procedures (IN PROGRESS)
- [ ] Visit: https://www.registrodetramitesyservicios.cdmx.gob.mx/
- [ ] Export procedure list for "Mercantile Establishments"
- [ ] Reformat as JSON: `procedures.json`
- [ ] Store in: `.claude/context/data/procedures.json`
- [ ] Saves tokens: ✓ Avoids API calls during hackathon

### Action: Cache DENUE Sample Data
- [ ] Download DENUE CSV sample (INEGI)
- [ ] Keep only essential columns: id, name, type, location, coordinates
- [ ] 100-200 rows (test zones only)
- [ ] Store in: `.claude/context/data/denue-sample.csv`
- [ ] Saves tokens: ✓ Avoids large API requests

---

## Priority 2: Lazy-Load Context (On-Demand Reading)

### Strategy: Read Context Only When Needed

**Bad** (loads everything):
```python
all_context = read_all_files_in_folder(".claude/context")  # ❌ 50KB+ tokens
use_only_procedures()
```

**Good** (lazy-load):
```python
procedures = read_file(".claude/context/data/procedures.json")  # ✓ 5KB tokens
use_procedures()
```

### Implementation:
- Each module loads only its required context
- Module 1 (Viability) needs: business-types.json + zones.json
- Module 2 (Roadmap) needs: procedures.json only
- Don't load Module 3-5 data if building MVP only

---

## Priority 3: Chunked Markdown Files

### Strategy: Modular, Readable Documentation

**Goal**: Each markdown file <2KB (easily consumed by Claude)

**Files Structure**:
```
.claude/context/
├── legal/
│   ├── ley-establecimientos-summary.md    # 1.5KB (key points only)
│   ├── ley-establecimientos-full.md       # (for reference, not loaded)
│   └── reglamento-summary.md              # 1.2KB (key sections)
├── data/
│   ├── business-types.json                # 3KB (taxonomy only)
│   ├── procedures.json                    # 5KB (structure + samples)
│   └── zones-synthetic.json               # 2KB (test data)
└── references/
    ├── retys-api-guide.md                 # 0.8KB (how-to)
    └── denue-search-guide.md              # 0.6KB (how-to)
```

**Benefits**:
- ✓ Each file independently loadable
- ✓ Clear context boundaries
- ✓ Easier to review/debug
- ✓ Minimal token overhead

---

## Priority 4: Synthetic Data Strategy

### Action: Design Minimal, Realistic Test Data

**Not this**:
```json
{
  "zones": [
    {
      "id": "z1",
      "name": "Centro Histórico",
      "coordinates": [19.432, -99.133],
      "description": "El corazón de la ciudad, con historia de 500 años...",  // ❌ Verbose
      "demographic_data": {...},  // ❌ Too much data
      "traffic_patterns": {...}   // ❌ Unnecessary detail
    }
  ]
}
```

**Do this**:
```json
{
  "zones": [
    {
      "id": "z1",
      "name": "Centro Histórico",
      "coords": [19.432, -99.133],
      "competition_index": 0.85,
      "foot_traffic": "high",
      "regulations": ["Histórico", "Peatonal"]
    }
  ]
}
```

**Token Savings**: ~60% reduction in data size

---

## Priority 5: Atomic Commits with Mini-Changelogs

### Strategy: Update changelog per commit, not in bulk

**Bad** (loses tokens on duplicate work):
```
Week 1: [Work on multiple features]
Week 2: Write one massive changelog entry (can't remember all details)
```

**Good** (atomic tracking):
```
Commit 1: "feat(module-1): viability checker"
  - Update .claude/changelog.md immediately
  - 3-4 lines describing what changed

Commit 2: "feat(module-2): roadmap API"
  - Update .claude/changelog.md immediately
  - No need to recall old work
```

**Benefit**: No need to re-read old code to write changelog

---

## Priority 6: Feature Tasks as Task Tracker

### Strategy: Use feature-tasks.md as single source of truth

**Instead of**:
- Slack messages (lost context)
- Multiple docs (conflicting info)
- Brain (forgets details)

**Use**: `.claude/feature-tasks.md`
- Mark tasks [x] as completed
- Link to commits
- Update effort estimates as you go

**Token Savings**: 
- ✓ No need to re-read scattered notes
- ✓ One coherent source of status

---

## Priority 7: Standard Ignore Patterns

### Create `.gitignore` Early

```
# Large files that shouldn't be committed
*.pdf                    # Don't commit source PDFs
*.csv                    # Raw data files
venv/                    # Virtual env
__pycache__/
node_modules/
.env                     # Credentials
*.log
dist/
build/
```

**Benefit**: 
- ✓ Repo stays lightweight (<5MB)
- ✓ Faster git operations
- ✓ No accidental API key commits

---

## Priority 8: README Links Instead of Full Docs

### Strategy: README points to context, doesn't repeat it

**Bad**:
```markdown
## Installation

To install, first download Python 3.9+, then create a virtual environment...
[300 words of detailed steps that exist in SETUP.md]
```

**Good**:
```markdown
## Installation

See `SETUP.md` for detailed 5-minute setup.

Quick start:
```bash
pip install -r requirements.txt
python app.py
```
```

**Benefit**: 
- ✓ README stays concise
- ✓ Single source of truth per doc
- ✓ Easier to maintain

---

## Token Budget (Estimated)

**Per Claude API Call**:
- Main CLAUDE.md: ~8KB tokens
- Feature-tasks.md: ~4KB tokens
- Changelog.md: ~2KB tokens
- One context file (procedures.json): ~5KB tokens
- **Total typical call**: 15-20KB tokens

**Hackathon Duration**:
- 8 hours = ~30-40 API calls (assuming call per task)
- Total: ~600KB tokens (well within limits)

**Savings vs. Alternative**:
- ❌ Loading all PDFs each call: 100KB+ tokens per call
- ❌ Reading entire repo context: 50KB+ tokens per call
- ✓ This strategy: 15-20KB tokens per call
- **Savings**: 70-80% reduction

---

## Checklist: Token Efficiency Implementation

- [ ] Download legal PDFs before hackathon
- [ ] Convert PDFs to markdown summaries (`.claude/context/legal/`)
- [ ] Create synthetic data files (`.claude/context/data/`)
- [ ] Create `.gitignore` (blocks large files)
- [ ] Structure markdown files <2KB each
- [ ] Update changelog atomically (per commit)
- [ ] Link between docs instead of repeating
- [ ] Use feature-tasks.md as task tracker
- [ ] Only load context needed by current module

---

## Example: Module 1 Context Load

When working on **Module 1 (Zone Viability)**:

1. Load: `.claude/feature-tasks.md` → Find Module 1 section
2. Load: `.claude/context/data/business-types.json` → Taxonomy
3. Load: `.claude/context/data/zones-synthetic.json` → Test data
4. Load: `.claude/instructions/module-1-viability.md` → Logic
5. **Don't load**: procedures.json, legal docs (not needed for Module 1)

**Token Cost**: ~15KB (vs. 50KB+ if loading everything)

---

*Updated: June 6, 2026 — Strategic optimization for hackathon*
