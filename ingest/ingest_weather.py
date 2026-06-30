"""Fetch weather for a stadium coordinate using OpenWeatherMap One Call API (4.0 timeline endpoint).
"""
import os
import requests
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)

OWM_KEY = os.getenv('OWM_API_KEY')
if not OWM_KEY:
    logging.warning('OWM_API_KEY not set; weather ingestion will not run.')

OWM_TPL = 'https://api.openweathermap.org/data/4.0/onecall/timeline/1day'


def fetch_weather_latlon(lat: float, lon: float):
    if not OWM_KEY:
        raise RuntimeError('OWM_API_KEY not set')
    params = {'lat': lat, 'lon': lon, 'appid': OWM_KEY}
    r = requests.get(OWM_TPL, params=params)
    r.raise_for_status()
    return r.json()


if __name__ == '__main__':
    # example: fetch for Yankee Stadium lat/lon (placeholder)
    lat, lon = 40.8296, -73.9262
    print(fetch_weather_latlon(lat, lon))
