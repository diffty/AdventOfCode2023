import re
import os


test_data = '''
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
'''


data = test_data
data = open(os.path.dirname(__file__) + "/data.txt").read()

card_line_reg = re.compile(r"^Card *(\d+)[^:]*:([0-9 ]*)\|([0-9 ]*)$", re.I)

card_matches = {}

for l in data.split("\n"):
    res = card_line_reg.search(l)
    if res:
        card_matches[int(res.group(1))] = len(set(res.group(2).strip().split()) & set(res.group(3).strip().split()))

# PART 1
print(sum(map(lambda v: 2 ** (v-1) if v > 0 else 0, card_matches.values())))

# PART 2
cards_stack = list(card_matches.items())

i = 0
while i < len(cards_stack):
    card_id = cards_stack[i][0]
    cards_stack.extend(cards_stack[card_id:card_id + card_matches[card_id]])
    i += 1

print(len(cards_stack))
