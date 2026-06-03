# System component requirements

This file uses the image as structure and `BusTracking System Documentation.md` as explanation source.

---

## Database

Database is the system memory. It stores operational data, historical GPS data, and model-training data owned by AAU.

### Users

**Requirement:** Store students, drivers, admins, roles, credentials, and access status.

**Use:** Authentication and role checks use this data so students, drivers, and admins only access their allowed features.

### Routes

**Requirement:** Store route name, ordered stops, route geometry, schedule template, and route version/history.

**Use:** Backend uses routes to draw map paths, assign buses, detect route deviation, and calculate ETA to upcoming stops.

### Stops

**Requirement:** Store stop name, coordinates, geofence radius, campus zone, and stop order inside routes.

**Use:** Frontend displays stops. Backend uses stops for ETA, arrival detection, notifications, and stop-arrival records.

### Trips

**Requirement:** Store bus, route, driver, planned/actual departure, planned/actual arrival, and trip status.

**Use:** Backend tracks active bus operation. Dashboards use trips for live monitoring and historical reports.

### GPS Locations

**Requirement:** Store bus ID, route ID, timestamp, coordinates, speed, heading, GPS accuracy, and metadata.

**Use:** Live map uses latest location. ML and analytics use historical traces for ETA, anomalies, and route performance.

### Stop Arrivals

**Requirement:** Store trip, stop, scheduled time, actual time, dwell time, and Google/model predicted ETA.

**Use:** Measures delays and ETA accuracy. Feeds model training and analytics.

---

## External APIs

External APIs provide bootstrap capability before AAU-owned models are ready.

### Google Maps API

**Requirement:** Maps JavaScript API, Routes API, Distance Matrix API, and optional Roads API with API key and quota control.

**Use:** Displays map, calculates early ETAs/routes, geocodes places, and provides baseline predictions for model comparison.

### Weather API

**Requirement:** Current weather by location/time and stable provider access.

**Use:** Adds weather context to trip records. Delay and ETA models use it as feature.

### LLM API

**Requirement:** LLM provider access, prompt control, rate limits, content filtering, and system-data grounding.

**Use:** BusBot converts student questions into useful bus answers using backend data.

---

## Configuration & Data

This layer keeps shared configuration, schemas, and database changes organized.

### Configuration Handler

**Requirement:** Load API keys, environment variables, service URLs, cost limits, and runtime settings.

**Use:** Backend services read one configuration source instead of hardcoded values.

### Data Models

**Requirement:** Define shared structures for buses, stops, routes, trips, GPS updates, ETAs, alerts, and users.

**Use:** Backend validates requests/responses. Frontend depends on same field names and meanings.

### Database Migrations

**Requirement:** Version database schema changes for users, routes, stops, trips, GPS data, stop arrivals, and ML tables.

**Use:** Team can evolve database safely as features expand.

---

## ML Models

ML models are the planned student AI contribution. They reduce Google dependency after enough AAU data exists.

### ETA Predictor

**Requirement:** Historical trips, GPS traces, stop arrivals, route distance, time/day patterns, weather, traffic, events, and driver behavior.

**Use:** Predicts bus arrival time for upcoming stops using AAU-specific patterns.

### Delay Classifier

**Requirement:** Labeled delay data, departure delay, stopped-time patterns, weather, traffic, event calendar, driver history, and maintenance context.

**Use:** Classifies delay cause such as traffic, mechanical issue, driver delay, weather, campus event, or unknown.

### Route Efficiency Scorer

**Requirement:** Trip duration, schedule adherence, delay frequency, dwell time, reliability variance, capacity/use data, and route cost signals.

**Use:** Scores routes so admins can compare performance and see which routes need review.

### Anomaly Detector

**Requirement:** Planned route geometry, normal GPS update frequency, expected speed ranges, normal dwell time, and route deviation history.

**Use:** Flags off-route buses, GPS silence, long stops, unusual speed, and other abnormal behavior.

---

## Backend

Backend is the system coordinator. It connects driver GPS, database, Google APIs, ML models, BusBot, and frontends.

### FastAPI Server

**Requirement:** API server with REST endpoints, validation, async request handling, docs, and production runtime.

**Use:** Main backend entry point for all portals and services.

### API Router

**Requirement:** Organized routes for buses, stops, routes, trips, geocoding, distance/ETA, auth, admin, and analytics.

**Use:** Frontends call router endpoints to read data or send updates.

### Authentication Service

**Requirement:** Login, token validation, user roles, driver/admin/student separation, and protected actions.

**Use:** Controls who can update locations, manage records, or view student-facing data.

### Bus Tracking Service

**Requirement:** Accept driver GPS updates, validate coordinates/timestamps, attach bus/driver/trip context, and store latest position.

**Use:** Powers live bus map and tracking history.

### Stop Arrival Service

**Requirement:** Use geofences, route order, active trip state, GPS location, and stop timing.

**Use:** Detects actual stop arrivals and records dwell time/delay.

### ETA Service

**Requirement:** Current bus location, route path, stop sequence, Google APIs in Phase 1, ML model in later phases.

**Use:** Gives students and dashboards estimated arrival times.

### Geocoding Service

**Requirement:** Convert address/stop name to coordinates and coordinates to formatted address.

**Use:** Supports stop setup, map display, and readable location info.

### Distance Matrix Service

**Requirement:** Origins, destinations, route distance, travel duration, and Google Distance Matrix/Routes access.

**Use:** Calculates travel time between bus and stops during bootstrap phase.

### Notification Service

**Requirement:** User preferences, selected stops/routes, bus approach events, delay events, and delivery channel.

**Use:** Alerts students when bus is near, delayed, or status changes.

### BusBot Service

**Requirement:** Intent extraction, entity extraction, LLM access, safety controls, and live system data access.

**Use:** Answers student questions like ETA, bus location, delay reason, and route info.

---

## Frontend

Frontend contains user-facing portals. Each portal shows different role-specific slice of the same transport system.

### Student Portal

**Requirement:** Live map, bus details, route/stops view, ETA display, favorite stops, notifications, route planner, and BusBot.

**Use:** Student checks bus location, arrival time, route details, and asks simple transport questions.

### Driver Portal

**Requirement:** Driver login, GPS permission, active bus/route assignment, passenger count, status updates, route deviation update, and end-trip action.

**Use:** Driver phone sends live GPS and operational state to backend.

### Admin Dashboard

**Requirement:** Live fleet map, bus/driver/student CRUD, route/schedule management, trip monitoring, alerts, system health, and analytics views.

**Use:** Admin manages transport operations and reviews performance.

---

## Main System Flow

1. Driver Portal sends GPS location and trip status.
2. Backend validates update and stores it in Database.
3. ETA/Distance services calculate arrival estimates.
4. Student Portal displays live buses, stops, routes, and ETAs.
5. Admin Dashboard monitors fleet and alerts.
6. Stored history feeds analytics and future ML models.
