import sys

def extrapolate(nums):
    if min(nums) == 0 and max(nums) == 0:
        l = list(nums)
        l.append(0)
        return l
    else:
        #l = [ ]
        r = list(nums)
        r.append(list(r[-1] + extrapolate(list((r[i+1] - r[i]for i in range(len(r)-1))[-1] ))))
        return r

with open(sys.argv[1]) as f:
    total = 0
    for l in f.read().splitlines():
        total +=  extrapolate(list(int(i) for i in l.split()))[-1]
    print(total)
