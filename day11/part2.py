import sys

sys.path.append('../lib')
from pmg import *

FACTOR = 1000000
with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

    grid = list(lines)
    rows_with_galaxy = set()
    cols_with_galaxy = set()
    for row_ix, row in enumerate(grid):
        for col_ix, cell in enumerate(row):
            if cell == '#':
                rows_with_galaxy.add(row_ix)
                cols_with_galaxy.add(col_ix)
    empty_rows = []
    empty_cols = []
    for i in range(len(grid[0])):
        if i not in cols_with_galaxy:
            empty_cols.append(i)
    for i in range(len(grid)):
        if i not in rows_with_galaxy:
            empty_rows.append(i)
    galaxies = []
    for row_ix, row in enumerate(grid):
        for col_ix, cell in enumerate(row):
            if cell == "#":
                galaxies.append( (row_ix, col_ix) )
    total_dist = 0
    for i, g1 in enumerate(galaxies):
        for j, g2 in enumerate(galaxies):
            if j > i:
                d = manhattan_dist(g1, g2)
                f1 = list(1 for c in empty_rows if c > min(g1[0], g2[0]) and c < max(g1[0], g2[0]))
                d += FACTOR * (sum(f1))
                f2 = list(1 for c in empty_cols if c > min(g1[1], g2[1]) and c < max(g1[1], g2[1]))
                d += FACTOR * (sum(f2))
                total_dist += d - len(f1) - len(f2)

    print(total_dist)

