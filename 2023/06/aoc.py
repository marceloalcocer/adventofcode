#!/usr/bin/env python3
import sys
import math

PREFIX_TIME = "Time:"
PREFIX_DISTANCE = "Distance:"

def parse_input_part_one(file):
	time_string = file.readline()
	assert time_string.startswith(PREFIX_TIME)
	times = map(
		int,
		time_string.removeprefix(PREFIX_TIME).split()
	)
	distance_string = file.readline()
	assert distance_string.startswith(PREFIX_DISTANCE)
	distances = map(
		int,
		distance_string.removeprefix(PREFIX_DISTANCE).split()
	)
	return zip(times, distances)

def parse_input_part_two(file):
	time_string = file.readline()
	assert time_string.startswith(PREFIX_TIME)
	time = int(time_string.removeprefix(PREFIX_TIME).strip().replace(" ",""))
	distance_string = file.readline()
	assert distance_string.startswith(PREFIX_DISTANCE)
	distance = int(distance_string.removeprefix(PREFIX_DISTANCE).strip().replace(" ",""))
	return (time, distance)

def charge_times(time, distance):

	# t_c = 0.5 * (t_r ± √((t_r**2) - 4d) )

	root_descriminant = math.sqrt(
		(time**2)
		- (4 * (distance + 1))		# FTW!
	)
	charge_times = (
		0.5 * (time - root_descriminant),
		0.5 * (time + root_descriminant)
	)
	return charge_times

def part_one(file):
	ways = 1
	for time, distance in parse_input_part_one(file):
		charges = charge_times(time, distance)
		ways *= len(
			range(
				math.ceil(charges[0]),
				math.floor(charges[1]) + 1
			)
		)
	return ways

def part_two(file):
	time, distance = parse_input_part_two(file)
	charges = charge_times(time, distance)
	return len(
		range(
			math.ceil(charges[0]),
			math.floor(charges[1]) + 1
		)
	)

if __name__ == "__main__":
	for part in (part_one, part_two):
		with open(sys.argv[1],"rt") as file:
			print(part(file))
