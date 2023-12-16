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
    walker = Walker(grid, start[0], start[1], find_start_directions(grid, start)[0])
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
    
    grouper = Grouper()
    last_row = spots[0][0]
    for s in spots:
        if s[0] != last_row:
            grouper.next()
            last_row = s[0]
        grouper.add(s)
    
    for g in grouper.groups:
        print(g)

    # ToDo
    # - identify active vs inactive horizontal groups
    # - sequence per row
    # - count what is inside
