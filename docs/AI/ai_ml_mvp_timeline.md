# AI/ML MVP timeline

This timeline is based on `docs/ai_ml_mvp_features.md`. It covers AI/ML work only.

---

## Timeline Summary

| Stage | Time | Goal | Main output |
|-------|------|------|-------------|
| 0 | Week 1 | Define shared AI schemas | Stable AI input/output contracts |
| 1 | Week 1-2 | Define Google baseline data shape | Fields needed to compare Google vs ML later |
| 2 | Week 2-3 | Build fixture data and examples | Mockable AI inputs/outputs for development |
| 3 | Week 3-4 | Build data and metrics pipeline | Training dataset format and ETA metrics |
| 4 | Week 4-6 | Train ETA model v1 | ETA model artifact and evaluation report |
| 5 | Week 6-7 | Add anomaly detection v1 | Rule-based off-route/GPS-silence detection |
| 6 | Week 7-8 | Add BusBot MVP logic | Grounded intent/entity pipeline |
| 7 | After labels exist | Train delay classifier | Delay reason model and metrics |
| 8 | After history exists | Add route efficiency scoring | 0-100 route score prototype |

---

## Stage 0 - Shared AI Schemas First

**Time:** Week 1  
**Status:** Start immediately  
**Why first:** AI work needs stable input/output contracts before training, inference, fixtures, or evaluation.

### Tasks

- Define `ETAInput` and `ETAOutput`.
- Define `AnomalyInput` and `AnomalyOutput`.
- Define `DelayInput` and `DelayOutput`.
- Define `BusBotInput` and `BusBotOutput`.
- Define shared enum values:
  - source: `google`, `ml`, `fallback`
  - delay_class: `traffic`, `mechanical`, `driver`, `weather`, `campus_event`, `unknown`
  - anomaly_type: `off_route`, `gps_silence`, `long_stop`, `speed_anomaly`
- Create JSON examples for each input/output schema.

### Done when

- AI schemas are documented.
- Example JSON exists for ETA, anomaly, delay, and BusBot flows.
- Later model code can use the same fields without changing contracts.

---

## Stage 1 - Google Baseline Data Shape

**Time:** Week 1-2  
**Status:** Start after schemas

### Goal

Define what Google Maps output must be captured so AAU models can be trained and evaluated later.

### Tasks

- Define `prediction_comparisons` fields:
  - `trip_id`
  - `bus_id`
  - `route_id`
  - `stop_id`
  - `prediction_timestamp`
  - `bus_location`
  - `google_eta_seconds`
  - `google_distance_meters`
  - `ml_eta_seconds`
  - `model_version`
  - `actual_arrival_timestamp`
  - `google_error_seconds`
  - `ml_error_seconds`
- Define which fields are required before model training.
- Define which fields can stay null until actual arrival or ML prediction exists.
- Define Google-vs-ML comparison metrics:
  - MAE
  - RMSE
  - 90th percentile absolute error

### Done when

- Google baseline data shape is clear.
- ETA comparison rows can be validated even before the ML model exists.

---

## Stage 2 - Fixture Data And Examples

**Time:** Week 2-3  
**Status:** Can start before real trip data exists

### Tasks

- Create synthetic sample rows for:
  - trips
  - GPS locations
  - stops
  - stop arrivals
  - prediction comparisons
- Create fixture examples for:
  - Google ETA output
  - ML ETA output
  - fallback ETA output
  - anomaly output
  - delay output
  - BusBot output
- Mark fixture metrics as development-only.

### Done when

- AI logic can be developed without live data.
- Training/evaluation scripts have a small dataset to run against.

---

## Stage 3 - Data And Metrics Pipeline

**Time:** Week 3-4  
**Status:** Can start with fixture data

### Tasks

- Build dataset export format.
- Build feature engineering v1:
  - current bus location
  - current speed
  - distance to target stop
  - route ID
  - stop order
  - stops remaining
  - time of day
  - day of week
  - trip elapsed time
- Build ETA metrics script.
- Support both fixture data and future real data.

### Done when

- ETA dataset can be generated.
- Metrics can compare `google_eta_seconds`, `ml_eta_seconds`, and actual arrival.
- The same pipeline can later run on real collected data.

---

## Stage 4 - ETA Model V1

**Time:** Week 4-6  
**Status:** Starts with fixture data; real validation needs completed trips

### Tasks

- Train a baseline model:
  - linear regression or random forest
- Train primary model if enough data exists:
  - XGBoost regressor
- Compare ML ETA vs Google ETA vs actual arrival.
- Produce route-level recommendation:
  - keep Google primary
  - run ML shadow mode
  - promote ML primary
- Save model artifact and metrics.

### Done when

- ETA model artifact exists.
- ETA metrics report exists.
- Model output matches `ETAOutput`.
- Promotion decision is based on route-level metrics, not assumptions.

---

## Stage 5 - Basic Anomaly Detection

**Time:** Week 6-7  
**Status:** Can start before heavy ML

### Tasks

- Define rule-based detectors:
  - off-route
  - GPS silence
  - long stop
  - speed anomaly
- Define severity levels:
  - low
  - medium
  - critical
- Create anomaly fixture examples.
- Add Isolation Forest later when enough normal trip history exists.

### Done when

- Anomaly output matches `AnomalyOutput`.
- Off-route and GPS-silence examples can be detected from fixture data.

---

## Stage 6 - BusBot MVP Logic

**Time:** Week 7-8  
**Status:** Can start with fixture data and mocked retrieval context

### Tasks

- Define supported intents:
  - ETA query
  - location query
  - route info
  - delay query
  - help
- Define entity extraction:
  - bus ID
  - route name
  - stop name
  - time reference
- Define grounded context format.
- Define fallback answers for missing data.
- Ensure BusBot does not invent schedules, locations, or delay reasons.

### Done when

- BusBot output matches `BusBotOutput`.
- Intent/entity logic works on sample messages.
- Replies are generated only from supplied context.

---

## Stage 7 - Delay Classifier

**Time:** After enough labeled delayed trips exist  
**Status:** Do not block ETA work on this

### Tasks

- Finalize delay classes:
  - traffic
  - mechanical
  - driver
  - weather
  - campus_event
  - unknown
- Define label format.
- Train classifier after enough labels exist.
- Report:
  - accuracy
  - precision
  - recall
  - confusion matrix
- Output class, probabilities, and model version.

### Done when

- Delay classifier returns valid `DelayOutput`.
- Metrics are documented.
- Missing label data is documented as a blocker if training cannot happen yet.

---

## Stage 8 - Route Efficiency Scoring

**Time:** After enough historical trips exist  
**Status:** Stretch

### Tasks

- Compute schedule adherence score.
- Compute travel-time variance score.
- Compute delay-frequency score.
- Combine into route score from 0 to 100.
- Provide basic explanation for each score.

### Done when

- A route has a 0-100 score.
- Score inputs and formula are documented.

---

## Critical Path

```text
AI schemas
  -> Google baseline data shape
  -> fixture dataset
  -> metrics pipeline
  -> ETA model shadow evaluation
  -> route-level ML promotion
```

Delay classification, BusBot delay explanations, and route efficiency should not block the core ETA migration.

---

## External Dependencies

These are not AI tasks, but AI needs them later for real validation:

- completed trips
- GPS history
- stop arrivals
- Google ETA and distance logs
- labeled delay examples
- route geometry

---

## Change Log

| Date | Note |
|------|------|
| 2026-05-20 | Revised timeline to keep AI/ML tasks only |
