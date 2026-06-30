"""ETL helpers to compute rolling aggregates (e.g., last 10 games) and populate aggregates table.
This file is a stub for the starter implementation.
"""
import os
from dotenv import load_dotenv
import logging
import sqlalchemy
import pandas as pd

load_dotenv()
logging.basicConfig(level=logging.INFO)

engine = sqlalchemy.create_engine(os.getenv('DATABASE_URL'))


def compute_recent_aggregates(as_of_date: str):
    """Example: compute last-10-games aggregates per player and write to aggregates table."""
    logging.info('Computing recent aggregates - placeholder implementation')
    # This function should query pitches/season_stats/lineups to build recent windows.
    # For the scaffold we leave a placeholder that can be filled once data exists.


if __name__ == '__main__':
    compute_recent_aggregates('2026-01-01')
