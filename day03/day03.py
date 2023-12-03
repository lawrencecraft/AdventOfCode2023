def pad_input(input: list[str]):
    input_width = len(input[0])

    padded_input: list[str] = []
    padded_input.append("." * (input_width + 2))
    padded_input.extend(f".{l}." for l in input)
    padded_input.append("." * (input_width + 2))
    return padded_input


def find_symbols(input_raw: list[str]):
    for x, l in enumerate(input_raw):
        for y, c in enumerate(l):
            if not c.isdigit() and c != ".":
                yield (x, y, c)


def visit_number(
    visited_row: list[bool], number_start: tuple[int, int], grid: list[str]
) -> int:
    row, start_col = number_start
    end_col = start_col

    visited_row[start_col] = True

    # find start x
    while grid[row][start_col - 1].isdigit():
        start_col -= 1
        visited_row[start_col] = True

    # find end x
    while grid[row][end_col + 1].isdigit():
        end_col += 1
        visited_row[end_col] = True

    return int(grid[row][start_col : end_col + 1])


def discover_part_numbers(
    visited: list[list[bool]], symbol_location: tuple[int, int], grid: list[str]
):
    row, col = symbol_location
    for drow in [-1, 0, 1]:
        for dcol in [-1, 0, 1]:
            new_row = row + drow
            new_col = col + dcol

            if grid[new_row][new_col].isdigit() and not visited[new_row][new_col]:
                yield visit_number(visited[new_row], (new_row, new_col), grid)


def find_all_neighbors(symbol_location: tuple[int, int], grid: list[str]):
    neighbors = []
    row, col = symbol_location
    for drow in [-1, 0, 1]:
        visited_row = [False for _ in grid[row]]
        for dcol in [-1, 0, 1]:
            new_row = row + drow
            new_col = col + dcol

            if grid[new_row][new_col].isdigit() and not visited_row[new_col]:
                neighbors.append(visit_number(visited_row, (new_row, new_col), grid))

    return neighbors


def part1(input_raw: list[str]):
    input = pad_input(input_raw)

    visited: list[list[bool]] = [[False for _ in l] for l in input]
    part_numbers: list[int] = []

    for row, col, _ in find_symbols(input):
        part_numbers.extend(discover_part_numbers(visited, (row, col), input))

    print(sum(part_numbers))


def part2(input_raw: list[str]):
    input = pad_input(input_raw)
    gear_ratios = 0
    for row, col, symbol in find_symbols(input):
        if (
            symbol == "*"
            and len(neighbors := find_all_neighbors((row, col), input)) == 2
        ):
            first, second = neighbors
            gear_ratios += first * second

    print(gear_ratios)


def main():
    with open("input", "r") as f:
        all_lines: list[str] = [l.strip() for l in f.readlines()]

        part1(all_lines)
        part2(all_lines)


if __name__ == "__main__":
    main()
