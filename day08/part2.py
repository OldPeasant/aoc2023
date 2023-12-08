import sys
import math

DIR = { 'L' : 0, 'R' : 1 }

class Moves:
    def __init__(self, lr):
        self.moves = lr
        self.index = 0
    def get(self):
        v = self.moves[self.index]
        self.index += 1
        if self.index >= len(self.moves):
            self.index = 0
        return v

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

    mappings = {}
    for l in lines[2:]:
        from_point, pair = l.split(" = ")
        mappings[from_point] = pair[1:-1].split(", ")

    deltas = []
    for s in filter(lambda s: s.endswith("A"), mappings.keys()):
        moves = Moves(lines[0])
        count = 0
        while True:
            s = mappings[s][DIR[moves.get()]]
            count += 1
            if s.endswith('Z'):
                deltas.append(count)
                break
    result = 1
    for d in deltas:
        result = lcm(result, d)
    print(result)
