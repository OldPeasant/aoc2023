import sys

sys.path.append('../lib')
from pmg import *

DIRS = [ (1, 0), (-1, 0), (0, 1), (0, -1) ]

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()
    grid = []
    grid.append("#" * (len(lines[0]) + 2))
    for l in lines:
        grid.append("#" + l + "#")
    grid.append("#" * (len(lines[0]) + 2))

    for r in grid:
        print(r)
    start = None
    for row_index, row in enumerate(grid):
        for col_index, cell in enumerate(row):
            if cell == 'S':
                start = (row_index, col_index)
                break
        if start is not None:
            break
    print(start)
    
    plots = set()
    plots.add(start)
    for step in range(64):
        next_plots = set()
        for p in plots:
            for d in DIRS:
                n = (p[0]+d[0], p[1] + d[1])
                if grid[n[0]][n[1]] in 'S.':
                    next_plots.add(n)
        plots = next_plots
        print(plots)
    print(len(plots))
