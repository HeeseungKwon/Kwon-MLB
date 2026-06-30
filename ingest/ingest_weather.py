import requests
import logging
import time

logging.basicConfig(level=logging.INFO)

# API 키가 필요 없는 전면 무료 날씨 API (Open-Meteo)
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

# [MLB 전 구장 좌표 데이터 가이드] 
# 각 팀의 홈구장 위도(lat)와 경도(lon) 매핑 테이블
MLB_STADIUMS = {
    "ARI": {"stadium": "Chase Field", "lat": 33.4450, "lon": -112.0667},
    "ATL": {"stadium": "Truist Park", "lat": 33.8911, "lon": -84.4680},
    "BAL": {"stadium": "Oriole Park at Camden Yards", "lat": 39.2835, "lon": -76.6219},
    "BOS": {"stadium": "Fenway Park", "lat": 42.3466, "lon": -71.0988},
    "CHC": {"stadium": "Wrigley Field", "lat": 41.9472, "lon": -87.6564},
    "CWS": {"stadium": "Guaranteed Rate Field", "lat": 41.8302, "lon": -87.6342},
    "CIN": {"stadium": "Great American Ball Park", "lat": 39.0975, "lon": -84.5070},
    "CLE": {"stadium": "Progressive Field", "lat": 41.4955, "lon": -81.6853},
    "COL": {"stadium": "Coors Field", "lat": 39.7557, "lon": -104.9942},
    "DET": {"stadium": "Comerica Park", "lat": 42.3395, "lon": -83.0490},
    "HOU": {"stadium": "Daikin Park", "lat": 29.7571, "lon": -95.3554},
    "KC":  {"stadium": "Kauffman Stadium", "lat": 39.0512, "lon": -94.4808},
    "LAA": {"stadium": "Angel Stadium", "lat": 33.7999, "lon": -117.8832},
    "LAD": {"stadium": "Dodger Stadium", "lat": 34.0734, "lon": -118.2402},
    "MIA": {"stadium": "loanDepot park", "lat": 25.7783, "lon": -80.2198},
    "MIL": {"stadium": "American Family Field", "lat": 43.0284, "lon": -87.9716},
    "MIN": {"stadium": "Target Field", "lat": 44.9817, "lon": -93.2783},
    "NYM": {"stadium": "Citi Field", "lat": 40.7566, "lon": -73.8460},
    "NYY": {"stadium": "Yankee Stadium", "lat": 40.8296, "lon": -73.9262},
    "ATH": {"stadium": "Sutter Health Park", "lat": 38.5802, "lon": -121.5126}, # 애슬레틱스 임시 홈
    "PHI": {"stadium": "Citizens Bank Park", "lat": 39.9056, "lon": -75.1666},
    "PIT": {"stadium": "PNC Park", "lat": 40.4471, "lon": -80.0062},
    "SD":  {"stadium": "Petco Park", "lat": 32.7071, "lon": -117.1571},
    "SF":  {"stadium": "Oracle Park", "lat": 37.7784, "lon": -122.3899},
    "SEA": {"stadium": "T-Mobile Park", "lat": 47.5911, "lon": -122.3329},
    "STL": {"stadium": "Busch Stadium", "lat": 38.6224, "lon": -90.1934},
    "TB":  {"stadium": "Tropicana Field", "lat": 27.7681, "lon": -82.6481},
    "TEX": {"stadium": "Globe Life Field", "lat": 32.7516, "lon": -97.0830},
    "TOR": {"stadium": "Rogers Centre", "lat": 43.6417, "lon": -79.3892},
    "WSH": {"stadium": "Nationals Park", "lat": 38.8726, "lon": -77.0077}
}

def fetch_weather_by_team(team_code: str):
    """
    팀 약자(예: 'LAD', 'BOS')를 입력받아 홈구장의 실시간 날씨 데이터를 가져옵니다.
    """
    team_code = team_code.upper().strip()
    if team_code not in MLB_STADIUMS:
        raise ValueError(f"알 수 없는 팀 약자입니다: {team_code}")
        
    info = MLB_STADIUMS[team_code]
    lat, lon, stadium = info["lat"], info["lon"], info["stadium"]
    
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "relative_humidity_2m", "precipitation", "rain", "wind_speed_10m", "wind_direction_10m"],
        "timezone": "auto",
        "forecast_days": 1
    }
    
    logging.info(f"[{stadium} 날씨 수집 중...] 팀: {team_code}")
    response = requests.get(WEATHER_URL, params=params)
    response.raise_for_status()
    
    data = response.json()
    # 템플릿 구조에 맞춰 보기 쉽게 커스텀 딕셔너리로 가공
    current = data.get("current", {})
    return {
        "team": team_code,
        "stadium": stadium,
        "temp": current.get("temperature_2m"),
        "humidity": current.get("relative_humidity_2m"),
        "rain": current.get("rain"),
        "wind_speed": current.get("wind_speed_10m"),
        "wind_direction": current.get("wind_direction_10m")
    }

def fetch_all_stadiums_weather():
    """
    30개 모든 MLB 구장의 날씨를 순서대로 전부 긁어옵니다.
    """
    all_weather = {}
    print("\n⚡ [시작] 메이저리그 전 구장 날씨 일괄 수집")
    for team_code in MLB_STADIUMS.keys():
        try:
            res = fetch_weather_by_team(team_code)
            all_weather[team_code] = res
            # 무료 API 매너를 위해 요청 사이에 0.2초 짧은 휴식
            time.sleep(0.2) 
        except Exception as e:
            logging.error(f"{team_code} 구장 날씨 수집 실패: {e}")
    return all_weather


if __name__ == '__main__':
    # 테스트 1: 특정 팀 구장 하나만 조회하고 싶을 때 (예: LA 다저스)
    try:
        dodgers_weather = fetch_weather_by_team("LAD")
        print("\n=== ⚾ 개별 구장 테스트 ===")
        print(f"구장명: {dodgers_weather['stadium']}")
        print(f"기온: {dodgers_weather['temp']}°C / 풍속: {dodgers_weather['wind_speed']} km/h\n")
    except Exception as e:
        print(f"에러: {e}")

    # 테스트 2: 전 구장 날씨 한 번에 다 가져오기
    # (결과가 너무 길어지므로 상위 3개만 샘플 출력해 봅니다)
    all_data = fetch_all_stadiums_weather()
    print("\n=== 📊 전 구장 수집 완료 (일부 결과 샘플) ===")
    sample_teams = list(all_data.keys())[:3]
    for t in sample_teams:
        w = all_data[t]
        print(f"[{w['team']} - {w['stadium']}] 기온: {w['temp']}°C, 풍속: {w['wind_speed']}km/h, 강수량: {w['rain']}mm")
