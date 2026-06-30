# MLB HR / HRR Prospects Analyzer

This repository is a starter scaffold for the HR/HRR prospects analyzer you requested. It includes:

- Docker Compose with Postgres and pgAdmin
- Basic DB schema (db/schema.sql)
- Ingest scripts (statcast, season stats, lineups/injuries, weather)
- A scoring engine (score/score_engine.py) implementing the component scoring functions
- A Streamlit starter app at app/streamlit_app.py
- README instructions and a .env.example for secrets

Next steps after cloning:

1. Copy .env.example to .env and fill in DATABASE_URL and OWM_API_KEY.
2. Start Postgres locally (docker-compose up -d) or use an external Postgres and set DATABASE_URL.
3. Run db/schema.sql against your database to create tables.
4. Install Python deps: pip install -r requirements.txt
5. Run ingestion scripts to populate tables (ingest/ingest_statcast.py, ingest/ingest_season_stats.py, ingest/ingest_lineups_injuries.py)
6. Compute aggregates and scores (extend etl/compute_aggregates.py and call score functions)
7. Run the Streamlit app: streamlit run app/streamlit_app.py

Notes:
- Rotowire fallback is configurable via ROTOWIRE_ENABLED in .env. Scraping fallbacks are provided as placeholders and must be implemented and used in compliance with Rotowire's terms.
- The OpenWeatherMap API key should be added to .env or provided as a GitHub secret when deploying.
- This scaffold is intentionally minimal; the scoring mappings, thresholds, and probability models need calibration against historical data.
