from sys import argv
from operator import mul
from functools import reduce

colors = ['blue', 'red', 'green']

with open(argv[1]) as f:
    result = 0
    for l in f.read().splitlines():
        max_counts = { c:0 for c in colors}
        for turn in l.split(": ")[1].split("; "):
            for col_str in turn.split(", "):
                cnt_str, col = col_str.split(" ")
                cnt = int(cnt_str)
                if cnt > max_counts[col]:
                    max_counts[col] = cnt
        result += reduce(mul, [max_counts[c] for c in colors])
    print(result)
