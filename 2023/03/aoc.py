#!/usr/bin/env python3
import sys
import re
import math

class Schematic:

	parts = None
	symbols = None

	def __init__(self, parts, symbols):
		self.parts = parts
		self.symbols = symbols

	@classmethod
	def from_file(cls, file):
		parts = []
		symbols = []
		for row, line in enumerate(file):
			line = line.strip()
			for match_ in re.finditer("(\d+|[^\d\.])",line):
				if match_[0].isdigit():
					parts.append(
						SchematicPart(
							int(match_[0]),
							row,
							match_.span()
						)
					)
				else:
					symbols.append(
						SchematicSymbol(
							match_[0],
							row,
							match_.span()
						)
					)
		return cls(parts, symbols)

	@property
	def part_numbers_iter(self):
		for part in self.parts:
			rows = range(part.row - 1, part.row + 1 + 1)
			cols = range(part.span[0] - 1, part.span[1] + 1)
			for symbol in self.symbols:
				if (
					(symbol.row in rows)
					and (symbol.span[0] in cols)
				):
					yield part.value
					break

	@property
	def gear_ratios_iter(self):
		for symbol in self.symbols:
			if symbol.value != "*":
				continue
			else:
				rows = range(symbol.row - 1, symbol.row + 1 + 1)
				cols = range(symbol.span[0] - 1, symbol.span[1] + 1)
				parts = [
					part.value
					for part in
					self.parts
					if (
						(part.row in rows)
						and ( set(range(*part.span)) & set(cols) )
					)
				]
				if len(parts) == 2:
					yield math.prod(parts)



class SchematicElement:

	value = None
	row = None
	span = None

	def __init__(self, value, row, span):
		assert row >= 0
		assert (
			(len(span) == 2)
			and (span[0] >= 0)
			and (span[1] >= 0)
		)
		self.value = value
		self.row = row
		self.span = span

	def __repr__(self):
		return f"<{self.__class__.__name__} value={self.value}, row={self.row}, span={self.span}>"

class SchematicPart(SchematicElement):

	def __init__(self, value, row, span):
		assert value >= 0
		super().__init__(value, row, span)

class SchematicSymbol(SchematicElement):

	def __init__(self, value, row, span):
		assert (
			(not value.isdigit())
			and (not value == ".")
		)
		super().__init__(value, row, span)

	

def part_one(file):
	schematic = Schematic.from_file(file)
	return sum(schematic.part_numbers_iter)

def part_two(file):
	schematic = Schematic.from_file(file)
	return sum(schematic.gear_ratios_iter)

if __name__ == "__main__":
	for part in (part_one, part_two):
		with open(sys.argv[1],"rt") as file:
			print(part(file))
