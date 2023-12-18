import sys

sys.path.append('../lib')
from pmg import *

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

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

    instr = []
    for l in lines:
        d, far_str = l.split()[:2]
        instr.append( (d, int(far_str)) )
    print(instr)
    if instr[0][0] == instr[-1][0]:
        raise Exception("Unexpected for me")
    BIG = 999999999999999999
    min_x = BIG
    max_x = -BIG
    min_y = BIG
    max_y = -BIG
    h_segments = []
    cx = 160
    cy = 238
    for ix, i in enumerate(instr):
        d, l = i
        print(d, l)
        nx = cx + l * DELTA[d][0]
        ny = cy + l * DELTA[d][1]
        if nx < min_x:
            min_x = nx
        if nx > max_x:
            max_x = nx
        if ny < min_y:
            min_y = ny
        if ny > max_y:
            max_y = ny
        print("-", d)
        if d in "UD":
            print("Fall A")
            changes_in_out = True
        else:
            print("Fall B")
            ud = instr[ix - 1] + instr[ix + 1 if ix < len(instr) - 2 else 0]
            changes_in_out = ("U" in ud) != ("D" in ud)
            print("===", ud, changes_in_out)
        h_segments.append( [ (cx, cy), (nx, ny), changes_in_out ] )
        cx, cy = nx, ny
    print("Range ({}, {}) - ({}, {})".format(min_x, min_y, max_x, max_y))
    for h in h_segments:
        print("SEG", h)
    splitters = []
    for ix, h in enumerate(h_segments):
        s1, s2, changes = h
        if s1[0] == s2[0]:
            # vertical
            y1 = s1[1]
            y2 = s2[1]
            for y in range(min(y1, y2) + 1, max(y1, y2)):
                if not changes:
                    raise Exception()
                splitters.append( (s1[0], s1[0], y, changes) )
        elif s1[1] == s2[1]:
            # horizontal
            x1 = s1[0]
            x2 = s2[0]
            splitters.append( (min(x1, x2), max(x1, x2), s1[1], changes) )

    for s in splitters:
        print("SPLITTER", s)
    by_row = DictOfLists()
    for s in splitters:
        by_row.add(s[2], s)
    for l in by_row.dict.values():
        l.sort(key = lambda r: r[0])
    count_inside = 0
    count_all = 0
    for y in range(min_y, max_y + 1):
        row = ['.'] * (1 + max_x - min_x)
        last_s = None
        is_inside = False
        for s in by_row.get(y): #splitters:
            if is_inside:
                for x in range(last_s[1] + 1, s[0]):
                    if row[x] != '.':
                        raise Exception()
                    row[x] = 'i'
                    count_all += 1
            if s[2] == y:
                for x in range(s[0], s[1] + 1):
                    if row[x] != '.':
                        raise Exception()
                    count_all += 1
                    row[x] = '#'
            if s[3]:
                is_inside = not is_inside
            last_s = s
            
        #print(row)
        print("".join(row)) #i"#" if c else "." for c in row))
    #exit(0)
    print("Das Finale")
    for y in range(min_y, max_y + 1):
        print(by_row.get(y))
        inside = False
        segs = by_row.get(y)
        prev = None
        rc = 0
        for s in segs:
            if inside:
                rc += s[0] - prev[1] - 1
            rc += s[1] - s[0] + 1
            if s[2]:
                inside = not inside
            prev = s
        print("Row", y, rc)
        count_inside += rc
    print("Total", count_inside)
    print(count_all)
# 88832 is wrong
# 88973 is too low
