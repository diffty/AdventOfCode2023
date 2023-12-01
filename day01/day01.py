import os


test_data1 = '''
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
'''

test_data2 = '''
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
'''


TRANSLATION_TABLE = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def find_first_digit(data_line, reverse=False):
    if reverse:
        data_line = data_line[::-1]
        translation_table = dict(
            map(lambda it: (it[0][::-1], it[1]), 
                TRANSLATION_TABLE.items()
            )
        )
    else:
        translation_table = TRANSLATION_TABLE
    
    translation_table.update(map(lambda i: (str(i), i), range(1, 10)))

    earliest_digit_idx = None
    earliest_digit = None

    for spelled_digit, digit in translation_table.items():
        idx = data_line.find(spelled_digit)

        if idx >= 0 and (earliest_digit_idx == None or idx < earliest_digit_idx):
            earliest_digit_idx = idx
            earliest_digit = digit

    return earliest_digit


def decode_line(data_line: str):
    first_digit = find_first_digit(data_line)
    last_digit = find_first_digit(data_line, True)
    return int(str(first_digit) + str(last_digit))


with open(os.path.dirname(__file__) + "/data.txt") as data_fp:
    test_data1_lines = test_data1.strip().split("\n")
    test_data2_lines = test_data2.strip().split("\n")
    data_lines = data_fp.readlines()

    # PART 1
    total = sum([decode_line(l) for l in test_data1_lines])
    print(total)

    # PART 2
    total = sum([decode_line(l) for l in test_data2_lines])
    print(total)

    total = sum([decode_line(l) for l in data_lines])
    print(total)

    #print(find_first_digit("dftzgeninsdc19threeseveeninnnine3twonevtwolinazdzad", True))
    #print(decode_line("87twopsix7eightwoj", True))
