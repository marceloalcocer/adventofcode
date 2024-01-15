#!/usr/bin/env python3
import sys

def parse_history(line):
	history = list(
		map(int, line.split())
	)
	assert len(history) > 0
	return history

def diff(iterable):
	for current, next_ in zip(
		iterable[0:-1],
		iterable[1:]
	):
		yield next_ - current

def diffs(iterable):
	while any(iterable):
		yield iterable
		iterable = list(diff(iterable))

def forecast(iterable):
	return sum(
		differences[-1]
		for differences in
		diffs(iterable)
	)

def backcast(iterable):
	extrapolated_value = 0
	for difference in reversed(
		[
			differences[0]
			for differences in
			diffs(iterable)
		]
	):
		extrapolated_value = difference - extrapolated_value
	return extrapolated_value

def part_one(file):
	return sum(
		forecast(parse_history(line))
		for line in file
	)

def part_two(file):
	return sum(
		backcast(parse_history(line))
		for line in file
	)

if __name__ == "__main__":
	for part in (part_one, part_two):
		with open(sys.argv[1],"rt") as file:
			print(part(file))


