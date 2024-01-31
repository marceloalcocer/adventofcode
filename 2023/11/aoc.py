#!/usr/bin/env python3
import sys
import itertools

class Image:

	_galaxy = "#"
	_empty = "."

	_array = None

	@classmethod
	def from_file(cls, file):
		_array = [
			line.strip()
			for line in
			file
		]
		return cls(_array)

	def __init__(self, _array):
		self._array = _array

	@property
	def _dims(self):
		return (len(self._array), len(self._array[0]))

	@property
	def _empty_rows(self):
		for i_row in range(self._dims[0]):
			if self._galaxy not in self._array[i_row]:
				yield i_row

	@property
	def _empty_cols(self):
		for i_col in range(self._dims[1]):
			if self._galaxy not in [
				self._array[i_row][i_col]
				for i_row in
				range(self._dims[1])
			]:
				yield i_col

	@staticmethod
	def _expanded_index(index, empty, expansion):
		return index + (
			sum(1 for i_empty in empty if index > i_empty)
			* (expansion - 1)
		)

	def galaxies(self, expansion=1):
		empty_rows = list(self._empty_rows)
		empty_cols = list(self._empty_cols)
		for i_row, row in enumerate(self._array):
			for i_col, value in enumerate(row):
				if value == self._galaxy:
					yield complex(
						self._expanded_index(i_row, empty_rows, expansion),
						self._expanded_index(i_col, empty_cols, expansion)
					)

def part_one(file):
	image = Image.from_file(file)
	galaxies = set(image.galaxies(expansion=2))
	galaxy_pairs = set(itertools.combinations(galaxies, 2))
	return sum(
		abs(int((galaxy_b - galaxy_a).real))
		+ abs(int((galaxy_b - galaxy_a).imag))
		for galaxy_a, galaxy_b in
		galaxy_pairs
	)

def part_two(file):
	image = Image.from_file(file)
	galaxies = set(image.galaxies(expansion=1000000))
	galaxy_pairs = set(itertools.combinations(galaxies, 2))
	return sum(
		abs(int((galaxy_b - galaxy_a).real))
		+ abs(int((galaxy_b - galaxy_a).imag))
		for galaxy_a, galaxy_b in
		galaxy_pairs
	)


if __name__ == "__main__":
	for part in (part_one, part_two):
		with open(sys.argv[1],"rt") as file:
			print(part(file))

