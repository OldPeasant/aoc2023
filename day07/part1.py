import sys
import functools

sys.path.append('../lib')
from pmg import *

CARDS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2', '1']
VALUES = {}
for ix, c in enumerate(CARDS):
    VALUES[c] = len(CARDS) - ix

class Hand:
    def __init__(self, cards):
        print(cards)
        self.cards = cards
        dl = {}
        for c in cards:
            dl[c] = dl.get(c, 0) + 1
        print(dl)
        count_matches = {}
        for card, count in dl.items():
            print("cc", card, count)
            count_matches[count] = count_matches.get(count, 0) + 1
        print(count_matches)
        if count_matches.get(5, 0) >= 1:
            s = 7
        elif count_matches.get(4, 0) >= 1:
            s = 6
        elif count_matches.get(3, 0) >= 1:
            if count_matches.get(2, 0) >= 1:
                s = 5
            else:
                s = 4
        elif count_matches.get(2, 0) >= 2:
            s = 3
        elif count_matches.get(2, 0) >= 1:
            s = 2
        else:
            s = 1
        self.strength = s

    def is_bigger_than(self, other_hand):
        print("is bigger", self, other_hand)
        if self.strength > other_hand.strength:
            print("", "yes, strengthi")
            return 1
        elif self.strength < other_hand.strength:
            print("", "no, strengthi")
            return -1
        for c_me, c_other in zip(self.cards, other_hand.cards):
            if VALUES[c_me] > VALUES[c_other]:
                print("", "yes", c_me, c_other)
                return 1
            elif VALUES[c_me] < VALUES[c_other]:
                print("", "no", c_me, c_other)
                return -1
        print("", "no")
        return 0
    def __repr__(self):
        return "".join(self.cards) + ": " + str(self.strength)

def compare_hands(h1, h2):
    print("compare", h1, h2)
    c = h1[0].is_bigger_than(h2[0])
    print("", c)
    return c

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

    hands_with_bids = []
    for l in lines:
        s = l.split()
        hands_with_bids.append( (Hand(list(s[0])), int(s[1])) )
    print(hands_with_bids)
    hands_with_bids.sort(key=functools.cmp_to_key(compare_hands))
    print(hands_with_bids)
    winnings = 0
    for ix, hwb in enumerate(hands_with_bids):
        print(ix, "|", hwb)
        w = (ix + 1) * hwb[1]
        print(w, hwb)
        winnings += w
    print(winnings)
