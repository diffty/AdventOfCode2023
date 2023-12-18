import os

test_data = '''
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
'''

data = test_data
data = open(os.path.dirname(__file__) + "/data.txt").read()

data_lines = data.strip().split()

data_lines_rot = list(map(lambda l: "".join(l), zip(*data_lines)))
print(data_lines_rot)

new_data_lines_rot = []

weight = 0

for i, l in enumerate(data_lines_rot):
    splitted_line = l.split('#')
    pos = len(l)

    for j, section in enumerate(splitted_line):
        nb_boulders = section.count("O")
        splitted_line[j] = ("O" * nb_boulders).ljust(len(section), '.')
        print(list(range(pos-nb_boulders+1,pos+1)))
        weight += sum(range(pos-nb_boulders+1,pos+1))
        pos -= len(section)+1
        print(weight)
    
    data_lines_rot[i]  = "#".join(splitted_line)

data_lines = list(map(lambda l: "".join(l), zip(*data_lines_rot)))
print(data_lines)

print(weight)
