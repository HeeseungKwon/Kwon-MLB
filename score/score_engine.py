"""Scoring engine for HR / HRR prospects analyzer.
Each component returns a 0..max_points value. The final score is the sum.
"""
import os
import math
from typing import Dict

# Component maxima
MAX_SEASON = 20
MAX_RECENT = 40
MAX_MATCHUP = 10
MAX_STATCAST = 15
MAX_PARK = 5
MAX_WEATHER = 5
MAX_BULLPEN = 5


def percentile_score(value, ptiles):
    """Map a metric to a percentile-based 0..1 score using ptiles dict {percentile:threshold}.
    Simple linear interpolation between percentiles.
    ptiles should be sorted ascending by percentile keys (0..100).
    """
    # naive fallback: if ptiles is empty, return 0.5
    if not ptiles:
        return 0.5
    # find where value fits
    items = sorted(ptiles.items(), key=lambda x: int(x[0]))
    prev_p, prev_v = 0, items[0][1]
    for p, v in items:
        p = int(p)
        if value <= v:
            # linear interp between prev and (p,v)
            if v == prev_v:
                return p/100.0
            frac = (value - prev_v)/(v - prev_v)
            return (prev_p + frac*(p-prev_p))/100.0
        prev_p, prev_v = p, v
    return 1.0


def season_score(hr_rate: float, min_pa: int = 50) -> float:
    """hr_rate: HR per PA or other normalized metric. Returns 0..MAX_SEASON."""
    # map hr_rate to points; example thresholds (to be tuned)
    # assume hr_rate between 0 and 0.1 (10% HR/PA extremely high)
    score = max(0.0, min(1.0, hr_rate / 0.06))
    return round(score * MAX_SEASON, 3)


def recent_score(recent_hrr_per_pa: float, pa_volume: int) -> float:
    """recent_hrr_per_pa: HRR per PA in last 10 games. pa_volume: PAs in window.
    Give more weight to higher volume.
    """
    # scale by volume factor (diminishing returns)
    vol_factor = min(1.0, pa_volume / 20.0)
    score = recent_hrr_per_pa / 0.25  # e.g., 0.25 HRR/PA is extremely high
    score = max(0.0, min(1.0, score)) * vol_factor
    return round(score * MAX_RECENT, 3)


def matchup_score(pitcher_hr9: float, pitcher_fip: float, platoon_advantage: float) -> float:
    """Compute matchup favorability. platoon_advantage: 1.0 if strong, 0.5 neutral, 0 if bad.
    Returns 0..MAX_MATCHUP
    """
    # simpler: higher pitcher_hr9 increases batter points (bad for pitcher)
    hr9_norm = max(0.0, min(1.0, pitcher_hr9 / 2.0))
    score = 0.6 * hr9_norm + 0.4 * platoon_advantage
    return round(score * MAX_MATCHUP, 3)


def statcast_score(barrel_pct: float, hardhit_pct: float, xwoba: float) -> float:
    # normalize inputs (assume barrel_pct/hardhit_pct in 0..100)
    b = barrel_pct/100.0
    h = hardhit_pct/100.0
    # xwoba roughly 0.200..0.450
    x = (xwoba - 0.250)/0.25
    x = max(0.0, min(1.0, x))
    comp = 0.45*b + 0.45*h + 0.10*x
    comp = max(0.0, min(1.0, comp))
    return round(comp * MAX_STATCAST, 3)


def park_score(park_factor: float) -> float:
    # park_factor: >1 favors hitters, <1 suppresses
    # map 0.9 -> 0, 1.1 -> MAX
    score = (park_factor - 0.9) / 0.2
    score = max(0.0, min(1.0, score))
    return round(score * MAX_PARK, 3)


def weather_score(wind_effect: float) -> float:
    # wind_effect: -1 (strong in) .. 0 neutral .. +1 (strong out)
    val = (wind_effect + 1) / 2.0
    val = max(0.0, min(1.0, val))
    return round(val * MAX_WEATHER, 3)


def bullpen_score(bullpen_hr9: float) -> float:
    # higher bullpen HR9 -> more favorable to hitters
    val = max(0.0, min(1.0, bullpen_hr9 / 2.0))
    return round(val * MAX_BULLPEN, 3)


def total_score(components: Dict[str, float]) -> float:
    s = sum(components.values())
    return round(s, 3)


if __name__ == '__main__':
    # quick sanity check
    comps = {
        'season_score': season_score(0.04),
        'recent_score': recent_score(0.05, 12),
        'matchup_score': matchup_score(1.2, 4.2, 0.8),
        'statcast_score': statcast_score(3.5, 35.0, 0.340),
        'park_score': park_score(1.02),
        'weather_score': weather_score(0.3),
        'bullpen_score': bullpen_score(1.1)
    }
    print(comps)
    print('total', total_score(comps))
