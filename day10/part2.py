import sys

sys.path.append('../lib')
from pmg import *

tiles = {
    "NS" : "|",
    "EW" : "-",
    "NE" : "L",
    "NW" : "J",
    "SW" : "7",
    "SE" : "F"
}

backwards = {}
for k, v in tiles.items():
    backwards[v] = k
backwards['.'] = "."
print(backwards)


def find_start_directions(grid, s):
    directions = []
    for conf in [
            ['N', -1, 0, 'S'],
            ['S', +1, 0, 'N'],
            ['W', 0, -1, 'E'],
            ['E', 0, +1, 'W']]:
        go_to, sr, sc, back = conf
        c = grid[s[0] + sr][s[1] + sc]
        if back in backwards[c]:
            directions.append(go_to)
    print("Start directions", directions)
    return directions


class Walker:
    def __init__(self, grid, row, col, direction):
        self.grid = grid
        self.row = row
        self.col = col
        self.direction = direction
        self.visited = [ (row, col) ]
    def __repr__(self):
        return "(" + str(self.col) + ", " + str(self.row) + "):" + self.direction

    def next(self):
        dr, dc, opp = {
                'N' : (-1, 0, 'S'),
                'S' : (+1, 0, 'N'),
                'W' : (0, -1, 'E'),
                'E' : (0, +1, 'W')
                }[self.direction]
        self.row += dr
        self.col += dc
        self.visited.append( (self.row, self.col) )
        f = self.grid[self.row][self.col]
        if f == 'S':
            return False
        b = backwards[f]
        l = list(b)
        l.remove(opp)
        self.direction = l[0]
        return True

def all_equal(walkers):
    x = set()
    y = set()
    for w in walkers:
        x.add(w.col)
        y.add(w.row)
    return len(x) == 1 and len(y) == 1

def replace_start_char(grid, start, sd):
    print("replace_start_char", start, sd)
    for dirs, c in tiles.items():
        print("check", dirs, c)
        if sd[0] in dirs and sd[1] in dirs:
            print("Yes")
            old_row = grid[start[0]]
            print("old row", old_row)
            new_row = ""
            if start[1] > 0:
                new_row += old_row[:start[1]]
            new_row += c
            if start[1] < len(grid[start[0]]) - 1:
                new_row += old_row[start[1] + 1:]
            print("new row", new_row)
            grid[start[0]] = new_row
            return
        else:
            print('no')
    print("No replacement found")

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

    grid = []
    grid.append("." * (len(lines[0]) + 2))
    for ix, l in enumerate(lines):
        grid.append("." + l + ".")
        if "S" in l:
            start = (ix + 1, l.index("S") + 1)
    grid.append("." * (len(lines[0]) + 2))
    print("\n".join(grid))
    print(start)
    print(grid[start[0]][start[1]])
    
    print("-------------------")
    sd = find_start_directions(grid, start)
    walker = Walker(grid, start[0], start[1], sd[0])
    while True:
        if not walker.next():
            break
    spots = walker.visited[:-1]
    print(spots)
    while spots[0][0] == spots[-1][0]:
        rot = [spots[-1]]
        rot.extend(spots[:-1])
        spots = rot
    print(spots)
    
    replace_start_char(grid, start, sd)
    grouper = Grouper()
    last_row = spots[0][0]
    for s in spots:
        if s[0] != last_row:
            grouper.next()
            last_row = s[0]
        grouper.add(s)
    
    groups_per_line = DictOfLists()
    for g in grouper.groups:
        print(g)
        col_indexes = list(a[1] for a in g)
        col_indexes.sort()
        c1 = grid[g[0][0]][col_indexes[0]]
        c2 = grid[g[0][0]][col_indexes[-1]]
        print("the c's", c1, c2)
        ends = backwards[c1] + backwards[c2]
        groups_per_line.add(g[0][0], (col_indexes[0], col_indexes[-1], 'N' in ends and 'S' in ends) )
        #if 'N' in ends and 'S' in ends:
        #    print(ends, "a changer")
        #else:
        #    print(ends, "not a changer")
    
    count_inside = 0
    for row_ix, row in enumerate(grid):
        ranges_per_row = groups_per_line.get(row_ix)
        ranges_per_row.sort(key= lambda a:a[0])
        #from_ix, to_ix, changer = ranges_per_row
        print("Row", row_ix, ranges_per_row)
        col = 0
        is_on = False
        last_range = None
        for r in ranges_per_row:
            print("check range", r, is_on)
            if is_on:
                inside = max(0, r[0] - last_range[1] - 1)
                print("inside", inside)
                count_inside += inside
            if r[2]:
                is_on = not is_on
            last_range = r
        if is_on:
            raise Exception()
    print(count_inside)

    # ToDo
    # - identify active vs inactive horizontal groups
    # - sequence per row
    # - count what is inside
