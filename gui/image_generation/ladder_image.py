import objects.bracket as Bracket
from gui.image_generation.match_box import MatchBox
from gui.image_generation.position import Position
from gui.image_generation.match_style import MatchStyle
import math
from PIL import Image, ImageDraw


def get_required_canvas_size(bracket) -> tuple[int, int]:
    max_x = max(bracket.Matches, key=lambda match: match.Position["X"]).Position["X"]
    max_y = max(bracket.Matches, key=lambda match: match.Position["Y"]).Position["Y"]

    return math.ceil(max_x / 300) * 300, math.ceil(max_y / 300) * 300


def gen_empty_image(bracket):
    image_size = get_required_canvas_size(bracket)
    img = Image.new("RGB", image_size, (255, 255, 255))
    return img


class LadderImage(object):
    def __init__(self, bracket: Bracket.Class):
        self.bracket = bracket
        self.image = gen_empty_image(self.bracket)
        self.canvas = ImageDraw.Draw(self.image)
        self.style = MatchStyle()
        self.matches = self.parse_matches()

    def draw_matches(self):
        for match in self.matches:
            match.draw_match(self.canvas)

    def parse_matches(self):
        output = []
        for match in self.bracket.Matches:
            temp = MatchBox(Position(match.Position["X"], match.Position["Y"]), match.Team1Acronym,
                            match.Team2Acronym, [match.Team1Score, match.Team2Score], self.style)
            output.append(temp)
        return output

    def draw_connections(self):
        has_passed_losers_bracket = False

        for progression in self.bracket.Progressions:
            if "Losers" in progression:
                continue
            source_id_match = self.bracket.get_match_from_id(progression["SourceID"])
            target_id_match = self.bracket.get_match_from_id(progression["TargetID"])

            if source_id_match.Losers != target_id_match.Losers:
                if not has_passed_losers_bracket:
                    has_passed_losers_bracket = True
                    continue
            self.draw_connection_lines(source_id_match, target_id_match)

    def draw_connection_lines(self, source_id_match, target_id_match):
        beginning_point = [source_id_match.Position["X"] + self.style.RectWidth + 5,
                           source_id_match.Position["Y"] + self.style.RectHeight]
        first_line_coords = beginning_point + [beginning_point[0] + 10, beginning_point[1]]
        self.canvas.line(first_line_coords, fill="black", width=1)

        second_line_coords = [first_line_coords[2], first_line_coords[3]] + \
                             [first_line_coords[2], target_id_match.Position["Y"] + self.style.RectHeight]
        self.canvas.line(second_line_coords, fill="black", width=1)

        third_line_coords = [second_line_coords[2], second_line_coords[3]] + \
                            [target_id_match.Position["X"] - 5, second_line_coords[3]]
        self.canvas.line(third_line_coords, fill="black", width=1)


if __name__ == "__main__":
    BRACKET = Bracket.load_json("bracket.json")
    test = LadderImage(BRACKET)
    test.draw_matches()
    test.draw_connections()
    test.image.show()
