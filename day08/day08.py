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

GENERAL_PARSER_REGEX = re.compile(r"([RL]+)\s+(.+)", re.I | re.DOTALL)
MAP_PARSER_REGEX = re.compile(r"(\w+) = \((\w+), (\w+)\)", re.I | re.DOTALL)

data = test_data2.strip()
data = open(os.path.dirname(__file__) + "/data.txt").read().strip()

map_nodes = {}

general_reg_res = GENERAL_PARSER_REGEX.search(data)

if general_reg_res:
    for res in MAP_PARSER_REGEX.finditer(general_reg_res.group(2)):
        map_nodes[res.group(1)] = res.groups()[1:]


directions = list(map(lambda l: {"L": 0, "R": 1}[l], general_reg_res.group(1)))
print(directions)
print(map_nodes)

i = 0
directions_cursor = 0

curr_node_name = "AAA"
while curr_node_name != "ZZZ":
    curr_node = map_nodes[curr_node_name]
    curr_node_name = curr_node[directions[directions_cursor]]

    directions_cursor = (directions_cursor + 1) % len(directions)
    i += 1

print(i)
