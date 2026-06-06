# Tools: Data Loaders

## Purpose
Load and index all 7 JSON data files at startup for sub-millisecond queries.

## Implementations

### load_business_types()
```python
def load_business_types():
    with open('.claude/data/business-types.json') as f:
        data = json.load(f)
    # Index by SCIAN code
    return {item['id']: item for item in data['business_types']}
```
**Returns**: Dict[SCIAN_code] → business profile

### load_zones()
```python
def load_zones():
    with open('.claude/data/zones.json') as f:
        data = json.load(f)
    # Index by zone code
    return {zone['code']: zone for zone in data['zones']}
```
**Returns**: Dict[zone_code] → zone characteristics

### load_procedures()
```python
def load_procedures():
    with open('.claude/data/procedures.json') as f:
        data = json.load(f)
    # Index by procedure code AND by business type
    return {
        'by_code': {...},
        'by_type': {...},
        'sequences': data['procedure_sequences']
    }
```
**Returns**: Indexed procedures for fast lookups

### load_costs()
```python
def load_costs():
    with open('.claude/data/costs.json') as f:
        return json.load(f)['costs']
```
**Returns**: Dict[SCIAN] → cost breakdown

### load_crime_index()
```python
def load_crime_index():
    with open('.claude/data/crime-index.json') as f:
        return json.load(f)
```
**Returns**: Crime data by zone and business type

### load_viability_model()
```python
def load_viability_model():
    with open('.claude/data/viability-model.json') as f:
        return json.load(f)['model']
```
**Returns**: Scoring algorithm with weights and thresholds

### startup_cache()
```python
@app.on_event("startup")
async def startup_cache():
    global BUSINESS_TYPES, ZONES, PROCEDURES, COSTS, CRIME, VIABILITY_MODEL
    BUSINESS_TYPES = load_business_types()
    ZONES = load_zones()
    PROCEDURES = load_procedures()
    COSTS = load_costs()
    CRIME = load_crime_index()
    VIABILITY_MODEL = load_viability_model()
```
**Timing**: All loaded in <100ms at startup

## Query Performance
- Business type lookup: <1ms (dict key)
- Zone lookup: <1ms (dict key)
- Cost calculation: <5ms (simple arithmetic)
- Full viability assessment: <100ms (6-factor calculation)

