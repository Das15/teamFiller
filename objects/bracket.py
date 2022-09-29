import json
import logging
import codecs
import objects.team as team
import objects.match as match
import objects.mappool as mappool
import objects.ruleset as ruleset
import jsonpickle as jp


class Class(object):
    def __init__(self, Ruleset, Matches, Rounds, Teams, Progressions, ChromaKeyWidth, PlayersPerTeam):
        temp = []
        self.Ruleset = ruleset.Class(**Ruleset)
        for Match in Matches:
            temp.append(match.Class(**Match))
        self.Matches = temp
        temp = []

        for Mappool in Rounds:
            temp.append(mappool.Class(**Mappool))
        self.Rounds = temp
        temp = []
        for Team in Teams:
            temp.append(team.Class(**Team))
        self.Teams = temp
        self.Progressions = Progressions
        self.ChromaKeyWidth = ChromaKeyWidth
        self.PlayersPerTeam = PlayersPerTeam

    def getAcronymFromName(self, teamName):
        for i in range(len(self.Teams)):
            if teamName == self.Teams[i].FullName:
                return self.Teams[i].Acronym
        return None

    def replaceMatch(self, matchData: match.Class):
        for i in range(len(self.Matches)):
            if matchData.ID == self.Matches[i].ID:
                self.Matches[i] = matchData
                return True
        return False

    def getMatchId(self, acronyms, caseInsensitive=True):
        for i in range(len(self.Matches)):
            if caseInsensitive:
                matchAcronyms = [self.Matches[i].Team1Acronym.lower(), self.Matches[i].Team2Acronym.lower()]
            else:
                matchAcronyms = self.Matches[i].Acronyms
            if acronyms[0] in matchAcronyms and acronyms[1] in matchAcronyms:
                return i
        return None

# Using jsonpickle to avoid json encoding issues, like crashes on datatime (no clue what this means exactly, huh)
    def writeToFile(self, filePath):
        if filePath is None:
            filePath = "output.json"
        jp.set_encoder_options("json", indent=2)
        with codecs.open(filePath, "w", encoding="utf-8") as file:
            file.write(jp.encode(self, unpicklable=False))


def load_json(filename):
    try:
        with codecs.open(filename, "r", encoding="utf-8") as file:
            logging.info("Loading json bracket from 'bracket.json'")
            return Class(**json.loads(file.read()))
    except FileNotFoundError:
        logging.error("Didn't find {}".format(filename))
        exit(2)
