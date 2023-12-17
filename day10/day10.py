from collections import deque


def pad_input(input: list[str]) -> list[str]:
    padded_input = []
    padded_input.append("".join("." for _ in range(len(input[0]) + 2)))
    padded_input.extend(f".{i}." for i in input)
    padded_input.append("".join("." for _ in range(len(input[0]) + 2)))

    return padded_input


def find_start(grid: list[str]) -> tuple[int, int]:
    for row_idx, row in enumerate(grid):
        for col_idx, col in enumerate(row):
            if col == "S":
                return row_idx, col_idx

    raise Exception("No start")


def connected_nodes(grid: list[str], row: int, col: int):
    if grid[row][col + 1] in ["-", "7", "J"]:
        yield (row, col + 1)

    if grid[row][col - 1] in ["-", "F", "L"]:
        yield (row, col - 1)

    if grid[row - 1][col] in ["|", "F", "7"]:
        yield (row - 1, col)

    if grid[row + 1][col] in ["|", "J", "L"]:
        yield (row + 1, col)


SYM_2_OFFSET = {
    "|": [(1, 0), (-1, 0)],
    "-": [(0, 1), (0, -1)],
    "F": [(1, 0), (0, 1)],
    "J": [(0, -1), (-1, 0)],
    "7": [(0, -1), (1, 0)],
    "L": [(0, 1), (-1, 0)],
}


def possible_nodes(row: int, col: int, symbol: str):
    for dr, dc in SYM_2_OFFSET[symbol]:
        yield (dr + row, dc + col)


def print_grid(grid: list[list[int | None]], padding=1):
    for i in grid:
        print(
            "".join(
                ".".rjust(padding) if j == None else str(j).rjust(padding) for j in i
            )
        )


def find_furthest(grid: list[str]) -> tuple[int, list[list[int | None]]]:
    visited: list[list[int | None]] = [[None for _ in r] for r in grid]
    start_row, start_col = find_start(grid)

    highest_seen = 0

    to_visit: deque[tuple[int, int, int]] = deque([(0, start_row, start_col)])
    visited[start_row][start_col] = 0

    while to_visit:
        current_distance, current_row, current_col = to_visit.popleft()

        if current_distance > highest_seen:
            highest_seen = current_distance

        next_distance = current_distance + 1

        next_gen = (
            connected_nodes(grid, current_row, current_col)
            if current_distance == 0
            else possible_nodes(
                current_row, current_col, grid[current_row][current_col]
            )
        )

        for node_row, node_col in next_gen:
            if visited[node_row][node_col] is not None:
                continue

            visited[node_row][node_col] = next_distance
            to_visit.append((next_distance, node_row, node_col))

    return highest_seen, visited


def part1(input: list[str]):
    padded_input = pad_input(input)
    print(find_furthest(padded_input)[0])


def part2(input: list[str]):
    padded_input = pad_input(input)
    padded_input = [list(s) for s in padded_input]
    _, visited = find_furthest(padded_input)
    num_inside = 0

    for row_idx, row in enumerate(padded_input):
        for col_idx, col in enumerate(row):
            if visited[row_idx][col_idx] is not None:
                continue

            inside = False
            current_col = col_idx + 1

            for right in range(current_col, len(row)):
                if visited[row_idx][right] is None:
                    continue

                if row[right] in ("F", "7", "|", "S"):
                    inside = not inside

            if inside:
                padded_input[row_idx][col_idx] = "I"
                num_inside += 1
            else:
                padded_input[row_idx][col_idx] = "O"
    # print_grid(visited, padding=3)
    # print_grid(padded_input)
    print(num_inside)


def main():
    with open("input", "r") as f:
        all_lines: list[str] = [l.strip() for l in f.readlines()]

        part1(all_lines)
        part2(all_lines)


if __name__ == "__main__":
    main()
