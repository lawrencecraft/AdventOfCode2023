from math import lcm


def parse_graph(input: list[str]) -> tuple[str, dict[str, tuple[str, str]]]:
    pattern = input[0]

    edges = {}
    for edge in input[2:]:
        components = [c.strip() for c in edge.split(" ")]
        source = components[0]
        left = components[2].strip("(), ")
        right = components[3].strip("(), ")

        edges[source] = (left, right)

    return (pattern, edges)


def part1(input: list[str]):
    pattern_offset = 0
    current_node = "AAA"
    hop_count = 0
    pattern, edges = parse_graph(input)

    while current_node != "ZZZ":
        direction = pattern[pattern_offset]
        left, right = edges[current_node]

        current_node = left if direction == "L" else right
        pattern_offset = (pattern_offset + 1) % len(pattern)
        hop_count += 1

    print(hop_count)


def at_end(nodes: list[str]):
    for node in nodes:
        if node[-1] != "Z":
            return False

    return True


def calculate_hops_per_node(
    node: str, pattern: str, edges: dict[str, tuple[str, str]]
) -> int:
    pattern_offset = 0
    hop_count = 0

    while node[-1] != "Z":
        direction = pattern[pattern_offset]
        left, right = edges[node]

        node = left if direction == "L" else right

        hop_count += 1
        pattern_offset = (pattern_offset + 1) % len(pattern)

    return hop_count


def part2(input: list[str]):
    pattern, edges = parse_graph(input)

    all_nodes = edges.keys()
    starting_nodes = [e for e in all_nodes if e[-1] == "A"]

    hops_from_start = [
        calculate_hops_per_node(n, pattern, edges) for n in starting_nodes
    ]

    print(lcm(*hops_from_start))


def main():
    with open("input", "r") as f:
        all_lines: list[str] = [l.strip() for l in f.readlines()]

        part1(all_lines)
        part2(all_lines)


if __name__ == "__main__":
    main()
