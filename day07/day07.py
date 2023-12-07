from collections import Counter
from typing import Generator

HANDS = [[5], [4, 1], [3, 2], [3, 1, 1], [2, 2, 1], [2, 1, 1, 1], [1, 1, 1, 1, 1]]

HAND_STRENGTH_P1 = "23456789TJQKA"
HAND_STRENGTH_P2 = "J23456789TQKA"


def base_hand_comparison_key(hand: str) -> tuple[int, int]:
    sorted_counts = sorted(Counter(hand).values(), reverse=True)
    return (len(sorted_counts), -sorted_counts[0])


def hand_comparison_key(hand: str, hand_strengths: str):
    hand_key = []
    l, m = base_hand_comparison_key(hand)
    hand_key.append(l)
    hand_key.append(m)
    hand_key.extend(-hand_strengths.index(h) for h in hand)

    return tuple(hand_key)


def generate_all_combinations(hand: str) -> Generator[str, None, None]:
    for nc in HAND_STRENGTH_P2[1:]:
        full_hand = hand.replace("J", nc)
        yield full_hand


def get_comparison_key_with_joker(hand: str):
    if "J" not in hand:
        return hand_comparison_key(hand, HAND_STRENGTH_P2)

    f, s = min(base_hand_comparison_key(h) for h in generate_all_combinations(hand))

    return (f, s, *[-HAND_STRENGTH_P2.index(h) for h in hand])


def parse_input(input: list[str]) -> list[tuple[str, int]]:
    split_lines = [l.split(" ") for l in input]
    return [(h, int(bet)) for h, bet in split_lines]


def part1(input: list[str]):
    all_hands = parse_input(input)

    all_hands.sort(
        key=lambda x: hand_comparison_key(x[0], HAND_STRENGTH_P1), reverse=True
    )

    print(sum((rank + 1) * bet for rank, (_, bet) in enumerate(all_hands)))


def part2(input: list[str]):
    all_hands = parse_input(input)

    all_hands.sort(key=lambda x: get_comparison_key_with_joker(x[0]), reverse=True)

    print(sum((rank + 1) * bet for rank, (_, bet) in enumerate(all_hands)))


def main():
    with open("input", "r") as f:
        all_lines: list[str] = [l.strip() for l in f.readlines()]

        part1(all_lines)
        part2(all_lines)


if __name__ == "__main__":
    main()
