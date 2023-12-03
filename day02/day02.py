from dataclasses import dataclass
from enum import StrEnum
from collections import defaultdict

class Color(StrEnum):
    GREEN = "green"
    BLUE = "blue"
    RED = "red"

@dataclass
class Reveal:
    count: int
    color: Color

@dataclass
class Game:
    id: int
    reveals: list[list[Reveal]]

COLOR_MAX = {
    Color.GREEN: 13,
    Color.RED: 12,
    Color.BLUE: 14
}

def _is_possible(game: Game) -> bool:
    for l in game.reveals:
        for reveal in l:
            if reveal.count > COLOR_MAX[reveal.color]:
                return False

    return True

def _max_color(g: Game, c: Color):
    matching_colors = [r.count for l in g.reveals for r in l if r.color == c]
    if not matching_colors:
        return 0
    return max(matching_colors)

def _calculate_power(g: Game):
    max_red = _max_color(g, Color.RED)
    max_blue = _max_color(g, Color.BLUE)
    max_green = _max_color(g, Color.GREEN)

    return max_red * max_blue * max_green

def _parse_input_line(line: str) -> Game:
    tokens = line.split(' ')
    tokens.reverse()
    tokens.pop()

    game_id: int = int(tokens.pop().strip(':'))

    all_reveals: list[list[Reveal]] = []
    current_reveal: list[Reveal] = []

    all_reveals.append(current_reveal)

    while tokens:
        count = int(tokens.pop())
        color_token = tokens.pop()

        reveal = Reveal(count=count, color=Color(color_token.strip(';,')))
        separator = color_token[-1]

        current_reveal.append(reveal)

        if separator != ',':
            current_reveal = []
            all_reveals.append(current_reveal)

    return Game(id=game_id, reveals=all_reveals)


def part1(input: list[str]):
    games = [_parse_input_line(line) for line in input]

    print(sum(g.id for g in games if _is_possible(g)))


def part2(input: list[str]):
    games = [_parse_input_line(line) for line in input]
    print(sum(_calculate_power(g) for g in games))

def main():
    with open('input', 'r') as f:
        all_lines: list[str] = [l.strip() for l in f.readlines()]

        part1(all_lines)
        part2(all_lines)

if __name__ == "__main__":
    main()
