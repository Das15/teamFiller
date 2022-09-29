import logging
import os


def parseCache(cache):
    temp = []
    for i in range(len(cache)):
        cache[i] = cache[i].replace("\n", "")
        if cache[i] == "":
            logging.warning(f"Found empty space in cache entry {i + 1}.")
            continue
        temp.append(cache[i].split("\t"))
    return temp


def readCache(cache_path):
    if not os.path.exists(cache_path):
        return None
    with open(cache_path, "r") as file:
        temp = file.readlines()
    cache = parseCache(temp)
    if not cache:
        return None
    return cache
