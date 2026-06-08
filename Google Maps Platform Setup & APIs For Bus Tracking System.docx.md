## 8. Routes API

### Purpose

Calculates optimal routes and estimated travel time.

### Key Features

* Traffic-aware routing

* ETA calculation

* Alternative routes

### Typical Use in Bus System

* Estimate arrival time to stops

* Optimize bus routes

### Enable Steps

1. Search **Routes API**

2. Click **Enable**

### Implementation Clarification

- For new MVP ETA work, prefer Routes API over legacy Distance Matrix or Directions API.
- Use `Compute Routes` when calculating one route between points.
- Use `Compute Route Matrix` when calculating ETA/distance from one bus to multiple stops.
- Keep the backend response simple so the frontend does not depend on Google response details.

### Files to Modify or Create

- Modify: `C:\Users\abdallah\Desktop\2026_BusTrackingSystem_Semester2\src\geo_map\services\distance.py`
  - Implement ETA/distance request logic.
  - Return normalized fields such as `distance_meters` and `duration_seconds`.
- Modify: `C:\Users\abdallah\Desktop\2026_BusTrackingSystem_Semester2\src\geo_map\route.py`
  - Expose the ETA endpoint.
- Modify: `C:\Users\abdallah\Desktop\2026_BusTrackingSystem_Semester2\static\index.js`
  - Call the ETA endpoint and display the result.

### Resources

- Routes API overview: https://developers.google.com/maps/documentation/routes
- Compute Routes: https://developers.google.com/maps/documentation/routes/compute_route_directions
- Compute Route Matrix: https://developers.google.com/maps/documentation/routes/compute_route_matrix

## 9. Distance Matrix API

### Purpose

Computes travel time and distance between multiple origins and destinations.

### Key Features

* Batch ETA calculation

* Traffic-aware duration

### Typical Use in Bus System

* Calculate ETA from bus to all upcoming stops

### Implementation Clarification

- This API may be useful if the current code already uses it, but it is legacy.
- For new implementation, prefer Routes API `Compute Route Matrix`.
- If kept temporarily, keep it behind the same backend endpoint contract so it can be replaced later without changing frontend code.

### Files to Modify or Check

- Modify/check: `C:\Users\abdallah\Desktop\2026_BusTrackingSystem_Semester2\src\geo_map\services\distance.py`
  - Current distance/ETA service belongs here.
- Modify/check: `C:\Users\abdallah\Desktop\2026_BusTrackingSystem_Semester2\src\geo_map\route.py`
  - ETA route should call the distance service.
- Modify/check: `C:\Users\abdallah\Desktop\2026_BusTrackingSystem_Semester2\static\index.js`
  - Frontend should expect the normalized backend response, not raw Google JSON.

### Resources

- Distance Matrix API overview: https://developers.google.com/maps/documentation/distance-matrix/overview
- Distance Matrix request and response: https://developers.google.com/maps/documentation/distance-matrix/distance-matrix
- Routes API Compute Route Matrix: https://developers.google.com/maps/documentation/routes/compute_route_matrix

## 10. Places API

### Purpose

Provides location data for places and stops.

### Key Features

* Place search

* Place details

* Place Autocomplete

### Typical Use in Bus System

* Search bus stops

* Autocomplete addresses for route planning

### Implementation Clarification

- This is optional for the MVP.
- Use it only if the UI needs a search/autocomplete box for locations.
- If stops are fixed and already stored in the database, do not use Places API for them.

### Files to Modify or Create

- Create only if needed: a frontend search input in `C:\Users\abdallah\Desktop\2026_BusTrackingSystem_Semester2\templates\index.html`
- Modify only if needed: `C:\Users\abdallah\Desktop\2026_BusTrackingSystem_Semester2\static\index.js`
  - Add autocomplete/search behavior.
- No backend file is required unless search results must be saved.

### Resources

- Places API with Maps JavaScript: https://developers.google.com/maps/documentation/javascript/place-get-started
- Place Autocomplete: https://developers.google.com/maps/documentation/javascript/place-autocomplete

## 11. Geocoding API

### Purpose

Converts addresses into geographic coordinates.

### Key Features

* Address -> Latitude/Longitude

* Reverse geocoding

### Typical Use in Bus System

* Convert stop names into map coordinates

### Implementation Clarification

- Use this only for converting text addresses or stop names into coordinates.
- For MVP stability, fixed AAU stops should eventually be saved with exact latitude/longitude instead of geocoded on every startup.
- Cache geocoding results if the service remains in use.

### Files to Modify or Check

- Modify/check: `C:\Users\abdallah\Desktop\2026_BusTrackingSystem_Semester2\src\geo_map\services\geocoding.py`
  - Handles Google geocoding requests.
- Modify/check: `C:\Users\abdallah\Desktop\2026_BusTrackingSystem_Semester2\src\geo_map\services\stops.py`
  - Current stop population may call geocoding.
- Modify/check: `C:\Users\abdallah\Desktop\2026_BusTrackingSystem_Semester2\src\helpers\back_fill.py`
  - Demo stop seed data currently lives here.
- Create later if database seeding is added: a seed or migration file for fixed stop coordinates.

### Resources

- Geocoding API docs: https://developers.google.com/maps/documentation/geocoding
- Geocoding requests: https://developers.google.com/maps/documentation/geocoding/requests-geocoding
- Reverse geocoding: https://developers.google.com/maps/documentation/geocoding/requests-reverse-geocoding

## 12. Roads API (Snap to Roads)

### Purpose

Aligns raw GPS data to real road geometry.

### Key Features

* GPS correction

* Road snapping

### Typical Use in Bus System

* Improve accuracy of live bus GPS tracking

### Implementation Clarification

- This is optional for MVP.
- The first demo can show raw GPS coordinates directly.
- Add Roads API later only if bus marker movement looks too noisy or inaccurate.
- If implemented, store raw GPS first; snapped points can be derived.

### Files to Modify or Create

- Create later if needed: `C:\Users\abdallah\Desktop\2026_BusTrackingSystem_Semester2\src\geo_map\services\roads.py`
- Modify later if needed: GPS ingest endpoint/service once it exists.
- Modify later if needed: database schema/migration if storing snapped coordinates separately.

### Resources

- Roads API docs: https://developers.google.com/maps/documentation/roads
- Snap to Roads: https://developers.google.com/maps/documentation/roads/snap
- Nearest Roads: https://developers.google.com/maps/documentation/roads/nearest

## 13. Time Zone API

### Purpose

Determines local time based on coordinates.

### Typical Use in Bus System

* Synchronize timestamps for tracking and reporting

### Implementation Clarification

- This is not needed for the current AAU-only MVP.
- Store backend timestamps consistently in UTC.
- Display local time in the frontend if needed.
- Do not call Time Zone API for every GPS update.

### Files to Modify or Create

- No file is needed for the current MVP.
- If time-zone support is added later, put conversion logic in a backend utility module, not in map rendering code.

### Resources

- Time Zone API overview: https://developers.google.com/maps/documentation/timezone/overview

## 14. Directions API 

### Purpose

Provides turn-by-turn directions.

### Typical Use

* Driver navigation support (optional feature)

### Implementation Clarification

- This is optional and should not be implemented for the current simple bus-tracking MVP.
- Use Routes API for route/ETA work.
- Add Directions only if the driver portal later needs turn-by-turn navigation.

### Files to Modify or Create

- No file is needed for the current MVP.
- If driver navigation becomes required later:
  - Create: `C:\Users\abdallah\Desktop\2026_BusTrackingSystem_Semester2\templates\driver.html`
  - Create: `C:\Users\abdallah\Desktop\2026_BusTrackingSystem_Semester2\static\driver.js`
  - Modify: `C:\Users\abdallah\Desktop\2026_BusTrackingSystem_Semester2\main.py`

### Resources

- Directions API docs: https://developers.google.com/maps/documentation/directions/get-directions
- Routes API docs: https://developers.google.com/maps/documentation/routes



### Implementation Clarification

- For the current MVP, focus only on map display, stop/bus markers, basic route display, and ETA.
- Avoid adding ML, BusBot, analytics, or route optimization in this Google Maps setup task.
- Keep API calls behind backend services where possible.
- Keep frontend responses simple and stable.

### Current MVP File Map

| Area | File |
| --- | --- |
| App entrypoint | `C:\Users\abdallah\Desktop\2026_BusTrackingSystem_Semester2\main.py` |
| Config/env loading | `C:\Users\abdallah\Desktop\2026_BusTrackingSystem_Semester2\src\utils\config.py` |
| API routes | `C:\Users\abdallah\Desktop\2026_BusTrackingSystem_Semester2\src\geo_map\route.py` |
| Map HTML | `C:\Users\abdallah\Desktop\2026_BusTrackingSystem_Semester2\templates\index.html` |
| Map JavaScript | `C:\Users\abdallah\Desktop\2026_BusTrackingSystem_Semester2\static\index.js` |
| Geocoding service | `C:\Users\abdallah\Desktop\2026_BusTrackingSystem_Semester2\src\geo_map\services\geocoding.py` |
| ETA/distance service | `C:\Users\abdallah\Desktop\2026_BusTrackingSystem_Semester2\src\geo_map\services\distance.py` |
| Bus service | `C:\Users\abdallah\Desktop\2026_BusTrackingSystem_Semester2\src\geo_map\services\buses.py` |
| Stop service | `C:\Users\abdallah\Desktop\2026_BusTrackingSystem_Semester2\src\geo_map\services\stops.py` |
| Demo seed data | `C:\Users\abdallah\Desktop\2026_BusTrackingSystem_Semester2\src\helpers\back_fill.py` |


