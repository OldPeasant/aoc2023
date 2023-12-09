import sys

with open(sys.argv[1]) as f:
    score = 0
    for i, l in enumerate(f.read().splitlines()): 
        winning, having = ([int(i) for i in parts.split()] for parts in l.split(": ")[1].split(" | "))
        count_match = len(list(n for n in having if n in winning))
        if count_match > 0:
            score += pow(2, count_match - 1)
    print(score)
