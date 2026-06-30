"""Ingest season-level batting stats using pybaseball as a starter.
This creates/updates season_stats table entries.
"""
import os
from dotenv import load_dotenv
import logging
import sqlalchemy
from datetime import date

load_dotenv()
logging.basicConfig(level=logging.INFO)

DATABASE_URL = os.getenv('DATABASE_URL')
engine = sqlalchemy.create_engine(DATABASE_URL)

try:
    from pybaseball import batting_stats
except Exception:
    logging.warning('pybaseball.batting_stats not available; ensure pybaseball is installed')


def ingest_season(season: int = None):
    if season is None:
        season = date.today().year
    logging.info(f"Fetching season batting stats for {season}")
    try:
        df = batting_stats(season)
    except Exception as e:
        logging.error(f"Error fetching batting stats: {e}")
        return
    if df is None or df.empty:
        logging.warning('No batting stats returned')
        return
    # Normalize and write minimal columns to season_stats
    cols_map = {
        'ID': 'player_id',
        'HR': 'hr',
        'RBI':'rbi',
        'R':'r',
        'H':'h',
        'BB':'bb',
        'SO':'so',
        'PA':'plate_appearances'
    }
    to_keep = [k for k in cols_map.keys() if k in df.columns]
    df_sel = df[to_keep].rename(columns=cols_map)
    df_sel['season'] = season
    # compute ISO if possible
    if 'h' in df_sel.columns and 'plate_appearances' in df_sel.columns:
        df_sel['iso'] = None
    df_sel.to_sql('season_stats', engine, if_exists='append', index=False)
    logging.info(f"Inserted season stats for {len(df_sel)} players")


if __name__ == '__main__':
    ingest_season()
