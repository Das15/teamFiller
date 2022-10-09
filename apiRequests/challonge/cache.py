import os
import json
import logging
import jsonpickle as jp
import time

CACHE_PATH = os.path.join(os.getcwd(), "data", "challonge_cache")


def add_entry_to_cache(request_data: {}) -> None:
    if not os.path.exists(CACHE_PATH):
        os.makedirs(CACHE_PATH)
    with open(os.path.join(CACHE_PATH, f'{request_data["url"].lower()}.json'), "w", encoding="utf-8") \
            as file:
        file.write(jp.encode(request_data, unpicklable=False))


def read_cache(tourney_name):
    path = os.path.join(CACHE_PATH, f"{tourney_name.lower()}.json")
    if os.path.exists(path):
        file_modification_timestamp = round(time.time() - os.path.getmtime(path))
        logging.info(f"Diff of current and file creation time of challonge responnse is {file_modification_timestamp} "
                     f"seconds.")
        if file_modification_timestamp > 7200:
            return None

        with open(path, "r", encoding="utf-8") as file:
            return jp.loads(file.read())
    return None


# For debugging purposes, ie checking if cache works correctly.
def get_obj_debug():
    path = os.path.join(os.getcwd(), "apiRequests", "challonge", "wmt_challonge_api.json")
    with open(path, "r", encoding="utf-8") as file:
        logging.info("Loading debug json challonge response.")
        return json.loads(file.read())
