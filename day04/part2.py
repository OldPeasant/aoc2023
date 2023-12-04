import sys

sys.path.append('../lib')
from pmg import *

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

    copies = [1] * len(lines)
    for i, l in enumerate(lines):
        caption, values = l.split(": ")
        winning_str, having_str = values.split(" | ")
        winning = [ int(n) for n in (s for s in winning_str.split(" ") if s)]
        having = [ int(n) for n in (s for s in having_str.split(" ") if s)]
        count_match = len(list(n for n in having if n in winning))
        for c in range(i + 1, i + 1 + count_match):
            if c < len(copies):
                copies[c] += copies[i]
    print(sum(copies))
