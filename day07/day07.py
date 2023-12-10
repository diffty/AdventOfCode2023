import itertools


test_data = '''
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
'''

card_rank = "AKQJT98765432"

raw_data = test_data

data_lines = raw_data.strip().split('\n')

for l in data_lines:
    cards, bid = l.split()
    sorted_cards = sorted(cards, key=lambda letter: card_rank.index(letter))
    cards_count = {}
    for card in sorted_cards:
        if card not in cards_count:
            cards_count[card] = 0
        cards_count[card] += 1
    cards_count_sorted = (sorted(cards_count.items(), key=lambda it: it[1], reverse=True))
    if cards_count_sorted[0][1] == 5:
        print ("Five of a kind")
