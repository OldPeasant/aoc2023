import sys

DIRS = { "H" : [(0, -1), (0, 1)], "V" : [(1, 0), (-1, 0)] }
OTHER_DIR = { "H" : "V", "V" : "H" }

class Grid:
    def __init__(self, lines):
        self.heat_loss = list( list( int(c) for c in row) for row in lines)
        self.height, self.width = len(lines), len(lines[0])
        self.reductions = {"H" : {}, "V" : {}}


with open(sys.argv[1]) as f:
    grid = Grid(f.read().splitlines())
    to_follow = { "H" : { (0, 0) : 0 }, "V" : { (0, 0) : 0 } }

    iter_count = 0
    while sum( len(x) for x in to_follow.values()) > 0:
        iter_count += 1
        #print("==== An iteration: {} ====".format(iter_count))
        ##print("iii         Update to_follow (H={},V={}): {}".format(len(to_follow["H"]), len(to_follow["H"]), to_follow))
        #print("iii         Update to_follow (H={},V={})".format(len(to_follow["H"]), len(to_follow["V"])))
        had_changes = False
        for d in DIRS.keys():
            #print("  Examing direction {}".format(d))
            #print(to_follow[d])
            for coord, level in to_follow[d].items():
                #print("Would follow {} / {}".format(coord, level))
                #print("    Examing coord {}".format(coord))
                for delta in DIRS[d]:
                    #print("      Follow delta {}".format(delta))
                    sr = level
                    for i in range(1, 11):
                        #print("        Range {}".format(i))
                        new_row = coord[0] + i * delta[0]
                        new_col = coord[1] + i * delta[1]
                        if new_row >= 0 and new_row < grid.height and new_col >= 0 and new_col < grid.width:
                            #print("        New row/col = {}/{}".format(new_row, new_col))
                            ##print("DEBUG {}".format(grid.heat_loss))
                            #print("        Heat loss at {}/{} is {}".format(new_row, new_col, grid.heat_loss[new_row][new_col]))
                            sr += grid.heat_loss[new_row][new_col]
                            #print("        Sum of reductions is now {}".format(sr))
                            #print("        Up to now reductions at {}:{}/{} was {}".format(d, new_row, new_col, grid.reductions[d].get(new_row, {}).get(new_col, sys.maxsize)))
                            if i >= 4 and sr < grid.reductions[d].get((new_row, new_col), sys.maxsize) and sr < to_follow[OTHER_DIR[d]].get( (new_row, new_col), sys.maxsize):
                                #print("          Updating grid.reductions ({})".format(sr))
                                grid.reductions[d][(new_row, new_col)] = sr
                                to_follow[OTHER_DIR[d]][ (new_row, new_col) ] = sr
                                #print("            Update to_follow (H={},V={}): {}".format(len(to_follow["H"]), len(to_follow["H"]), to_follow))
                                ##print("            Update to_follow (H={},V={})".format(len(to_follow["H"]), len(to_follow["H"])))
                            #else:
                            #    print("          Ignoring this one")
                        #else:
                        #    print("        Oh, {},{} is outside, ignoring".format(new_row, new_col))
                #print("EXTRA1            Update to_follow (H={},V={})".format(len(to_follow["H"]), len(to_follow["H"])))
                #print("EXTRA2            Update to_follow (H={},V={})".format(len(to_follow["H"]), len(to_follow["H"])))
            to_follow[d] = {}
    print(min(grid.reductions[s][(grid.height - 1), grid.width - 1] for s in DIRS.keys()))


# 1286 too hight

