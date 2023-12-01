import sys

sys.path.append('../lib')
from pmg import *

chars = [
    ["one", 1],
    ["two", 2],
    ["three", 3],
    ["four", 4],
    ["five", 5],
    ["six", 6],
    ["seven", 7],
    ["eight", 8],
    ["nine", 9],
    ["zero", 0],
]

def replace_chars(s):
    n = ""
    for i in range(len(s)):
        n += s[i]
        for m in chars:
            if s[i:].startswith(m[0]):
                n += str(m[1])
    return n

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

    total = 0
    for l in lines:
        nums = []
        repl = replace_chars(l)
        for c in repl:
            if c.isnumeric():
                nums.append(int(c))
        if len(nums) > 0:
            p = 10 * nums[0] + nums[-1]
        total += p
    print(total)
