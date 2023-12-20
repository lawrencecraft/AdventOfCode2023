from dataclasses import dataclass

@dataclass
class Spring:
	pattern: list[int]
	layout: str

def parse_line_into_spring(line: str) -> Spring:
	layout, pattern_raw = line.split(' ')
	pattern = [int(i) for i in pattern_raw.split(',')]

	return Spring(pattern=pattern, layout=layout)

def can_satisfy_part(so_far: str, pattern: list[int]) -> list[int] | None:
	current_pattern_idx = 0
	active_streak = 0 
	completed = []
	
	for c in so_far:
		# print(c, active_streak, current_pattern_idx)
		if c == '#':
			if current_pattern_idx >= len(pattern):
				return None
			active_streak += 1
			if active_streak > pattern[current_pattern_idx]:
				return None

		if c == '.':
			if active_streak and active_streak != pattern[current_pattern_idx]:
				return None
			if not active_streak:
				continue
			
			completed.append(pattern[current_pattern_idx])
			active_streak = 0
			current_pattern_idx += 1

	if current_pattern_idx < len(pattern) and active_streak == pattern[current_pattern_idx]:
		completed.append(pattern[current_pattern_idx])

	return completed 

def count_number_of_solutions(spring: Spring, so_far: str, remaining: str):
	parts_done = can_satisfy_part(so_far, spring.pattern)

	if parts_done is None:
		return 0

	if parts_done == spring.pattern and not remaining:
		return 1

	if not remaining: 
		return 0

	# print(remaining)

	character_to_check = remaining[0]
	remaining = remaining[1:]

	if character_to_check == '?':
		return count_number_of_solutions(spring, so_far + '.', remaining) + count_number_of_solutions(spring, so_far + '#', remaining)
	else:
		return count_number_of_solutions(spring, so_far + character_to_check, remaining)
	

	
	

def part1(input: list[str]):
	springs = [parse_line_into_spring(s) for s in input]
	print(sum(count_number_of_solutions(sp, "", sp.layout) for sp in springs))


def part2(input: list[str]):
	pass



def main():
	with open("input", 'r') as f:
		stripped_input = [l.strip() for l in f.readlines()]

	part1(stripped_input)
	part2(stripped_input)

if __name__=="__main__":
   	main() 
