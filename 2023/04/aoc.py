#!/usr/bin/env python3
import sys
import time


class Card:

	_ID_PREFIX = "Card "

	id_ = None
	values = None
	winning_values = None

	def __init__(self, id_, values, winning_values):
		assert id_ > 0
		self.id_ = id_
		assert len(values) > 0
		self.values = values
		assert len(winning_values) > 0
		self.winning_values = winning_values

	@classmethod
	def from_string(cls, card_string):

		# ID
		id_string, numbers_string = card_string.split(":")
		assert id_string.startswith(cls._ID_PREFIX)
		id_ = int(id_string.removeprefix(cls._ID_PREFIX).strip())
		assert id_ > 0

		# Values
		winning_values_string, values_string = numbers_string.split("|")
		winning_values = set(map(int, winning_values_string.split()))
		values = set(map(int, values_string.split()))
		assert len(values) > len(winning_values)

		return cls(id_, values, winning_values)

	@property
	def matches(self):
		return len(self.values & self.winning_values)
		

	@property
	def points(self):
		return (2**(self.matches - 1)) if self.matches else 0

	def __repr__(self):
		#return f"<{self.__class__.__name__} id_={self.id_}, values={self.values}, winning_values={self.winning_values}>"
		return f"<{self.__class__.__name__} id_={self.id_}, matches={self.matches}>"

class CardTree:

	cards = None

	def __init__(self, cards):
		assert (len(cards) > 0)
		self.cards = cards

	def decendents(self, parents=None):
		if parents == None:
			parents = self.cards
		children = []
		for parent in parents:
			children += self.cards[parent.id_ : parent.id_ + parent.matches]
		if children:
			return parents + self.decendents(children)
		else:
			return parents

def part_one(file):
	return sum(
		Card.from_string(line).points
		for line in
		file
	)

def part_two(file):
	return len(
		CardTree(
			[
				Card.from_string(line)
				for line in
				file
			]
		).decendents()
	)

if __name__ == "__main__":
	for part in (part_one, part_two):
		with open(sys.argv[1],"rt") as file:
			print(part(file))
