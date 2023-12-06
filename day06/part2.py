import sys

sys.path.append('../lib')
from pmg import *

def ways_to_win(t, d):
    ww = 0
    for w in range(t):
        f = w * (t - w)
        if f > d:
            ww += 1
    return ww

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()
    time = int("".join(s.strip() for s in lines[0].split(":")[1].split()))
    distance = int("".join(s.strip() for s in lines[1].split(":")[1].split()))
    print(ways_to_win(time, distance))
