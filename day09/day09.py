def get_next_element(input_key: list[int]):
    if input_key == [0 for _ in input_key]:
        return 0

    parent_series = [i - input_key[idx] for idx, i in enumerate(input_key[1:])]
    return input_key[-1] + get_next_element(parent_series)


def parse_row(row: str):
    return [int(x) for x in row.split(" ")]


def part1(input: list[str]):
    parsed_input = [parse_row(x) for x in input]

    print(sum(map(get_next_element, parsed_input)))


def part2(input: list[str]):
    parsed_input = [list(reversed(parse_row(x))) for x in input]

    print(sum(map(get_next_element, parsed_input)))


def main():
    with open("input", "r") as f:
        all_lines: list[str] = [l.strip() for l in f.readlines()]

        part1(all_lines)
        part2(all_lines)


if __name__ == "__main__":
    main()
