"""Basic unit tests for score normalization functions."""
from score.score_engine import season_score, recent_score, statcast_score


def test_season_score_range():
    s = season_score(0.0)
    assert s >= 0 and s <= 20
    s2 = season_score(0.06)
    assert s2 <= 20


def test_recent_score_zero():
    r = recent_score(0.0, 0)
    assert r == 0


def test_statcast_score_bounds():
    s = statcast_score(0.0, 0.0, 0.200)
    assert s >= 0 and s <= 15
