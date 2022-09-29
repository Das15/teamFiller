import objects.bracket as bracket


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

    # TODO: Refactor this function
    def getMatchFromSuggestedOrder(self, challongeMatchId: int):
        internalMatchId = challongeMatchId - 1
        poolLength = len(self.ladder[0])
        i = 0
        passedMatchesCount = 0
        checksFulfilled = 0
        # Why the fuck is this loop so hard to read?
        while checksFulfilled < 3:
            if i == 0:
                if challongeMatchId <= poolLength:
                    return self.ladder[i][internalMatchId]
                passedMatchesCount = poolLength
            else:
                if checksFulfilled == 0:
                    passedMatchesCount += poolLength * 2 if i == 1 else poolLength * 4
                else:
                    passedMatchesCount += 1
                if challongeMatchId <= passedMatchesCount:
                    # Offset what? Why did i make it like this? I don't get it
                    offset = passedMatchesCount - poolLength
                    matchCount = poolLength * 4
                    if checksFulfilled > 1:
                        matchCount -= 1
                    middleIndex = int(matchCount / 2)
                    if i % 2 == 0:
                        if challongeMatchId > offset and i != len(self.ladder) - 1:
                            return self.ladder[i][internalMatchId - passedMatchesCount + poolLength]
                        if i == 4:
                            matchIndex = internalMatchId - passedMatchesCount + middleIndex
                            return self.getMatchFromFifthRound(matchIndex, middleIndex, poolLength)
                        matchIndex = -challongeMatchId + passedMatchesCount - poolLength
                        if matchIndex < poolLength:
                            matchIndex = -challongeMatchId + passedMatchesCount - middleIndex
                        return self.ladder[i][matchIndex]

                    if challongeMatchId > offset:
                        return self.ladder[i][internalMatchId - passedMatchesCount + poolLength]
                    if i == 3:
                        matchIndex = -challongeMatchId + passedMatchesCount - middleIndex
                        return self.getMatchFromFourthRound(matchIndex, middleIndex, poolLength)
                    return self.ladder[i][internalMatchId - passedMatchesCount + poolLength]
            i += 1
            poolLength = int(poolLength / 2)
            if poolLength < 1:
                checksFulfilled += 1
                poolLength = 1
            i = i if i < len(self.ladder) else len(self.ladder) - 1
        if challongeMatchId == len(self.ladder[0]) * 4 - 1:
            return self.ladder[i][-1]
        return None

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
        return self.getMatchFromSuggestedOrder(challongeMatchId)
