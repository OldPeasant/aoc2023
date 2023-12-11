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

class Walker:
    def __init__(self, grid, row, col, direction):
        self.grid = grid
        self.row = row
        self.col = col
        self.direction = direction
    def __repr__(self):
        return "(" + str(self.col) + ", " + str(self.row) + "):" + self.direction

    def next(self):
        if self.direction == "N":
            self.row -= 1
            f = self.grid[self.row][self.col]
            b = backwards[f]
            l = list(b)
            if "S" not in l:
                return None
            l.remove("S")
            self.direction = l[0]
        elif self.direction == "S":
            self.row += 1
            f = self.grid[self.row][self.col]
            b = backwards[f]
            l = list(b)
            if "N" not in l:
                return None
            l.remove("N")
            self.direction = l[0]
        elif self.direction == "E":

            self.col += 1
            f = self.grid[self.row][self.col]
            b = backwards[f]
            l = list(b)
            if "W" not in l:
                return None
            l.remove("W")
            self.direction = l[0]
        elif self.direction == "W":

            self.col -= 1
            f = self.grid[self.row][self.col]
            b = backwards[f]
            l = list(b)
            if "E" not in l:
                return None
            l.remove("E")
            self.direction = l[0]
        else:
            raise Exception()
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
    walkers = list(Walker(grid, start[0], start[1], direction) for direction in ["N", "S", "E", "W"])
    count = 0
    line = [start]
    while True:
        remaining_walkers = []
        for w in walkers:
            if w.next():
                line.append( (w.row, w.col) )
                remaining_walkers.append(w)
        walkers = remaining_walkers
        count += 1
        if all_equal(walkers):
            print(line)
            print(count)
        print(count, walkers)
