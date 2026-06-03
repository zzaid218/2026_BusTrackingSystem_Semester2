# AI/ML MVP features

This document defines the minimum AI/ML scope for the AAU bus tracking system, validated against `BusTracking System Documentation.md`.

It covers only student-developed intelligence: ETA prediction, model evaluation, anomaly detection, delay classification, and BusBot. Platform work such as Supabase setup, authentication, driver GPS upload, map rendering, and admin CRUD is required by the full product, but is not counted as AI/ML MVP work here.

---

## Validation Against Main Documentation

The main documentation defines four AI model areas plus BusBot:

- ETA Prediction Model
- Delay Classification Model
- Route Efficiency Scoring
- Anomaly Detection System
- BusBot conversational assistant

For MVP, the safest interpretation is:

- **Must-have:** ETA prediction pipeline, Google baseline comparison, reproducible training, model inference API.
- **Should-have:** Basic anomaly detection because it can start with rules plus lightweight ML.
- **Should-have after labels exist:** Delay classification, because it needs labeled delay data.
- **Thin MVP only:** BusBot, limited to grounded ETA/location/route answers.
- **Stretch:** Route efficiency scoring, because it needs enough historical trips and admin analytics context.

This matches the project plan: Phase 1 collects data and uses Google as a baseline; Phase 2 introduces custom ML models once enough AAU data exists.

---

## Google Bootstrap To AAU Models Strategy

The AI/ML path is a controlled migration, not an immediate replacement of Google Maps.

| Phase | Source of prediction | Purpose |
|-------|----------------------|---------|
| Phase 1 - Bootstrap | Google Distance Matrix / Routes API | Provide working ETA/routing, collect baseline predictions, and store training labels |
| Phase 2 - Model validation | Google + AAU ML model | Train on AAU history, compare ML ETA against Google ETA and actual arrivals |
| Phase 3 - Model primary | AAU ML model with Google fallback | Use the custom model when metrics are reliable; call Google when data is missing or confidence is low |

Google results must be stored with operational data:

- GPS location at prediction time
- route and target stop
- Google ETA and distance
- actual arrival time once known
- ML ETA and model version once the model exists
- Google error and ML error after trip completion

Promotion from Google-first to ML-first should happen per route, not globally. A route can use ML as the primary ETA source when it has enough completed trips, valid feature coverage, and model MAE at or below the accepted threshold. Until then, Google remains the source of truth and training baseline.

---

## AI/ML MVP Goal

Build a first AAU-owned intelligence layer that can:

1. Use Google Maps results first to collect ETA, distance, and arrival-comparison data.
2. Train an AAU ETA model from that collected history.
3. Compare ML ETA against Google ETA and actual arrivals before switching traffic to ML.
4. Detect obvious anomalies like off-route buses, GPS silence, and unusually long stops.
5. Classify delay causes when enough labeled examples exist.
6. Let BusBot answer basic student questions from real system data.

The MVP is not expected to fully beat Google on day one. It must create the measurement and migration pipeline that makes replacing Google prediction logic realistic.

---

## Current AI Baseline In Repo

| Area | Current status | Notes |
|------|----------------|-------|
| Custom ML models | Not started | No `src/ml/` package yet |
| ETA | Google bootstrap only | `src/geo_map/services/distance.py` calls Distance Matrix and should become the baseline collector |
| Feature engineering | Not started | `src/geo_map/query.py` is empty |
| Model training | Not started | No training scripts or datasets |
| Model inference | Not started | No `/api/ml/*` endpoints |
| Google baseline logging | Not started | No `prediction_comparisons` storage |
| Delay classification | Not started | Needs labeled delay data |
| Anomaly detection | Not started | Can begin with rules before model training |
| BusBot | Not started | No LLM integration |

Google Maps is the bootstrap baseline and fallback. The AI/ML MVP should capture Google predictions as training/evaluation data, then gradually replace them with AAU models when route-level metrics prove the model is reliable.

---

## Data Required From The Platform

These are prerequisites provided by the non-AI backend. They are not AI tasks, but AI work cannot be validated without them.

- `gps_locations`: bus ID, route ID, timestamp, lat/lng, speed, heading, GPS accuracy.
- `trips`: bus, route, driver, planned/actual departure, planned/actual arrival, trip status.
- `stops`: stop name, coordinates, geofence radius, campus zone, route order.
- `stop_arrivals`: trip, stop, scheduled time, actual time, dwell time.
- `prediction_comparisons`: Google ETA, ML ETA, actual arrival, errors, model version.

If real data is not available yet, build the pipeline with seeded or simulated trips, but mark model metrics as development-only.

---

## Frontend And Backend Dependency Sorting

Use this order so AI/ML work can move in parallel with the frontend and backend teams without blocking them on models that are not trained yet.

| Order | Work lane | Can start now? | Depends on | Output for other teams |
|-------|-----------|----------------|------------|------------------------|
| 1 | Shared AI input/output schemas | Yes | Current repo only | Frontend/backend/AI can start independently from stable contracts |
| 2 | Google baseline contract | Yes | Existing Google ETA service shape | Backend knows what to store: Google ETA, distance, stop, route, timestamp |
| 3 | Synthetic/seed dataset pipeline | Yes | Example GPS/trip/stop rows | AI team can build training/evaluation code before backend has live data |
| 4 | ETA API contract | Yes | Agreed request/response schema | Frontend can render ETA using `source: google`, `source: ml`, or `source: fallback` |
| 5 | Feature engineering v1 | Yes, with fixture data | Backend field names for GPS/trips/stops | AI can reuse same fields backend will later store |
| 6 | ETA baseline model | Yes, with synthetic/seed data | Dataset export format | Backend can expose mocked ML ETA before production model is ready |
| 7 | Anomaly event contract | Yes | Active trip + GPS update fields | Frontend can build anomaly/admin UI from mocked anomaly events |
| 8 | BusBot intent/API contract | Yes | ETA/location/route API contracts | Frontend can build chat UI before LLM/model integration is complete |
| 9 | ETA production training | Later | Real completed trips + stop arrivals | Backend switches `auto` mode to ML only when route metrics pass |
| 10 | Delay label workflow/spec | Yes | Agreed delay classes | Backend/admin UI knows what labels to collect |
| 11 | Delay classifier training | Later | Enough labeled delayed trips | Frontend/backend can display delay reason once model exists |
| 12 | Route efficiency scoring | Wait | Historical trips and analytics needs | Frontend can add route score after enough history exists |

Frontend/backend integration rules:

- First work item is defining shared input/output schemas. Frontend can mock them, backend can expose them, and AI can train/infer against them.
- Frontend should not wait for trained ML. It can render mocked ETA, anomaly, delay, and BusBot outputs using the agreed schemas.
- Backend should not wait for trained ML. It should first store Google prediction rows and expose stable input/output fields.
- ETA responses should always include `source`, so frontend can display Google ETA now and ML ETA later without UI rewrites.
- Delay and route-efficiency models should not block map, GPS, route, stop, or ETA API work.
- BusBot UI can start with route/location/Google ETA answers, then add ML ETA and delay explanations later.

---

## External Services For AI/ML MVP

| Service | MVP role |
|---------|----------|
| Google Distance Matrix / Routes API | ETA baseline and fallback |
| LLM API | BusBot natural-language response generation |
| Weather API | Optional feature source for ETA/delay models |

Local ML stack:

- `pandas`, `numpy` for data processing
- `scikit-learn` for baseline models, anomaly detection, metrics
- `xgboost` for ETA and delay models when dataset is ready
- `joblib` for model serialization
- `mlflow` optional for experiment tracking; do not block MVP on it

Post-MVP:

- TensorFlow/Keras LSTM models
- full ETA ensemble
- online learning
- automated retraining and drift detection
- A/B testing

---

## P0 - AI Data And Evaluation Foundation

This is the first AI milestone. It proves that Google-generated ETA data can be captured, joined with actual arrivals, and converted into training/evaluation data for AAU models.

- [ ] **Define shared input/output schemas first**
  - This is the first task before backend, frontend, or AI model work.
  - Define `ETAInput` and `ETAOutput`.
  - Define `AnomalyInput` and `AnomalyOutput`.
  - Define `DelayInput` and `DelayOutput`.
  - Define `BusBotInput` and `BusBotOutput`.
  - Keep fields stable so frontend can build mocks, backend can expose endpoints, and AI can implement models independently.
  - ETA output must include `source` with values like `google`, `ml`, or `fallback`.

- [ ] **Create AI package structure**
  - Add `src/ml/features/`
  - Add `src/ml/training/`
  - Add `src/ml/inference/`
  - Add `src/ml/evaluation/`
  - Add `src/ml/schemas.py` for shared input/output models

- [ ] **Define model artifact convention**
  - Store trained artifacts outside source control under `models/`
  - Each model has `model.joblib`, `metrics.json`, and `metadata.json`
  - Metadata includes model type, version, training date, training row count, feature list

- [ ] **Build training dataset export**
  - Input tables: trips, GPS locations, stops, stop arrivals, routes, prediction comparisons
  - Output one row per prediction target, normally `(trip_id, stop_id, timestamp)`
  - Label: seconds/minutes until actual stop arrival
  - Include Google ETA and Google distance as baseline columns, not as labels
  - Export to CSV or Parquet

- [ ] **Build feature engineering v1**
  - Current bus location and speed
  - Distance to target stop
  - Route ID and stop order
  - Number of stops remaining
  - Time of day and day of week
  - Time since trip started
  - Last stop dwell time if available
  - Historical mean travel time for route segment if enough data exists

- [ ] **Add Google baseline comparison**
  - Store Google ETA at prediction time
  - Store Google distance and route/stop context used for the prediction
  - Store actual arrival after trip completion
  - Compute Google error and ML error on the same rows
  - Required metrics: MAE, RMSE, 90th percentile absolute error

Acceptance criteria:

- A dataset can be exported with labels.
- A metrics script can compare any ETA prediction column against actual arrival.
- Google baseline metrics can be produced before the custom model is trained.
- The same dataset can later be reused to train and evaluate AAU ETA models.

---

## P1 - ETA Prediction Model MVP

This is the core AI MVP feature and the strongest match to the main documentation. The model should not replace Google immediately; it should first run in evaluation mode against Google and actual arrivals.

Target:

- First realistic target: MAE under 3 minutes on held-out AAU trips.
- Stretch target after enough data: outperform Google baseline on AAU-specific routes/times.

- [ ] **Baseline ETA model**
  - Start with linear regression or random forest regressor.
  - Use a time-based train/validation/test split to avoid leakage.
  - Train only on completed trips with actual arrival labels.
  - Save metrics and artifact.

- [ ] **Primary ETA model**
  - Train XGBoost regressor for short-term ETA, especially next 1-2 stops.
  - Tune basic hyperparameters: max depth, learning rate, n estimators.
  - Keep feature list simple and explainable.

- [ ] **Evaluation report**
  - Overall MAE, RMSE, 90th percentile error.
  - Breakdown by route.
  - Breakdown by hour of day.
  - Comparison against Google on the same test rows.
  - Recommendation per route: keep Google primary, run ML shadow mode, or promote ML primary.

- [ ] **Inference API**
  - Add `POST /api/ml/eta` or `GET /api/ml/eta`.
  - Input: bus ID or current bus location, route ID, target stop ID.
  - Output: ETA seconds, confidence, model version, source.
  - Support fallback source: `ml`, `google`, or `auto`.
  - In `auto` mode, return the source actually used so clients know whether ETA came from Google or AAU ML.

- [ ] **Promotion and fallback rule**
  - Use ML only if route has enough completed trips and current features are valid.
  - Promote ML to primary only when route-level validation meets the accepted MAE threshold.
  - Fall back to Google when model confidence is low or data is missing.

Out of MVP:

- LSTM route-sequence model.
- Weighted XGBoost/LSTM/linear ensemble.
- Weekly automatic retraining.
- A/B testing.

---

## P2 - Basic Anomaly Detection MVP

This is useful early because it can start with rules before enough training data exists.

Anomaly types:

| Type | MVP detection method |
|------|----------------------|
| Off-route | Distance from planned route exceeds threshold |
| GPS silence | No update for active bus after configured timeout |
| Long stop | Dwell time exceeds historical or configured threshold |
| Speed anomaly | Speed outside expected range for route segment |

- [ ] **Rule-based detector first**
  - Off-route threshold, e.g. 100 meters from route geometry.
  - GPS silence threshold, e.g. 2-5 minutes depending on update interval.
  - Long stop threshold, e.g. stop dwell time greater than expected.

- [ ] **ML detector after history exists**
  - Train Isolation Forest on normal trip feature vectors.
  - Features: distance from route, speed delta, dwell time, GPS update gap.

- [ ] **Anomaly API**
  - `GET /api/ml/anomalies?active=true`
  - Return active anomaly list with bus ID, trip ID, type, severity, timestamp.

- [ ] **Anomaly log**
  - Persist anomaly events for later review and model improvement.

Out of MVP:

- Autoencoder detector.
- Ensemble anomaly voting.
- Push notifications.
- False-positive feedback loop.

---

## P3 - Delay Classification MVP

This should start after there are enough completed trips and labeled delays.

Classes from the main documentation:

- `traffic`
- `mechanical`
- `driver`
- `weather`
- `campus_event`
- `unknown`

- [ ] **Create label workflow**
  - Admin or operator can label delayed trips.
  - Store label, notes, and reviewer.
  - Allow `unknown` when cause is unclear.

- [ ] **Weak-label bootstrap**
  - Late departure can suggest `driver`.
  - Long low-speed segment can suggest `traffic`.
  - Bad weather can suggest `weather`.
  - No rule should overwrite a human label.

- [ ] **Feature set v1**
  - Scheduled vs actual departure delay.
  - Total stopped time during trip.
  - Speed pattern by segment.
  - Weather severity if available.
  - Recent same-route delay frequency.
  - Driver punctuality rolling average if available.

- [ ] **Model**
  - Start with logistic regression or random forest.
  - Use XGBoost if dataset is large enough.
  - Report accuracy, precision, recall, and confusion matrix.

- [ ] **Inference API**
  - `GET /api/ml/delay/{trip_id}`
  - Return predicted class, probabilities, model version, top contributing features if available.

Acceptance target:

- Development target: at least 75-80% accuracy on labeled validation set.
- Full-plan stretch: 83%+ accuracy after enough labels.

Out of MVP:

- Active learning.
- Maintenance-record integration.
- Automatic student delay notifications.

---

## P4 - BusBot AI MVP

BusBot should be grounded in system data. It should not invent schedules, locations, or delay reasons.

Supported intents:

- `eta_query`: "When will bus 3 reach the main gate?"
- `location_query`: "Where is bus 3?"
- `delay_query`: "Why is my bus late?"
- `route_info`: "Which stops are on this route?"
- `help`: explain supported questions

- [ ] **Intent and entity extraction**
  - Extract bus ID, route name, stop name, and time reference.
  - Use regex/simple parser first; use LLM structured output only where needed.

- [ ] **Grounding layer**
  - Query live bus location.
  - Query ML ETA or Google fallback ETA.
  - Query delay classifier if available.
  - Query route and stop data.

- [ ] **LLM response layer**
  - Provide only retrieved facts to the LLM.
  - System prompt restricts the assistant to AAU bus tracking.
  - Return fallback message when data is missing.

- [ ] **BusBot API**
  - `POST /api/busbot/chat`
  - Request: message and optional session ID.
  - Response: reply, intent, resolved entities, data sources.

- [ ] **Safety**
  - Do not expose driver personal data.
  - Rate limit requests.
  - Reject off-topic prompts.
  - Cache common read-only answers with short TTL.

Out of MVP:

- Full multi-turn route planning.
- Voice interface.
- Long-term conversation memory.
- Advanced analytics questions.

---

## P5 - Route Efficiency Scoring Stretch

The main documentation includes route efficiency scoring, but it depends on enough historical trips and analytics needs. Treat this as stretch, not core AI MVP.

- [ ] Compute schedule adherence score.
- [ ] Compute travel-time variance score.
- [ ] Compute delay-frequency score.
- [ ] Combine into route score from 0 to 100.
- [ ] Expose `GET /api/ml/routes/{route_id}/efficiency`.

Out of MVP:

- Optimization recommendations.
- Simulation of alternate schedules.
- Multi-objective route optimization.

---

## AI/ML MVP Definition Of Done

The AI/ML MVP is done when:

1. ETA training data can be exported reproducibly.
2. Google ETA baseline is logged and evaluated against actual arrivals.
3. ETA model v1 is trained, evaluated, versioned, and callable through an API.
4. ETA API can fall back to Google when ML is not reliable.
5. Basic anomaly detection flags off-route and GPS-silence cases.
6. Delay classifier has a label workflow and either a trained v1 model or documented blocker due to lack of labels.
7. BusBot answers ETA, location, route, and delay questions from retrieved backend data.
8. Metrics are documented so the team can compare Google vs custom AI over time.

---

## Recommended Implementation Order

```text
Now, no platform blocker:
  P0 shared input/output schemas
  -> metrics + synthetic dataset
  -> Google baseline storage contract
  -> ETA request/response contract for backend and frontend
  -> anomaly event contract for backend and frontend
  -> BusBot intent/entity contract for chat UI

When backend starts storing real trips:
  Google baseline evaluation
  -> ETA training on completed trips
  -> ETA shadow mode against Google
  -> route-level ML promotion decision

When labels/history exist:
  delay classifier training
  -> BusBot delay answers
  -> route efficiency scoring
```

Reasoning:

- Shared input/output schemas come first so frontend, backend, and AI can work in parallel without waiting on trained models.
- Metrics, fixtures, and contracts unblock frontend/backend immediately after schemas are agreed.
- ETA is the highest-value AI feature and has the clearest metric, but production training needs completed trips.
- Anomaly detection can start with rules and does not require many labels.
- Delay classification depends on labeled delay examples, so only its label contract should start early.
- BusBot can start with route/location/Google ETA answers, then consume ML ETA and delay outputs as they become available.
- Route efficiency needs historical data, so it comes last.

---

## Suggested File Structure

| Work | Suggested location |
|------|--------------------|
| Feature engineering | `src/ml/features/` |
| Training scripts | `src/ml/training/train_eta.py`, `train_delay.py`, `train_anomaly.py` |
| Evaluation | `src/ml/evaluation/metrics.py` |
| Inference services | `src/ml/inference/` |
| API router | `src/ml/router.py` |
| Schemas | `src/ml/schemas.py` |
| BusBot | `src/ml/busbot/` |
| Model artifacts | `models/` (gitignored) |
| Reports | `docs/ml/` |

---

## Explicitly Not Included In AI/ML MVP

- Supabase setup and migrations.
- Driver app and GPS upload implementation.
- Auth and role-based access.
- Student/admin dashboard UI.
- General map bug fixes.
- Push notifications.
- Full analytics dashboard.
- Deep learning LSTM ETA model.
- Full ensemble model.
- Automated retraining and drift detection.
- Production A/B testing.

---

## Change Log

| Date | Note |
|------|------|
| 2026-05-20 | Validated against main documentation and refocused on AI/ML MVP only |
