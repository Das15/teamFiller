from gui.image_generation.match_style import MatchStyle
from gui.image_generation.position import Position
from PIL import ImageFont, ImageDraw
from sys import platform

if platform in ["linux", "linux2"]:
    TEAM_FONT = ImageFont.truetype("FreeSerif.ttf", 16)
else:
    TEAM_FONT = ImageFont.truetype("bahnschrift.ttf", 17)


def draw_name(name: str, canvas: ImageDraw, coords: list[int, int]) -> None:
    if name:
        name = name.upper()
        if len(name) > 3:
            name = name[0:2]
    else:
        name = ""
    canvas.text(coords, name, font=TEAM_FONT, fill=(0, 0, 0, 255))


class MatchBox(object):
    def __init__(self, Coordinates: Position, Team1Name: str, Team2Name: str, Scores: list[int, int],
                 Style: MatchStyle = MatchStyle()):
        self.Coordinates = Coordinates
        self.Team1Name = Team1Name
        self.Team2Name = Team2Name
        for i in range(len(Scores)):
            if not Scores[i]:
                Scores[i] = 0
        self.Scores = Scores
        self.Style = Style

    def draw_team_names(self, canvas: ImageDraw) -> None:
        points = [self.Coordinates.X + self.Style.Padding, self.Coordinates.Y + self.Style.Padding]
        draw_name(self.Team1Name, canvas, points)
        points[1] += self.Style.RectHeight
        draw_name(self.Team2Name, canvas, points)

    def draw_scores(self, canvas: ImageDraw) -> None:
        beginning_point = [self.Coordinates.X + self.Style.RectWidth * self.Style.NameToScoreRatio + self.Style.Padding,
                           self.Coordinates.Y + self.Style.Padding]
        canvas.text(beginning_point, str(self.Scores[0]), font=TEAM_FONT, fill=(0, 0, 0, 255))
        beginning_point[1] += self.Style.RectHeight
        canvas.text(beginning_point, str(self.Scores[1]), font=TEAM_FONT, fill=(0, 0, 0, 255))

    def draw_match(self, canvas: ImageDraw) -> None:
        beginning_point = self.Coordinates.list()
        vertex = [self.Coordinates.X + self.Style.RectWidth, self.Coordinates.Y + self.Style.RectHeight]
        canvas.rectangle(beginning_point + vertex, outline="black")

        beginning_point = [self.Coordinates.X, self.Coordinates.Y + self.Style.RectHeight]
        vertex = [self.Coordinates.X + self.Style.RectWidth, self.Coordinates.Y + self.Style.RectHeight*2]
        canvas.rectangle(beginning_point + vertex, outline="black")

        self.draw_team_names(canvas)
        if self.Team1Name is not None or self.Team2Name is not None:
            self.draw_scores(canvas)

        beginning_point = [self.Coordinates.X + self.Style.RectWidth * self.Style.NameToScoreRatio, self.Coordinates.Y]
        vertex = [self.Coordinates.X + self.Style.RectWidth * self.Style.NameToScoreRatio,
                  self.Coordinates.Y + self.Style.RectHeight*2]
        canvas.line(beginning_point + vertex, fill=0)
