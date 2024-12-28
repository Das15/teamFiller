import os
import logging
import jsonpickle as jp
import time

CACHE_PATH = os.path.join(os.getcwd(), "data", "challonge_cache")


def add_entry_to_cache(request_data: {}) -> None:
    """Writes json entry to the data/challonge_cache folder, if dir doesn't exist creates one."""
    if not os.path.exists(CACHE_PATH):
        os.makedirs(CACHE_PATH)
    with open(os.path.join(CACHE_PATH, f'{request_data["url"].lower()}.json'), "w", encoding="utf-8") \
            as file:
        file.write(jp.encode(request_data, unpicklable=False))


def read_cache(tourney_name: str, acceptable_time_difference: int = 7200):
    """
    Reads entry from challonge directory cache, if the time passed since modifying exeeds acceptable_time_difference,
    returns None.
    """
    path = os.path.join(CACHE_PATH, f"{tourney_name.lower()}.json")
    if os.path.exists(path):
        file_modification_timestamp = round(time.time() - os.path.getmtime(path))
        logging.info(f"Diff of current and file creation time of challonge response is {file_modification_timestamp} "
                     f"seconds.")
        if file_modification_timestamp > acceptable_time_difference:
            return None

        with open(path, "r", encoding="utf-8") as file:
            return jp.loads(file.read())
    return None
