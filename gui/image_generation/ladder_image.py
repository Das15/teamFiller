import objects.bracket as Bracket
from gui.image_generation.match_box import MatchBox
from gui.image_generation.position import Position
import math
from PIL import Image, ImageDraw


def get_required_canvas_size(bracket) -> tuple[int, int]:
    max_x = max(bracket.Matches, key=lambda match: match.Position["X"]).Position["X"]
    max_y = max(bracket.Matches, key=lambda match: match.Position["Y"]).Position["Y"]

    return math.ceil(max_x/300)*300, math.ceil(max_y/300)*300


def gen_empty_image(bracket):
    image_size = get_required_canvas_size(bracket)
    img = Image.new("RGB", image_size, (255, 255, 255))
    return img


class LadderImage(object):
    def __init__(self, bracket: Bracket.Class):
        self.bracket = bracket
        self.image = gen_empty_image(self.bracket)
        self.canvas = ImageDraw.Draw(self.image)
        self.matches = self.parse_matches()

    def draw_matches(self):
        for match in self.matches:
            match.draw_match(self.canvas)

    def parse_matches(self):
        output = []
        for match in self.bracket.Matches:
            temp = MatchBox(Position(match.Position["X"], match.Position["Y"]), match.Team1Acronym,
                            match.Team2Acronym, [match.Team1Score, match.Team2Score])
            output.append(temp)
        return output


if __name__ == "__main__":
    BRACKET = Bracket.load_json("bracket.json")
    test = LadderImage(BRACKET)
    test.draw_matches()
    test.image.show()
