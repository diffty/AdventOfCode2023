import os
import sys

test_data = '''
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
'''

test_data2 = '''
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
'''


def display_map(m):
    for y in range(len(m)):
        print("".join(m[y]))


data = test_data2
data = open(os.path.dirname(__file__) + "/data.txt").read()

tiles = [list(l) for l in data.strip().split("\n")]

distance_map = []
for y in range(len(tiles)):
    distance_map.append(list([-1] * len(tiles[0])))


starting_point_pos = None
for y, l in enumerate(tiles):
    for x, t in enumerate(l):
        if t == 'S':
            starting_point_pos = (x, y)
            break


tiles_type = { 
    "|": (
        lambda d: d[0] == 0 and d[1] != 0,
        lambda d: d[0] == 0 and d[1] != 0
    ),
    "-": (
        lambda d: d[0] != 0 and d[1] == 0,
        lambda d: d[0] != 0 and d[1] == 0
    ),
    "L": (
        lambda d: d in [(-1, 0), (0,  1)],
        lambda d: d in [( 1, 0), (0, -1)],
    ),
    "J": (
        lambda d: d in [( 1, 0), (0,  1)],
        lambda d: d in [(-1, 0), (0, -1)],
    ),
    "7": (
        lambda d: d in [( 1, 0), (0, -1)],
        lambda d: d in [(-1, 0), (0,  1)],
    ),
    "F": (
        lambda d: d in [(-1, 0), (0, -1)],
        lambda d: d in [( 1, 0), (0,  1)],
    ),
}

curr_pos = starting_point_pos
prev_pos = None

end_reached = False

i = 0

distance_map[curr_pos[1]][curr_pos[0]] = 0

while not end_reached:
    for next_dir in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        next_pos = (curr_pos[0] + next_dir[0], curr_pos[1] + next_dir[1])
        direction = (next_pos[0] - curr_pos[0], next_pos[1] - curr_pos[1])

        if next_pos[0] < 0 or next_pos[0] >= len(tiles[0]) or next_pos[1] < 0 or next_pos[1] >= len(tiles):
            continue
        
        if next_pos != prev_pos:
            next_t = tiles[next_pos[1]][next_pos[0]]
            curr_t = tiles[curr_pos[1]][curr_pos[0]]

            #print(f"{curr_t} ({curr_pos}) => {next_t} ({next_pos})")

            next_tile_rules = tiles_type.get(next_t, None)
            curr_tile_rules = tiles_type.get(curr_t, None)

            if (next_tile_rules is None or next_tile_rules[0](direction)) \
                and (curr_tile_rules is None or curr_tile_rules[1](direction)):

                if next_t == "S":
                    end_reached = True

                distance_map[curr_pos[1]][curr_pos[0]] = i

                prev_pos = curr_pos
                curr_pos = next_pos
                break

    i += 1

print(int(i / 2))
