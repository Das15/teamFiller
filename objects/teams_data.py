import logging
import objects.team as team
import objects.player as player
from objects.data import loadRawData
from apiRequests.bancho.querries import getUserId, checkIfUserIdExists


class Class(object):
    def __init__(self, filePath, assumeOrderBySeeds=False):
        data = parseRawData(loadRawData(filePath))
        self.teams = createTeamsFromParsedData(data, assumeOrderBySeeds)


def checkForTeamNameInData(teamName, data):
    for i in range(len(data)):
        if teamName == data[i]["teamName"]:
            return i
    return None


def extractAcronyms(teams):
    acronyms = []
    for entry in teams:
        acronyms.append(entry.Acronym)
    return acronyms


# TODO: Extract acronym matching funtion so it can be accessed from other files
def verifyAcronyms(teams):
    acronyms = extractAcronyms(teams)
    duplicatedEntries = []
    for i in range(len(teams)):
        if teams[i].Acronym in acronyms:
            tempArray = acronyms.copy()
            tempArray.remove(teams[i].Acronym)
            if teams[i].Acronym in tempArray:
                if acronyms.index(teams[i].Acronym) == i:
                    temp = [tempArray.index(teams[i].Acronym), i]
                    duplicatedEntries.append([min(temp), max(temp)+1])
    return duplicatedEntries


def parsePlayerId(rawPlayerId):
    if rawPlayerId == "":
        return None
    if rawPlayerId.isdigit() and checkIfUserIdExists(rawPlayerId):
        return rawPlayerId
    else:
        playerId = getUserId(rawPlayerId)
        return playerId


def parseRawData(data):
    teams = []
    maxLength = len(max(data, key=len))
    for line in data:
        temp = {"teamName": "",
                "players": []}
        for i in range(len(line)):
            if i == 0:
                temp["teamName"] = line[i]
            else:
                playerId = parsePlayerId(line[i])
                if playerId is not None:
                    temp["players"].append(playerId)
        check = checkForTeamNameInData(temp["teamName"], teams)
        if check is not None:
            for entry in temp["players"]:
                teams[check]["players"].append(entry)
        else:
            if temp["teamName"]:
                if not temp["players"] and maxLength == 1:
                    temp["players"].append(parsePlayerId(temp["teamName"]))
                teams.append(temp)
    return teams


def parseAcronyms(teams):
    duplicatedEntries = verifyAcronyms(teams)
    for entry in duplicatedEntries:
        oldAcronym = teams[entry[1]].Acronym
        teams[entry[1]].parseAcronym(4)
        if oldAcronym == teams[entry[1]].Acronym:
            teams[entry[1]].Acronym += " "
        if teams[entry[0]].Acronym == teams[entry[1]]:
            logging.error("Something went wrong and entries {} and {} are the same.".format(*entry))
            pass
    return teams


def createTeamsFromParsedData(data, assumeOrderBySeeds):
    temp = []
    currSeed = 1
    for entry in data:
        players = []
        for playerId in entry["players"]:
            players.append(player.Class(playerId))
        team_data = team.Class(entry["teamName"], currSeed) if assumeOrderBySeeds else team.Class(entry["teamName"])
        currSeed += 1
        team_data.Players = players
        temp.append(team_data)
    return temp
