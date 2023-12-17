from itertools import combinations

def calculate_offset_array(galaxy: list[str]) -> tuple[list[int], list[int]]:
    offset_array_row = []
    empty_rows_seen = 0
    for row in galaxy:
        if row == '.' * len(row):
            empty_rows_seen += 1
        offset_array_row.append(empty_rows_seen)

    offset_array_col = []
    empty_cols_seen = 0
    for col_idx in range(len(galaxy[0])):
        full_column = [g[col_idx] for g in galaxy]

        if set(full_column) == {'.'}:
            empty_cols_seen += 1
        
        offset_array_col.append(empty_cols_seen)

    return offset_array_row, offset_array_col

def fetch_galaxies(input: list[str]):
    galaxies = []
    for row_idx, row in enumerate(input):
        for col_idx, col in enumerate(row):
            if col == '#':
                galaxies.append((row_idx, col_idx))

    return galaxies

def calc_distance(input: list[str], scaling_factor: int):
    offset_array_row, offset_array_col = calculate_offset_array(input)
    galaxies = [(row + offset_array_row[row] * scaling_factor, col + offset_array_col[col] * scaling_factor) for row, col in fetch_galaxies(input)]

    total_distance = 0

    for ((row1, col1), (row2, col2)) in combinations(galaxies, 2):
        total_distance += abs(row2 - row1)
        total_distance += abs(col2 - col1)

    return (total_distance)

def part1(input: list[str]):
    print(calc_distance(input, scaling_factor=1))


def part2(input: list[str]):
    print(calc_distance(input, scaling_factor=(1000000-1)))


def main():
    with open('input', 'r') as f:
        all_lines: list[str] = [l.strip() for l in f.readlines()]

        part1(all_lines)
        part2(all_lines)


if __name__ == "__main__":
    main()
