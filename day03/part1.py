import sys

sys.path.append('../lib')
from pmg import *

def is_isolated(matrix, row, col_begin, col_end):
    print("check", col_begin, col_end, len(matrix[row]), len(matrix[row+1]))
    for x in range(col_begin - 1, col_end + 1):
        if matrix[row-1][x] != '.' or matrix[row+1][x] != '.':
            return False
    if matrix[row][col_begin - 1] != '.' or matrix[row][col_end] != '.':
        return False
    return True

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

    width = len(lines[0])
    matrix = []
    matrix.append("." * (width + 2))
    for l in lines:
        matrix.append("." + l + ".")
    matrix.append("." * (width + 2))
    for l in matrix:
        print(l)

    sum_isolated = 0
    for row, l in enumerate(matrix):
        for col in range(0, len(l)):
            if matrix[row][col].isnumeric() and not matrix[row][col - 1].isnumeric():
                col_end = col
                while matrix[row][col_end].isnumeric():
                    col_end += 1

                print("To check: ", row, col_end, matrix[row][col:col_end])
                if not is_isolated(matrix, row, col, col_end):

                    print(" It is not isolated")
                    sum_isolated += int(matrix[row][col:col_end])
    print(sum_isolated)
