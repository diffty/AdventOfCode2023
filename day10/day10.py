import os
import sys
import copy
import itertools


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

nice_tiles = {
    "|": "║",
    "-": "═",
    "L": "╚",
    "J": "╝",
    "7": "╗",
    "F": "╔",
    "S": "S",
}

curr_pos = starting_point_pos
prev_pos = None

end_reached = False

i = 0

distance_map[curr_pos[1]][curr_pos[0]] = 0
nice_map = [[" "]*len(tiles[0]) for y in range(len(tiles))]


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
                nice_map[curr_pos[1]][curr_pos[0]] = nice_tiles.get(curr_t, " ")

                prev_pos = curr_pos
                curr_pos = next_pos
                break

    i += 1

    # preview_buffer = ""

    # for y in range(len(tiles)):
    #     for x in range(len(tiles[x])):
    #         if curr_pos == (x, y):
    #             preview_buffer += "@"
    #         else:
    #             preview_buffer += tiles[y][x]
    #     preview_buffer += '\n'
    
    # print(preview_buffer)


    # preview_buffer = ""

    # for y in range(len(distance_map)):
    #     for x in range(len(distance_map[x])):
    #         preview_buffer += str(distance_map[y][x])
    #     preview_buffer += '\n'
    
    # print(preview_buffer)

    #input()




print(int(i / 2))


display_map(nice_map)

import copy
io_map = copy.deepcopy(distance_map)

for y in range(len(io_map)):
    for x in range(len(io_map[y])):
        if nice_map[y][x] != " ":
            io_map[y][x] = "P" if distance_map[y][x] >= 0 else " "
        else:
            io_map[y][x] = " "


display_map(io_map)

open_tiles_list = []

for y in range(len(io_map)):
    for x in range(len(io_map[0])):
        curr_pos = (x, y)

        if nice_map[y][x] == " ":
            if x in [0, len(io_map[0])-1] or y in [0, len(io_map)-1]:
                io_map[y][x] = "O"
            else:
                pipe_count_l = io_map[y][:x].count("P")
                pipe_count_r = io_map[y][x+1:].count("P")

                io_map_rot = list(zip(*io_map))

                pipe_count_u = io_map_rot[x][:y].count("P")
                pipe_count_d = io_map_rot[x][y+1:].count("P")

                pipe_count = [pipe_count_l, pipe_count_r, pipe_count_u, pipe_count_d]

                if 0 in pipe_count:
                    io_map[y][x] = "O"
                else:
                    io_map[y][x] = "I" if len(list(filter(lambda c: c % 2 == 1, pipe_count))) else "O"
                
                #print(curr_pos, pipe_count, io_map[y][x])

        if io_map[y][x] == "O":
            open_tiles_list.append(curr_pos)
                

    #print(f"y={y}: {''.join(io_map[y])}")

#for tile_pos in open_tiles_list:

print()
display_map(io_map)


def fill(tile_map, start_tiles, fill_tile, replacable_tile):
    next_tiles = list(start_tiles)

    while len(next_tiles) > 0:
        tile_pos = next_tiles.pop(0)

        for rx in range(-1, 2):
            for ry in range(-1, 2):
                next_tile_pos = (tile_pos[0] + rx, tile_pos[1] + ry)
                if next_tile_pos[0] > 0 and next_tile_pos[0] < len(tile_map[0])-1 and next_tile_pos[1] > 0 and next_tile_pos[1] < len(tile_map)-1:
                    if tile_map[tile_pos[1] + ry][tile_pos[0] + rx] in replacable_tile:
                        tile_map[tile_pos[1] + ry][tile_pos[0] + rx] = fill_tile
                        next_tiles.append(next_tile_pos)


fill(io_map, open_tiles_list, "O", ["I"])

print()
display_map(io_map)

print(list(itertools.chain(*io_map)).count("I"))
