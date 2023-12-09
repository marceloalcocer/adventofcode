#!/usr/bin/env python3
import sys
import math

COLORS = {
	"red": 12,
	"green": 13,
	"blue": 14
}
PREFIX_GAME = "game "
DELIM_GAME = ":"
DELIM_DRAW = ";"
DELIM_CUBE = ","

class Cube:

	color = None
	count = None

	def __init__(self, color, count):
		assert color is not None
		assert count > 0
		self.color = color
		self.count = count

	@staticmethod
	def _parse_color(cube_string):
		for color in COLORS:
			if color in cube_string:
				return color

	@staticmethod
	def _parse_count(cube_string, color):
		return int(cube_string.strip().removesuffix(color).strip())

	@classmethod
	def from_string(cls, cube_string):
		color = cls._parse_color(cube_string)
		count = cls._parse_count(cube_string, color)
		return cls(color, count)

class Game:

	id_ = None
	possible = None
	fewest = None

	def __init__(self, id_, possible, fewest):
		assert id_ > 0
		assert isinstance(possible, bool)
		assert isinstance(fewest, dict)
		self.id_ = id_
		self.possible = possible
		self.fewest = fewest

	@staticmethod
	def _parse_id(id_string):
		assert id_string.startswith(PREFIX_GAME)
		return int(id_string.removeprefix(PREFIX_GAME))

	@classmethod
	def from_string(cls, game_string):
		id_string, draws_string = game_string.lower().split(DELIM_GAME)
		id_ = cls._parse_id(id_string)
		possible = True
		fewest = { color: 0 for color in COLORS }
		for draw_string in draws_string.split(DELIM_DRAW):
			for cube_string in draw_string.split(DELIM_CUBE):
				cube = Cube.from_string(cube_string)
				possible &= (cube.count <= COLORS[cube.color])
				fewest[cube.color] = max(cube.count, fewest[cube.color])
		return cls(id_, possible, fewest)

def part_one(file):
	return sum(
		game.id_
		for game in (
			Game.from_string(game_string)
			for game_string in file
		)
		if game.possible
	)

def part_two(file):
	return sum(
		math.prod(game.fewest.values())
		for game in (
			Game.from_string(game_string)
			for game_string in file
		)
	)

if __name__ == "__main__":
	for part in (part_one, part_two):
		with open(sys.argv[1],"rt") as file:
			print(part(file))
