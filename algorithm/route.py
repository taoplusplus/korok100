import sys
import json
import math

class Korok:
	def __init__(self, k_id, k_pos, k_type):
	    self.id = k_id
	    self.pos = k_pos
	    self.type = k_type

wetland_stable = [890.25, 131.28, 157.06] # Wetland Stable

korok_pos = {}

def squared_distance(pos1, pos2):
	dx = pos1[0] - pos2[0]
	dz = pos1[1] - pos2[1]
	dy = pos1[2] - pos2[2]
	dist = dx*dx + dz*dz + dy*dy
	return dist

def add_weight(korok):
	additional_weight = 0

	# penalty for castle koroks
	if 'X' in korok.id:
		additional_weight += 1000

	# penalty for flower trails, rock pattern, melt ice block
	if korok.type in ['Flower Trail', 'Rock Pattern', 'Melt Ice Block']:
		additional_weight += 1000

	return additional_weight

def nearest_neighbor(pos, neighbors):
	min_korok = None
	min_distance = 99999
	for korok_id in neighbors:
		# compute weighted distance
		weighted_dist = math.sqrt(squared_distance(pos, neighbors[korok_id].pos))
		weighted_dist += add_weight(neighbors[korok_id])

		if weighted_dist < min_distance and weighted_dist > 0:
			min_distance = weighted_dist
			min_korok = korok_id
	return min_korok


def nearest_neighbor_A_star(pos, neighbors, param):
	min_korok = None
	min_distance = 999999
	for korok_id in neighbors:
		# compute weighted distance
		weighted_dist = math.sqrt(squared_distance(pos, neighbors[korok_id].pos)) * (100 - param)/100.0
		# weighted_dist += add_weight(neighbors[korok_id])
		# add heuristic
		weighted_dist += math.sqrt(squared_distance(neighbors[korok_id].pos, wetland_stable)) * param/100.0

		if weighted_dist < min_distance:
			min_distance = weighted_dist
			min_korok = korok_id
	return min_korok


def reverse_A_star(ending_korok, neighbors, length):
	current = neighbors[ending_korok].pos
	neighbors.pop(ending_korok) # remove the starting location
	path = [ending_korok]
	while len(path) <= length:
		next_korok = nearest_neighbor_A_star(current, neighbors, len(path))
		path.append(next_korok)
		current = neighbors[next_korok].pos
		neighbors.pop(next_korok)
	path.reverse()
	return path


def create_path(starting, neighbors, length):
	current = starting
	path = []
	while len(path) <= length:
		next_korok = nearest_neighbor(current, neighbors)
		path.append(next_korok)
		current = neighbors[next_korok].pos
		neighbors.pop(next_korok)
	return path

def path2celer(path):
	celer_string = ""
	for korok_id in path:
		celer_string += "    - _Korok::" + korok_id + "\n"
	return celer_string

# load json data
f = open(sys.argv[1])
data = json.load(f)
f.close()

# create position dictionary
for element in data:
	k_id = element["korok_id"]
	k_pos = element["pos"]
	k_type = element["korok_type"]
	korok_pos[k_id] = Korok(k_id, k_pos, k_type)

# test
# print(korok_pos['H07'])
# print(nearest_neighbor(starting,korok_pos))
# print(path2celer(create_path(wetland_stable, korok_pos, 100)))
print(path2celer(reverse_A_star("L26", korok_pos, 100)))