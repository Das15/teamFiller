import logging

import objects.bracket as bracket
import objects.ladder as ladder
import objects.match as match


ALPHABET_LENGTH = 26


def get_match_id(identifier: str) -> int:
    match_id = 0
    exponential = 0
    for i in reversed(range(len(identifier))):
        position_of_letter = ord(identifier[i]) - 64
        match_id += (ALPHABET_LENGTH ** exponential) * position_of_letter
        exponential += 1
    return match_id


def assign_scores(match_data: match.Class, scores: []) -> match.Class:
    if scores[0] != "" and scores[1] != "":
        if scores[1] == "-1":
            match_data.Team1Score = match_data.PointsToWin
            match_data.Team2Score = "0"
        elif scores[0] == "-1":
            match_data.Team1Score = "0"
            match_data.Team2Score = match_data.PointsToWin
        else:
            match_data.Team1Score = scores[0]
            match_data.Team2Score = scores[1]
    else:
        match_data.Team1Score = "0"
        match_data.Team2Score = "0"
    return match_data


class Class(object):
    def __init__(self, body):
        self._body = body

    def get_team_name(self, team_id):
        for player in self.body["participants"]:
            temp = player["participant"]
            if temp["id"] == team_id:
                return temp["name"]
        return None

    @property
    def body(self):
        return self._body

    def replace_acronyms(self, bracket_data: bracket.Class) -> bracket.Class:
        ladder_data = ladder.Class(bracket_data)
        for i in range(len(self.body["matches"])):
            challonge_match = self.body["matches"][i]["match"]
            try:
                if challonge_match["player1_id"] is None or challonge_match["player2_id"] is None:
                    continue
                team_names = [self.get_team_name(challonge_match["player1_id"]),
                              self.get_team_name((challonge_match["player2_id"]))]
                acronyms = [bracket_data.get_acronym_from_name(team_names[0]),
                            bracket_data.get_acronym_from_name(team_names[1])]
                match_id = get_match_id(challonge_match["identifier"])
                bracket_match = ladder_data.get_match(match_id, True)
                minus_pos = challonge_match["scores_csv"].find("-")
                if minus_pos == 0:
                    scores = [0, bracket_match.PointsToWin]
                else:
                    scores = [challonge_match["scores_csv"][0:minus_pos], challonge_match["scores_csv"][minus_pos+1:]]
                bracket_match.replace_acronyms(acronyms)
                bracket_match = assign_scores(bracket_match, scores)
                bracket_match.Completed = True
                bracket_match.Current = False
                bracket_data.replace_match(bracket_match)
            except AttributeError:
                logging.fatal(f'Cannot find match id {challonge_match["suggested_play_order"]} in bracket json file.')
                print("Fatal error, read logs for details.")
                exit(1)
        logging.info(f"Processed {len(self.body['matches'])} matches from challonge response.")
        return bracket_data
