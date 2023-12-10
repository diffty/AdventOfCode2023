import re
import os

test_data = '''
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
'''

test_data2 = '''
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
'''

test_data3 = '''
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
'''


GENERAL_PARSER_REGEX = re.compile(r"([RL]+)\s+(.+)", re.I | re.DOTALL)
MAP_PARSER_REGEX = re.compile(r"(\w+) = \((\w+), (\w+)\)", re.I | re.DOTALL)


# PARSING DATA
data = test_data2.strip()
data = open(os.path.dirname(__file__) + "/data.txt").read().strip()

map_nodes = {}

general_reg_res = GENERAL_PARSER_REGEX.search(data)

if general_reg_res:
    for res in MAP_PARSER_REGEX.finditer(general_reg_res.group(2)):
        map_nodes[res.group(1)] = res.groups()[1:]


directions = list(map(lambda l: {"L": 0, "R": 1}[l], general_reg_res.group(1)))


### PART 1
i = 0
directions_cursor = 0

curr_node_name = "AAA"
while curr_node_name != "ZZZ":
    curr_node = map_nodes[curr_node_name]
    curr_node_name = curr_node[directions[directions_cursor]]

    directions_cursor = (directions_cursor + 1) % len(directions)
    i += 1

print(i)


### PART 2

# FINDING ITERATION NUMBER WHERE PATH LOOPS
curr_nodes_name_list = list(filter(lambda n: n.endswith('A'), map_nodes))
directions_cursor = 0
delta_list = []

for node_n in range(len(curr_nodes_name_list)):
    curr_i = 0
    prev_i = 0
    curr_delta = 0
    prev_delta = 0

    node_name = curr_nodes_name_list[node_n]

    while curr_delta != prev_delta or curr_delta == 0:
        curr_node = map_nodes[node_name]
        node_name = curr_node[directions[directions_cursor]]

        directions_cursor = (directions_cursor + 1) % len(directions)

        if node_name.endswith('Z'):
            prev_delta = curr_delta
            curr_delta = curr_i - prev_i
            prev_i = curr_i

        curr_i += 1

    delta_list.append(curr_delta)


# CALCULATE FIRST COMMON MULTIPLE BETWEEN ALL DELTAS
curr_delta = delta_list[0]

while len(delta_list) >= 2:
    while curr_delta % delta_list[1] != 0:
        curr_delta += delta_list[0]

    delta_list = delta_list[1:]
    delta_list[0] = curr_delta

print(delta_list[0])
