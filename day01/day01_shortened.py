import os


def find_first_digit(data_line: str, reverse = False):
    digit_table = list(map(lambda d: d[::-1] if reverse else d, ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"] + list(map(str, range(10)))))
    return str(sorted(list(filter(lambda d: d[1] >= 0, map(lambda d: (d[0] % 10, (data_line[::-1] if reverse else data_line).find(d[1])), enumerate(digit_table)))), key=lambda d: d[1])[0][0])


with open(os.path.dirname(__file__) + "/data.txt") as data_fp:
    data_lines = data_fp.readlines()
    print(sum([int(find_first_digit(l) + find_first_digit(l, reverse=True)) for l in data_lines]))
