import re


# Possible repeat of class's method?
def parse_acronym(team_name, length=3):
    stripped_team_name = remove_non_ascii_chars(team_name.FullName).replace(" ", "")
    team_name.Acronym = stripped_team_name[0:length] if len(stripped_team_name) >= length else stripped_team_name


class Class(object):
    # noinspection PyPep8Naming
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
            self.parse_flag_name()
        if Acronym is None:
            self.parse_acronym()

    def parse_flag_name(self):
        path_regex = re.compile("[^\\w|^-|^()]")
        non_ascii_name = remove_non_ascii_chars(self.FullName)
        self.FlagName = path_regex.sub("_", non_ascii_name.lower())

    def parse_acronym(self, length=3):
        stripped_team_name = remove_non_ascii_chars(self.FullName).replace(" ", "")
        self.Acronym = stripped_team_name[0:length] if len(stripped_team_name) >= length else stripped_team_name


def remove_non_ascii_chars(string):
    return "".join(char for char in string if 0 < ord(char) < 127)


def get_team_name(teams, acronym):
    for team in teams:
        if team.Acronym == acronym:
            return team.FullName
    return None


def get_team_acronym(teams, name):
    for team in teams:
        if team.FullName == name:
            return team.Acronym
    return None
