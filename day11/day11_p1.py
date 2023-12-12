import os
import re
import itertools

EXPANSION_COEF = 2

test_data = '''
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
'''

data = test_data
data = open(os.path.dirname(__file__) + "/data.txt").read()

universe = [list(l) for l in data.strip().split("\n")]

def _row_is_empty(row):
    return all(map(lambda c: c == '.', row))

def _expand_universe(universe):
    return list(itertools.chain(*[[l] * (EXPANSION_COEF if _row_is_empty(l) else 1) for l in universe]))

universe = _expand_universe(universe)
rot_universe = zip(*universe)
rot_universe = _expand_universe(rot_universe)
universe = list(zip(*rot_universe))

for l in universe:
    print("".join(l))

galaxies_pos_list = [(res.start(), y) for y, l in enumerate(universe) for res in re.finditer("#", "".join(l), re.I)]
print(galaxies_pos_list)
print()

galaxies = dict(enumerate(galaxies_pos_list))
print(galaxies)
print()

galaxies_pairs = list(itertools.combinations(galaxies.keys(), 2))
print(galaxies_pairs)
print()

def sub_vect(a, b):
    return (abs(b[0] - a[0]), abs(b[1] - a[1]))

distances_per_pair = dict(map(lambda p: ((p[0], p[1]), sum(sub_vect(galaxies[p[0]], galaxies[p[1]]))), galaxies_pairs))
print(distances_per_pair)
print()

print(sum(distances_per_pair.values()))
