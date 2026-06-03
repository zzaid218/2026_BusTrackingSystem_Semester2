# Project File Structure

Current workspace snapshot as of 2026-06-03.

```text
.
├── .env
├── .git/
├── .gitignore
├── Makefile
├── __pycache__/
├── docs/
│   ├── BusTracking System Documentation.md
│   ├── ai_ml_mvp_features.md
│   ├── ai_ml_mvp_timeline.md
│   ├── current_state_of_the_project.md
│   ├── mvp_features.md
│   ├── system_component_requirements.md
│   └── system_componetens.png
├── main.py
├── requirements.txt
├── src/
│   ├── geo_map/
│   │   ├── __pycache__/
│   │   ├── model.py
│   │   ├── query.py
│   │   ├── route.py
│   │   └── services/
│   │       ├── __pycache__/
│   │       ├── buses.py
│   │       ├── directions.py
│   │       ├── distance.py
│   │       ├── geocoding.py
│   │       └── stops.py
│   ├── helpers/
│   │   ├── __pycache__/
│   │   └── back_fill.py
│   └── utils/
│       ├── __pycache__/
│       └── config.py
├── static/
│   ├── index.js
│   └── style.css
├── templates/
│   └── index.html
└── venv/
```

This file reflects the project as it exists now, including local environment and generated folders that are present in the workspace.