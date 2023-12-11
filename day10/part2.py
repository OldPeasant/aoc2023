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

step = {
    "N" : [-1, 0, "S"],
    "S" : [ 1, 0, "N"],
    "E" : [ 0, 1, "W"],
    "W" : [ 0,-1, "E"]
}

class Walker:
    def __init__(self, grid, row, col, direction):
        self.grid = grid
        self.row = row
        self.col = col
        self.direction = direction
        self.horizontals = Grouper()
        self.horizontals.add((self.row, self.col))
    def __repr__(self):
        return "(" + str(self.col) + ", " + str(self.row) + "):" + self.direction

    
    def _gen_next(self, row_inc, col_inc, ch):
        print("next", self.row, self.col, row_inc, col_inc, ch)
        self.row += row_inc
        self.col += col_inc
        print("    n", self.row, self.col)
        if col_inc == 0:
            self.horizontals.next()
        self.horizontals.add((self.row, self.col))

        print("get f {},{}: {}".format(self.row, self.col, self))
        f = self.grid[self.row][self.col]
        b = backwards[f] if f in backwards else ''
        l = list(b)
        if ch not in l:
            return None
        l.remove(ch)
        self.direction = l[0]
        return True

    def next(self):
        return self._gen_next(*step[self.direction])

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
    walkers = list(Walker(grid, start[0], start[1], direction) for direction in ["N", "S", "E", "W"])
    count = 0
    line = [start]
    ended_walkers = []
    while True:
        remaining_walkers = []
        for w in walkers:
            #print("walker ", w)
            if w.next():
                #print("   has next")
                line.append( (w.row, w.col) )
                remaining_walkers.append(w)
            else:
                print("walker ", w)
                print("   has no next")
                ended_walkers.append(w)
                for row_ix, row in enumerate(grid):
                    l = ""
                    for col_ix, cell in enumerate(row):
                        flats = [item for sublist in w.horizontals.groups for item in sublist]

                        if (row_ix, col_ix) in flats:
                            l += "*"
                        else:
                            l += cell
                    print(l)
                per_row = DictOfLists()
                for h in w.horizontals.groups:
                    row = h[0][0]
                    rng = ( min(c[1] for c in h), max(c[1] for c in h ) )
                    per_row.add(row, rng)

                print(per_row.dict)
        walkers = list(w for w in  ended_walkers if len(w.horizontals.groups) > 1)
        count += 1
        print("----------")
        print(walkers)
        print("- - - - - - - - -")
        if start == (walkers[0].row, walkers[0].col):

            print(line)
            print(count)
            break
    count_inside = 0
    w = walkers[0]
    print(w)
    exit(0)
    for row_ix, row in enumerate(grid):
        print(row)
        curr_inside = False
        for col_ix, cell in enumerate(grid[row_ix]):
            cell_ix = (row_ix, col_ix)
            print("ci", cell_ix)
            if cell_ix in line:
                if cell == '|':
                    curr_inside = not curr_inside

            if cell_ix in line and cell != '-':
                curr_inside = not curr_inside
            print(curr_inside)
            if cell == "." and curr_inside:
                count_inside += 1
                print("count", count_inside)
    print(count_inside)
