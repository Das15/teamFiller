import re


def parseAcronym(teamName, length=3):
    strippedTeamName = removeNonAsciiChars(teamName.FullName).replace(" ", "")
    teamName.Acronym = strippedTeamName[0:length] if len(strippedTeamName) >= length else strippedTeamName


class Class(object):
    def __init__(self, FullName, Seed=None, FlagName=None, Acronym=None, SeedingResults=None, LastYearPlacing=0,
                 AverageRank=None, Players=None):
        if SeedingResults is None:
            SeedingResults = []
        if Players is None:
            Players = []

        self.FullName = FullName
        self.FlagName = FlagName
        self.Acronym = Acronym
        self.SeedingResults = SeedingResults
        self.Seed = Seed
        self.LastYearPlacing = LastYearPlacing
        self.AverageRank = AverageRank
        self.Players = Players

        if FlagName is None:
            self.parseFlagName()
        if Acronym is None:
            self.parseAcronym()

    def parseFlagName(self):
        pathRegex = re.compile("[^\\w|^-|^()]")
        nonAsciiName = removeNonAsciiChars(self.FullName)
        self.FlagName = pathRegex.sub("_", nonAsciiName.lower())

    def parseAcronym(self, length=3):
        strippedTeamName = removeNonAsciiChars(self.FullName).replace(" ", "")
        self.Acronym = strippedTeamName[0:length] if len(strippedTeamName) >= length else strippedTeamName


def removeNonAsciiChars(string):
    return "".join(char for char in string if 0 < ord(char) < 127)


def getTeamName(teams, acronym):
    for team in teams:
        if team.Acronym == acronym:
            return team.FullName
    return None


def getTeamAcronym(teams, name):
    for team in teams:
        if team.FullName == name:
            return team.Acronym
    return None
