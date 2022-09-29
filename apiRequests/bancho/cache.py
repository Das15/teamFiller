import os
import apiRequests.cache as baseCache

CACHE_PATH = os.path.join(os.getcwd(), "data", "bancho_cache")


def addEntryToCache(username, userId):
    with open(CACHE_PATH, "a") as file:
        file.write(f"{username}\t{userId}\n")


def checkUsername(username):
    cache = baseCache.readCache(CACHE_PATH)
    if cache is None:
        return None
    for entry in cache:
        if username == entry[0]:
            return entry[1]
    return None


def checkUserId(userId):
    cache = baseCache.readCache(CACHE_PATH)
    if cache is None:
        return None
    for entry in cache:
        if userId == entry[1]:
            return entry[0]
    return None
