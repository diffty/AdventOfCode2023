import os

test_data = '''
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
'''

test_data2 = '''
#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
'''

def find_pattern_vertical_mirror_axis(pattern_lines):
    for y in range(1, len(pattern_lines)):
        min_y = y-1
        max_y = y

        while (min_y >= 0 and max_y < len(pattern_lines)):
            up_slice = pattern_lines[min_y:y]
            down_slice = list(reversed(pattern_lines[y:max_y+1]))
            
            min_y -= 1
            max_y += 1

        if up_slice == down_slice:
            return y
            
    return None


data = test_data
data = open(os.path.dirname(__file__) + "/data.txt").read()

patterns = data.strip().split("\n\n")

total = 0

for i, p in enumerate(patterns):
    print(f"---- PATTERN #{i}----")
    pattern_lines = p.split("\n")

    for l in pattern_lines:
        print(" ".join(list(l)))

    y = find_pattern_vertical_mirror_axis(pattern_lines)
    pattern_lines_rot = list(map(lambda l: "".join(l), zip(*pattern_lines)))
    x = find_pattern_vertical_mirror_axis(pattern_lines_rot)
    print(f"{x=}", f"{y=}")

    if y is not None:
        total += y * 100
    
    if x is not None:
        total += x
    
    print()


print(f"{total=}")