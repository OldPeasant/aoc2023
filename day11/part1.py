import sys

sys.path.append('../lib')
from pmg import *

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

    grid_small = []
    for l in lines:
        grid_small.append(l)
    rows_with_galaxy = set()
    cols_with_galaxy = set()
    for row_ix, row in enumerate(grid_small):
        for col_ix, cell in enumerate(row):
            if cell == '#':
                rows_with_galaxy.add(row_ix)
                cols_with_galaxy.add(col_ix)
    empty_rows = []
    empty_cols = []
    for i in range(len(grid_small[0])):
        if i not in cols_with_galaxy:
            empty_cols.append(i)
    for i in range(len(grid_small)):
        if i not in rows_with_galaxy:
            empty_rows.append(i)
    print(empty_rows)
    print(empty_cols)
    grid_big = []
    for row_ix, row in enumerate(grid_small):
        new_row = []
        for col_ix, cell in enumerate(row):
            new_row.append(cell)
            if col_ix in empty_cols:
                new_row.append(".")
        grid_big.append(new_row)
        if row_ix in empty_rows:
            grid_big.append("." * (len(grid_small[0]) + len(empty_cols)))
    print("\n".join("".join(r) for r in grid_big))
    galaxies = []
    for row_ix, row in enumerate(grid_big):
        for col_ix, cell in enumerate(row):
            if cell == "#":
                galaxies.append( (row_ix, col_ix) )
    print(galaxies)
    total_dist = 0
    for i, g1 in enumerate(galaxies):
        for j, g2 in enumerate(galaxies):
            if j > i:
                d = manhattan_dist(g1, g2)
                print(d)
                total_dist += d

    print(total_dist)

