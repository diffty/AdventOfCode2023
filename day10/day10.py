import os
import sys
import copy
import itertools
import copy
import time


test_data = '''
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
'''

test_data2 = '''
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
'''

def _print(text, x=0, y=0):
    sys.stdout.write("\033[{};{}H".format(y, x))
    #sys.stdout.write("\033[K")
    sys.stdout.write(text)
    sys.stdout.flush()


def display_map(m):
    for y in range(len(m)):
        for x in range(len(m[0])):
            sys.stdout.write(m[y][x])
        sys.stdout.write('\n')
    sys.stdout.write('\n')



def display_map_old(m):
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

nice_tiles = {
    "|": "║",
    "-": "═",
    "L": "╚",
    "J": "╝",
    "7": "╗",
    "F": "╔",
    "S": "S",
}

directions = [(0, -1), (1,  0), (0,  1), (-1, 0)]

curr_pos = starting_point_pos
prev_pos = None

end_reached = False

i = 0

distance_map[curr_pos[1]][curr_pos[0]] = 0
nice_map = [[" "]*len(tiles[0]) for y in range(len(tiles))]
io_map = [["I"]*len(tiles[0]) for y in range(len(tiles))]

open_tiles_list = []

directions_list = []

while not end_reached:
    for next_dir in directions:
        next_pos = (curr_pos[0] + next_dir[0], curr_pos[1] + next_dir[1])
        direction = (next_pos[0] - curr_pos[0], next_pos[1] - curr_pos[1])

        if next_pos[0] < 0 or next_pos[0] >= len(tiles[0]) or next_pos[1] < 0 or next_pos[1] >= len(tiles):
            continue
        
        if next_pos != prev_pos:
            next_t = tiles[next_pos[1]][next_pos[0]]
            curr_t = tiles[curr_pos[1]][curr_pos[0]]

            next_tile_rules = tiles_type.get(next_t, None)
            curr_tile_rules = tiles_type.get(curr_t, None)

            if      (next_tile_rules is None or next_tile_rules[0](direction)) \
                and (curr_tile_rules is None or curr_tile_rules[1](direction)):

                if next_t == "S":
                    end_reached = True

                distance_map[curr_pos[1]][curr_pos[0]] = i
                nice_map[curr_pos[1]][curr_pos[0]] = nice_tiles.get(curr_t, " ")
                
                enter_dir = None

                if prev_pos is not None:
                    enter_dir = (curr_pos[0] - prev_pos[0], curr_pos[1] - prev_pos[1])

                exit_dir = direction
                
                directions_list.append((curr_pos, enter_dir, exit_dir))

                io_map[curr_pos[1]][curr_pos[0]] = "P"

                prev_pos = curr_pos
                curr_pos = next_pos

                break

    i += 1


def _tag_tile_using_dir(dir):
    right_dir = directions[(directions.index(dir) + 1) % len(directions)]
    right_pos = (curr_pos[0] + right_dir[0], curr_pos[1] + right_dir[1])

    if right_pos[0] >= 0 and right_pos[0] < len(tiles[0]) and right_pos[1] >= 0 and right_pos[1] < len(tiles) and io_map[right_pos[1]][right_pos[0]] != "P":
        io_map[right_pos[1]][right_pos[0]] = "O"
        open_tiles_list.append(right_pos)


for tile_info in directions_list:
    curr_pos, enter_dir, exit_dir = tile_info

    if enter_dir:
        _tag_tile_using_dir(enter_dir)
    
    _tag_tile_using_dir(exit_dir)


print(int(i / 2))

display_map(nice_map)
print()

display_map(io_map)
print()


def fill(tile_map, start_tiles, fill_tile, replacable_tile):
    next_tiles = list(start_tiles)

    while len(next_tiles) > 0:
        tile_pos = next_tiles.pop(0)

        for rx in range(-1, 2):
            for ry in range(-1, 2):
                if rx != 0 and ry != 0:
                    next_tile_pos = (tile_pos[0] + rx, tile_pos[1] + ry)
                    if next_tile_pos[0] >= 0 and next_tile_pos[0] <= len(tile_map[0])-1 and next_tile_pos[1] >= 0 and next_tile_pos[1] <= len(tile_map)-1:
                        if tile_map[next_tile_pos[1]][next_tile_pos[0]] in replacable_tile:
                            tile_map[next_tile_pos[1]][next_tile_pos[0]] = fill_tile
                            #_print(fill_tile, next_tile_pos[0], next_tile_pos[1])
                            #time.sleep(0.05)
                            #input()
                            next_tiles.append(next_tile_pos)
        
        #display_map(tile_map)


fill(io_map, open_tiles_list, "O", ["I"])

display_map(io_map)
print()

print(f'\n[[{list(itertools.chain(*io_map)).count("I")}]]')
