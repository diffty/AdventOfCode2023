import os


test_data = '''
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
'''

APPLY_JOKER_RULE = True

#card_rank = "AKQJT98765432"  # PART 1
card_rank = "AKQT98765432J"  # PART 2

card_rank_indexed = dict(map(lambda it: (it[1], it[0]), enumerate(reversed(card_rank))))

print(card_rank_indexed)

#raw_data = test_data
raw_data = open(os.path.dirname(__file__) + "/data.txt").read()

data_lines = raw_data.strip().split('\n')

hands_sorted = []


for l in data_lines:
    cards, bid = l.split()
    #sorted_cards = sorted(cards, key=lambda letter: card_rank.index(letter))
    cards_count = {}
    for card in cards:
        if card not in cards_count:
            cards_count[card] = 0
        cards_count[card] += 1

    cards_count_sorted = sorted(cards_count.items(), key=lambda it: it[1], reverse=True)
    
    hand_encoded = "".join(map(lambda c: str(hex(card_rank_indexed[c]))[2:], cards))

    if APPLY_JOKER_RULE:
        joker_count = cards_count.get("J", 0)
        
        if cards_count_sorted[0][0] == 'J' and len(cards_count_sorted) > 1:
            cards_count_sorted[0] = (cards_count_sorted[0][0], cards_count_sorted[0][1] + cards_count_sorted[1][1])
        elif cards_count_sorted[0][0] != 'J':
            cards_count_sorted[0] = (cards_count_sorted[0][0], cards_count_sorted[0][1] + joker_count)

    
    if cards_count_sorted[0][1] == 5:
        hand_encoded = '7' + hand_encoded

    elif cards_count_sorted[0][1] == 4:
        hand_encoded = '6' + hand_encoded

    elif cards_count_sorted[0][1] == 3 and cards_count_sorted[1][1] == 2:
        hand_encoded = '5' + hand_encoded

    elif cards_count_sorted[0][1] == 3:
        hand_encoded = '4' + hand_encoded

    elif cards_count_sorted[0][1] == 2 and cards_count_sorted[1][1] == 2:
        hand_encoded = '3' + hand_encoded

    elif cards_count_sorted[0][1] == 2:
        hand_encoded = '2' + hand_encoded

    else:
        hand_encoded = '1' + hand_encoded

    #print(cards, hand_encoded)

    hands_sorted.append((hand_encoded, cards, bid))

hands_sorted = sorted(hands_sorted, key=lambda h: h[0])
for h in enumerate(hands_sorted):
    print(h, h[0] + 1, int(h[1][2]), (h[0] + 1) * int(h[1][2]))

print(sum(map(lambda h: (h[0] + 1) * int(h[1][2]), enumerate(hands_sorted))))
