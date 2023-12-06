from dataclasses import dataclass
from typing import Iterator
from itertools import batched

RawRangeMap = list[tuple[int, int, int]]


@dataclass
class RawDocument:
    seeds: list[int]
    seed_to_soil: RawRangeMap
    soil_to_fertilizer: RawRangeMap
    fertilizer_to_water: RawRangeMap
    water_to_light: RawRangeMap
    light_to_temperature: RawRangeMap
    temperature_to_humidity: RawRangeMap
    humidity_to_location: RawRangeMap


def parse_range(doc_stack: list[str]) -> Iterator[tuple[int, int, int]]:
    while doc_stack and (line := doc_stack.pop()):
        destination_start, source_start, range_length = [
            int(x) for x in line.split(" ")
        ]
        yield destination_start, source_start, range_length


def parse_document(input: list[str]):
    document_stack = input.copy()
    document_stack.reverse()

    seed_line = document_stack.pop()
    seeds = [int(s) for s in seed_line.split(" ")[1:]]

    document_stack.pop()
    assert document_stack.pop() == "seed-to-soil map:"

    seed_to_soil = list(parse_range(document_stack))

    assert document_stack.pop() == "soil-to-fertilizer map:"
    soil_to_fertilizer = list(parse_range(document_stack))

    assert document_stack.pop() == "fertilizer-to-water map:"
    fertilizer_to_water = list(parse_range(document_stack))

    assert document_stack.pop() == "water-to-light map:"
    water_to_light = list(parse_range(document_stack))

    assert document_stack.pop() == "light-to-temperature map:"
    light_to_temperature = list(parse_range(document_stack))

    assert document_stack.pop() == "temperature-to-humidity map:"
    temperature_to_humidity = list(parse_range(document_stack))

    assert document_stack.pop() == "humidity-to-location map:"
    humidity_to_location = list(parse_range(document_stack))

    return RawDocument(
        seeds=seeds,
        seed_to_soil=seed_to_soil,
        soil_to_fertilizer=soil_to_fertilizer,
        fertilizer_to_water=fertilizer_to_water,
        water_to_light=water_to_light,
        light_to_temperature=light_to_temperature,
        temperature_to_humidity=temperature_to_humidity,
        humidity_to_location=humidity_to_location,
    )


def resolve_value(value: int, target_range: RawRangeMap):
    for destination_start, source_start, range_length in target_range:
        if value >= source_start and (offset := value - source_start) < range_length:
            return destination_start + offset

    return value


def find_location(seed: int, doc: RawDocument):
    ranges = [
        doc.seed_to_soil,
        doc.soil_to_fertilizer,
        doc.fertilizer_to_water,
        doc.water_to_light,
        doc.light_to_temperature,
        doc.temperature_to_humidity,
        doc.humidity_to_location,
    ]

    for r in ranges:
        seed = resolve_value(seed, r)

    return seed


# def merge_intervals(intervals):
#     # Sort intervals based on the start value
#     intervals.sort(key=lambda x: x[0])

#     merged = []
#     for interval in intervals:
#         # If merged list is empty or current interval doesn't overlap with the previous one
#         if not merged or merged[-1][1] < interval[0]:
#             merged.append(interval)
#         else:
#             # Merge the current interval with the previous one
#             merged[-1] = (merged[-1][0], max(merged[-1][1], interval[1]))

#     return merged

# def apply_mapping_to_interval(initial: tuple[int, int], mapping: RawRangeMap):
#     destination_start, source_start, range_length = mapping
#     new_ranges = []
#     for initial_range_start, initial_range_end in initial:
#         # No overlap
#         if (
#             initial_range_end < source_start
#             or source_start + range_length < initial_range_start
#         ):
#             new_ranges.append((initial_range_start, initial_range_end))
#             print("no overlaps", destination_start, source_start, range_length)
#             continue

#         offset = destination_start - source_start

#         # fully contained range - 1 segment
#         if (
#             source_start <= initial_range_start
#             and initial_range_end <= source_start + range_length
#         ):
#             # print('fully contained', offset)
#             new_ranges.append(
#                 (initial_range_start + offset, initial_range_end + offset)
#             )
#             print("overlaps", destination_start, source_start, range_length)
#             continue

#         # Initial range overlaps beginning of mask range
#         if (
#             initial_range_start <= source_start
#             and initial_range_end <= source_start + range_length
#         ):
#             print('beginning mask')
#             new_ranges.append((initial_range_start, source_start - 1))
#             new_ranges.append((source_start + offset, initial_range_end + offset))
#             continue

#         # Initial range overlaps end of mask range
#         if (
#             source_start < initial_range_start
#             and source_start + range_length < initial_range_end
#         ):
#             print('end mask')
#             new_ranges.extend(
#                 [
#                     (
#                         initial_range_start + offset,
#                         source_start + range_length + offset,
#                     ),
#                     (source_start + range_length + offset + 1, initial_range_start),
#                 ]
#             )
#             continue

#         # Overlaps entire range
#         if (
#             initial_range_start < source_start
#             and source_start + range_length < initial_range_end
#         ):
#             print("whole overlap")
#             new_ranges.extend(
#                 [
#                     (initial_range_start, source_start - 1),
#                     (source_start + offset, source_start + range_length + offset),
#                     (source_start + range_length + 1, initial_range_end),
#                 ]
#             )
#             continue
#     return merge_intervals(new_ranges)

# def collapse_possible_range(initial: list[tuple[int, int]], destination: RawRangeMap):
#     for mapping in destination:
#         initial = apply_mapping_to_interval(initial, mapping)
#     return initial


@dataclass
class Range:
    offset: int
    start: int
    end: int


def to_interval_and_offset(range: tuple[int, int, int]):
    destination_start, source_start, range_length = range
    return Range(
        start=source_start,
        end=source_start + range_length,
        offset=destination_start - source_start,
    )


def search_and_modify(interval: list[tuple[int, int]], ranges: list[RawRangeMap]):
    seed_ranges: list[tuple[tuple[int, int], int]] = [(i, 0) for i in interval]
    answers = []

    while seed_ranges:
        current_interval, stage = seed_ranges.pop()
        print(current_interval, stage)

        if stage == len(ranges):
            answers.append(current_interval[0])
            continue

        current_range = ranges[stage]

        remaining = [current_interval]

        for range in map(to_interval_and_offset, current_range):
            new_remaining = []
            for start_seed, end_seed in remaining:
                # No overlap, put it back
                if end_seed < range.start or start_seed > range.end:
                    print('nope')
                    new_remaining.append((start_seed, end_seed))
                    continue

                # Full overlap
                if range.start <= start_seed and end_seed <= range.end:
                    print('full', start_seed + range.offset, range.offset)
                    seed_ranges.append(
                        (
                            (start_seed + range.offset, end_seed + range.offset),
                            stage + 1,
                        )
                    )
                    continue

                # Part overlap - beginning
                if range.start <= start_seed and range.end < end_seed:
                    print('part-beg')
                    new_remaining.append((range.end + 1, end_seed))
                    seed_ranges.append(
                        (
                            (start_seed + range.offset, range.end + range.offset),
                            stage + 1,
                        )
                    )
                    continue

                # Part overlap - end
                if start_seed < range.start and end_seed <= range.end:
                    print('part-end')
                    new_remaining.append((start_seed, range.start - 1))
                    seed_ranges.append(
                        (
                            (range.start + range.offset, end_seed + range.offset),
                            stage + 1,
                        )
                    )
                    continue

                # Middle overlap
                if start_seed < range.start and range.end < end_seed:
                    print('mid')
                    new_remaining.append((start_seed, range.start - 1))
                    new_remaining.append((range.end + 1, end_seed))
                    seed_ranges.append(
                        (
                            (range.start + range.offset, range.end + range.offset),
                            stage + 1,
                        )
                    )
                    continue

            remaining = new_remaining

        seed_ranges.extend((r, stage + 1) for r in remaining)

    print(min(answers))


def part1(input: list[str]):
    doc = parse_document(input)

    print(min(find_location(s, doc) for s in doc.seeds))


def part2(input: list[str]):
    doc = parse_document(input)
    # seeds: list[tuple[int, int]] = [
    seed_batches = [tuple(t) for t in batched(doc.seeds, 2)]
    print(seed_batches)
    seeds = [(s, s + l) for s, l in seed_batches]

    ranges = [
        doc.seed_to_soil,
        doc.soil_to_fertilizer,
        doc.fertilizer_to_water,
        doc.water_to_light,
        doc.light_to_temperature,
        doc.temperature_to_humidity,
        doc.humidity_to_location,
    ]

    search_and_modify(seeds, ranges)


def main():
    with open("input", "r") as f:
        all_lines: list[str] = [l.strip() for l in f.readlines()]

        part1(all_lines)
        part2(all_lines)


if __name__ == "__main__":
    main()
