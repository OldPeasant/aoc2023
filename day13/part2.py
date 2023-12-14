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
        #print(i)
        mirrors = True
        j = 0
        while True:
            if i - j < 0 or i + 1 + j >= len(row):
                #print("break outside")
                break
            if row[i-j] != row[i+j+1]:
                #print("break unequal at", i, j, row[i-j], row[i+j+1])
                mirrors = False
                break
            j += 1
        if mirrors:
            result.append(i + 1)
        #print(result)
    return result

def find_cols_left(g):
    mc = None
    for row in g:
        #print("row", row)
        cl = find_cols_left_for_row(row)
        if mc is None:
            mc = set()
            mc.update(cl)
        else:
            mc = mc.intersection(cl)
        #print(mc)
    #print("!", mc)
    return mc

def convert(m):
    result = []
    for c in range(len(m[0])):
        new_row = []
        for r in range(len(m)):
            new_row.append(m[r][c])
        result.append(new_row)
    return result

SWAPPED = {'.':'#', '#':'.'}
def copy_smudged(g, r, c):
    #print("smudge at ", r, c)
    #for row in g:
    #    print(row)
    
    result = []
    for row_ix, row in enumerate(g):
        new_row = str(row)
        if r == row_ix:
            new_row = new_row[:c] + SWAPPED[row[c]] + new_row[c + 1:]
            #print("smudge at ", row_ix, c)
            #print(row)
            #print(new_row)
        result.append(new_row)
    #print("becomes")
    #for row in result:
    #    print(row)
    #print("--------------")
    return result

def smudged(g):
    result = []
    for row_ix, row in enumerate(g):
        for col_ix, cell in enumerate(row):
            result.append(copy_smudged(g, row_ix, col_ix))
    return result

def eq(s1, s2):
    for v in s1:
        if v not in s2:
            return False
    for v in s2:
        if v not in s1:
            return False
    return True

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
    for g_orig in grouper.groups:
        set_c = set()
        set_r = set()
        print("Orig Group")
        for l in g_orig:
            print(l)
        for g in smudged(g_orig):
            cl = find_cols_left(g)
            rt = find_rows_top(convert(g))
            if len(cl) > 0 or len(rt) > 0:
                print("''''''''''''''''''''''''''''''''''''")
                print("smudged group")
                for l in g:
                    print(l)
                print(cl, rt)
            if len(cl) + len(rt) >= 1:
                clo = find_cols_left(g_orig)
                rto = find_rows_top(convert(g_orig))
                #if len(clo) + len(rto) == 1:
                if True or not eq(cl, clo) or not eq(rt, rto):
                    print("=====================")
                    print(clo, rto)
                    print(g)
                    print("bla", cl, rt)
                    set_c.update(cl)
                    set_r.update(rt)
                else:
                    print("oops", cl, clo, rt, rto)
        cols_left += sum(set_c)
        rows_top += sum(set_r)
        #print(cols_left, rows_top)
        print("----------------------------")
    print(cols_left + 100 * rows_top)



# wrong    36870
# too high 163255
