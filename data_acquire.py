"""
Bonneville Power Administration, United States Department of Energy
"""
import time
import sched
import pandas
import logging
import requests
from io import StringIO
import json

import utils
from database import upsert_weather

API_KEY = "eb0b9ddfad9c74ffb30cffe72e9ad2c8"
WEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/weather?units=imperial&APPID={}&q=".format(API_KEY)
BPA_SOURCE = "https://transmission.bpa.gov/business/operations/Wind/baltwg.txt"
MAX_DOWNLOAD_ATTEMPT = 5
DOWNLOAD_PERIOD = 60         # second
logger = logging.Logger(__name__)
utils.setup_logger(logger, 'data.log')
CITIES = ["Providence", "Miami", "Dallas", "Seattle"]
UTC_TO_EASTERN_SECONDS = 18000

def download_weather(city, url=WEATHER_BASE_URL, retries=MAX_DOWNLOAD_ATTEMPT):
    """Returns weather text from `WEATHER_BASE_URL` and the city
    Returns None if network failed
    """
    full_url = WEATHER_BASE_URL + city
    text = None
    for _ in range(retries):
        try:
            req = requests.get(full_url, timeout=0.5)
            req.raise_for_status()
            text = req.text
        except requests.exceptions.HTTPError as e:
            logger.warning("Retry on HTTP Error: {}".format(e))
    if text is None:
        logger.error('download_weather too many FAILED attempts')
    return text

def filter_weather(text):
    """Converts `text` to `JSON` (dictionary), converts time to datetime
    """
    weather_dict = json.loads(text)
    weather_dict['dt'] = pandas.to_datetime(weather_dict['dt'] - UTC_TO_EASTERN_SECONDS, unit='s')
    return weather_dict

def update_weather_once(city):
    text = download_weather(city)
    weather_dict = filter_weather(text)
    upsert_weather(weather_dict)


def main_loop(timeout=DOWNLOAD_PERIOD):
    scheduler = sched.scheduler(time.time, time.sleep)

    def _worker():
        try:
            for city in CITIES:
                update_weather_once(city)
        except Exception as e:
            logger.warning("main loop worker ignores exception and continues: {}".format(e))
        scheduler.enter(timeout, 1, _worker)    # schedule the next event

    scheduler.enter(0, 1, _worker)              # start the first event
    scheduler.run(blocking=True)


if __name__ == '__main__':
    main_loop()


