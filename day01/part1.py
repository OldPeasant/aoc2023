import sys

sys.path.append('../lib')
from pmg import *

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

    total = 0
    for l in lines:
        nums = []
        for c in l:
            if c.isnumeric():
                nums.append(int(c))
        if len(nums) > 0:
            p = 10 * nums[0] + nums[-1]
        total += p
    print(total)
