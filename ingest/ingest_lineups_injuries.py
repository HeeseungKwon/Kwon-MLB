"""Fetch lineups and injuries using MLB Stats API (official) with a Rotowire fallback option.
This module writes to lineups and injuries tables.
"""
import os
import requests
from dotenv import load_dotenv
import logging
import sqlalchemy
from datetime import date

load_dotenv()
logging.basicConfig(level=logging.INFO)

DATABASE_URL = os.getenv('DATABASE_URL')
engine = sqlalchemy.create_engine(DATABASE_URL)

ROTOWIRE_ENABLED = os.getenv('ROTOWIRE_ENABLED', 'false').lower() in ('1','true','yes')

MLB_SCHEDULE_URL = 'https://statsapi.mlb.com/api/v1/schedule'
BOX_URL_TPL = 'https://statsapi.mlb.com/api/v1/game/{gamePk}/boxscore'


def fetch_games_on(date_str: str):
    params = {'sportId':1, 'date':date_str}
    r = requests.get(MLB_SCHEDULE_URL, params=params)
    r.raise_for_status()
    return r.json()


def fetch_boxscore(game_pk: int):
    url = BOX_URL_TPL.format(gamePk=game_pk)
    r = requests.get(url)
    r.raise_for_status()
    return r.json()


def ingest_lineups_for_date(date_str: str):
    logging.info(f"Fetching schedule for {date_str}")
    sched = fetch_games_on(date_str)
    games = sched.get('dates', [])
    for d in games:
        for game in d.get('games', []):
            game_pk = game.get('gamePk')
            logging.info(f"Processing game {game_pk}")
            try:
                box = fetch_boxscore(game_pk)
                # extract batting orders if present
                teams = box.get('teams', {})
                for side in ('home','away'):
                    team = teams.get(side, {})
                    team_id = team.get('team', {}).get('id')
                    batters = team.get('batters')
                    # batters is a list of player IDs in lineup order
                    lineup_json = {'batters': batters}
                    # write to DB
                    insert_lineup(game_pk, team_id, lineup_json)
            except Exception as e:
                logging.warning(f"Failed to fetch boxscore for {game_pk}: {e}")
                if ROTOWIRE_ENABLED:
                    logging.info('ROTOWIRE fallback enabled — attempting estimated lineup (not implemented)')
                continue


def insert_lineup(game_pk, team_id, lineup_json):
    with engine.begin() as conn:
        conn.execute(
            "INSERT INTO lineups (game_pk, team_id, batting_order) VALUES (%s, %s, %s)",
            (game_pk, team_id, sqlalchemy.sql.literal_column("%s"))
        )


if __name__ == '__main__':
    today = date.today().isoformat()
    ingest_lineups_for_date(today)
