import sys

sys.path.append('../lib')
from pmg import *

DIRS = {
    "N" : (-1,  0),
    "S" : ( 1,  0),
    "W" : ( 0, -1),
    "E" : ( 0,  1)
}

OPPOSITES = { "N" : "S", "S": "N", "E": "W", "W": "E" }

class PointInfo:
    def __init__(self):
        self.best = {}
        m = sys.maxsize
        for d in DIRS.keys():
            self.best[d] = [m, m, m]

class Grid:
    def __init__(self, lines):
        self.lines = lines
        self.point_infos = []
        for l in lines:
            row = []
            for i in l:
                row.append(PointInfo())
            self.point_infos.append(row)

class Walker:
    def __init__(self, row, col, direction, same_dir_count, reduction):
        self.row = row
        self.col = col
        self.direction = direction
        self.same_dir_count = same_dir_count
        self.reduction = reduction

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()
    grid = Grid(list( list( int(c) for c in row) for row in lines))
    walkers = [ Walker(0, 0, "E", 0, 0), Walker(0, 0, "S", 0, 0) ]

    while len(walkers) > 0:
        #print("====== a new iteration through the walkers =========")
        new_walkers = []
        for w in walkers:
            #print("We have walker", w.row, w.col, w.direction, w.same_dir_count, w.reduction)
            new_row = w.row + DIRS[w.direction][0]
            new_col = w.col + DIRS[w.direction][1]
            if new_row >= 0 and new_row < len(grid.lines) and new_col >= 0 and new_col < len(grid.lines[0]):
                #print("  ", "new coords are in the grid", new_row, new_col)
                new_reduction = w.reduction + grid.lines[new_row][new_col]
                #print("as reduction of ({}, {}) is {}, new_reduction is {}".format(new_row, new_col, grid.lines[new_row][new_col], new_reduction))
                new_same_dir_count = w.same_dir_count + 1
                pi = grid.point_infos[new_row][new_col]
                made_a_change = False
                for i in range(w.same_dir_count, 3):
                    if pi.best[w.direction][i] > new_reduction:
                        pi.best[w.direction][i] = new_reduction
                        made_a_change = True
                    else:
                        break
                #print("so pi ({}, {}) is now {}".format(new_row, new_col, pi.best))
                if made_a_change:
                    if new_same_dir_count < 3:
                        new_walkers.append(Walker(new_row, new_col, w.direction, new_same_dir_count, new_reduction))
                    for d in (d for d in DIRS if d != w.direction and d != OPPOSITES[w.direction]):
                        new_walkers.append(Walker(new_row, new_col, d, 0, new_reduction))
            
        walkers = new_walkers
    #print(len(grid.point_infos))
    print(min( min( v for v in perdir) for perdir in grid.point_infos[-1][-1].best.values()))
#    for r in range(4):
#        for c in range(4):
#            print(r, c, grid.point_infos[r][c].best)
