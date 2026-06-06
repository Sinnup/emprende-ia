# SEDECO MVP: Colonia-Level Analysis Enhancement

## Objective
Add neighborhood (Colonia) granularity to the viability assessment. Users will select **Alcaldía → Colonia** instead of just Alcaldía. All metrics (rent, traffic, crime, competitors) will be colonia-specific.

---

## 📋 Task Checklist

- [ ] Load colonias.json into app.py
- [ ] Add colonia dropdown (dependent on alcaldía selection)
- [ ] Update viability calculation to use colonia metrics
- [ ] Filter competitors by proximity to colonia
- [ ] Update heatmap to show colonia-specific competitors
- [ ] Test 3 test cases
- [ ] Verify no errors in Spanish UI

---

## 🚀 Implementation Steps

### STEP 1: Load colonias.json (2 mins)

In `app.py`, in the **data loading section** (around line 80-90 where other JSON files load), add:

```python
# Load colonia data
with open(".claude/data/colonias.json") as f:
    DATA["colonias"] = json.load(f)
```

**Verify it loads**: 
- Should have keys like "Cuauhtémoc", "Miguel Hidalgo", etc.
- Each alcaldía has "colonias" array with 4-8 neighborhoods

---

### STEP 2: Add Colonia Selector to UI (8 mins)

**Location**: Find the form section in `app.py` where alcaldía is selected (around line 150-170).

**Current code looks like**:
```python
zone_key = st.selectbox("Zona (Alcaldía)", list(DATA["zones"].keys()))
```

**Replace with this block**:
```python
# Alcaldía selector
zone_key = st.selectbox("Zona (Alcaldía)", list(DATA["zones"].keys()))

# NEW: Colonia selector (dependent on zone)
st.write("---")
colonias_list = DATA["colonias"].get(zone_key, {}).get("colonias", [])
colonia_names = [c["name"] for c in colonias_list]

if colonias_list:
    colonia_name = st.selectbox(
        "Colonia",
        colonia_names,
        help="Selecciona la colonia específica para análisis más preciso"
    )
    # Find the selected colonia object
    colonia = next((c for c in colonias_list if c["name"] == colonia_name), None)
else:
    colonia = None
    st.warning(f"⚠️ Sin datos de colonias para {zone_key}")
```

**Result**: Users will see a cascading dropdown: Alcaldía → Colonia

---

### STEP 3: Update calculate() Function (5 mins)

**Location**: Find the `calculate()` function (around line 300-400).

**In the section where zone_data is loaded** (looks like `zone_data = DATA["zones"][zone_key]`), **after that line, add**:

```python
# Override zone metrics with colonia metrics if selected
if colonia:
    zone_data_copy = zone_data.copy()  # Don't modify original
    zone_data_copy["foot_traffic_daily"] = colonia.get("foot_traffic_daily", zone_data["foot_traffic_daily"])
    zone_data_copy["rental_cost_sqm_annual"] = colonia.get("rental_cost_sqm_annual", zone_data["rental_cost_sqm_annual"])
    zone_data_copy["crime_index"] = colonia.get("crime_index", zone_data["crime_index"])
    zone_data = zone_data_copy
```

**Effect**: Now rent calculation, traffic, and crime will use colonia-specific values instead of zone-level values.

**Example**:
- Cuauhtémoc (zone) avg rent: $1,200/m²
- Centro (colonia in Cuauhtémoc): $1,500/m² (higher, downtown)
- Roma Norte (colonia in Cuauhtémoc): $1,200/m² (matches zone)

---

### STEP 4: Filter Competitors by Colonia Proximity (5 mins)

**Location**: Find where heatmap data is prepared (around line 350-380, where `zone_competitors` is loaded).

**After loading zone_competitors, add this**:

```python
# Filter competitors by colonia proximity if colonia selected
if colonia and zone_competitors:
    colonia_lat = colonia.get("lat")
    colonia_lon = colonia.get("lon")
    
    if colonia_lat and colonia_lon:
        # Keep competitors within ~1.5 km (0.015 degrees of latitude)
        filtered = [
            c for c in zone_competitors
            if (abs(c.get("lat", 0) - colonia_lat) <= 0.015 and 
                abs(c.get("lon", 0) - colonia_lon) <= 0.015)
        ]
        # Use filtered if found, otherwise show all zone competitors
        zone_competitors = filtered if filtered else zone_competitors
```

**Effect**: Competitors map and count will be colonia-specific, not zone-wide.

---

### STEP 5: Update Heatmap Title (2 mins)

**Location**: Find where heatmap title is set (around line 400, where folium map is created).

**Current**:
```python
st.subheader(f"🗺️ Mapa de Competidores en {zone_key}")
```

**Change to**:
```python
colonia_display = f", {colonia_name}" if colonia else ""
st.subheader(f"🗺️ Mapa de Competidores en {zone_key}{colonia_display}")
```

**Result**: Map title will show "Mapa de Competidores en Cuauhtémoc, Centro" (neighborhood-specific).

---

### STEP 6: Update Statistics Display (2 mins)

**Location**: Find where competitor statistics are displayed (around line 420-440).

**Look for**:
```python
st.metric("Total Competidores", len(zone_competitors))
```

**This already works** — it will automatically show filtered count (e.g., "3 competitors in Centro" instead of "8 in Cuauhtémoc").

No changes needed here! The filtering from STEP 4 handles it.

---

## 🧪 Testing (10 mins)

### Test Case 1: Centro, Cuauhtémoc (High-Traffic Downtown)
```
Select:
  Tipo de Negocio: Restaurante
  Zona (Alcaldía): Cuauhtémoc
  Colonia: Centro
  Presupuesto: $500,000
  Espacio: 100 m²

Expected Results:
  ✓ Rent cost: $1,500/m²/year (highest in zone - downtown premium)
  ✓ Foot traffic: 50,000/day (highest in zone)
  ✓ Crime index: 65 (moderate)
  ✓ Viability score: HIGH (good traffic, affordable for restaurant)
  ✓ Competitors: 3-4 restaurants shown on map (centered on Centro)
```

### Test Case 2: Roma Norte, Cuauhtémoc (Trendy Middle-Market)
```
Select:
  Tipo de Negocio: Restaurante
  Zona (Alcaldía): Cuauhtémoc
  Colonia: Roma Norte
  Presupuesto: $500,000
  Espacio: 100 m²

Expected Results:
  ✓ Rent cost: $1,200/m²/year (lower than Centro, higher vibe)
  ✓ Foot traffic: 35,000/day (decent foot traffic)
  ✓ Crime index: 55 (safer than Centro)
  ✓ Viability score: HIGH (good balance)
  ✓ Competitors: 2-3 restaurants (different from Centro!)
```

### Test Case 3: Polanco, Miguel Hidalgo (Upscale)
```
Select:
  Tipo de Negocio: Restaurante
  Zona (Alcaldía): Miguel Hidalgo
  Colonia: Polanco
  Presupuesto: $500,000
  Espacio: 100 m²

Expected Results:
  ✓ Rent cost: $1,800/m²/year (most expensive)
  ✓ Foot traffic: 40,000/day (upscale clientele)
  ✓ Crime index: 40 (very safe)
  ✓ Viability score: MEDIUM (high costs, good safety)
  ✓ Competitors: 2 high-end restaurants
```

**Validation**:
- [ ] Test Case 1 results differ from Test Case 2 (different colonias = different metrics)
- [ ] Test Case 3 has highest rent (Polanco is expensive)
- [ ] Test Case 1 has most competitors (Centro is busy)
- [ ] All maps show different competitor locations
- [ ] No errors or warnings in UI
- [ ] All text is in Spanish

---

## 📊 Expected Changes in Output

### Before Enhancement
```
Restaurante en Cuauhtémoc
Rent: $1,200/m²/year (zone average)
Foot traffic: 28,000/day (zone average)
Viability: MEDIUM
Competitors: 8 total in Cuauhtémoc
```

### After Enhancement
```
Restaurante en Colonia Centro, Cuauhtémoc
Rent: $1,500/m²/year (Centro premium)
Foot traffic: 50,000/day (Centro busy)
Viability: HIGH
Competitors: 4 in Centro area
```

Much more precise! 🎯

---

## ✅ Success Criteria

After implementation:
- [ ] Colonia dropdown appears and is dependent on Alcaldía selection
- [ ] Changing Alcaldía updates available Colonias
- [ ] Metrics change when Colonia selected (rent, traffic, crime visible in results)
- [ ] Competitors count drops when colonia selected (filtered to location)
- [ ] Heatmap title shows colonia name
- [ ] Heatmap markers are centered on colonia coordinates
- [ ] All 3 test cases pass
- [ ] No errors in console
- [ ] All UI text remains in Spanish

---

## 🔄 Implementation Flow (Copy-Paste Ready)

**In order**:

1. **Load colonias.json** (line ~85)
   ```python
   with open(".claude/data/colonias.json") as f:
       DATA["colonias"] = json.load(f)
   ```

2. **Add colonia selector** (after zone selector, line ~155)
   ```python
   colonias_list = DATA["colonias"].get(zone_key, {}).get("colonias", [])
   colonia_names = [c["name"] for c in colonias_list]
   if colonias_list:
       colonia_name = st.selectbox("Colonia", colonia_names, ...)
       colonia = next((c for c in colonias_list if c["name"] == colonia_name), None)
   else:
       colonia = None
   ```

3. **Override metrics in calculate()** (after zone_data load, line ~310)
   ```python
   if colonia:
       zone_data_copy = zone_data.copy()
       zone_data_copy["foot_traffic_daily"] = colonia.get("foot_traffic_daily", ...)
       zone_data_copy["rental_cost_sqm_annual"] = colonia.get("rental_cost_sqm_annual", ...)
       zone_data_copy["crime_index"] = colonia.get("crime_index", ...)
       zone_data = zone_data_copy
   ```

4. **Filter competitors** (where zone_competitors loads, line ~360)
   ```python
   if colonia and zone_competitors:
       colonia_lat = colonia.get("lat")
       colonia_lon = colonia.get("lon")
       if colonia_lat and colonia_lon:
           filtered = [c for c in zone_competitors if ...]
           zone_competitors = filtered if filtered else zone_competitors
   ```

5. **Update map title** (line ~405)
   ```python
   colonia_display = f", {colonia_name}" if colonia else ""
   st.subheader(f"🗺️ Mapa de Competidores en {zone_key}{colonia_display}")
   ```

---

## 📝 Notes

- **colonias.json location**: `.claude/data/colonias.json` (already created, 13 KB)
- **Existing files**: No existing files need to be deleted
- **Data structure**: Each colonia has lat, lon, foot_traffic_daily, rental_cost_sqm_annual, crime_index
- **Backward compatible**: If colonia is None, code falls back to zone metrics
- **UI flow**: Alcaldía selection → Colonia dropdown populates → User selects → Metrics update

---

## ⏱️ Time Estimate
- Load data: 1 min
- Add selector: 3 min
- Update calculation: 2 min
- Filter competitors: 3 min
- Update titles: 1 min
- Testing: 10 min
- **Total: 20 minutes**

Ready to implement? Copy this prompt and run it in Claude Code! 🚀

