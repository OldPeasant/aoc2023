import sys

from copy import deepcopy

sys.path.append('../lib')
from pmg import *

def move_north(grid, row_ix, col_ix):
    if grid[row_ix][col_ix] != 'O':
        return
    while True:
        if row_ix > 0 and grid[row_ix - 1][col_ix] == '.':
            grid[row_ix - 1][col_ix] = 'O'
            grid[row_ix][col_ix] = '.'
            row_ix -= 1
        else:
            return
def move_south(grid, row_ix, col_ix):
    if grid[row_ix][col_ix] != 'O':
        return
    while True:
        if row_ix < len(grid)-1 and grid[row_ix + 1][col_ix] == '.':
            grid[row_ix + 1][col_ix] = 'O'
            grid[row_ix][col_ix] = '.'
            row_ix += 1
        else:
            return
def move_west(grid, row_ix, col_ix):
    if grid[row_ix][col_ix] != 'O':
        return
    while True:
        if col_ix > 0 and grid[row_ix][col_ix - 1] == '.':
            grid[row_ix][col_ix - 1] = 'O'
            grid[row_ix][col_ix] = '.'
            col_ix -= 1
        else:
            return
def move_east(grid, row_ix, col_ix):
    if grid[row_ix][col_ix] != 'O':
        return
    while True:
        if col_ix < len(grid[0]) - 1 and grid[row_ix][col_ix + 1] == '.':
            grid[row_ix][col_ix + 1] = 'O'
            grid[row_ix][col_ix] = '.'
            col_ix += 1
        else:
            return

def grids_equal(g1, g2):
    if len(g1) != len(g2):
        return false
    for r1, r2 in zip(g1, g2):
        if len(r1) != len(r2):
            return False
        for c1, c2 in zip(r1, r2):
            if c1 != c2:
                return False
    return True

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

    grid = []
    for l in lines:
        grid.append(list(c for c in l))
    #for row in grid:
    #    print("".join(row))
    #print()
    grids_after_4 = []
    for i in range(120):
        print(i)
        for row_ix, row in enumerate(grid):
            for col_ix, cell in enumerate(row):
                move_north(grid, row_ix, col_ix)
    #    for row in grid:
    #        print("".join(row))
    #    print()
        for row_ix, row in enumerate(grid):
            for col_ix, cell in enumerate(row):
                move_west(grid, row_ix, col_ix)
    #    for row in grid:
    #        print("".join(row))
    #    print()
        for row_ix, row in enumerate(grid):
            for col_ix, cell in enumerate(row):
                move_south(grid, len(grid) - row_ix - 1, col_ix)
    #    for row in grid:
    #        print("".join(row))
    #    print()
        for row_ix, row in enumerate(grid):
            for col_ix, cell in enumerate(row):
                move_east(grid, row_ix, len(row) - col_ix - 1)
    #    for row in grid:
    #        print("".join(row))
    #    print()
        grids_after_4.append(deepcopy(grid))
        for gi, g in enumerate(grids_after_4[:-1]):
            #print("check eq", g, grid)
            if grids_equal(g, grid):
                print("Equal:", gi, len(grids_after_4)-1)
                m_should = gi
                while m_should % 7 != 1000000 % 7:
                    m_should += 1
                g = grids_after_4[m_should]
                rc = len(g)
                score = 0
                for row_ix, row in enumerate(g):
                    for cell in row:
                        if cell == 'O':
                            p = rc - row_ix
                            print(p)
                            score += p
                print(score)
                exit(0)
                #for row in g:
                #    print("".join(row))
                #print()
                #for row in grid:
                #    print("".join(row))
                #print()
            else:
                print("NEQ", gi, len(grids_after_4)-1)
                #for row in g:
                #    print("".join(row))
                #print()
                #for row in grid:
                #    print("".join(row))
                #print()
                #exit(0)
