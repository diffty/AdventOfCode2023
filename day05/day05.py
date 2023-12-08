import re
import os


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

data = test_data.strip()
data = open(os.path.dirname(__file__) + "/data.txt").read().strip()

d = re.compile(r"([a-z\-]*)(?: ([a-z]+))?:((?:[ \n\t\r]*\d+)*)", re.I)
d2 = re.compile(r"([0-9a-z]+)(?:-to-([0-9a-z]+))?", re.I)

parsed_data = {}

for it in d.finditer(data):
    var_name, var_type, var_value = it.groups()
    parsed_data[var_name] = (var_type, var_value.strip())

seeds = list(map(int, parsed_data["seeds"][1].split()))

def remap(value, src_start, src_end, dst_start, dst_end):
    return dst_start + ((value - src_start) / (src_end - src_start)) * (dst_end - dst_start)

mappings = {}
mappers = {}

for var_name, var_content in parsed_data.items():
    var_type, var_value = var_content
    if var_type == "map":
        src, dst = d2.search(var_name).groups()
        
        mappings[src] = (dst, list(map(str.split, var_value.split("\n"))))
        

def make_mapping(dest_range_start, source_range_start, range_length):
    return dict(zip(list(range(dest_range_start, dest_range_start + range_length)),
                    list(range(source_range_start, source_range_start + range_length))))
    

def m(start_name, value):
    curr_mapping = mappings[start_name]

    while curr_mapping is not None:
        for dst_range_start, src_range_start, range_length in curr_mapping[1]:
            dst_range_start = int(dst_range_start)
            src_range_start = int(src_range_start)
            range_length = int(range_length)

            if src_range_start <= value and value <= src_range_start + range_length:
                value = dst_range_start + (value - src_range_start)
                break

        start_name = mappings[start_name][0]
        curr_mapping = mappings.get(start_name, None)
    
    return value


print(min([m("seed", s) for s in seeds]))
