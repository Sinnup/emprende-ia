# Module 1: Zone Viability Checker

## Purpose
Determine if a business can succeed in a specific CDMX location.

## Input Fields
1. **Business Type** (SCIAN dropdown)
   - Load from: `business-types.json`
   - Display: Spanish names with descriptions
   - Required: Yes

2. **Location** (Zone selector)
   - Load from: `zones.json`
   - Display: 16 CDMX borough options
   - Required: Yes

3. **Available Budget** (MXN numeric input)
   - Validation: > 0
   - Required: Yes

4. **Space Size** (m² numeric input)
   - Validation: > 0, < 10000
   - Required: Yes

## Processing Steps
1. Validate all inputs
2. Look up business profile
3. Look up zone characteristics
4. Calculate costs (rent based on zone + m²)
5. Calculate 6-factor viability score
6. Identify risks
7. Generate recommendation

## Output Display
1. **Viability Score Card** (0-100)
   - Color-coded: 80+ green, 65-79 yellow, 50-64 orange, <50 red
   - Label: "Highly Viable", "Viable", "Marginal", "Not Recommended"

2. **Factor Breakdown** (6 bars or radar chart)
   - Budget, Competition, Location, Security, Growth, Legal
   - Show score and interpretation for each

3. **Cost Summary Table**
   - Procedure costs
   - Monthly fixed costs (itemized)
   - First-year total projection
   - Monthly break-even timeline

4. **Risk Assessment**
   - Security risk (crime index)
   - Competition intensity
   - Growth outlook
   - Legal blockers (if any)

5. **Procedures Timeline**
   - Expandable cards showing each procedure
   - Name, timeline, cost, documents

6. **Recommendation Text**
   - "Proceed with caution", "Monitor these risks", etc.

## Success Criteria
- Response time: <100ms
- All data from embedded JSON files
- No external API calls
- Handles missing data gracefully
- Works for any business-type × zone combination

