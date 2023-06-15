import apiRequests.bancho.querries as bancho_api
import apiRequests.challonge.querries as challonge_api


def initialize_api_keys() -> None:
    """It is probably a terrible design, but it will do for now."""
    # TODO: Find a way to make getting api keys more logical and easier to read.
    bancho_api.initialize()
    challonge_api.initialize()
