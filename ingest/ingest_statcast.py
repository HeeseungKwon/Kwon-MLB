"""Ingest Statcast pitch-level data for the given date range using pybaseball.
This script is intentionally simple and meant for the starter scaffold.
"""
import os
from datetime import date
from dotenv import load_dotenv
import pandas as pd
import sqlalchemy
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise RuntimeError("Set DATABASE_URL in environment or .env")

engine = sqlalchemy.create_engine(DATABASE_URL)

try:
    from pybaseball import statcast
except Exception as e:
    logging.error("pybaseball is required to run this script. Install via pip install pybaseball")
    raise


def ingest_statcast(start_date: str, end_date: str):
    """Fetch statcast from start_date to end_date (YYYY-MM-DD) and write to pitches table."""
    logging.info(f"Fetching statcast from {start_date} to {end_date}")
    df = statcast(start_date, end_date)
    if df is None or df.empty:
        logging.warning("No statcast data returned for range")
        return
    # select subset of columns to store
    cols = [
        'game_pk','at_bat_number','pitch_type','release_speed','release_pos_x','release_pos_z',
        'exit_velocity','launch_angle','events','description','player_name','pitcher','batter','pitch_id'
    ]
    available = [c for c in cols if c in df.columns]
    df_sel = df[available].copy()
    # rename to match schema
    rename_map = {
        'at_bat_number':'at_bat_id',
        'exit_velocity':'launch_speed',
        'player_name':'player_name',
        'pitcher':'pitcher_id',
        'batter':'batter_id',
        'pitch_id':'pitch_id'
    }
    df_sel = df_sel.rename(columns=rename_map)
    df_sel['created_at'] = pd.Timestamp.now()
    # write to DB
    df_sel.to_sql('pitches', engine, if_exists='append', index=False)
    logging.info(f"Inserted {len(df_sel)} pitch rows into pitches table")


if __name__ == '__main__':
    # default: ingest last 7 days
    end = date.today()
    start = end
    # default single-day ingest (can be adjusted)
    ingest_statcast(start.isoformat(), end.isoformat())
