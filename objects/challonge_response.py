import objects.bracket as bracket
import objects.ladder as ladder
import logging


ALPHABET_LENGTH = 26


def getMatchId(identifier):
    id = 0
    exponential = 0
    for i in reversed(range(len(identifier))):
        orderOfLetter = ord(identifier[i]) - 64
        id += (ALPHABET_LENGTH ** exponential) * orderOfLetter
        exponential += 1
    return id


def assignScores(matchData, scores):
    if scores[0] != "" and scores[1] != "":
        if scores[1] == "-1":
            matchData.Team1Score = matchData.PointsToWin
            matchData.Team2Score = "0"
        elif scores[0] == "-1":
            matchData.Team1Score = "0"
            matchData.Team2Score = matchData.PointsToWin
        else:
            matchData.Team1Score = scores[0]
            matchData.Team2Score = scores[1]
    else:
        matchData.Team1Score = "0"
        matchData.Team2Score = "0"
    return matchData


class Class(object):
    def __init__(self, body):
        self._body = body

    def getPlayerName(self, playerId):
        for player in self.body["participants"]:
            if player["id"] == playerId:
                return player["name"]
        return None

    @property
    def body(self):
        return self._body

    def replaceAcronyms(self, bracketData: bracket.Class):
        ladderData = ladder.Class(bracketData)
        for i in range(len(self.body["matches"])):
            challongeMatch = self.body["matches"][i]
            try:
                if challongeMatch["player1_id"] is None or challongeMatch["player2_id"] is None:
                    continue
                teamNames = [self.getPlayerName(challongeMatch["player1_id"]),
                             self.getPlayerName((challongeMatch["player2_id"]))]
                acronyms = [bracketData.getAcronymFromName(teamNames[0]), bracketData.getAcronymFromName(teamNames[1])]
                matchId = getMatchId(challongeMatch["identifier"])
                bracketMatch = ladderData.getMatch(matchId, True)
                minusPos = challongeMatch["scores_csv"].find("-")
                if minusPos == 0:
                    scores = [0, bracketMatch.PointsToWin]
                else:
                    scores = [challongeMatch["scores_csv"][0:minusPos], challongeMatch["scores_csv"][minusPos+1:]]
                bracketMatch.replaceAcronyms(acronyms)
                bracketMatch = assignScores(bracketMatch, scores)
                bracketMatch.Completed = True
                bracketMatch.Current = False
                bracketData.replaceMatch(bracketMatch)
            except AttributeError:
                logging.fatal(f'Cannot find match id {challongeMatch["suggested_play_order"]} in bracket json file.')
                print("Fatal error, read logs for details.")
                exit(1)
        logging.info(f"Processed {len(self.body['matches'])} matches from challonge response.")
        return bracketData
