-- DB schema for MLB Analyzer (starter)

CREATE TABLE IF NOT EXISTS players (
  player_id BIGINT PRIMARY KEY,
  mlb_id BIGINT,
  full_name TEXT,
  primary_position TEXT,
  handedness TEXT,
  team_id BIGINT
);

CREATE TABLE IF NOT EXISTS games (
  game_pk BIGINT PRIMARY KEY,
  game_date DATE,
  home_team_id BIGINT,
  away_team_id BIGINT
);

CREATE TABLE IF NOT EXISTS lineups (
  id SERIAL PRIMARY KEY,
  game_pk BIGINT REFERENCES games(game_pk),
  team_id BIGINT,
  batting_order JSONB,
  fetched_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS injuries (
  id SERIAL PRIMARY KEY,
  player_id BIGINT,
  status TEXT,
  details JSONB,
  updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS pitches (
  pitch_id BIGINT PRIMARY KEY,
  game_pk BIGINT,
  at_bat_id BIGINT,
  pitcher_id BIGINT,
  batter_id BIGINT,
  pitch_type TEXT,
  pitch_speed NUMERIC,
  release_speed NUMERIC,
  launch_speed NUMERIC,
  launch_angle NUMERIC,
  events TEXT,
  description TEXT,
  created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS season_stats (
  id SERIAL PRIMARY KEY,
  player_id BIGINT,
  season INTEGER,
  plate_appearances INTEGER,
  hr INTEGER,
  r INTEGER,
  rbi INTEGER,
  h INTEGER,
  doubles INTEGER,
  triples INTEGER,
  bb INTEGER,
  so INTEGER,
  iso NUMERIC,
  woba NUMERIC,
  updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS aggregates (
  id SERIAL PRIMARY KEY,
  player_id BIGINT,
  as_of DATE,
  window TEXT,
  pa INTEGER,
  hr INTEGER,
  h INTEGER,
  r INTEGER,
  rbi INTEGER,
  hrr INTEGER,
  hard_hit_rate NUMERIC,
  barrel_rate NUMERIC,
  xwoba NUMERIC
);

CREATE TABLE IF NOT EXISTS scores (
  id SERIAL PRIMARY KEY,
  player_id BIGINT,
  as_of DATE,
  season_score NUMERIC,
  recent_score NUMERIC,
  matchup_score NUMERIC,
  statcast_score NUMERIC,
  park_score NUMERIC,
  weather_score NUMERIC,
  bullpen_score NUMERIC,
  total_score NUMERIC
);

CREATE TABLE scores (
    as_of DATE,
    player_id INT,
    total_score FLOAT,
    season_score FLOAT,
    recent_score FLOAT,
    matchup_score FLOAT,
    statcast_score FLOAT,
    park_score FLOAT,
    weather_score FLOAT,
    bullpen_score FLOAT,
    PRIMARY KEY (as_of, player_id)
);