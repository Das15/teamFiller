import json
import logging
import codecs
import jsonpickle as jp

import objects.team as team
import objects.match as match
import objects.mappool as mappool
import objects.ruleset as ruleset


class Class(object):
    # noinspection PyPep8Naming
    def __init__(self, Ruleset: ruleset, Matches: match, Rounds: list[dict], Teams: list[dict], Progressions: [],
                 ChromaKeyWidth: int, PlayersPerTeam: int, AutoProgressScreens: bool):
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
        self.AutoProgressScreens = AutoProgressScreens

    def get_acronym_from_name(self, team_name: str) -> str | None:
        for i in range(len(self.Teams)):
            if team_name == self.Teams[i].FullName:
                return self.Teams[i].Acronym
        return None

    def replace_match(self, match_data: match.Class) -> bool:
        for i in range(len(self.Matches)):
            if match_data.ID == self.Matches[i].ID:
                self.Matches[i] = match_data
                return True
        return False

    def get_match_from_id(self, match_id: int) -> match.Class:
        for temp_match in self.Matches:
            if temp_match.ID == match_id:
                return temp_match

    def get_match_id(self, acronyms: [], case_insensitive: bool = True) -> int | None:
        for i in range(len(self.Matches)):
            if case_insensitive:
                match_acronyms = [self.Matches[i].Team1Acronym.lower(), self.Matches[i].Team2Acronym.lower()]
            else:
                match_acronyms = self.Matches[i].Acronyms
            if acronyms[0] in match_acronyms and acronyms[1] in match_acronyms:
                return i
        return None

# Using jsonpickle to avoid json encoding issues, like crashes on datatime (no clue what this means exactly, huh)
    def write_to_file(self, file_path: str) -> None:
        if file_path is None:
            file_path = "output.json"
        jp.set_encoder_options("json", indent=2)
        with codecs.open(file_path, "w", encoding="utf-8") as file:
            file.write(jp.encode(self, unpicklable=False))


def load_json(filename: str) -> Class:
    try:
        with codecs.open(filename, "r", encoding="utf-8") as file:
            logging.info("Loading json bracket from 'bracket.json'")
            return Class(**json.loads(file.read()))
    except FileNotFoundError:
        logging.error("Didn't find {}".format(filename))
        exit(-1)
