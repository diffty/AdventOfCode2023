import os
import re
import itertools

EXPANSION_COEF = 1000000

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


def get_shortest_distance_between_each_galaxy_pairs(universe, expansion_coef):
    def _row_is_empty(row):
        return all(map(lambda c: c == '.', row))

    def _expand_universe_coord_map(universe, coord_map, axis_x=False):
        offset = 0

        if axis_x:
            coord_map = list(zip(*coord_map))
            universe = list(zip(*universe))

        for y, l in enumerate(universe):
            if _row_is_empty(l):
                offset += expansion_coef - 1
            
            if offset > 0:
                coord_map[y] = list(
                    map(
                        lambda expand_line: (expand_line[0], expand_line[1] + offset) if not axis_x
                                            else (expand_line[0] + offset, expand_line[1]),
                        coord_map[y]
                    )
                )

        if axis_x:
            coord_map = list(zip(*coord_map))
            universe = list(zip(*universe))

        return coord_map

    def _sub_vect(a, b):
        return (abs(b[0] - a[0]), abs(b[1] - a[1]))


    coord_map = [[(x, y) for x in range(len(universe[0]))] for y in range(len(universe))]
    coord_map = _expand_universe_coord_map(universe, coord_map)
    coord_map = _expand_universe_coord_map(universe, coord_map, axis_x=True)

    galaxies_pos_list = [coord_map[y][res.start()] for y, l in enumerate(universe) for res in re.finditer("#", "".join(l), re.I)]
    galaxies = dict(enumerate(galaxies_pos_list))
    galaxies_pairs = list(itertools.combinations(galaxies.keys(), 2))

    distances_per_pair = dict(map(lambda p: ((p[0], p[1]), sum(_sub_vect(galaxies[p[0]], galaxies[p[1]]))), galaxies_pairs))
    return distances_per_pair


# PART 1
print(sum(get_shortest_distance_between_each_galaxy_pairs(universe, 2).values()))

# PART 2
print(sum(get_shortest_distance_between_each_galaxy_pairs(universe, 1000000).values()))
