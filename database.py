import logging
import pymongo
import pandas as pds
import expiringdict

import utils

client = pymongo.MongoClient()
logger = logging.Logger(__name__)
utils.setup_logger(logger, 'db.log')
RESULT_CACHE_EXPIRATION = 10             # seconds


def upsert_weather(weather_dict):
    """
    Update MongoDB database `weather` and collection for city with the given `weather_dict`.
    """
    db = client.get_database("weather")
    city_name = weather_dict["name"]
    collection = db.get_collection(city_name)
    result = collection.replace_one(
        filter={'dt': weather_dict['dt']},
        replacement=weather_dict,                     
        upsert=True)        
    logger.info("City: {}, Total Data Points: {}, Update: {}".format(city_name, len(list(collection.find())), result.matched_count == 0))

def fetch_all_weather(city="ALL"):
    db = client.get_database("weather")
    collections = []
    if city == "ALL":
        for city_name in db.collection_names():
            collection = db.get_collection(city_name)
            collections.extend(list(collection.find()))
    else:
        collection = db.get_collection(city)
        return list(collection.find())

_fetch_all_weather_cache = expiringdict.ExpiringDict(max_len=1,
                                                       max_age_seconds=RESULT_CACHE_EXPIRATION)


if __name__ == '__main__':
    pass
