import sys

sys.path.append('../lib')
from pmg import *

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

    score = 0
    for l in lines:
        caption, values = l.split(": ")
        winning_str, having_str = values.split(" | ")
        winning = [ int(n) for n in (s for s in winning_str.split(" ") if s)]
        having = [ int(n) for n in (s for s in having_str.split(" ") if s)]
        print(winning)
        print(having)
        count_match = len(list(n for n in having if n in winning))
        print(count_match)
        if count_match > 0:
            points = pow(2, count_match - 1)
            print(points)
            score += points
    print(score)
