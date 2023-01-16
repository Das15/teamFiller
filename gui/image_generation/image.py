import math
from PIL import Image, ImageDraw, ImageFont

import objects.match as Match
import objects.bracket as Bracket

TEAM_FONT = ImageFont.truetype("bahnschrift.ttf", 17)
BRACKET = Bracket.load_json("bracket.json")


def get_required_canvas_size(bracket=BRACKET):
    max_x = max(bracket.Matches, key=lambda match: match.Position["X"]).Position["X"]
    max_y = max(bracket.Matches, key=lambda match: match.Position["Y"]).Position["Y"]

    return math.ceil(max_x/300)*300, math.ceil(max_y/300)*300


def draw_text(x: int, y: int, text: str, canvas: ImageDraw):
    if text:
        text = text.upper()
    else:
        text = ""
    canvas.text((x, y), text, font=TEAM_FONT, fill=(0, 0, 0, 255))


def gen_match(x: int, y: int, canvas: ImageDraw, match: Match.Class):
    rect_width = 65
    rect_height = 25
    padding = 5
    label_size = 0.7
    score_pos = int(x+rect_width*label_size)

    canvas.rectangle((x, y) + (x+rect_width, y+rect_height), outline="black")
    canvas.rectangle((x, y+rect_height) + (x+rect_width, y+rect_height*2), outline="black")

    draw_text(x+padding, y+padding, match.Team1Acronym, canvas)
    draw_text(x+padding, y+padding+rect_height, match.Team2Acronym, canvas)

    canvas.line(((score_pos, y), (score_pos, y+rect_height*2)), fill=0)

    draw_scores((score_pos + padding, y + padding), match.Team1Score, canvas)
    draw_scores((score_pos+padding, y+padding+rect_height), match.Team2Score, canvas)


def draw_scores(coordinates: tuple[int, int], score: int, canvas):
    if not score:
        score = 0
    canvas.text(coordinates, str(score), font=TEAM_FONT, fill=(0, 0, 0, 255))


def gen_empty_image(sizeWidthHeight: tuple[int, int]):

    img = Image.new("RGB", sizeWidthHeight, (255, 255, 255))
    return img


def gen_using_bracket_coords(cursor, bracket=BRACKET):
    for match in bracket.Matches:
        gen_match(match.Position["X"], match.Position["Y"], cursor, match)


def main():
    img = gen_empty_image(get_required_canvas_size())
    cursor = ImageDraw.Draw(img)
    gen_using_bracket_coords(cursor)

    img.show()


if __name__ == '__main__':
    main()
