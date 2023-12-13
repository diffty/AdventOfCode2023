import re
import os
import math
import itertools


FP = open("output.log", "w")


test_data = '''
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
'''

test_data2 = '''
????.#...#... 4,1,1
#####.#### 5,4
'''

test_data3 = '''
??????????????? 6,2
'''


def print_to_disk(*s):
    s = list(map(str, s))
    FP.write(" ".join(s))
    FP.write("\n")
    print(*s)


data = test_data
data = open(os.path.dirname(__file__) + "/data.txt").read()

data_lines = data.strip().split('\n')

FP.close()

total_nb_arrangements = 0

for line_num, line_data in enumerate(data_lines):
    FP = open("output.log", "a")

    curr_line_nb_arrangements = 0

    row_map, broken_count_raw = line_data.split(" ")
    print_to_disk(f"-- {line_num+1}/{len(data_lines)} ({round(line_num/len(data_lines)*100)}%) --")

    broken_count = list(map(int, broken_count_raw.split(',')))
    #print(f"{broken_count=}")

    unknown_coord_list = [res.start() for res in re.finditer('\?', row_map, re.I)]
    #print(f"{unknown_coord_list=}")

    nb_spaces = len(row_map) - sum(broken_count)
    #print(f"{nb_spaces=}")

    same = False

    parsed_broken_blocks = re.findall("(#+)", row_map, re.I)

    if len(parsed_broken_blocks) == len(broken_count) and len(unknown_coord_list) == 0:
        for broken_parts_block_num, res in enumerate(parsed_broken_blocks):
            #print(broken_parts_block_num, res)

            if broken_parts_block_num >= len(broken_count):
                break

            if broken_count[broken_parts_block_num] != len(res):
                break            
        else:
            print_to_disk(row_map)
            print_to_disk("OMG???")
            same = True

    if same:
        curr_line_nb_arrangements += 1
    else:
        spaces_permutations = []

        for broken_count_idx in range(len(broken_count)+1):
            single_permutation = []

            if broken_count_idx in [0, len(broken_count)]:
                single_permutation.append("")
            else:
                single_permutation.append(None)

            for s in range(1, nb_spaces+1):
                single_permutation.append("".join(["."] * s))
            
            spaces_permutations.append(single_permutation)

        #print(f"{spaces_permutations=}")

        w = len(spaces_permutations[0])
        h = len(spaces_permutations)

        print_to_disk(f"{w}^{h} = {w ** h}")
        print_to_disk(row_map, broken_count_raw)

        for i in range(w ** h):
            comb = [int((i / (w**row if row > 0 else 1)) % w) for row in range(h)]
            #print(comb)
            curr_combination = [spaces_permutations[n][c] for n, c in enumerate(comb)]
            #print(curr_combination)
            #print_to_disk(curr_combination)

            # if None not in curr_combination:
            #     result = ""

            #     for j, s in enumerate(curr_combination[:-1]):
            #         result += s + "#" * broken_count[j]

            #     result += curr_combination[-1]
            #     print(
            #         "✅" if len("".join(curr_combination)) == nb_spaces else "❌",
            #         "✅" if all([result[res.start()] == res.group(1) for res in re.finditer('([#.])', row_map, re.I)]) else "❌",
            #         result)
            
            if None not in curr_combination and len("".join(curr_combination)) == nb_spaces:
                result = ""

                for j, s in enumerate(curr_combination[:-1]):
                   result += s + "#" * broken_count[j]

                result += curr_combination[-1]

                if all([result[res.start()] == res.group(1) for res in re.finditer('([#.])', row_map, re.I)]):
                    print_to_disk(result)
                    curr_line_nb_arrangements += 1
        
    total_nb_arrangements += curr_line_nb_arrangements
    print_to_disk(f"{curr_line_nb_arrangements=}")
    print_to_disk()

    FP.close()

FP = open("output.log", "a")

print_to_disk(f"{total_nb_arrangements=}")

FP.close()
