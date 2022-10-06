import apiRequests.bancho.querries as banchoApi
import apiRequests.challonge.querries as challongeApi


def initializeApiKeys():
    banchoApi.initialize()
    challongeApi.initialize()
