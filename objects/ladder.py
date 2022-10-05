import objects.bracket as bracket
import objects.ladder_legacy as ladder_legacy


def getMatchId(matchData):
    return matchData.ID


def extractRoundNames(rounds):
    names = []
    for entry in rounds:
        if entry.Name not in names:
            if entry.Name == "":
                names.append(entry.Description)
                continue
            names.append(entry.Name)
    return names


def scanMatches(bracketData, roundNames):
    ladderTree = []
    for i in range(len(roundNames)):
        ladderTree.append([])
    for i in range(len(roundNames)):
        for entry in bracketData.Matches:
            if entry.ID in bracketData.Rounds[i].Matches:
                ladderTree[i].append(entry)
        ladderTree[i].sort(key=getMatchId)
        if i >= 2 and len(ladderTree[i]) >= 3:
            amounfOfMovedMatches = 0
            j = int(len(ladderTree[0])/pow(2, i)) - 1
            while j < len(ladderTree[i]) - amounfOfMovedMatches - 1:
                j += 2
                ladderTree[i].insert(len(ladderTree[i]), ladderTree[i].pop(j))
                amounfOfMovedMatches += 1
    return ladderTree


class Class(object):
    def __init__(self, bracketData: bracket.Class):
        self.roundNames = extractRoundNames(bracketData.Rounds)
        self.ladder = scanMatches(bracketData, self.roundNames)

    def getMatches(self):
        matches = []
        for mappoolRound in self.ladder:
            for entry in mappoolRound:
                matches.append(entry)
        return matches

    def getMatchFromFourthRound(self, matchIndex, middleIndex, poolLength):
        if matchIndex >= middleIndex / 2:
            return self.ladder[3][matchIndex]
        if matchIndex >= 0:
            return self.ladder[3][matchIndex + middleIndex]
        if matchIndex >= -poolLength / 2:
            return self.ladder[3][matchIndex - int(poolLength / 2)]
        return self.ladder[3][matchIndex + int(poolLength / 2)]

    def getMatchFromFifthRound(self, matchIndex, middleIndex, poolLength):
        if matchIndex < -poolLength:
            return self.ladder[4][matchIndex]
        if -poolLength <= matchIndex < 0:
            return self.ladder[4][matchIndex + middleIndex]
        matchIndex = -matchIndex - int(poolLength / 2)
        if poolLength == 1:
            matchIndex = -matchIndex
        return self.ladder[4][matchIndex]

    def getMatchFromIdentifier(self, challongeMatchId: int):
        amountOfWinnerMatches = len(self.ladder[0]) * 2
        amountOfPassedWinnerMatches = 0
        totalAmountOfPassedMatches = 0
        maxRoundMatchId = amountOfWinnerMatches / 2
        for matches in self.ladder:
            totalAmountOfPassedMatches += len(matches)
            if challongeMatchId <= amountOfWinnerMatches:  # Winner's bracket
                if challongeMatchId <= maxRoundMatchId + amountOfPassedWinnerMatches:
                    matchId = challongeMatchId - amountOfPassedWinnerMatches
                    return matches[matchId - 1]
            else:  # Loser's bracket
                if matches is self.ladder[1]:
                    if challongeMatchId <= totalAmountOfPassedMatches + len(matches) / 2 + 1:
                        matchId = challongeMatchId - amountOfWinnerMatches + int(len(matches) / 2) - 2
                        return matches[matchId]
                testing = totalAmountOfPassedMatches + len(matches) / 4 + 1
                if matches is not self.ladder[0] and matches is not self.ladder[1]:
                    if challongeMatchId <= totalAmountOfPassedMatches + len(matches) / 4 + 1:
                        matchId = challongeMatchId - totalAmountOfPassedMatches + len(matches) - int(maxRoundMatchId * 2) - 2 + int(maxRoundMatchId)
                        if matches is self.ladder[-1]:
                            return matches[-2]
                        return matches[matchId]
            amountOfPassedWinnerMatches += int(maxRoundMatchId)
            maxRoundMatchId /= 2
        if challongeMatchId == amountOfWinnerMatches:
            return self.ladder[-1][0]
        return None

    def getMatch(self, challongeMatchId: int, isIdentifier: bool = False):
        if isIdentifier:
            return self.getMatchFromIdentifier(challongeMatchId)
        return ladder_legacy.getMatchFromSuggestedOrder(self, challongeMatchId)
