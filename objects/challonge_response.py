import logging
import re

import objects.bracket as bracket
import objects.ladder as ladder
import objects.match as match


ALPHABET_LENGTH = 26


def get_match_id(identifier: str) -> int:
    # Converting from ascii characters was an interesting problem to solve.
    match_id = 0
    exponential = 0
    for i in reversed(range(len(identifier))):
        position_of_letter = ord(identifier[i]) - 64
        match_id += (ALPHABET_LENGTH ** exponential) * position_of_letter
        exponential += 1
    return match_id


def assign_scores(match_data: match.Class, scores: []) -> match.Class:
    # I'm fairly certain this can be simplified further
    if scores[0] != "" and scores[1] != "":
        if scores[1] == "-1":
            match_data.Team1Score = match_data.PointsToWin
            match_data.Team2Score = "-1"
        elif scores[0] == "-1":
            match_data.Team1Score = "-1"
            match_data.Team2Score = match_data.PointsToWin
        else:
            match_data.Team1Score = scores[0]
            match_data.Team2Score = scores[1]
    else:
        match_data.Team1Score = "0"
        match_data.Team2Score = "0"
    return match_data


def count_scores(scores: str) -> []:
    returned_score = [0, 0]
    parsed_scores = scores.split(",")
    for score_line in parsed_scores:
        score = [int(entry) for entry in score_line.split("-")]
        returned_score[0] += score[0]
        returned_score[1] += score[1]
    return returned_score


def calculate_scores(scores: str) -> []:
    parsing_regex = r"-{0,1}[0-9]{1,2}"
    parsed_scores = re.findall(parsing_regex, scores)

    # First case, score contains the collection of points, we need to count
    if "," in scores:
        return count_scores(scores)
    # Second case, score string contains the final value, we dont need to count
    # If the second score is not WBD, strip leading minus
    if parsed_scores[1] != "-1" or parsed_scores[0] == "-1":
        parsed_scores[1] = parsed_scores[1][1:]
    return parsed_scores


class Class(object):
    def __init__(self, body):
        self._body = body

    def get_team_name(self, team_id):
        for player in self.body["participants"]:
            temp = player
            if temp["id"] == team_id:
                return temp["name"]
        logging.error(f"Didn't find player {team_id} in challonge response.")
        return None

    @property
    def body(self):
        return self._body

    def replace_acronyms(self, bracket_data: bracket.Class) -> bracket.Class:
        ladder_data = ladder.Class(bracket_data)
        if not self.body:
            logging.fatal("Did not receive JSON response!")
            exit(-1)
        for i in range(len(self.body["matches"])):
            challonge_match = self.body["matches"][i]
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
                if not challonge_match.get("scores_csv"):
                    scores = [0, 0]
                else:
                    scores = calculate_scores(challonge_match["scores_csv"])
                    logging.debug(f"Parsed {challonge_match["scores_csv"]} as "
                                  f"Team1: {scores[0]}, Team2: {scores[1]}.")
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
