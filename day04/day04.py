from dataclasses import dataclass


@dataclass
class Scratchcard:
    id: int
    winners: list[int]
    picks: list[int]


def match_count(line: str):
    left, right = line.split("|")

    left_tokens = [t for t in reversed(left.split(" ")) if t]
    right_tokens = [t for t in reversed(right.split(" ")) if t]

    left_tokens.pop()
    left_tokens.pop()

    winners = set(int(x) for x in left_tokens)
    picks = set(int(x) for x in right_tokens)

    winning_picks = winners.intersection(picks)

    return len(winning_picks)


def score_card(line: str):
    matches = match_count(line)
    if not matches:
        return 0
    return 1 << (match_count(line) - 1)


def part1(input_raw: list[str]):
    print(sum(score_card(l) for l in input_raw))


def part2(input_raw: list[str]):
    card_counts = [1 for _ in input_raw]

    for idx, line in enumerate(input_raw):
        matched = match_count(line)
        incr_amount = card_counts[idx]

        for i in range(matched):
            card_counts[idx + i + 1] += incr_amount

    print(sum(card_counts))


def main():
    with open("input", "r") as f:
        all_lines: list[str] = [l.strip() for l in f.readlines()]

        part1(all_lines)
        part2(all_lines)


if __name__ == "__main__":
    main()
