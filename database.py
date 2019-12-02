import logging
import pymongo
import pandas as pds
import expiringdict

import utils

client = pymongo.MongoClient()
logger = logging.Logger(__name__)
utils.setup_logger(logger, 'db.log')
RESULT_CACHE_EXPIRATION = 10             # seconds


def upsert_bpa(df):
    """
    Update MongoDB database `energy` and collection `energy` with the given `DataFrame`.
    """
    db = client.get_database("energy")
    collection = db.get_collection("energy")
    update_count = 0
    for record in df.to_dict('records'):
        result = collection.replace_one(
            filter={'Datetime': record['Datetime']},    # locate the document if exists
            replacement=record,                         # latest document
            upsert=True)                                # update if exists, insert if not
        if result.matched_count > 0:
            update_count += 1
    logger.info("rows={}, update={}, ".format(df.shape[0], update_count) +
                "insert={}".format(df.shape[0]-update_count))


def upsert_weather(weather_dict):
    """
    Update MongoDB database `weather` and collection for city with the given `weather_dict`.
    """
    db = client.get_database("weather")
    city_name = weather_dict["name"]
    collection = db.get_collection(city_name)
    update_count = 0
    result = collection.replace_one(
        filter={'dt': record['dt']},
        replacement=weather_dict,                     
        upsert=True)             


def fetch_all_bpa():
    db = client.get_database("energy")
    collection = db.get_collection("energy")
    return list(collection.find())

def fetch_all_weather(city="ALL"):
    db = client.get_database("weather")
    collections = []
    if city == "ALL":
        for city_name in db.collection_names():
            collection = db.get_collection(city_name)
            collections.extend(list(collection.find()))
    else:
        collection = db.get_collection(city_name)
        return list(collection.find())


_fetch_all_bpa_as_df_cache = expiringdict.ExpiringDict(max_len=1,
                                                       max_age_seconds=RESULT_CACHE_EXPIRATION)

_fetch_all_weather_cache = expiringdict.ExpiringDict(max_len=1,
                                                       max_age_seconds=RESULT_CACHE_EXPIRATION)


def fetch_all_bpa_as_df(allow_cached=False):
    """Converts list of dicts returned by `fetch_all_bpa` to DataFrame with ID removed
    Actual job is done in `_worker`. When `allow_cached`, attempt to retrieve timed cached from
    `_fetch_all_bpa_as_df_cache`; ignore cache and call `_work` if cache expires or `allow_cached`
    is False.
    """
    def _work():
        data = fetch_all_bpa()
        if len(data) == 0:
            return None
        df = pds.DataFrame.from_records(data)
        df.drop('_id', axis=1, inplace=True)
        return df

    if allow_cached:
        try:
            return _fetch_all_bpa_as_df_cache['cache']
        except KeyError:
            pass
    ret = _work()
    _fetch_all_bpa_as_df_cache['cache'] = ret
    return ret


if __name__ == '__main__':
    print(fetch_all_bpa_as_df())
