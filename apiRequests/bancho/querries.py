import logging
import os
import time
import requests
import apiRequests.bancho.cache as cache
import config

APIKEY = config.getConfigValue("bancho_api_key")


def requestUserId(username):
    data = {"k": APIKEY, "u": username, "type": "string"}
    logging.info(f"Getting user_id for username '{username}'.")

    time.sleep(0.6)

    re = requests.get("https://osu.ppy.sh/api/get_user", params=data)
    if re.status_code != 200:
        raise Exception(f"Expected status code 200, got instead {re.status_code}")
    try:
        jsonData = re.json()[0]
        userId = jsonData["user_id"]
    except IndexError:
        logging.error(f"Didn't find {username} on bancho.")
        userId = None
    return userId


def checkIfUserIdExists(userId):
    if cache.checkUserId(userId):
        return True
    data = {"k": APIKEY, "u": userId, "type": "id"}
    logging.info(f"Checking if user with ID {userId} exists.")

    re = requests.get("https://osu.ppy.sh/api/get_user", params=data)
    if int(re.status_code) == 200 and re.json() != []:
        return True
    else:
        return False


def getUserId(username):
    cacheCheckResult = cache.checkUsername(username)
    if cacheCheckResult:
        return cacheCheckResult
    userId = requestUserId(username)
    if userId is not None:
        cache.addEntryToCache(username, userId)
    return userId
