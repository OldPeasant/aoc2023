import sys

sys.path.append('../lib')
from pmg import *

HEX_VAL = {l:v for v, l in enumerate('0123456789abcdef')}

def hex_to_dec(hex_str):
    return HEX_VAL[hex_str[-1]] + 16 * hex_to_dec(hex_str[:-1]) if len(hex_str) > 0 else 0

DIRECTIONS = "RDLU"

DELTA = {
        "R": (1, 0),
        "L": (-1, 0),
        "U": (0, -1),
        "D": (0, 1)
}

def find_vertical_switchers(h_segments, y_coord):
    matches = []
    for s in h_segments:
        min_y = min(s[0][1], s[1][1])
        max_y = max(s[0][1], s[1][1])
        if s[0][0] == s[1][0] and min_y <= y_coord and max_y >= y_coord:
            matches.append(s[0][0])
    matches.sort()
    return matches

def find_horizontallers(h_segments, y_split):
    result = []
    for s in h_segments:
        if s[0][0] == s[1][0]:
            if min(s[0][1], s[1][1]) < y_split and max(s[0][1], s[1][1]) > y_split:
                result.append( (s[0][0], s[0][0], True) )
        else:
            if s[0][1] == y_split:
                result.append( (min(s[0][0], s[1][0]), max(s[0][0], s[1][0]), s[2]) )
    result.sort(key=lambda a: a[0])
    return result

with open(sys.argv[1]) as f:
    instr = []
    for l in f.read().splitlines():
        direction, count_str = l.split()[:2]
        distance = int(count_str)
        instr.append( (direction, distance) )
    h_segments = []
    cx, cy = 0, 0
    y_splitter_set = set()
    y_splitter_set.add(0)
    for ix, i in enumerate(instr):
        d, l = i
        nx, ny = cx + l * DELTA[d][0], cy + l * DELTA[d][1]
        y_splitter_set.add(ny)
        if d in "UD":
            changes_in_out = True
        else:
            ud = instr[ix - 1] + instr[ix + 1 if ix < len(instr) - 2 else 0]
            changes_in_out = ("U" in ud) != ("D" in ud)
        h_segments.append( [ (cx, cy), (nx, ny), changes_in_out ] )
        cx, cy = nx, ny
    y_splitters = sorted(y_splitter_set)
    last_y_split = y_splitters[0]
    total = 0
    for y_split in y_splitters:
        if y_split - last_y_split > 1:
            x_switchers = find_vertical_switchers(h_segments, last_y_split + 1)
            for i in range(0, len(x_switchers), 2):
                w = x_switchers[i+1] - x_switchers[i] + 1
                contrib = w * (y_split - last_y_split - 1)
                total += contrib
            total += 0
        horizontallers = find_horizontallers(h_segments, y_split)
        is_on = False
        last_h = None
        for h in horizontallers:
            total += h[1] - h[0] + 1
            if is_on:
                total += h[0] - last_h[1] - 1
            if h[2]:
                is_on = not is_on
            last_h = h
        last_y_split = y_split
    print(total)
