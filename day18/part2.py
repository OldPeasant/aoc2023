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

CHANGER = {
    "R" : "UD",
    "L" : "UD",
    "U" : "LR",
    "D" : "LR"
}

def find_vertical_switchers(h_segments, y_coord):
    #print("find vertical switchers at y={}".format(y_coord))
    matches = []
    for s in h_segments:
        #print("     check segment {}".format(s))
        min_y = min(s[0][1], s[1][1])
        max_y = max(s[0][1], s[1][1])
        if s[0][0] == s[1][0] and min_y <= y_coord and max_y >= y_coord:
            matches.append(s[0][0])
            #print("         yes")
            if s[2] is not True:
                raise Exception()
        #else:
        #    print("         no")
    matches.sort()
    return matches

def find_horizontallers(h_segments, y_split):
    result = []
    for s in h_segments:
        if s[0][0] == s[1][0]:
            # It's vertical
            if min(s[0][1], s[1][1]) < y_split and max(s[0][1], s[1][1]) > y_split:
                # Vertical applies, always as changer
                result.append( (s[0][0], s[0][0], True) )
        else:
            if s[0][1] != s[1][1]:
                raise Exception()
            # It's horizontal
            if s[0][1] == y_split:
                result.append( (min(s[0][0], s[1][0]), max(s[0][0], s[1][0]), s[2]) )
    result.sort(key=lambda a: a[0])

    return result

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

    instr = []
    for l in lines:
        ## Part 1
        #direction, count_str = l.split()[:2]
        #distance = int(count_str)
        #instr.append( (direction, distance) )
        # Part 2
        alleged_col = l.split()[2:][0][2:-1]
        direction = DIRECTIONS[int(alleged_col[-1])]
        distance = hex_to_dec(alleged_col[:-1])
        instr.append( (direction, distance) )
    print(instr)
    if instr[0][0] == instr[-1][0]:
        raise Exception("Unexpected for me")
    BIG = 999999999999999999

    h_segments = []
    cx = 0
    cy = 0
    y_splitter_set = set()
    y_splitter_set.add(0)
    for ix, i in enumerate(instr):
        d, l = i
        print(d, l)
        nx = cx + l * DELTA[d][0]
        ny = cy + l * DELTA[d][1]
        y_splitter_set.add(ny)
        print("-", d)
        if d in "UD":
            changes_in_out = True
        else:
            ud = instr[ix - 1] + instr[ix + 1 if ix < len(instr) - 2 else 0]
            changes_in_out = ("U" in ud) != ("D" in ud)
        h_segments.append( [ (cx, cy), (nx, ny), changes_in_out ] )
        cx, cy = nx, ny
    for h in h_segments:
        print("SEG", h)
    y_splitters = sorted(y_splitter_set)
    print("Y splitters:", y_splitters)
    last_y_split = y_splitters[0]
    total = 0
    print("===============================================")
    for y_split in y_splitters:
        if y_split - last_y_split > 1:
            print("An y-multi-thingy from {} to {}".format(last_y_split + 1, y_split - 1))
            x_switchers = find_vertical_switchers(h_segments, last_y_split + 1)
            print("switchers: {}".format(x_switchers))
            for i in range(0, len(x_switchers), 2):
                w = x_switchers[i+1] - x_switchers[i] + 1
                print("   w={}".format(w))
                contrib = w * (y_split - last_y_split - 1)
                print("   contrib={}".format(contrib))
                total += contrib
            #x_changers = list( (seg[0][0], seg[1][0], seg[2]) for seg in h_segments if seg[0][1] == seg[1][1] and seg[0][1] in range(last_y_split, y_split) )
            #print(x_changers)
            # calc in-outs for row y_split-1, only considering vertical changes_in_out=True items
            # multiply with y_split-last_y_split

            # calc for row y_split
            total += 0
            print()
        print("A horizontaller at y={}".format(y_split))
        horizontallers = find_horizontallers(h_segments, y_split)
        print("horizontallers={}".format(horizontallers))
        row_total = 0
        is_on = False
        last_h = None
        for h in horizontallers:
            row_total += h[1] - h[0] + 1
            if is_on:
                row_total += h[0] - last_h[1] - 1
            if h[2]:
                is_on = not is_on
            last_h = h
        if is_on:
            raise Exception()
        print("   row_total = {}".format(row_total))
        total += row_total
        print()
            
        last_y_split = y_split
    print(total)
    exit(0)
