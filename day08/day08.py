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

data = test_data2.strip()
data = open(os.path.dirname(__file__) + "/data.txt").read().strip()
#data = test_data3.strip()

map_nodes = {}

general_reg_res = GENERAL_PARSER_REGEX.search(data)

if general_reg_res:
    for res in MAP_PARSER_REGEX.finditer(general_reg_res.group(2)):
        map_nodes[res.group(1)] = res.groups()[1:]


directions = list(map(lambda l: {"L": 0, "R": 1}[l], general_reg_res.group(1)))


# PART 1
'''
i = 0
directions_cursor = 0

curr_node_name = "AAA"
while curr_node_name != "ZZZ":
    curr_node = map_nodes[curr_node_name]
    curr_node_name = curr_node[directions[directions_cursor]]

    directions_cursor = (directions_cursor + 1) % len(directions)
    i += 1

print(i)
'''

# PART 2

directions_cursor = 0

start_nodes_names = list(filter(lambda n: n.endswith('A'), map_nodes))
#print(start_nodes_names)

end_nodes_names = list(filter(lambda n: n.endswith('Z'), map_nodes))
#print(end_nodes_names)

curr_nodes_name_list = list(start_nodes_names)

i = 0

while not all([n.endswith("Z") for n in curr_nodes_name_list]):    
    for node_num, node_name in enumerate(curr_nodes_name_list):
        curr_node = map_nodes[node_name]
        curr_nodes_name_list[node_num] = curr_node[directions[directions_cursor]]

    #print(curr_nodes_name_list)

    directions_cursor = (directions_cursor + 1) % len(directions)
    i += 1

print(i)
