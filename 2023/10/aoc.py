#!/usr/bin/env python3
import sys
import enum
import math

class Sketch:

	cardinals = {
		# real: row, imag: column
		"N": complex(-1, 0),
		"S": complex( 1, 0),
		"W": complex( 0,-1),
		"E": complex( 0, 1),
	}
	tiles = {
		"|": {cardinals["N"], cardinals["S"]},
		"-": {cardinals["W"], cardinals["E"]},
		"L": {cardinals["N"], cardinals["E"]},
		"J": {cardinals["N"], cardinals["W"]},
		"7": {cardinals["S"], cardinals["W"]},
		"F": {cardinals["S"], cardinals["E"]},
		".": set(),
	}

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
		self._init_tiles()

	def __getitem__(self, coords):
		"""Get item from _array (with bounds checking)"""
		row = int(coords.real)
		col = int(coords.imag)
		try:
			if (row < 0) or (col < 0):
				raise IndexError
			tile = self._array[row][col]
		except IndexError:
			return None
		else:
			return tile

	def _init_tiles(self):
		coords = self.start_coords
		tile = {
			cardinal
			for cardinal in self.cardinals.values()
			if (
				self[coords + cardinal]
				and (-cardinal in self.tiles[self[coords + cardinal]])
			)
		}
		assert len(tile) == 2, "Start pipe not connected to exactly 2 pipes"
		self.tiles = self.tiles | {"S": tile}			# Don't mutate!

	@property
	def dims(self):
		return (len(self._array), len(self._array[0]))

	@property
	def start_coords(self):
		"""Start tile coordinates"""
		key = "S"
		coords = [
			complex(row, line.index(key))
			for row, line in enumerate(self._array)
			if key in line
		]
		assert len(coords) == 1, "More than 1 start pipe"
		return coords.pop()

	@property
	def loop_coords(self):
		"""Traverse loop from starting point"""
		start_coords = self.start_coords
		try:
			tile = self.tiles[self[start_coords]]
			cardinal = next(-cardinal for cardinal in tile)
		except KeyError:
			raise ValueError("Start tile out of bounds")
		except StopIteration:
			raise ValueError("Start tile not a pipe")
		coords = start_coords
		while True:
			yield coords
			cardinal = next(cardinal for cardinal in tile - {-cardinal})
			coords = coords + cardinal
			try:
				tile = self.tiles[self[coords]]
			except KeyError:
				raise StopIteration("Hit boundary")
			if -cardinal not in tile:
				raise StopIteration("Disconnected pipe")
			elif coords == start_coords:
				break

	def _left_adjacent_coords(self, loop_coords):
		for previous_coords, current_coords in zip(
			loop_coords[-1:] + loop_coords[:-1],
			loop_coords
		):
			forward_cardinal = current_coords - previous_coords
			left_cardinal = (forward_cardinal * complex(0,1))
			pipe = self.tiles[self[current_coords]]
			if left_cardinal in pipe:
				# Inside corner
				left_coords = set()
			elif forward_cardinal in pipe:
				# Straight
				left_coords = {current_coords + left_cardinal}
			else:
				# Outside corner
				left_coords = {
					current_coords + left_cardinal,
					current_coords + forward_cardinal,
					current_coords + left_cardinal + forward_cardinal,
				}
			for coords in left_coords:
				if (coords not in loop_coords) and (self[coords] is not None):
					yield coords

	def left_coords(self, loop_coords):
		neighbours = set()
		for left_adjacent_coords in self._left_adjacent_coords(loop_coords):
			potential_neighbours = {left_adjacent_coords}
			while potential_neighbours:
				coords = potential_neighbours.pop()
				if (coords not in neighbours) and (coords not in loop_coords):
					yield coords
					neighbours.add(coords)
					potential_neighbours |= {
						coords + cardinal
						for cardinal in
						self.cardinals.values()
						if (self[coords + cardinal] is not None)
					}
		#return neighbours						# Probably more efficient…

	@property
	def edge_coords(self):
		n_rows, n_cols = self.dims
		for coords in (
			{   complex(     row , 0       ) for row in range(n_rows) }
			| { complex(       0 , col     ) for col in range(n_cols) }
			| { complex(     row , n_cols-1) for row in range(n_rows) }
			| { complex(n_rows-1 , col     ) for col in range(n_cols) }
		):
			yield coords

def part_one(file):
	sketch = Sketch.from_file(file)
	for i_coords, coords in enumerate(sketch.loop_coords):
		pass
	assert (i_coords + 1) % 2 == 0		# Even number of pipes (0-indexed)
	return (i_coords + 1) // 2

def part_two(file):

	sketch = Sketch.from_file(file)
	loop_coords = list(sketch.loop_coords)
	left_coords = set(sketch.left_coords(loop_coords))
	right_coords = set(sketch.left_coords(loop_coords[::-1]))
	assert (
		(set(loop_coords) ^ left_coords ^ right_coords)
		== (set(loop_coords) | left_coords | right_coords)
	) , "Loop/left/right not mutually exclusive"
	assert (
		len(set(loop_coords) | left_coords | right_coords)
		== math.prod(sketch.dims)
	) , "Unclassified coordinates"

	edge_coords = set(sketch.edge_coords)
	if loop_coords == edge_coords:
		assert 0 in {len(left_coords), len(right_coords)}
		return (
			len(left_coords)
			if len(left_coords) != 0
			else len(right_coords)
		)
	else:
		return (
			len(left_coords)
			if not (edge_coords & left_coords)
			else len(right_coords)
		)


if __name__ == "__main__":
	for part in (part_one, part_two):
		with open(sys.argv[1],"rt") as file:
			print(part(file))

