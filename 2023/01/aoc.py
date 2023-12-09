#!/usr/bin/env python3
import sys

DIGITS_ENGLISH = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine")

def replace_english_digits(line):
	indices = {
		index: word
		for index, word in
		zip(
			map(line.find, DIGITS_ENGLISH),
			DIGITS_ENGLISH
		)
		if index >= 0
	}
	rindices = {
		index: word
		for index, word in
		zip(
			map(line.rfind, DIGITS_ENGLISH),
			DIGITS_ENGLISH
		)
		if index >= 0
	}

	if indices and rindices:

		i_first = sorted(indices)[0]
		i_last = sorted(rindices)[-1]
		word_first = indices[i_first]
		word_last = rindices[i_last]

		# Two word overlap — replace both
		if(
			(len(indices) == 2)
			and (len(rindices) == 2)
			and ((i_first + len(word_first)) > i_last)
		):
			line = line.replace(
				word_first,
				str(DIGITS_ENGLISH.index(word_first) + 1)
				+ str(DIGITS_ENGLISH.index(word_last) + 1)
			)

		# One or multiple — replace first and last only
		else:
			for word in (word_first, word_last):
				line = line.replace(
					word,
					str(DIGITS_ENGLISH.index(word) + 1)
				)

	return line

def part_one(file):
	lines = [
		[
			digit
			for digit in
			filter(str.isdigit, line)
		]
		for line in
		file
	]
	return sum(
		int(digits[0] + digits[-1])
		for digits in
		lines
	)

def part_two(file):
	lines = (
		[
			digit
			for digit in
			filter(
				str.isdigit,
				replace_english_digits(line)
			)
		]
		for line in
		file.readlines()
	)
	return sum(
		int(digits[0] + digits[-1])
		for digits in
		lines
	)

if __name__ == "__main__":
	for part in (part_one, part_two):
		with open(sys.argv[1],"rt") as file:
			print(part(file))
