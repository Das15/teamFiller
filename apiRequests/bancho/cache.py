import os

import apiRequests.cache as base_cache

CACHE_PATH = os.path.join(os.getcwd(), "data", "bancho_cache")


def add_entry_to_cache(username: str, user_id: str) -> None:
    """Adds line of text into cache file."""
    with open(CACHE_PATH, "a") as file:
        file.write(f"{username}\t{user_id}\n")


def check_username(username: str) -> str | None:
    """Checks if cache contains the username, if does returns it, otherwise returns None."""
    cache = base_cache.read_cache(CACHE_PATH)
    if cache is None:
        return None
    for entry in cache:
        if username == entry[0]:
            return entry[1]
    return None


def check_user_id(user_id: str) -> str | None:
    """Reads cache file, then checks if user id is in cache, returns username, else it returns none."""
    cache = base_cache.read_cache(CACHE_PATH)
    if cache is None:
        return None
    for entry in cache:
        if user_id == entry[1]:
            return entry[0]
    return None
