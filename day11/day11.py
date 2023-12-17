def part1(input: list[str]):
    pass


def part2(input: list[str]):
    pass


def main():
    with open('input', 'r') as f:
        all_lines: list[str] = [l.strip() for l in f.readlines()]

        part1(all_lines)
        part2(all_lines)


if __name__ == "__main__":
    main()
