import sys

sys.path.append('../lib')
from pmg import *

def aoc_hash(s):
    cv = 0
    for c in s.encode('ascii'):
        print(c)
        cv += c
        print(cv)
        cv *= 17
        print(cv)
        cv = cv % 256
        print(cv)
    return cv
with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

    print(aoc_hash("HASH"))
    total = 0
    for l in lines:
        for s in l.split(','):
            total += aoc_hash(s)
    print(total)
