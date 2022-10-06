import apiRequests.bancho.querries as bancho_api
import apiRequests.challonge.querries as challonge_api


def initialize_api_keys():
    bancho_api.initialize()
    challonge_api.initialize()
