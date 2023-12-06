from math import sqrt, floor, ceil
from dataclasses import dataclass

@dataclass
class Race:
    time: int
    distance: int

REAL_RACES = [
    Race(time=54, distance=446),
    Race(time=81, distance=1292),
    Race(time=70, distance=1035),
    Race(time=88, distance=1007)
]

FAKE_RACES = [
    Race(time=7, distance=9),
    Race(time=15, distance=40),
    Race(time=30, distance=200)
]

def solve_race_interval(race_time, distance):
    upper_bound = (-race_time - sqrt(race_time * race_time - 4 * distance)) / -2
    lower_bound = (-race_time + sqrt(race_time * race_time - 4 * distance)) / -2

    print(lower_bound, upper_bound)

    floor_upper_bound = floor(upper_bound)
    if floor_upper_bound == upper_bound:
        floor_upper_bound -= 1
    
    ceil_lower_bound = ceil(lower_bound)
    if ceil_lower_bound == lower_bound:
        ceil_lower_bound += 1

    print(floor_upper_bound, ceil_lower_bound)


    return floor_upper_bound - ceil_lower_bound + 1


def part1(input: list[str]):
    agg = 1
    for race in REAL_RACES:
        solns = solve_race_interval(race.time, race.distance)
        print(race, solns)
        agg *= solns
    print(agg)



def part2(input: list[str]):
    print(solve_race_interval(54817088, 446129210351007))


def main():
    with open("input", "r") as f:
        all_lines: list[str] = [l.strip() for l in f.readlines()]

        part1(all_lines)
        part2(all_lines)

if __name__ == "__main__":
    main()
