import sys
import json
import math

starting = [890.25, 131.28, 157.06]

korok_pos = {}

def squared_distance(pos1, pos2):
	dx = pos1[0] - pos2[0]
	dz = pos1[1] - pos2[1]
	dy = pos1[2] - pos2[2]
	return dx*dx + dz*dz + dy*dy

def nearest_neighbor(pos, neighbors):
	min_korok = None
	min_distance = 99999
	for korok_id in neighbors:
		dist = math.sqrt(squared_distance(pos, neighbors[korok_id]))
		if dist < min_distance and dist > 0:
			min_distance = dist
			min_korok = korok_id
	return min_korok

def create_path(starting, neighbors, length):
	current = starting
	path = []
	while len(path) <= length:
		next_korok = nearest_neighbor(current, neighbors)
		path.append(next_korok)
		current = neighbors[next_korok]
		neighbors.pop(next_korok)
	return path

def path2celer(path):
	celer_string = ""
	for korok_id in path:
		celer_string += "- _Korok::" + korok_id + "\n"
	return celer_string

# load json data
f = open(sys.argv[1])
data = json.load(f)
f.close()

# create position dictionary
for element in data:
	kid = element["korok_id"]
	pos = element["pos"]
	korok_pos[kid] = pos

# test
# print(korok_pos['H07'])
# print(nearest_neighbor(starting,korok_pos))
print(path2celer(create_path(starting, korok_pos, 100)))