# TODO: Refactor this function
def getMatchFromSuggestedOrder(ladderObj, challongeMatchId: int):
    internalMatchId = challongeMatchId - 1
    poolLength = len(ladderObj.ladder[0])
    i = 0
    passedMatchesCount = 0
    checksFulfilled = 0
    # Why the fuck is this loop so hard to read?
    while checksFulfilled < 3:
        if i == 0:
            if challongeMatchId <= poolLength:
                return ladderObj.ladder[i][internalMatchId]
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
                    if challongeMatchId > offset and i != len(ladderObj.ladder) - 1:
                        return ladderObj.ladder[i][internalMatchId - passedMatchesCount + poolLength]
                    if i == 4:
                        matchIndex = internalMatchId - passedMatchesCount + middleIndex
                        return ladderObj.getMatchFromFifthRound(matchIndex, middleIndex, poolLength)
                    matchIndex = -challongeMatchId + passedMatchesCount - poolLength
                    if matchIndex < poolLength:
                        matchIndex = -challongeMatchId + passedMatchesCount - middleIndex
                    return ladderObj.ladder[i][matchIndex]

                if challongeMatchId > offset:
                    return ladderObj.ladder[i][internalMatchId - passedMatchesCount + poolLength]
                if i == 3:
                    matchIndex = -challongeMatchId + passedMatchesCount - middleIndex
                    return ladderObj.getMatchFromFourthRound(matchIndex, middleIndex, poolLength)
                return ladderObj.ladder[i][internalMatchId - passedMatchesCount + poolLength]
        i += 1
        poolLength = int(poolLength / 2)
        if poolLength < 1:
            checksFulfilled += 1
            poolLength = 1
        i = i if i < len(ladderObj.ladder) else len(ladderObj.ladder) - 1
    if challongeMatchId == len(ladderObj.ladder[0]) * 4 - 1:
        return ladderObj.ladder[i][-1]
    return None
