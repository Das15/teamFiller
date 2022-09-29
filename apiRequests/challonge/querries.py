import logging
import challonge
import apiRequests.challonge.cache as cache
import config


APIKEY = config.getConfigValue("challonge_api_key")
USERNAME = config.getConfigValue("challonge_username")


# Does not have time.sleep, use it cautiously
def requestTournament(tourneyName):
    logging.info(f"Getting challonge bracket for tournament {tourneyName}.")
    challonge.set_credentials(USERNAME, APIKEY)
    tournament = challonge.tournaments.show(tourneyName)
    tournament["participants"] = challonge.participants.index(tourneyName)
    tournament["matches"] = challonge.matches.index(tourneyName)

    return tournament


def getTournament(tourneyName):
    cacheCheckResult = cache.readCache(tourneyName)
    if cacheCheckResult:
        return cacheCheckResult
    tournament = requestTournament(tourneyName)
    if tournament is not None:
        cache.addEntryToCache(tournament)
    return tournament
