#!/usr/bin/env python3
import sys
import enum

class Card(enum.IntEnum):
	_j = enum.auto()
	_2 = enum.auto()
	_3 = enum.auto()
	_4 = enum.auto()
	_5 = enum.auto()
	_6 = enum.auto()
	_7 = enum.auto()
	_8 = enum.auto()
	_9 = enum.auto()
	_T = enum.auto()
	_J = enum.auto()
	_Q = enum.auto()
	_K = enum.auto()
	_A = enum.auto()

class HandType(enum.IntEnum):
	HIGH_CARD = enum.auto()
	ONE_PAIR = enum.auto()
	TWO_PAIR = enum.auto()
	THREE_OF_A_KIND = enum.auto()
	FULL_HOUSE = enum.auto()
	FOUR_OF_A_KIND = enum.auto()
	FIVE_OF_A_KIND = enum.auto()

class Hand:

	cards = None
	bid = None

	@classmethod
	def from_string(cls, hand_string):
		card_string, bid_string = hand_string.split()
		assert len(card_string) == 5
		cards = [
			Card[f"_{card}"]
			for card in
			card_string
		]
		bid = int(bid_string)
		return cls(cards, bid)

	def __init__(self, cards, bid):
		assert len(cards) == 5
		self.cards = cards
		assert bid > 0
		self.bid = bid

	def __repr__(self):
		return f"<{self.__class__.__name__} cards={[card.name[-1] for card in self.cards]}, bid={self.bid}>"

	def _type_(self):
		labels = set(self.cards)
		n_labels = len(labels)
		if(n_labels == 1):
			return HandType.FIVE_OF_A_KIND
		elif(n_labels == 2):
			label_count = set(
				map(self.cards.count, labels)
			)
			if label_count == {1,4}:
				return HandType.FOUR_OF_A_KIND
			elif label_count == {2,3}:
				return HandType.FULL_HOUSE
			else:
				raise ValueError(f"Unexpected hand: {self}")
		elif(n_labels == 3):
			label_count = set(
				map(self.cards.count, labels)
			)
			if label_count == {3,1}:
				return HandType.THREE_OF_A_KIND
			elif label_count == {2,1}:
				return HandType.TWO_PAIR
			else:
				raise ValueError(f"Unexpected hand: {self}")
		elif(n_labels == 4):
			return HandType.ONE_PAIR
		else:
			assert n_labels == 5
			return HandType.HIGH_CARD
	
	def type_(self, jokers=False):
		if jokers and (Card._j in self.cards):
			hands = (
				Hand(
					[
						label
						if card is Card._j
						else card
						for card in self.cards
					],
					self.bid
				)
				for label in
				set(self.cards)
			)
			return sorted_hands(hands)[-1]._type_()
		else:
			return self._type_()

def sorted_hands(hands, jokers=False):
	hands = sorted(hands, key=lambda hand: hand.cards[4])
	hands = sorted(hands, key=lambda hand: hand.cards[3])
	hands = sorted(hands, key=lambda hand: hand.cards[2])
	hands = sorted(hands, key=lambda hand: hand.cards[1])
	hands = sorted(hands, key=lambda hand: hand.cards[0])
	hands = sorted(hands, key=lambda hand: hand.type_(jokers=jokers))
	return hands

def part_one(file):
	hands = (
		Hand.from_string(line)
		for line in
		file
	)
	return sum(
		(rank + 1) * hand.bid
		for rank, hand in
		enumerate(sorted_hands(hands))
	)

def part_two(file):
	hands = (
		Hand.from_string(line.replace("J","j"))
		for line in
		file
	)
	return sum(
		(rank + 1) * hand.bid
		for rank, hand in
		enumerate(sorted_hands(hands, jokers=True))
	)

if __name__ == "__main__":
	for part in (part_one, part_two):
		with open(sys.argv[1],"rt") as file:
			print(part(file))

