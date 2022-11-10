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
type_weights = {}

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
	if korok.type in type_weights:
		additional_weight += type_weights[korok.type]

	return additional_weight

def nearest_neighbor(pos, neighbors):
	min_korok = None
	min_distance = 99999
	for korok_id in neighbors:
		# compute straight-line distance
		weighted_dist = math.sqrt(squared_distance(pos, neighbors[korok_id].pos))

		# additional weight
		weighted_dist += add_weight(neighbors[korok_id])
		if neighbors[korok_id].pos[1] - pos[1] > 80:
			weighted_dist += 200

		if weighted_dist < min_distance and weighted_dist > 0:
			min_distance = weighted_dist
			min_korok = korok_id
	return min_korok, min_distance


def nearest_neighbor_A_star(pos, neighbors, param):
	min_korok = None
	min_distance = 1e100
	for korok_id in neighbors:
		# compute weighted distance
		weighted_dist = math.sqrt(squared_distance(pos, neighbors[korok_id].pos)) * (100 - param)
		weighted_dist += math.sqrt(squared_distance(neighbors[korok_id].pos, wetland_stable)) * param

		if weighted_dist < min_distance:
			min_distance = weighted_dist
			min_korok = korok_id
	return min_korok, min_distance


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
	total_dist = 0
	while len(path) <= length:
		next_korok, dist_to_next = nearest_neighbor(current, neighbors)
		path.append(next_korok)
		current = neighbors[next_korok].pos
		neighbors.pop(next_korok)
		total_dist += dist_to_next
	print(total_dist)
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
	if k_type not in ['Melt Ice Block', 'Jump the Funces'] and k_id not in ['P09']:
		korok_pos[k_id] = Korok(k_id, k_pos, k_type)

g = open('weights_by_type.json')
data = json.load(g)
g.close()

for element in data:
	k_type = element["type"]
	k_weight = element["weight"]
	type_weights[k_type] = k_weight


route_string = ""
with open('../route-header.txt') as header:
    for s in header.readlines():
    	route_string += s
header.close()

route_string += "\n" + path2celer(create_path(wetland_stable, korok_pos, 100))

main_route = open('../main.celer', 'w')
main_route.write(route_string)
main_route.close()