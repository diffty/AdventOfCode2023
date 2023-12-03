import re
import os
from functools import reduce


test_data = '''
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
'''


with open(os.path.dirname(__file__) + "/data.txt") as fp:
    #data = test_data.strip().split('\n')
    data = fp.read().strip().split('\n')

    number_map = []
    symbol_map = []

    for y, l in enumerate(data):
        curr_line = []
        reg_res = re.finditer(r"(?:(\d+)|([^.]))", l, re.I)
        for r in reg_res:
            if r.group(1) is not None:
                curr_line.append((r.group(1), r.span()))

            if r.group(2) is not None:
                symbol_map.append((r.span()[0], y))
        
        number_map.append(curr_line)

    parts = []
    gear_ratios = []

    for s in symbol_map:
        curr_symbol_numbers = []

        for y in range(max(s[1]-1, 0), min(s[1]+2, len(number_map))):
            for n in number_map[y]:
                number, span = n
                if s[0] >= span[0]-1 and s[0] < span[1]+1:
                    curr_symbol_numbers.append(int(number))
        
        if len(curr_symbol_numbers) == 2:
            gear_ratios.append(reduce(lambda a, b: a * b, curr_symbol_numbers))

        parts.extend(curr_symbol_numbers)

    # PART 1
    print(sum(parts))

    # PART 2
    print(sum(gear_ratios))
