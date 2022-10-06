from importlib import reload
from apiRequests.general import initializeApiKeys

import command_ui
import objects.bracket as bracket
import objects.teams_data as teams_data
import logging
import objects.mappool_data as mappool_data
import objects.challonge_response as challonge_response
import apiRequests.challonge.querries as challonge_request


def loadTeamsFromFile(bracketFile, filepath, assumeOrderBySeeds):
    teams = teams_data.Class(filepath, assumeOrderBySeeds).teams
    for team in teams:
        bracketFile.Teams.append(team)
    return bracketFile


def loadMappoolFromFile(bracketFile):
    mappool = mappool_data.Class(bracketFile.Rounds, "mods.txt", "mappool.txt")
    mappool.getMappool()
    return mappool.bracketMappools


def downloadLadderFromChallonge(bracketFile):
    challongeData = challonge_response.Class(challonge_request.getTournament("N2VC"))
    return challongeData.replaceAcronyms(bracketFile)


def legacyEditBracket():
    bracketData = bracket.load_json("bracket.json")
    bracketData.Rounds = loadMappoolFromFile(bracketData)
    bracketData = loadTeamsFromFile(bracketData, "teams.txt", assumeOrderBySeeds=True)
    bracketData = downloadLadderFromChallonge(bracketData)

    bracketData.writeToFile("output.json")


def main():
    reload(logging)
    logging.basicConfig(level=logging.DEBUG, filename="logs.log", filemode="w",
                        format='%(asctime)s %(levelname)s - %(message)s', datefmt="%d-%m-%y %H:%M:%S")
    initializeApiKeys()
    command_ui.initializeUi()


if __name__ == "__main__":
    main()
