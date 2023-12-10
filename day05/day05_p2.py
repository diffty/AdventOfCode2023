import re
import os
import itertools


test_data = '''
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
'''


# VARS & DATA STRUCTURES
parsed_data = {}
mappings = {}


# DATA PARSING
data = test_data.strip()
data = open(os.path.dirname(__file__) + "/data.txt").read().strip()

DATA_PARSER1_REGEX = re.compile(r"([a-z\-]*)(?: ([a-z]+))?:((?:[ \n\t\r]*\d+)*)", re.I)
DATA_PARSER2_REGEX = re.compile(r"([0-9a-z]+)(?:-to-([0-9a-z]+))?", re.I)

for it in DATA_PARSER1_REGEX.finditer(data):
    var_name, var_type, var_value = it.groups()
    parsed_data[var_name] = [var_type, var_value.strip()]

seeds = list(map(int, parsed_data["seeds"][1].split()))


# DATA PROCESSING
for var_name, var_content in parsed_data.items():
    var_type, var_value = var_content
    if var_type == "map":
        src, dst = DATA_PARSER2_REGEX.search(var_name).groups()
        
        mappings[src] = [dst, list(map(str.split, var_value.split("\n")))]
        

# MAKE INITIAL PART 1 SEEDS INTERVALS
sections = [(s, s) for s in seeds]

# MAKE INITIAL PART 2 SEEDS INTERVALS (comment to compute following part 1 rules)
sections = list(zip(seeds[::2], map(sum, zip(seeds[::2], seeds[1::2]))))
sections = sorted(sections, key=lambda item: item[0])


# REMAP INTERVALS
def remap(value, src_start, src_end, dst_start, dst_end):
    return dst_start + ((value - src_start) / (src_end - src_start)) * (dst_end - dst_start)


def cut_sections(section, mapping):
    for dst_range_start, src_range_start, range_length in mapping:
        range_length = int(range_length)
        src_range_start = int(src_range_start)
        src_range_end = int(src_range_start + range_length)

        i = 0
        for section_start, section_end in list(sections):
            section_start = int(section_start)
            section_end = int(section_end)

            if section_start < src_range_start and src_range_start < section_end:
                sections[i] = (src_range_start, sections[i][1])
                sections.insert(i, (section_start, src_range_start-1))
                i += 1
                
            if section_start < src_range_end and src_range_end < section_end:
                sections[i] = (sections[i][0], src_range_end-1)
                sections.insert(i+1, (src_range_end, section_end))
                i += 1
            
            i += 1
    
    return sections


def remap_sections(sections, mapping):
    new_sections = list(sections)

    for i, s in enumerate(sections):
        new_s = s

        for dst_range_start, src_range_start, range_length in mapping:
            range_length = int(range_length)
            src_range_start = int(src_range_start)
            src_range_end = int(src_range_start + range_length)
            dst_range_start = int(dst_range_start)
            dst_range_end = int(dst_range_start + range_length)

            if src_range_start <= s[0] and s[1] <= src_range_end:
                new_s = (
                    int(remap(s[0], src_range_start, src_range_end, dst_range_start, dst_range_end)),
                    int(remap(s[1], src_range_start, src_range_end, dst_range_start, dst_range_end))
                )
        
        new_sections[i] = new_s
        
    return new_sections


sections = sorted(sections, key=lambda item: item[0])

next_mapping_name, curr_mapping = mappings["seed"]

while curr_mapping != None:
    sections = cut_sections(sections, curr_mapping)
    sections = remap_sections(sections, curr_mapping)

    next_mapping_name, curr_mapping = mappings.get(next_mapping_name, (None, None))


# UNPACKING AND FINDING MINIMUM INTERVAL VALUE (also get puzzle response)
print(min(itertools.chain.from_iterable(sections)))
