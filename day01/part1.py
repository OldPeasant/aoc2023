import sys

with open(sys.argv[1]) as f:
    total = 0
    for l in f.read().splitlines():
        nums = [int(c) for c in l if c.isnumeric()]
        total += 10 * nums[0] + nums[-1]
    print(total)
