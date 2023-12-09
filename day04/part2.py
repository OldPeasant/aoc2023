import sys

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()
    copies = [1] * len(lines)
    for i, l in enumerate(lines):
        winning, having = ([int(i) for i in parts.split()] for parts in l.split(": ")[1].split(" | "))
        for c in range(i + 1, min(i + 1 + len(list(n for n in having if n in winning)), len(copies))):
            copies[c] += copies[i]
    print(sum(copies))
