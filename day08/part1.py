import sys

sys.path.append('../lib')
from pmg import *

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

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

    moves = Moves(lines[0])
    mappings = {}
    for l in lines[2:]:
        from_point, pair = l.split(" = ")
        mappings[from_point] = pair[1:-1].split(", ")
    count = 0
    curr = "AAA"
    while True:
        curr = mappings[curr][DIR[moves.get()]]
        count += 1
        if curr == 'ZZZ':
            print(count)
            exit(0)
