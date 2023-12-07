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
        self.cards = cards
        dl = {}
        for c in cards:
            dl[c] = dl.get(c, 0) + 1
        count_matches = {}
        for card, count in dl.items():
            count_matches[count] = count_matches.get(count, 0) + 1
        if count_matches.get(5, 0) >= 1:
            # Five of a kind
            s = 7
        elif count_matches.get(4, 0) >= 1:
            # Four of a kind
            s = 6
        elif count_matches.get(3, 0) >= 1:
            if count_matches.get(2, 0) >= 1:
                # Full house
                s = 5
            else:
                # Three of a kind
                s = 4
        elif count_matches.get(2, 0) >= 2:
            # Two pairs
            s = 3
        elif count_matches.get(2, 0) >= 1:
            # One pair
            s = 2
        else:
            # High card
            s = 1
        self.strength = s

    def compare_to(self, other_hand):
        if self.strength > other_hand.strength:
            return 1
        elif self.strength < other_hand.strength:
            return -1
        for c_me, c_other in zip(self.cards, other_hand.cards):
            if VALUES[c_me] > VALUES[c_other]:
                return 1
            elif VALUES[c_me] < VALUES[c_other]:
                return -1
        return 0

    def __repr__(self):
        return "".join(self.cards) + ": " + str(self.strength)

def compare_hands(h1, h2):
    return h1[0].compare_to(h2[0])

with open(sys.argv[1]) as f:
    hands_with_bids = []
    for l in f.read().splitlines():
        s = l.split()
        hands_with_bids.append( (Hand(list(s[0])), int(s[1])) )
    hands_with_bids.sort(key=functools.cmp_to_key(compare_hands))
    winnings = 0
    for ix, hwb in enumerate(hands_with_bids):
        winnings += (ix + 1) * hwb[1]
    print(winnings)
