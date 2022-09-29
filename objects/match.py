class Class(object):
    def __init__(self, ID, Team1Acronym=None, Team1Score=None, Team2Acronym=None, Team2Score=None, Completed=None,
                 Losers=None, PicksBans=None, Current=None, Date=None, ConditionalMatches=None, Position=None,
                 Acronyms=None, WinnerColour=None, PointsToWin=None):
        if PicksBans is None:
            PicksBans = []
        self.ID = ID
        self.Team1Acronym = Team1Acronym
        self.Team1Score = Team1Score
        self.Team2Acronym = Team2Acronym
        self.Team2Score = Team2Score
        self.Completed = Completed
        self.Losers = Losers
        self.PicksBans = PicksBans
        self.Current = Current
        self.Date = Date
        self.ConditionalMatches = ConditionalMatches
        self.Position = Position
        self.Acronyms = Acronyms
        self.WinnerColour = WinnerColour
        self.PointsToWin = PointsToWin

    def replaceAcronyms(self, newAcronyms: []):
        self.Team1Acronym = newAcronyms[0]
        self.Team2Acronym = newAcronyms[1]
        self.Acronyms = newAcronyms
