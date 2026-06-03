# Schema design rationale

Schema lives at `src/geo_map/database/schema`.

---

## Why this schema exists

Project needs two things at once: run working demo now, collect real data for ML later. Schema serves both without over-engineering either.

---

## Core tables

### Route, Bus, Stop

Direct mirror of current in-memory demo data. Route is anchor. Bus and Stop hang off it. Stop carries order on route and geofence radius — both needed later to detect arrivals automatically without manual input.

### Trip

Single run of bus on route. Holds planned times alongside actual times. Gap between planned and actual is the delay signal. Without trip as unit of measurement, no before/after comparison exists. Every ML label traces back to a trip.

### GPSLocation

Raw ping log. One row per GPS reading from bus. Stores speed and heading alongside position. Speed and heading are features for ETA model — not decorative. Tied to both bus and trip so data can be queried from either direction.

### StopArrival

When bus actually reached each stop during a trip. This is the ground truth. Distance Matrix gives a prediction. StopArrival gives what actually happened. Difference between the two is the training label.

---

## Google bootstrap tables

These three tables exist specifically to survive on Google APIs now and graduate to ML later without a data migration.

### GeocodingCache

Current code geocodes same stop names repeatedly on every request — known bug. Cache table fixes this. One row per unique query. All fields prefixed `google_` because every value in this table comes directly from Google's response. If geocoding provider changes later, prefix makes origin unambiguous.

### DistanceMatrixLog

One row per Distance Matrix API call. Saves everything Google returned plus the request context — bus position, speed, target stop. `actual_arrival` column starts null and gets filled when bus reaches the stop. `google_error_seconds` gets computed at that point. This table is the raw collection bucket. Nothing is thrown away at request time.

All Google-sourced fields carry `google_` prefix. Fields without the prefix — bus position, speed, trip context — are system-generated, not from Google.

### PredictionComparison

Cleaned join of DistanceMatrixLog and StopArrival built after each trip completes. One row = one labeled training example. Has features on left side, label on right. When ML work starts this table gets exported directly to CSV or Parquet. No transformation needed, no schema change needed.

Purpose of separating this from DistanceMatrixLog: log table is append-only raw capture, comparison table is analysis-ready. Keeps raw data clean and export logic simple.

---

## Why google_ prefix matters

Two data sources live in same tables: Google API responses and system-generated values. Without prefix, ambiguity grows as tables gain columns. Prefix makes auditing API usage, estimating costs, and switching providers straightforward.

---

## ML readiness without ML code

No model exists yet. Schema does not pretend otherwise. ML columns like `google_error_seconds` and `stops_remaining` are collected now because they cost nothing to store and are impossible to reconstruct retroactively. By the time model training starts, months of labeled examples already exist in PredictionComparison.

Schema makes this transition zero-cost: same tables, no migration, export and train.