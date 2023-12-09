#!/usr/bin/env python3
import sys

PREFIX_SEEDS = "seeds: "

def seeds_part_one(file):
	seed_string = file.readline()
	assert seed_string.startswith(PREFIX_SEEDS)
	seeds = [
		range(start, start + 1)
		for start in
		map(int, seed_string.removeprefix(PREFIX_SEEDS).split())
	]
	assert not file.readline().split()
	return seeds

def seeds_part_two(file):
	seed_string = file.readline()
	assert seed_string.startswith(PREFIX_SEEDS)
	iter_ = iter(seed_string.removeprefix(PREFIX_SEEDS).split())
	seeds = []
	for start in iter_:
		start = int(start)
		length = int(next(iter_))
		seeds.append(range(start, start + length))
	assert not file.readline().split()
	return seeds

def mappings(file):
	mapping = {}
	for line in file:
		if line.endswith(" map:\n"):
			mapping = {}
			continue
		elif line == "\n":
			yield mapping
			continue
		dest_start, src_start, length = map(int,line.split())
		src = range(src_start, src_start + length)
		dest = range(dest_start, dest_start + length)
		mapping[src] = dest
	yield mapping

def decompose(mapping, inputs):
	outputs = []
	for src, dest in mapping.items():
		for _ in range(len(inputs)):

			# Extract input
			input_ = inputs.pop(0)

			# Compute overlap
			overlap_start = max(input_.start, src.start)
			overlap_stop = min(input_.stop, src.stop)

			# Overlap
			if overlap_start < overlap_stop:

				# Append mapped overlap to output
				overlap = range(
					dest[src.index(overlap_start)],
					dest[src.index(overlap_stop-1)] + 1
				)
				outputs.append(overlap)

				# Append non-overlap back to input
				pre_overlap = range(input_.start, overlap_start)
				post_overlap = range(overlap_stop, input_.stop)
				assert (
					len(pre_overlap)
					+ len(overlap)
					+ len(post_overlap)
				) == len(input_)
				inputs.extend(
					[
						range_
						for range_ in
						(pre_overlap, post_overlap)
						if len(range_) > 0
					]
				)

			# No overlap
			else:
				# Append non-overlap (entirity) back to input
				inputs.append(input_)

	
	# Map remaining inputs as outputs
	inputs.extend(outputs)

def part_one(file):
	inputs = seeds_part_one(file)
	for mapping in mappings(file):
		decompose(mapping, inputs)
	return min(range_.start for range_ in inputs)

def part_two(file):
	inputs = seeds_part_two(file)
	for mapping in mappings(file):
		decompose(mapping, inputs)
	return min(range_.start for range_ in inputs)

if __name__ == "__main__":
	for part in (part_one, part_two):
		with open(sys.argv[1],"rt") as file:
			print(part(file))
