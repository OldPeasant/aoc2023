import sys

sys.path.append('../lib')
from pmg import *

def extrapolate(nums):
    print("n", nums)
    if min(nums) == 0 and max(nums) == 0:
        l = list(nums)
        l.append(0)
        print("l", l)
        return l
    else:
        l = []
        for i in range(len(nums)-1):
            l.append(nums[i+1] - nums[i])
        v = extrapolate(l)
        print("ex", v)
        r = list(nums)
        r.insert(0, nums[0] - v[0] )
        print("e", r)
        return r

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

    total = 0
    for l in lines:
        p = extrapolate(list(int(i) for i in l.split()))[0]
        print("*", p)
        total +=  p
    print(total)
