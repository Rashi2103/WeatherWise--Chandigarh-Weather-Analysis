# WeatherWise — Chandigarh Weather & Disaster Awareness Explorer

**A Python + SQL science-outreach project** that helps learners explore historical daily temperature and rainfall observations, compare seasonal patterns, and inspect simple threshold flags.

> **Important data note:** This repository does not bundle invented observations or claim that a disaster was predicted. Run the fetch script to download actual historical observations from the Open-Meteo Historical Weather API. Threshold flags (daily maximum temperature ≥ 40°C; daily precipitation ≥ 50 mm) are illustrative screening rules for learning—not official warnings, climatological definitions, or validated risk predictions.

## Why this project?

This project extends the theme of my IEEE-published work, *“Real-Time Weather Data Analysis for Disaster Management and Response,”* by making weather data exploration interactive and student-friendly. It is designed to support science communication: learners can explore the data, ask questions, and understand the difference between an observed weather condition and a verified disaster event.

## Features

- Downloads historical daily maximum/minimum temperature and precipitation for Chandigarh.
- Cleans types, missing values, negative precipitation values, and duplicate dates.
- Stores the cleaned records in SQLite and includes example SQL queries.
- Visualizes temperature trends and monthly rainfall patterns.
- Flags days crossing transparent, user-defined thresholds for further investigation.
- Provides plain-language learning prompts and CSV export.
- Uses no API key; internet access is required to fetch data.

## Tech stack

Python, pandas, requests, SQLite, SQL, Matplotlib, Streamlit.

## Run locally

Python 3.10+ recommended.

```bash
# 1. Create and activate a virtual environment (optional but recommended)
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

# 2. Install packages
pip install -r requirements.txt

# 3. Fetch actual historical observations (requires internet)
python fetch_weather.py

# 4. Clean data and build SQLite database
python prepare_data.py

# 5. Launch the dashboard
streamlit run app.py
```

Open the local URL printed by Streamlit. If the archive API is temporarily unavailable, retry later; this repository intentionally does not substitute fabricated data for observations.

## Data source and attribution

Data is retrieved from the [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api), using coordinates for Chandigarh (30.7333° N, 76.7794° E). The default period is 1 January 2019 through 31 December 2025. API availability and permitted redistribution/attribution can change; review Open-Meteo's current terms before publishing a downloaded dataset. The script saves the returned data to `data/chandigarh_weather.csv`.

## SQL examples

See [`sql/analysis_queries.sql`](sql/analysis_queries.sql) for annual summaries, month-wise rainfall, threshold flags, and a duplicate-date quality check.

## Interpretation and limitations

- A threshold flag is a screening rule, not a forecast or official alert.
- This project does not infer that a flood, heatwave, or disaster happened; that requires independent event records and validated definitions.
- Historical patterns are descriptive. They do not establish causation or guarantee future conditions.
- The default analysis covers one location. Spatial comparisons, official weather warnings, and evaluation against event data are future work.

## Future improvements

1. Add official IMD alerts and verified historical event records with clear citations.
2. Compare multiple locations and evaluate seasonal differences.
3. Add data-quality tests and automated refresh scheduling.
4. Co-design short classroom activities and a glossary with teachers/students.
5. Only after collecting suitable labelled data, evaluate a baseline model using time-aware validation and publish precision/recall with limitations.

## Portfolio note

This is a compact learning prototype, not a production disaster-management system. Explain which parts you implemented yourself and be ready to discuss data cleaning, SQL queries, charts, thresholds, and limitations.
