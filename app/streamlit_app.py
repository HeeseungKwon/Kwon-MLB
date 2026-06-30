"""Streamlit app to display top picks based on scores table."""

import os
from datetime import date

from dotenv import load_dotenv
import streamlit as st
import sqlalchemy
import pandas as pd

# -------------------------------------------------
# Load environment variables
# -------------------------------------------------
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    st.error("DATABASE_URL not found in .env")
    st.stop()

engine = sqlalchemy.create_engine(DATABASE_URL)

# -------------------------------------------------
# Streamlit UI
# -------------------------------------------------
st.set_page_config(
    page_title="MLB HR / HRR Analyzer",
    layout="wide"
)

st.title("⚾ MLB HR / HRR Prospects Analyzer")

st.write("Displays the highest scoring hitters from the scores table.")

selected_date = st.date_input(
    "As of date",
    value=date.today()
)

# -------------------------------------------------
# Load Scores
# -------------------------------------------------

if st.button("Load Top Picks"):

    query = """
    SELECT
        player_id,
        total_score,
        season_score,
        recent_score,
        matchup_score,
        statcast_score,
        park_score,
        weather_score,
        bullpen_score
    FROM scores
    WHERE as_of = %s
    ORDER BY total_score DESC
    LIMIT 200;
    """

    try:

        with engine.connect() as conn:

            df = pd.read_sql_query(
                query,
                conn,
                params=(selected_date,)
            )

    except Exception as e:

        st.error(f"Error reading scores from DB:\n\n{e}")
        st.stop()

    if df.empty:

        st.warning(
            "No scores found for this date.\n\n"
            "Run the ingestion and scoring pipeline first."
        )

    else:

        st.success(f"Loaded {len(df)} players.")

        st.subheader("Top 50 Overall")

        st.dataframe(
            df.head(50),
            use_container_width=True
        )

        st.subheader("Top 10 HR Prospects")

        st.dataframe(
            df.head(10),
            use_container_width=True
        )