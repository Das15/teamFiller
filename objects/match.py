from dataclasses import dataclass
from typing import Any


@dataclass
class Class(object):
    ID: int
    Team1Acronym: str = None
    Team1Score: int = None
    Team2Acronym: str = None
    Team2Score: int = None
    Completed: bool = None
    Losers: bool = None
    PicksBans: [] = list[Any]
    Current: bool = None
    Date: str = None
    ConditionalMatches: [] = list[Any]
    Position: {} = dict[Any]
    Acronyms: [] = list[Any]
    WinnerColour: str = None
    PointsToWin: int = None

    def replace_acronyms(self, new_acronyms: []):
        self.Team1Acronym = new_acronyms[0]
        self.Team2Acronym = new_acronyms[1]
        self.Acronyms = new_acronyms
