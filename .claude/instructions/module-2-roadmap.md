# Module 2: Regulatory Roadmap

## Purpose
Show entrepreneurs the exact steps and timeline to legally open their business.

## Data Flow
1. Accept business type + entity type (individual or corporate)
2. Load procedure sequence from `procedures.json`
3. Load costs and timelines
4. Show ordered list with dependencies

## Procedure Sequence Logic
- RFC always first (1 day, free)
- Then: Registro Mercantil, Uso de Suelo (parallel possible)
- Then: Licencia Municipal (depends on Uso de Suelo)
- Then: SIAPEM (if environmental assessment needed)
- Finally: Sanitario (if food service) or other specialized

## Output: Procedures List
Each procedure card shows:
- **Sequence number** (1, 2, 3...)
- **Name** (Spanish + English)
- **Timeline** (days)
- **Cost** (MXN)
- **Required Documents** (bulleted list)
- **Agency** (where to apply)
- **Blocking**: Which procedures must complete first
- **Status**: "Required", "Conditional", "Optional"

## Timeline Visualization
- Gantt chart or sequential timeline
- Shows: Critical path, parallel activities, total duration
- Color-coded by agency (SAT, Ventanilla Única, SEDEMA, etc.)

## Success Criteria
- Shows correct sequence for every business type
- Includes all procedures and only required ones
- Accurate timelines and costs
- Clear explanation of blockers/dependencies
- Mobile-friendly visualization

