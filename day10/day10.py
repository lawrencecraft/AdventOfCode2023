from collections import deque


def pad_input(input: list[str]):
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


def print_grid(grid: list[list[int | None]]):
    for i in grid:
        print("".join("." if j == None else str(j) for j in i))


def find_furthest(grid: list[str]) -> int:
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

        for node_row, node_col in connected_nodes(grid, current_row, current_col):
            if visited[node_row][node_col] is not None:
                continue

            visited[node_row][node_col] = next_distance
            to_visit.append((next_distance, node_row, node_col))

    # print_grid(visited)
    return highest_seen


def part1(input: list[str]):
    padded_input = pad_input(input)
    print(find_furthest(padded_input))
    # print(list(connected_nodes(padded_input, 3, 4)))


def part2(input: list[str]):
    pass


def main():
    with open("input", "r") as f:
        all_lines: list[str] = [l.strip() for l in f.readlines()]

        part1(all_lines)
        part2(all_lines)


if __name__ == "__main__":
    main()
