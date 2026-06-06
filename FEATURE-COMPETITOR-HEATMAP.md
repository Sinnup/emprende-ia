# Feature: Competitor Heatmap Visualization

**Status**: Optional Enhancement  
**Complexity**: Medium (15-20 minutes)  
**Impact**: Shows market saturation visually  

---

## 🗺️ The Challenge

Getting competitor data WITHOUT payment is difficult:

| Source | Data | Cost | API Key | Notes |
|--------|------|------|---------|-------|
| **Google Places** | Real competitors | $$$$ | Required | Most complete |
| **Foursquare** | Real competitors | $$$ | Required | Good data |
| **Yelp** | Real competitors | $$$ | Required | Detailed |
| **OpenStreetMap** | Limited | Free | Not needed | Lacks business data |
| **DENUE (INEGI)** | All CDMX businesses | Free | Not needed | **Best option for MX** |
| **Nominatim** | Address lookup | Free | Not needed | No business search |

---

## ✅ RECOMMENDED SOLUTION: Hybrid Approach

### Option 1: Synthetic Competitor Data (No API Key) ⭐ RECOMMENDED

**How it works**:
1. Pre-load synthetic competitor data (JSON file)
2. Filter by business type (SCIAN) and zone
3. Display on map with Folium (free, open source)
4. Show heatmap visualization

**Advantages**:
- ✅ No API key required
- ✅ Fast (data pre-loaded)
- ✅ Works for hackathon
- ✅ Can be replaced with real data later

**Disadvantages**:
- ❌ Synthetic data (not real competitors)
- ❌ Won't show actual market saturation

---

### Option 2: Google Places API (With API Key)

**How it works**:
1. User provides Google Places API key
2. Store in `.properties` or `.env` file
3. Query real competitors on-demand
4. Display on interactive map

**Advantages**:
- ✅ Real competitor data
- ✅ Accurate market assessment
- ✅ Production-ready

**Disadvantages**:
- ❌ Requires API key (user must get it)
- ❌ Costs money ($$$)
- ❌ Slower (API calls)

---

## 🚀 IMPLEMENTATION PLAN

### PHASE 1: Synthetic Heatmap (15 mins) - START HERE

**Step 1**: Create synthetic competitors dataset
```json
// .claude/data/competitors.json
{
  "722110": {  // SCIAN for Restaurant
    "Cuauhtémoc": [
      {"name": "Restaurant A", "lat": 19.4326, "lon": -99.1332, "rating": 4.2},
      {"name": "Restaurant B", "lat": 19.4350, "lon": -99.1298, "rating": 3.8},
      ...
    ]
  }
}
```

**Step 2**: Add map visualization to app.py
```python
import folium
from streamlit_folium import st_folium

# After results section, add:
st.subheader("🗺️ Competidores en la Zona")
map = folium.Map(location=[19.43, -99.13], zoom_start=14)
# Add markers for competitors
st_folium(map, width=700, height=500)
```

**Step 3**: Install dependency
```bash
pip install folium streamlit-folium
```

**Result**: Interactive map showing competitors in zone

---

### PHASE 2: Google Places API Integration (25 mins) - OPTIONAL

**If user provides API key**:

**Step 1**: Create `.properties` file
```properties
GOOGLE_PLACES_API_KEY=YOUR_KEY_HERE
```

**Step 2**: Add Google Places logic
```python
import googlemaps

gmaps = googlemaps.Client(key=API_KEY)
results = gmaps.places_nearby(
    location=(lat, lon),
    radius=1000,
    type='restaurant'  # Based on business type
)
```

**Step 3**: Show real vs synthetic toggle
```python
use_real_data = st.checkbox("Usar datos reales de Google Places")
if use_real_data and GOOGLE_PLACES_API_KEY:
    # Show real competitors
else:
    # Show synthetic competitors
```

**Result**: Real-time competitor data (if API key provided)

---

## 📋 QUICK IMPLEMENTATION: Synthetic Heatmap Only

If you want to ADD THIS NOW (15 minutes):

### File 1: Create competitors.json

```json
{
  "722110": {
    "Cuauhtémoc": [
      {"name": "Casa Lucio", "lat": 19.432, "lon": -99.133, "rating": 4.5, "reviews": 2340},
      {"name": "Contramar", "lat": 19.434, "lon": -99.131, "rating": 4.7, "reviews": 5600},
      {"name": "Restaurante Balcón", "lat": 19.435, "lon": -99.135, "rating": 4.1, "reviews": 890},
      {"name": "Casa de Comidas", "lat": 19.430, "lon": -99.129, "rating": 3.9, "reviews": 650}
    ],
    "Miguel Hidalgo": [
      {"name": "Pujol", "lat": 19.443, "lon": -99.158, "rating": 4.8, "reviews": 8900},
      {"name": "Quintonil", "lat": 19.441, "lon": -99.160, "rating": 4.7, "reviews": 4200}
    ]
  },
  "461110": {
    "Cuauhtémoc": [
      {"name": "Abarrotes Central", "lat": 19.432, "lon": -99.132, "rating": 4.2, "reviews": 450},
      {"name": "Tienda López", "lat": 19.433, "lon": -99.134, "rating": 3.8, "reviews": 320}
    ]
  }
}
```

### File 2: Modify app.py

Add after the "Claude Recommendation" section:

```python
# HEATMAP: Competitor Analysis
st.subheader("🗺️ Mapa de Competidores en la Zona")

try:
    import folium
    from streamlit_folium import st_folium
    
    # Load competitors
    competitors_data = DATA.get("competitors", {}).get(btype, {})
    zone_competitors = competitors_data.get(zone_key, [])
    
    if zone_competitors:
        # Get zone coordinates (approximate centers)
        zone_coords = DATA["zones"][zone_key]
        zone_lat = zone_coords.get("lat", 19.43)
        zone_lon = zone_coords.get("lon", -99.13)
        
        # Create map
        m = folium.Map(
            location=[zone_lat, zone_lon],
            zoom_start=14,
            tiles="OpenStreetMap"
        )
        
        # Add competitor markers
        for comp in zone_competitors:
            folium.CircleMarker(
                location=[comp["lat"], comp["lon"]],
                radius=5 if comp["rating"] < 4 else 8,
                popup=f"{comp['name']}<br>Rating: {comp['rating']}/5",
                color='red' if comp['rating'] >= 4.5 else 'orange',
                fill=True,
                fillColor='red' if comp['rating'] >= 4.5 else 'orange',
                fillOpacity=0.6
            ).add_to(m)
        
        # Add your location marker (approximate)
        folium.CircleMarker(
            location=[zone_lat, zone_lon],
            radius=10,
            popup="Tu Ubicación (aprox.)",
            color='blue',
            fill=True,
            fillColor='blue',
            fillOpacity=0.8
        ).add_to(m)
        
        # Display map
        st_folium(m, width=700, height=500)
        
        # Statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Competidores Detectados", len(zone_competitors))
        with col2:
            avg_rating = sum(c["rating"] for c in zone_competitors) / len(zone_competitors)
            st.metric("Rating Promedio", f"{avg_rating:.1f}/5")
        with col3:
            high_rated = len([c for c in zone_competitors if c["rating"] >= 4.5])
            st.metric("Bien Calificados (4.5+)", high_rated)
    
    else:
        st.info("No hay datos de competidores para esta zona")

except ImportError:
    st.warning("Instala: pip install folium streamlit-folium")
```

### File 3: Install dependency

```bash
pip install folium streamlit-folium
```

---

## 🎯 Two Path Options

### PATH A: Quick (Synthetic, 15 mins)
1. Create `competitors.json`
2. Add code to app.py
3. Install `folium streamlit-folium`
4. Test in app
5. ✅ Done - Heatmap works

### PATH B: Complete (With Google API option, 40 mins)
1. Do PATH A
2. Create `.properties` file for API key storage
3. Add Google Places integration code
4. Add toggle for real/synthetic data
5. Test both modes
6. ✅ Done - Full-featured heatmap

---

## 📊 Data I Can Generate

I can create realistic synthetic competitors for:
- All 9 business types (SCIAN codes)
- All 16 CDMX zones
- Realistic ratings, review counts, locations
- Based on actual zone coordinates

**Example output**: ~15-25 competitors per business type per zone = realistic density

---

## 🔧 API Key Option (If You Want Real Data)

If you want to use Google Places API (with your API key):

**Step 1**: Get free $300 credit
- Go to https://console.cloud.google.com
- Enable "Places API"
- Create API key
- **Cost**: ~$0.01 per competitor search

**Step 2**: Store in `.properties`
```properties
# .env or properties file
GOOGLE_PLACES_API_KEY=YOUR_KEY_HERE
```

**Step 3**: Code handles both modes
```python
if GOOGLE_PLACES_API_KEY:
    # Use real data from Google
else:
    # Use synthetic data (fallback)
```

---

## 📋 MY RECOMMENDATION

### For Hackathon: **PATH A (Synthetic)**
- ✅ 15 minutes to implement
- ✅ No API key needed
- ✅ Demonstrates feature
- ✅ Can upgrade later

### For Production: **PATH B (With API Option)**
- ✅ 40 minutes to implement
- ✅ User can choose real data
- ✅ Professional-grade
- ✅ API key stored securely

---

## ❓ DECISION NEEDED

Which path do you want?

1. **Just synthetic heatmap** (15 mins, no API key)
2. **Synthetic + Google API option** (40 mins, optional API key)
3. **Skip this feature** (focus on core MVP)

Let me know and I'll provide the complete implementation prompt for Claude Code! 🚀

