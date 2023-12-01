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


def replace_spelled_digits(data_line: str):
    end_reached = False

    while not end_reached:
        earliest_digit_found = None
        earliest_digit_found_idx = None

        for spelled_digit, digit in TRANSLATION_TABLE.items():
            found_idx = data_line.find(spelled_digit)

            if found_idx >= 0 and \
                (
                    earliest_digit_found_idx == None or \
                    earliest_digit_found_idx > found_idx
                ):
                
                earliest_digit_found = spelled_digit
                earliest_digit_found_idx = found_idx

        if earliest_digit_found is not None:
            data_line = data_line[:earliest_digit_found_idx] \
                + str(TRANSLATION_TABLE[earliest_digit_found]) \
                + data_line[earliest_digit_found_idx+len(earliest_digit_found):]
        else:
            end_reached = True
    
    return data_line


def decode_line(data_line: str, convert_spelled_numbers = False):
    if convert_spelled_numbers:
        data_line = replace_spelled_digits(data_line)
    
    data_line = list(filter(lambda c: c.isnumeric(), data_line))

    return int(data_line[0] + data_line[-1])


with open(os.path.dirname(__file__) + "/data.txt") as data_fp:
    data_lines = data_fp.readlines()
    #data_lines = test_data1.strip().split("\n")
    #data_lines = test_data2.strip().split("\n")

    # PART 1
    #total = sum([decode_line(l) for l in data_lines])
    #print(total)

    # PART 2
    total = sum([decode_line(l, True) for l in data_lines])
    #print(total)

    print(decode_line("dftzgsdc19threesevennine3twonevl", True))
    #print(decode_line("87twopsix7eightwoj", True))
