import logging
# TODO: Remove this module from application
import challonge
import apiRequests.challonge.cache as cache
import config
import requests


API_KEY = None
# I must say, why the heck do i have to spook user-agent? Oh well...
DEFAULT_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows 6.1; Win64; x64"}


def initialize():
    """
Loads api key and username from config file.
    """
    global API_KEY
    API_KEY = config.get_config_value("challonge_api_key")


# Does not have time.sleep, use it cautiously
# TODO: Remove the redundant "participant" and "match" subdirectories in json response.
def request_tournament(tourney_name, get_participants_and_matches=True):
    data = {"api_key": API_KEY, "include_participants": 0, "include_matches": 0}
    if get_participants_and_matches:
        data["include_participants"] = 1
        data["include_matches"] = 1
    logging.info(f"Getting challonge bracket for tournament '{tourney_name}'.")
    re = requests.get(f"https://api.challonge.com/v1/tournaments/{tourney_name}.json", data, headers=DEFAULT_HEADERS)
    if re.status_code == 200:
        return re.json()["tournament"]
    logging.error(f"Requesting tournament failed, response code: '{re.status_code}'")


def check_challonge_key(challonge_api_key):
    data = {"api_key": challonge_api_key, "include_participants": 0, "include_matches": 0}
    logging.info(f"Checking if '{challonge_api_key}' challonge key is valid.")

    re = requests.get("https://api.challonge.com/v1/tournaments/MP5D.json", data, headers=DEFAULT_HEADERS)
    if re.status_code == 200:
        return True
    logging.error(f"Checking challonge key failed, response code: '{re.status_code}'.")
    return False


def get_tournament(tourney_name):
    cache_check_result = cache.read_cache(tourney_name)
    if cache_check_result:
        return cache_check_result
    tournament = request_tournament(tourney_name)
    if tournament is not None:
        cache.add_entry_to_cache(tournament)
    return tournament
