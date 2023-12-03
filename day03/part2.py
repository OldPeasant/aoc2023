import sys

sys.path.append('../lib')
from pmg import *


def full_number(matrix, row, col):
    c_min = col
    while matrix[row][c_min].isnumeric():
        c_min -= 1
    c_max = col
    while matrix[row][c_max].isnumeric():
        c_max += 1
    return int("".join(matrix[row][c_min+1:c_max]))

def gear_ratio(matrix, row, col):
    gears = []
    for c in [col - 1, col + 1]:
        if matrix[row][c].isnumeric():
            gears.append(full_number(matrix, row, c))
    for r in [row - 1, row + 1]:
        if matrix[r][col].isnumeric():
            gears.append(full_number(matrix, r, col))
        else:
            for c in [col - 1, col + 1]:
                if matrix[r][c].isnumeric():
                    gears.append(full_number(matrix, r, c))
    if len(gears) == 2:
        return gears[0] * gears[1]
    else:
        return 0

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

    filler = "." * len(lines[0])
    matrix = [filler]
    for l in lines:
        matrix.append("." + l + ".")
    matrix.append(filler)

    sum_gear_ratio = 0
    for row, l in enumerate(matrix):
        for col in range(0, len(l)):
            if matrix[row][col] == '*':
                sum_gear_ratio += gear_ratio(matrix, row, col)
    print(sum_gear_ratio)
