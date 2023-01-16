import objects.match as Match
from gui.image_generation.position import Position
from PIL import ImageFont


class MatchBox(object):
    def __init__(self, Coordinates: Position, Team1: Match.Class, Team2: Match.Class, Scores, Font: ImageFont):
        self.Coordinates = Coordinates
        self.Team1 = Team1
        self.Team2 = Team2
        self.Scores = Scores
        self.Font = Font
