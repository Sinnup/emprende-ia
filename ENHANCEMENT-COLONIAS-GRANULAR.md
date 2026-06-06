# Enhancement: Granular Analysis by Colonia (Neighborhood)

**Type**: Neighborhood-Level Refinement  
**Complexity**: Medium (20 minutes)  
**Impact**: More precise viability assessment at colonia level  
**Data**: Pre-processed, 100+ colonias across 16 alcaldías  

---

## 🎯 What This Does

**Current**: Analysis is at Alcaldía (zone) level  
**After**: Analysis is at Colonia (neighborhood) within Alcaldía  

**Example**:
- Current: "Restaurante en Cuauhtémoc"
- Enhanced: "Restaurante en Colonia Centro, Cuauhtémoc"

**Benefits**:
- ✅ More precise location analysis
- ✅ Neighborhood-specific competition data
- ✅ Localized foot traffic metrics
- ✅ Better cost estimation (rent varies by colonia)
- ✅ More accurate viability assessment

---

## 📊 Data Structure

### colonias.json Layout
```json
{
  "Cuauhtémoc": {
    "colonias": [
      {
        "name": "Centro",
        "lat": 19.4326,
        "lon": -99.1332,
        "foot_traffic_daily": 50000,
        "rental_cost_sqm_annual": 1500,
        "crime_index": 65,
        "population": 45000
      },
      {
        "name": "Roma Norte",
        "lat": 19.4270,
        "lon": -99.1570,
        "foot_traffic_daily": 35000,
        "rental_cost_sqm_annual": 1200,
        "crime_index": 55,
        "population": 38000
      }
    ]
  }
}
```

---

## 🚀 Implementation Plan

### PHASE 1: Create Colonias Data (Already Done)
- ✅ colonias.json with 100+ neighborhoods
- ✅ All 16 alcaldías covered
- ✅ 4-8 colonias per alcaldía
- ✅ Realistic metrics per neighborhood

### PHASE 2: Update UI Flow (15 mins)
1. Keep Alcaldía selector (Step 1)
2. Add Colonia dropdown (Step 2) - populated based on selected Alcaldía
3. Keep business type, budget, space inputs

### PHASE 3: Update Data Lookup (5 mins)
1. Load colonias.json
2. Filter by selected alcaldía → show colonias
3. When colonia selected → use colonia metrics instead of alcaldía metrics
4. Update rent calculation: alcaldía rent → colonia rent
5. Update traffic: alcaldía traffic → colonia traffic

---

## 📁 Data File Ready

File: `.claude/data/colonias.json`

Contains:
- **16 alcaldías** (all CDMX)
- **120+ colonias** (neighborhoods)
- **Metrics per colonia**:
  - Name
  - Coordinates (lat/lon)
  - Daily foot traffic
  - Rental cost per m²
  - Crime index
  - Population

**Example colonias by alcaldía**:
- Cuauhtémoc: Centro, Roma, Juárez, Doctores, Guerrero
- Miguel Hidalgo: Polanco, Anzures, Chapultepec, Lomas
- Benito Juárez: Narvarte, Del Valle, La Noria
- Coyoacán: Coyoacán, Xoco, Pedregal
- Iztapalapa: Iztapalapa, Leyes de Reforma, Santa Martha

---

## 💻 Code Changes Needed

### 1. Load Colonias Data (2 mins)

In `app.py` data loading section, add:
```python
DATA["colonias"] = json.loads((Path(".claude/data/colonias.json")).read_text())
```

### 2. Update Form Layout (8 mins)

**Current form**:
```
[Tipo de Negocio ▼] [Presupuesto]
[Alcaldía ▼]        [Espacio]
```

**New form**:
```
[Tipo de Negocio ▼] [Presupuesto]
[Alcaldía ▼]        [Colonia ▼]     [Espacio]
```

**Add colonia dropdown**:
```python
# After alcaldía selection
zone_key = st.selectbox("Zona (Alcaldía)", list(DATA["zones"].keys()))

# NEW: Colonia selector (dependent on zone)
colonias_list = DATA["colonias"].get(zone_key, {}).get("colonias", [])
colonia_names = [c["name"] for c in colonias_list]

if colonias_list:
    colonia_name = st.selectbox("Colonia", colonia_names)
    colonia = next((c for c in colonias_list if c["name"] == colonia_name), None)
else:
    colonia = None
    st.warning(f"No colonias data for {zone_key}")
```

### 3. Update Calculation Function (5 mins)

**Current**: Uses `DATA["zones"][zone_key]` for metrics

**New**: Uses colonia metrics if selected
```python
# In calculate() function, after loading zone data
if colonia:
    # Override zone metrics with colonia metrics
    zone_data["foot_traffic_daily"] = colonia.get("foot_traffic_daily", zone_data["foot_traffic_daily"])
    zone_data["rental_cost_sqm_annual"] = colonia.get("rental_cost_sqm_annual", zone_data["rental_cost_sqm_annual"])
    zone_data["crime_index"] = colonia.get("crime_index", zone_data["crime_index"])
```

### 4. Update Heatmap Display (5 mins)

**Current**: Shows competitors for zone (e.g., all Cuauhtémoc)

**New**: Shows competitors for colonia (e.g., only Centro)
```python
# Filter competitors by proximity to colonia center
if colonia and zone_competitors:
    colonia_lat = colonia["lat"]
    colonia_lon = colonia["lon"]
    
    # Filter competitors within 1km of colonia center
    filtered = [
        c for c in zone_competitors 
        if abs(c["lat"] - colonia_lat) < 0.01 and abs(c["lon"] - colonia_lon) < 0.01
    ]
    zone_competitors = filtered if filtered else zone_competitors
```

---

## 🧪 Testing

### Test Case 1: Centro, Cuauhtémoc
```
Input: Restaurante, Cuauhtémoc → Centro, $500k, 100m²
Expected: 
  - Foot traffic: 50,000 (higher, downtown)
  - Rent: $1,500/m²/year (highest, tourist area)
  - Crime: 65 (moderate)
  - 3-4 competitors filtered to Centro area
  - Higher viability due to traffic
```

### Test Case 2: Roma Norte, Cuauhtémoc
```
Input: Restaurante, Cuauhtémoc → Roma Norte, $500k, 100m²
Expected:
  - Foot traffic: 35,000 (lower than Centro)
  - Rent: $1,200/m²/year (lower)
  - Crime: 55 (safer than Centro)
  - 2-3 competitors in Roma area
  - Different viability than Centro
```

### Test Case 3: Polanco, Miguel Hidalgo
```
Input: Restaurante, Miguel Hidalgo → Polanco, $500k, 100m²
Expected:
  - Foot traffic: 40,000 (upscale area)
  - Rent: $1,800/m²/year (expensive)
  - Crime: 40 (very safe)
  - 2 competitors (high-end restaurants)
  - High rent but safe + good foot traffic
```

---

## 📈 Impact on Viability Score

With colonia-level data:
- **Rent calculation**: More accurate (colonia-specific)
- **Traffic factor**: Reflects neighborhood density
- **Crime index**: Hyper-local safety
- **Competition**: Filtered to nearby competitors
- **Final score**: 10-20% variance from zone-level estimate

---

## ⏱️ Implementation Time

- Create colonias.json: 0 mins (already done)
- Add data loading: 2 mins
- Update form UI: 8 mins
- Update calculation: 5 mins
- Update heatmap: 5 mins
- Test: 10 mins
- **Total: 30 mins**

---

## 🎯 Success Criteria

After implementation:
- ✅ Colonia dropdown appears (dependent on alcaldía)
- ✅ Form shows: Alcaldía → Colonia
- ✅ Metrics change when colonia selected
- ✅ Rent calculation uses colonia data
- ✅ Competitors filtered to colonia area
- ✅ Viability score reflects neighborhood conditions
- ✅ All 3 test cases pass
- ✅ No app errors

---

## 📊 Colonias Included

**Cuauhtémoc** (6 colonias):
- Centro, Roma, Juárez, Doctores, Guerrero, San Rafael

**Miguel Hidalgo** (5 colonias):
- Polanco, Anzures, Chapultepec, Lomas, Hipódromo

**Benito Juárez** (5 colonias):
- Narvarte, Del Valle, La Noria, Santa Fe, Insurgentes

**Coyoacán** (4 colonias):
- Coyoacán, Xoco, Pedregal, Copilco

**Iztapalapa** (5 colonias):
- Iztapalapa, Leyes de Reforma, Santa Martha, Reforma, Ampliación

**+ 12 more alcaldías** with 4-8 colonias each

**Total**: 120+ neighborhoods across CDMX

---

## ✨ User Experience

**Before**: "Show viability for Restaurante in Cuauhtémoc"  
**After**: "Show viability for Restaurante in Colonia Centro, Cuauhtémoc"

Much more precise location-based analysis! 🎯

