import re
import os
import math
import itertools


test_data = '''
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
'''

data = test_data
#data = open(os.path.dirname(__file__) + "/data.txt").read()

data_lines = data.strip().split('\n')

total_nb_arrangements = 0

for line_num, line_data in enumerate(data_lines):
    curr_line_nb_arrangements = 0

    row_map, broken_count_raw = line_data.split(" ")
    print(f"-- {line_num+1}/{len(data_lines)} ({round(line_num/len(data_lines)*100)}%) --")
    print(row_map, broken_count_raw)

    broken_count = list(map(int, broken_count_raw.split(',')))
    unknown_coord_list = [res.start() for res in re.finditer('\?', row_map, re.I)]
    nb_spaces = len(row_map) - sum(broken_count)

    spaces_possibilities = [["" if i in [0, len(broken_count)] else None] + ["".join(["."]*s) for s in range(1, nb_spaces)] for i in range(len(broken_count)+1)]

    combinations = []
    w = len(spaces_possibilities[0])
    h = len(spaces_possibilities)

    for i in range(((w ** h))):
        comb = [int((i / (w**row if row > 0 else 1)) % w) for row in range(h)]
        combinations.append([spaces_possibilities[n][c] for n, c in enumerate(comb)])
    
    combinations = list(filter(lambda c: None not in c and len("".join(c)) == nb_spaces, combinations))

    for spaces in combinations:
        result = ""

        for i, s in enumerate(spaces[:-1]):
            result += s + "#" * broken_count[i]

        result += spaces[-1]

        if all([result[res.start()] == res.group(1) for res in re.finditer('([#.])', row_map, re.I)]):
            print(result)
            curr_line_nb_arrangements += 1
    
    total_nb_arrangements += curr_line_nb_arrangements
    print(f"{curr_line_nb_arrangements=}")
    print()

print(f"{total_nb_arrangements=}")
