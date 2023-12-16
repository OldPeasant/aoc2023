import sys

sys.path.append('../lib')
from pmg import *
DIR = {
    "N" : (-1, 0),
    "S" : (1, 0),
    "W" : (0, -1),
    "E" : (0, 1)
}

SEE_THROUGH = {
    'N' : '|',
    'S' : '|',
    'W' : '-',
    'E' : '-'
}

SPLIT = {
    'N' : '-',
    'S' : '-',
    'W' : '|',
    'E' : '|'
}

SPLIT_DIRS = {
    'N' : ['W', 'E'],
    'S' : ['W', 'E'],
    'W' : ['N', 'S'],
    'E' : ['N', 'S']
}

REFLECT = {
        'N' : {'\\' : 'W', '/' : 'E'},
        'S' : {'\\' : 'E', '/' : 'W'},
        'W' : {'\\' : 'N', '/' : 'S'},
        'E' : {'\\' : 'S', '/' : 'N'},
}
class Beam:
    def __init__(self, row, col, direction):
         self.row = row
         self.col = col
         self.direction = direction
    def __repr__(self):
        return "({}, {}) -> {}".format(self.row, self.col, self.direction)

class Playfield:
    def __init__(self, grid, start_beam):
        self.grid = grid
        self.beams = [start_beam]
        self.energized = set()
        #self.energized.add(str(start_beam.row) + str(start_beam.col))
        self.beams_done_before = set()
    def next(self):
        while True:
            if len(self.beams) == 0:
                return False
            beam = self.beams.pop()
            if str(beam) not in self.beams_done_before:
                break
        self.beams_done_before.add(str(beam))
        delta = DIR[beam.direction]
        new_row = beam.row + delta[0]
        new_col = beam.col + delta[1]
        if new_row < 0 or new_col < 0 or new_row >= len(self.grid) or new_col >= len(self.grid[0]):
            #print("Bean {} goes outside: ({}, {})".format(beam, new_row, new_col))
            return True
        self.energized.add(str(new_row) + '|' + str(new_col))
        beam.row = new_row
        beam.col = new_col
        #print("new coords are", new_row, new_col)
        ch = self.grid[new_row][new_col]
        if ch == '.' or ch == SEE_THROUGH[beam.direction]:
            #print("Char is {}, so it is see through".format(ch))
            self.beams.append(beam)
            return True
        if ch == SPLIT[beam.direction]:
            #print("we have a split")
            sd = SPLIT_DIRS[beam.direction]
            #print("Split dirs of {} are {}".format(beam.direction, sd))
            self.beams.append(Beam(new_row, new_col, sd[0]))
            self.beams.append(Beam(new_row, new_col, sd[1]))
            return True
        if ch not in ['\\', '/']:
            raise Exception(ch)
        beam.direction = REFLECT[beam.direction][ch]
        self.beams.append(beam)
        return True
        
    def __repr__(self):
        lines = []
        for r, row in enumerate(self.grid):
            row_str_left = ""
            row_str_right = ""
            for c, cell in enumerate(row):
                row_str_left += cell
                if str(r) + '|' + str(c) in self.energized:
                    row_str_right += "*"
                else:
                    row_str_right += cell
            lines.append(row_str_left + "  " + row_str_right)
        return "\n".join(lines)
def start_beans(grid):
    # from the left and right:
    for i in range(len(grid)):
        yield Beam(i, -1, "E")
        yield Beam(i, len(grid[0]), "W")
    for i in range(len(grid[0])):
        yield Beam(-1, i, "S")
        yield Beam(len(grid), i, "N")

with open(sys.argv[1]) as f:
    grid = f.read().splitlines()
    best = -1
    for b in start_beans(grid):
        playfield = Playfield(grid, b)
        count = 0
        while playfield.next():
            count += 1
            l = len(playfield.energized)
            if l > best:
                best = l
            print(count, l, best)
        #print(playfield.current_beam)
        #print(playfield)
    #print(playfield.energized)
    print(best)
