import sys

sys.path.append('../lib')
from pmg import *

def fill(s, n):
    i = 0
    new_s = ""
    for c in s:
        if c == '?':
            if n & pow(2, i) > 0:
                new_s += "#"
            else:
                new_s += "."
            i += 1
        else:
            new_s += c
    return new_s

def fits(s, actual_counts):
    counts = Grouper()
    for i,c in enumerate(s):
        if c == "#":
            counts.add(1)
        else:
            counts.next()
    lengths = list(len(g) for g in counts.groups)
    #print(lengths)
    if len(lengths) != len(actual_counts):
        return False
    for a, b in zip(lengths, actual_counts):
        if a != b:
            return False
    return True

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

    total = 0
    for l in lines:
        row, counts_str = l.split()
        counts = list(int(c) for c in counts_str.split(","))
        count_question_marks = sum(1 for c in row if c == '?')
        total_per_row = 0
        for i in range(pow(2, count_question_marks)):
            mapped = fill(str(row), i)
            #print(i, mapped)
            if fits(mapped, counts):
                #print("", "fits", mapped)
                total_per_row += 1
            #else:
            #    print("", "no fit", mapped)
        print(row, counts, count_question_marks, total_per_row)
        total += total_per_row
    print(total)
