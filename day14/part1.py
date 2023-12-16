import sys

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

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

    grid = []
    for l in lines:
        grid.append(list(c for c in l))
    for row in grid:
        print("".join(row))
    print()
    for row_ix, row in enumerate(grid):
        for col_ix, cell in enumerate(row):
            move_north(grid, row_ix, col_ix)
    for row in grid:
        print("".join(row))
    print()
    rc = len(grid)
    score = 0
    for row_ix, row in enumerate(grid):
        for cell in row:
            if cell == 'O':
                p = rc - row_ix
                print(p)
                score += p
    print(score)
