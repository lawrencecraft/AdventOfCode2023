WORDS = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

WORD_TO_DIGIT_MAP = {
    value: idx for idx, value in enumerate(WORDS)
}

def get_first_last_digit(line: str) -> tuple[int, int]:
    just_nums = [int(c) for c in line if c.isdigit()]
    return just_nums[0], just_nums[-1]

def part1(input: list[str]):
    all_nums = [first * 10 + last for first, last in map(get_first_last_digit, input)]
    print(sum(all_nums))

def get_digits(line: str):
    for i, c in enumerate(line):
        if c.isdigit():
            yield int(c)
        
        for word in WORDS:
            if line[i:].startswith(word):
                yield WORD_TO_DIGIT_MAP[word]

def part2(input: list[str]):
    digits = (list(get_digits(l)) for l in input)
    first_last = [d[0] * 10 + d[-1] for d in digits]

    print(sum(first_last))


def main():
    with open('input', 'r') as f:
        all_lines: list[str] = [l.strip() for l in f.readlines()]

        part1(all_lines)
        part2(all_lines)

if __name__ == "__main__":
    main()
