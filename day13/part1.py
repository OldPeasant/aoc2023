import sys

sys.path.append('../lib')
from pmg import *

def find_rows_top_for_col(col):
    result = []
    for i in range(0, len(col)-1 ):
        #print(i)
        mirrors = True
        j = 0
        while True:
            if i - j < 0 or i + 1 + j >= len(col):
                #print("break outside")
                break
            if col[i-j] != col[i+j+1]:
                #print("break unequal at", i, j, col[i-j], col[i+j+1])
                mirrors = False
                break
            j += 1
        if mirrors:
            result.append(i + 1)
        #print(result)
    return result

def find_rows_top(g):
    mc = None
    for col in g:
        #print("col", col)
        cl = find_rows_top_for_col(col)
        if mc is None:
            mc = set()
            mc.update(cl)
        else:
            mc = mc.intersection(cl)
        #print(mc)
    #print("!", mc)
    return mc

def find_cols_left_for_row(row):
    result = []
    for i in range(0, len(row)-1 ):
        print(i)
        mirrors = True
        j = 0
        while True:
            if i - j < 0 or i + 1 + j >= len(row):
                print("break outside")
                break
            if row[i-j] != row[i+j+1]:
                print("break unequal at", i, j, row[i-j], row[i+j+1])
                mirrors = False
                break
            j += 1
        if mirrors:
            result.append(i + 1)
        print(result)
    return result

def find_cols_left(g):
    mc = None
    for row in g:
        print("row", row)
        cl = find_cols_left_for_row(row)
        if mc is None:
            mc = set()
            mc.update(cl)
        else:
            mc = mc.intersection(cl)
        print(mc)
    print("!", mc)
    return mc

def convert(m):
    result = []
    for c in range(len(m[0])):
        new_row = []
        for r in range(len(m)):
            new_row.append(m[r][c])
        result.append(new_row)
    return result

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

    grouper = Grouper()
    for l in lines:
        if not l:
            grouper.next()
        else:
            grouper.add(l)
    cols_left = 0
    rows_top = 0
    for g in grouper.groups:
        cl = find_cols_left(g)
        rt = find_rows_top(convert(g))
        print("bla", cl, rt)
        cols_left += sum(cl)
        rows_top += sum(rt)
        print(cols_left, rows_top)
        print("----------------------------")
    print(cols_left + 100 * rows_top)



# wrong    36870
# too high 163255
