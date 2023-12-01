import sys

chars = [
    ["one", "1"],["two", "2"], ["three", "3"], ["four", "4"], ["five", "5"],
    ["six", "6"], ["seven", "7"], ["eight", "8"], ["nine", "9"], ["zero", "0"],
]

def preprocess(s):
    n = ""
    for i in range(len(s)):
        n += s[i]
        for m in chars:
            if s[i:].startswith(m[0]):
                n += m[1]
    return n

with open(sys.argv[1]) as f:
    total = 0
    for l in f.read().splitlines():
        nums = [int(c) for c in preprocess(l) if c.isnumeric()]
        total += 10 * nums[0] + nums[-1]
    print(total)
