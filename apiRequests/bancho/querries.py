import logging
import time
import requests

import apiRequests.bancho.cache as cache
import config

API_KEY = None


def initialize():
    """
    Also loads api key from config file. It is probably a bad idea to get api_key on init.
    """
    global API_KEY
    API_KEY = config.get_config_value("bancho_api_key")


def request_user_id(username: str) -> str:
    """Has time.sleep built in, will avoid limit rates but makes function slower."""
    data = {"k": API_KEY, "u": username, "type": "string"}
    logging.info(f"Getting user_id for username '{username}'.")

    time.sleep(0.6)

    re = requests.get("https://osu.ppy.sh/api/get_user", params=data)
    if re.status_code != 200:
        raise Exception(f"Expected status code 200, got instead {re.status_code}")
    try:
        json_data = re.json()[0]
        user_id = json_data["user_id"]
    except IndexError:
        logging.error(f"Didn't find {username} on bancho.")
        user_id = None
    return user_id


def check_if_user_id_exists(user_id: str) -> bool:
    """Doesn't check if it cannot fetch user_id because of connection issues."""
    if cache.check_user_id(user_id):
        return True
    data = {"k": API_KEY, "u": user_id, "type": "id"}
    logging.info(f"Checking if user with ID '{user_id}' exists.")

    re = requests.get("https://osu.ppy.sh/api/get_user", params=data)
    if int(re.status_code) == 200 and re.json() != []:
        return True
    else:
        return False


def get_user_id(username: str) -> str:
    """Caches username and id if it wasn't found in cache."""
    cache_check_result = cache.check_username(username)
    if cache_check_result:
        return cache_check_result
    user_id = request_user_id(username)
    if user_id is not None:
        cache.add_entry_to_cache(username, user_id)
    return user_id
