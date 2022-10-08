import logging
# TODO: Remove this module from application
import challonge
import apiRequests.challonge.cache as cache
import config
import requests


API_KEY = None
USERNAME = None


def initialize():
    """
Loads api key and username from config file.
    """
    global API_KEY, USERNAME
    API_KEY = config.get_config_value("challonge_api_key")
    USERNAME = config.get_config_value("challonge_username")


# Does not have time.sleep, use it cautiously
def request_tournament(tourney_name, get_participants_and_matches=True):
    logging.info(f"Getting challonge bracket for tournament '{tourney_name}'.")
    challonge.set_credentials(USERNAME, API_KEY)
    tournament = challonge.tournaments.show(tourney_name)
    if get_participants_and_matches:
        tournament["participants"] = challonge.participants.index(tourney_name)
        tournament["matches"] = challonge.matches.index(tourney_name)
    return tournament


def check_challonge_key(challonge_api_key):
    data = {"api_key": challonge_api_key, "include_participants": 0, "include_matches": 0}
    # I wish challonge api wouldn't require me to add user agent.
    headers = {"User-Agent": "Mozilla/5.0 (Windows 6.1; Win64; x64"}
    logging.info(f"Checking if '{challonge_api_key}' challonge key is valid.")

    re = requests.get("https://api.challonge.com/v1/tournaments/MP5D.json", data, headers=headers)
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
