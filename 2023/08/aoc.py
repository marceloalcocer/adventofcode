#!/usr/bin/env python3
import sys
import math

def parse_directions(file):
	directions = file.readline().strip()
	assert file.readline() == "\n"
	return directions

def parse_nodes(file):
	nodes = {}
	for line in file:
		node, edges_string = map(
			str.strip,
			line.split("=")
		)
		edges = map(
			str.strip,
			edges_string.replace("(","").replace(")","").split(",")
		)
		nodes[node] = {
			direction: edge
			for direction, edge in zip(
				("L","R"),
				edges
			)
		}
	return nodes

class Traversal:

	directions = None
	nodes = None

	_node = None

	def __init__(self, directions, nodes, start_node):
		self.directions = directions
		self.nodes = nodes
		self._node = start_node

	def __iter__(self):
		yield self._node				# Start node
		while True:
			for direction in self.directions:
				self._node = self.nodes[self._node][direction]
				yield self._node

def part_one(file):

	# Parse directions
	directions = parse_directions(file)
	assert (
		directions.count("L") + directions.count("R")
		== len(directions)
	)

	# Parse nodes
	nodes = parse_nodes(file)
	assert "AAA" in nodes
	assert "ZZZ" in nodes

	# Traverse network to stop node
	traversal = Traversal(directions, nodes, "AAA")
	for step, node in enumerate(traversal):
		if node == "ZZZ":
			return step

def part_two(file):

	# Parse directions
	directions = parse_directions(file)
	assert (
		directions.count("L") + directions.count("R")
		== len(directions)
	)

	# Parse nodes
	nodes = parse_nodes(file)

	# Instantiate traversals and cycles
	traversals = [
		Traversal(directions, nodes, node)
		for node in nodes
		if node.endswith("A")
	]
	cycles = [
		{
			"start": None,
			"period": None,
			"phase": None
		}
		for traversal in traversals
	]

	for traversal, cycle in zip(traversals, cycles):

		# Traverse network until cyclical
		history = []
		for step, node in enumerate(traversal):
			if (
				(node in history)						# Visited node before…
				and (
					(step % len(directions))
					in (
						history_step % len(directions)
						for history_step, history_node in enumerate(history)
						if history_node == node
					)
				)										# …at same direction index…
			):
				break									# … => cyclic traversal
			else:
				history.append(node)

		# Extract cycle start
		#
		#	The cyclical part of each traversal can begin at any step, e.g.;
		#
		#	Traversal 0;
		#
		#	0   1   2   3   4   …
		#	A - * - * - * - * - * - *
		#	            |           |
		#	            * - * - * - *
		#
		#	Traversal 1;
		#
		#	0   1   2   …
		#	A - * - * - * - * - * - *
		#	    |                   |
		#	    * - * - * - * - * - *
		#
		gen = (
			history_step
			for history_step, history_node in enumerate(history)
			if (
				(history_node == node)
				and (history_step % len(directions)) == (step % len(directions))
			)
		)											# Cycle start step generator
		cycle["start"] = next(gen)
		assert next(gen, None) is None				# Traversal stopped after one cycle

		# Compute cycle period
		cycle["period"] = step - cycle["start"]

		# Extract stop node position
		#
		#	Inspection reveals that there is only one stop node per traversal,
		#	and that it lies within the cyclical part of the traversal, e.g.;
		#
		#	0   1   2   3   4   …
		#	A - * - * - * - * - * - *
		#	            |           |
		#	            * - * - Z - *
		#
		gen = (
			history_step
			for history_step, history_node in enumerate(history)
			if history_node.endswith("Z")
		)											# Stop node step generator
		cycle["phase"] = next(gen)
		assert next(gen, None) is None				# Only one stop node (empirical)
		assert cycle["phase"] > cycle["start"]		# Stop node in cycle (empirical)

	# Align cycle starts
	#
	#	As stop nodes only lie within cyclical parts of traversals, can
	#	disregard initial linear parts. This can be achieved by aligning all
	#	cycles to latest cycle start, e.g.;
	#
	#	Traversal 0;
	#
	#	0   1   2   3   4   …
	#	A - * - * - # - * - * - *
	#	            |           |
	#	            * - * - Z - *
	#
	#	Traversal 1;
	#
	#	0   1   2   3   4   …
	#	A - * - * - # - * - * - *
	#	    |                   |
	#	    * - Z - * - * - * - *
	#
	#	Stop node occurance can now be considered as periodic with period, Tₗ,
	#	and phase, φₗ, for each of the n traversals, e.g.;
	#
	#   3   4   …
	#   # - * - Z - * - * - * - Z …
	#   |<----->|<------------->|
	#      φ₀          T₀
	#
	#   3   4   …
	#   # - * - * - * - Z - * - * - * - * - * - Z …
	#   |<------------->|<--------------------->|
	#          φ₁                T₁
	#
	max_start = max(cycle["start"] for cycle in cycles)
	for cycle in cycles:
		cycle["start"] = max_start
		cycle["phase"] -= cycle["start"]

	# Compute phase matching
	#
	#	Inspection reveals constant difference, k, between periods, T, and
	# 	phases, φ, of all n cycles;
	#
	#	Tₗ - φₗ = k    ,    l = 1, …, n
	#
	k = (cycles[0]["period"] - cycles[0]["phase"])
	assert all(cycle["period"] - cycle["phase"] == k for cycle in cycles)
	#
	# This implies phase matching occurs -k steps from cycle start.
	#
	#           3   4   …
	#   Z - * - # - * - Z - * - * - * - Z …
	#   |<----->|<----->|<------------->|
	#       k      φ₀          T₀
	#   |<------------->|
	#          T₀
	#
	#           3   4   …
	#   Z - * - # - * - * - * - Z - * - * - * - * - * - Z …
	#   |<----->|<------------->|<--------------------->|
	#       k          φ₁                T₁
	#   |<--------------------->|
	#              T₁
	#
	# As phase matching is cyclical in lowest common multiplier of cycle
	# periods, lcm(Tₗ), reverse traversal of k steps is equivalent to forward
	# traversal of lcm(Tₗ) - k steps.
	#
	lcm = math.lcm(*(cycle["period"] for cycle in cycles))
	return cycles[0]["start"] + lcm - k

if __name__ == "__main__":
	for part in (part_one, part_two):
		with open(sys.argv[1],"rt") as file:
			print(part(file))


