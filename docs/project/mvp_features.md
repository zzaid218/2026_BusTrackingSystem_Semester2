# MVP features — what remains to ship

This document defines the **Minimum Viable Product** for the AAU bus tracking system, based on the current codebase and Phase 1 scope from `BusTracking System Documentation.md`.

**MVP goal:** A student opens a map, sees live bus positions on AAU routes, and gets ETA to stops. A driver sends GPS from a phone. Data persists in a database so the system can collect history for later ML work.

**Out of MVP scope (Phase 2+):** ML models, BusBot, analytics dashboard, delay classification, anomaly detection, push notifications at scale, admin analytics, cost monitoring.

---

## Current baseline (already in repo)

| Area | Status | Notes |
|------|--------|-------|
| FastAPI server | Done | `main.py` — serves API + map page |
| Map UI (Google Maps) | Done | `templates/index.html`, `static/index.js` |
| Demo buses/stops | Done | Hardcoded in `src/helpers/back_fill.py` |
| Geocoding service | Done | `src/geo_map/services/geocoding.py` |
| REST endpoints (read-only) | Partial | `/api/buses`, `/api/stops`, `/api/routes`, `/api/distance/eta`, geocode |
| Pydantic models | Partial | `Location`, `Bus`, `Stop`, `Route` only |
| Env config | Done | `GOOGLE_MAPS_API_KEY` via `src/utils/config.py` |

---

## MVP feature backlog

Tasks are ordered roughly by dependency. Each item includes acceptance criteria.

### P0 — Fix what exists (demo must work end-to-end)

These are blockers before adding new features. See `docs/current_state_of_the_project.md` for details.

- [ ] **Fix `/api/routes` response shape**
  - Return a JSON array (`[{ ... }]`), not a single object.
  - Frontend `loadRoutes()` expects `data.forEach(...)`.
  - Files: `src/geo_map/route.py`, `static/index.js`

- [ ] **Fix `/api/distance/eta` async + contract**
  - `await` calls to `buses()` and `populate_stops()` in `distance_metrix()`.
  - Accept `origins` and `destinations` query params from frontend (or pick one canonical contract).
  - Align response with frontend: `{ results: [{ distance_meters, duration_seconds }] }`.
  - Files: `src/geo_map/services/distance.py`, `src/geo_map/route.py`, `static/index.js`

- [ ] **Fix bus cache duplication**
  - `PopulateBuses.buses()` appends on every call → duplicate buses.
  - Load once (startup or idempotent populate), reuse shared instance.
  - Files: `src/geo_map/services/buses.py`, `main.py`, `src/geo_map/route.py`

- [ ] **Fix stop cache duplication**
  - Same issue in `PopulateStops.populate_stops()`.
  - Share one `PopulateStops` instance between lifespan startup and API routes.
  - Files: `src/geo_map/services/stops.py`, `main.py`, `src/geo_map/route.py`

- [ ] **Fix `loadBuses` frontend bug**
  - `busObj` referenced outside the `else` branch → `ReferenceError` on updates.
  - Guard ETA info-window update when `fetchETA` returns `null`.
  - Files: `static/index.js`

- [ ] **Map center consistency**
  - Use AAU coordinates in HTML template (remove NYC default).
  - Files: `templates/index.html`, `static/index.js`

- [ ] **Google API error handling**
  - Handle missing key, quota errors, non-OK Distance Matrix elements without 500s.
  - Files: `src/geo_map/services/geocoding.py`, `src/geo_map/services/distance.py`

---

### P1 — Data layer (replace in-memory demo)

- [ ] **Choose and connect database**
  - Supabase/PostgreSQL per original plan.
  - Add client lib, connection config, and health check.
  - Files: new `src/db/`, update `src/utils/config.py`, `requirements.txt`

- [ ] **Core schema + migrations**
  - Tables: `users`, `routes`, `stops`, `route_stops` (ordered), `buses`, `trips`, `gps_locations`.
  - Minimum columns per `docs/system_component_requirements.md`.
  - Seed AAU stops/routes from admin script or migration, not `back_fill.py`.

- [ ] **Replace hardcoded read paths**
  - `/api/buses`, `/api/stops`, `/api/routes` read from DB.
  - Keep Pydantic models; map DB rows to existing response shapes.
  - Deprecate append-only in-memory caches.

- [ ] **GPS ingest endpoint**
  - `POST /api/gps` (or `/api/buses/{id}/location`) — lat, lng, speed, heading, timestamp.
  - Validate coords, attach `bus_id` + active `trip_id`, persist to `gps_locations`.
  - Update latest position used by `/api/buses`.

- [ ] **Trip lifecycle (minimal)**
  - `POST /api/trips/start` — driver starts trip (bus + route).
  - `POST /api/trips/end` — closes trip.
  - `/api/buses` returns position from latest GPS row for active trip.

---

### P2 — Authentication & roles (minimal)

- [ ] **Supabase Auth integration**
  - Login for driver and admin; student view can stay public read-only for MVP if needed.
  - JWT validation middleware on write endpoints (GPS, trip start/end, admin CRUD).

- [ ] **Role model**
  - Roles: `student`, `driver`, `admin`.
  - RLS or backend checks: only drivers post GPS for assigned bus; only admins manage routes/stops.

- [ ] **Driver assignment**
  - Link user → bus (and optional default route).
  - Driver portal shows assigned bus before sending GPS.

---

### P3 — Live tracking UX

- [ ] **Polling or realtime bus updates**
  - MVP option A: frontend polls `/api/buses` every 10–15s.
  - MVP option B: WebSocket or Supabase Realtime channel for `gps_locations` inserts.
  - Map markers move without full page reload.

- [ ] **Route geometry from ordered stops**
  - Store stop order per route; build polyline from stop coordinates.
  - Optional: Google Routes API for road-following path (Phase 1 enhancement).

- [ ] **ETA on map**
  - Show ETA per bus to next stop (and optionally all stops on route).
  - Use fixed Distance Matrix contract from P0; cache ETAs briefly to limit API cost.

- [ ] **Stop arrival detection (basic)**
  - Geofence radius per stop; when bus enters fence, record `stop_arrivals` row.
  - No notifications required for MVP — DB record is enough.

---

### P4 — Driver portal (mobile-friendly web)

- [ ] **Driver UI page**
  - Login, see assigned bus/route, start/end trip buttons.
  - Request geolocation permission; send GPS every 10–30s while trip active.
  - Show connection/status indicator (last upload time).

- [ ] **Background-friendly GPS upload**
  - Use `navigator.geolocation.watchPosition` with sensible throttle.
  - Retry on network failure; queue last N points client-side if offline (optional stretch).

---

### P5 — Admin essentials

- [ ] **Admin CRUD (minimal)**
  - Manage routes, stops (name + lat/lng or geocode), bus records, driver ↔ bus assignment.
  - Simple form UI or Supabase dashboard for MVP if UI is deferred.

- [ ] **Live fleet view**
  - Reuse student map with admin-only extras: all buses, trip status, last GPS time.

---

### P6 — Data collection for future ML (MVP hooks only)

- [ ] **Log Google ETA baseline**
  - When computing ETA, store `google_predicted_eta` on GPS or stop_arrival rows for later model comparison.

- [ ] **Historical GPS retention**
  - Partition or index `gps_locations` by time; no ML pipeline required yet.

---

## MVP definition of done

The MVP is complete when all of the following are true:

1. **Student map:** Loads AAU-centered map with routes, stops, and live bus markers that update without refresh.
2. **ETA:** At least one stop shows a working ETA per bus (Distance Matrix or equivalent).
3. **Driver flow:** Driver logs in, starts a trip, phone GPS flows to backend and appears on the map within ~30s.
4. **Persistence:** Buses, stops, routes, trips, and GPS history survive server restart (database, not `back_fill.py`).
5. **Auth:** Write operations require authenticated driver/admin; read map can remain public if product decision allows.
6. **Stability:** No known P0 bugs; API contracts match frontend; repeated API calls do not duplicate in-memory data.

---

## Suggested implementation order

```
P0 fixes → P1 database + GPS ingest → P3 polling/realtime → P4 driver portal
         → P2 auth (can parallel with P4) → P5 admin CRUD → P6 baseline logging
```

---

## File touch map (quick reference)

| MVP work | Primary files |
|----------|----------------|
| API fixes | `src/geo_map/route.py`, `src/geo_map/services/*.py` |
| Frontend map | `static/index.js`, `templates/index.html` |
| Config / deps | `src/utils/config.py`, `requirements.txt`, `.env` |
| New DB layer | `src/db/` (to create), migrations |
| Driver UI | `templates/driver.html`, `static/driver.js` (to create) |
| Auth | `src/auth/` (to create), middleware in `main.py` |

---

## Change log

| Date | Note |
|------|------|
| 2026-05-20 | Initial MVP backlog from codebase + Phase 1 scope |
