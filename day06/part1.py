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
    times = list(int(t) for t in lines[0].split(":")[1].split())
    distances = list(int(t) for t in lines[1].split(":")[1].split())
    result = 1
    for i in range(len(times)):
        t = times[i]
        d = distances[i]
        result *= ways_to_win(times[i], distances[i])
    print(result)
