import logging
import challonge
import apiRequests.challonge.cache as cache
import config
import requests


APIKEY = None
USERNAME = None


def initialize():
    """
Loads api key and username from config file.
    """
    global APIKEY, USERNAME
    APIKEY = config.getConfigValue("challonge_api_key")
    USERNAME = config.getConfigValue("challonge_username")


# Does not have time.sleep, use it cautiously
def requestTournament(tourneyName, getParticipantsAndMatches=True):
    logging.info(f"Getting challonge bracket for tournament '{tourneyName}'.")
    challonge.set_credentials(USERNAME, APIKEY)
    tournament = challonge.tournaments.show(tourneyName)
    if getParticipantsAndMatches:
        tournament["participants"] = challonge.participants.index(tourneyName)
        tournament["matches"] = challonge.matches.index(tourneyName)
    return tournament


def checkChallongeKey(challongeApiKey):
    data = {"api_key": challongeApiKey, "include_participants": 0, "include_matches": 0}
    # I wish challonge api wouldn't require me to add user agent.
    headers = {"User-Agent": "Mozilla/5.0 (Windows 6.1; Win64; x64"}
    logging.info(f"Checking if '{challongeApiKey}' challonge key is valid.")

    re = requests.get("https://api.challonge.com/v1/tournaments/MP5D.json", data, headers=headers)
    if re.status_code == 200:
        return True
    logging.error(f"Checking challonge key failed, response code: '{re.status_code}'.")
    return False


def getTournament(tourneyName):
    cacheCheckResult = cache.readCache(tourneyName)
    if cacheCheckResult:
        return cacheCheckResult
    tournament = requestTournament(tourneyName)
    if tournament is not None:
        cache.addEntryToCache(tournament)
    return tournament
