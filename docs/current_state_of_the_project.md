# Current state against original plan

This document compares current repo state with `BusTracking System Documentation.md`.

## Done from original plan

### Backend foundation

FastAPI backend exists and serves both API routes and main map page. Current scope is demo-level backend, not production transport platform.

### Map frontend

Browser map exists. It loads stops, routes, and buses from backend, then displays them with Google Maps markers/polyline.

### Google Maps usage

Google APIs are wired for stop geocoding and intended ETA/distance calculation. This covers early Phase 1 bootstrap direction from original plan.

### Demo tracking data

Repo has in-memory buses and stops. Buses already have coordinates; stops are names that get geocoded at runtime. No real driver GPS stream yet.

### API layer

Backend exposes first map/tracking endpoints:

| Endpoint | Source | What it returns now |
|----------|--------|---------------------|
| `GET /` | `main.py` | HTML map page from `templates/index.html` |
| `GET /api/buses` | `src/geo_map/route.py` | List of static demo buses from `back_fill.py` |
| `GET /api/stops` | `src/geo_map/route.py` | List of stop records after Google geocoding |
| `GET /api/routes` | `src/geo_map/route.py` | One dynamic route built from geocoded stop locations |
| `GET /api/distance/eta` | `src/geo_map/route.py` | Intended ETA/distance response from Google Distance Matrix service |
| `GET /api/geocode/address` | `src/geo_map/route.py` | Latitude, longitude, and formatted address for a text address |
| `GET /api/geocode/reverse` | `src/geo_map/route.py` | Formatted address for latitude/longitude |

### Current schemas

Current schema is only map data: location, bus, stop, route.

```python
# file: src/geo_map/model.py
class Location(BaseModel):
    lat: float
    lng: float

class Bus(BaseModel):
    id: int
    location: Location
    speed: float | None = None

class Stop(BaseModel):
    id: int
    name: str
    location: Location

class Route(BaseModel):
    id: int
    name: str
    path: List[Location]
```

### Current seed data

Current bus and stop data is hardcoded. Buses already include coordinates. Stops only include names, then Google Geocoding adds coordinates at runtime.

```python
# file: src/helpers/back_fill.py
buses = [
    {
        "id": 1,
        "location": {"lat": 32.009463, "lng": 35.863501},
        "speed": 35
    }
]

stops = [
    {
        "id": 1,
        "name": "Al-Ahliyya Amman University Main Gate",
    }
]
```

### Environment config

The Google Maps key is loaded from environment configuration, which supports the original plan's requirement to keep API credentials outside the code.

## What is left from the original plan

### Real driver mobile application

### Live GPS updates from driver smartphones

### Persistent database layer

### Supabase authentication and row-level security

### Role-based student, driver, and admin access

### Real-time updates through WebSocket or Supabase Realtime

### Admin dashboard

### Student dashboard

### Driver portal

### Route and schedule management

### Trip confirmation workflow

### Push notifications

### Data collection pipeline

### Historical GPS and trip storage

### Google Routes/Roads/Distance Matrix production flow

### ETA prediction model

### Delay classification model

### Route efficiency scoring

### Anomaly detection system

### BusBot conversational assistant

### Analytics dashboard

### Cost tracking and API usage monitoring

### Model training, versioning, and evaluation

### Deployment and production reliability work

---

# Known issues

This section records current code mismatches only. No implementation guidance.

## Discovery notes

- Project Python files parse clean through `uv run python`.
- Review covered `main.py`, `src/geo_map/`, `static/`, `templates/`, `requirements.txt`, and repo status.

## 1. `/api/routes` response shape

`/api/routes` is declared as `List[Route]`, but returns one route object. Frontend treats response as an array and calls `forEach`, so browser can throw `TypeError: data.forEach is not a function`.

Key files: `src/geo_map/route.py`, `static/index.js`.

## 2. `/api/distance/eta` data flow

`distance_metrix` calls async bus/stop services without `await`, so values become coroutine objects instead of lists. Same endpoint also ignores frontend query params (`origins`, `destinations`) and returns a different shape than `fetchETA` expects.

Key files: `src/geo_map/services/distance.py`, `static/index.js`.

## 3. Distance Matrix endpoint shape

Frontend expects `data.results`. Backend builds a bus-grouped list with `bus_id` and `etas`. Same feature has two response contracts.

Key files: `src/geo_map/services/distance.py`, `static/index.js`.

## 4. `loadBuses` variable scope

`busObj` is created only when bus is new. Existing bus path updates marker, then later code still references `busObj`, which can cause `ReferenceError: busObj is not defined`.

Key file: `static/index.js`.

## 5. `fetchETA` null path

`fetchETA` can return `null`, but caller immediately reads `eta.etaSeconds`. If ETA call fails or response shape does not match, frontend can throw when building bus info window.

Key file: `static/index.js`.

## 6. Stop cache grows on repeated calls

`PopulateStops.populate_stops()` appends to `geocoding_stops` every call. `/api/stops` and `/api/routes` both call it, so repeated requests can duplicate stop records in memory.

Key files: `src/geo_map/services/stops.py`, `src/geo_map/route.py`.

## 7. Bus cache grows on repeated calls

`PopulateBuses.buses()` appends static bus data to `geocoding_buses` every call. Repeated `/api/buses` calls can duplicate bus records in memory.

Key files: `src/geo_map/services/buses.py`, `src/geo_map/route.py`.

## 8. `PopulateBuses` docstring mismatch

Docstring says it geocodes stops. Actual behavior copies static bus data from `back_fill.py`.

Key files: `src/geo_map/services/buses.py`, `src/helpers/back_fill.py`.

## 9. `PopulateBuses` unused geocoding dependency

`PopulateBuses` creates a `GeocodingService`, but bus population does not use geocoding.

Key file: `src/geo_map/services/buses.py`.

## 10. Startup geocoding is separate from route service cache

`main.py` geocodes stops in lifespan using one `PopulateStops` instance. API routes use another global `PopulateStops` instance, so startup work is not reused by `/api/stops` or `/api/routes`.

Key files: `main.py`, `src/geo_map/route.py`, `src/geo_map/services/stops.py`.

## 11. Google API error handling is thin

Geocoding and Distance Matrix services assume expected Google response fields exist. Network errors, quota errors, invalid keys, or unexpected JSON can surface as runtime errors.

Key files: `src/geo_map/services/geocoding.py`, `src/geo_map/services/distance.py`.

## 12. Debug prints in service path

Distance Matrix service prints destinations and results during request handling. This mixes runtime API behavior with console debug output.

Key file: `src/geo_map/services/distance.py`.

## 13. Empty module

`src/geo_map/query.py` exists but is empty.

Key file: `src/geo_map/query.py`.

## 14. Map center mismatch

HTML map starts with New York coordinates. JavaScript later recenters to AAU coordinates. This creates duplicate center source and possible first-load mismatch.

Key files: `templates/index.html`, `static/index.js`.

## 15. Frontend has old commented implementation

`static/index.js` keeps an older commented `loadBuses` implementation. Active and inactive versions sit together, which makes current behavior harder to read.

Key file: `static/index.js`.

## 16. Repository contains generated Python cache files

Working tree contains generated `__pycache__` files and a deleted old Python cache entry.

Key paths: `__pycache__/`, `src/**/__pycache__/`.

## 17. Plan vs repo scope

Original plan includes Supabase, auth, dashboards, ML models, BusBot, realtime updates, and production data storage. Current repo is smaller: FastAPI, static map, demo buses/stops, Google geocoding, and intended Distance Matrix integration.

## Change log

| Date | Note |
|------|------|
| 2026-05-20 | Initial state review |
