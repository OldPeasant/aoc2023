import sys

sys.path.append('../lib')
from pmg import *

class Mapping:
    def __init__(self, mapping_lines):
        title = mapping_lines[0]
        elems = title.split(" ")[0].split("-")
        self.map_src = elems[0]
        self.map_dest = elems[2]
        self.ranges = []
        for row in mapping_lines[1:]:
            self.ranges.append(list([int(v) for v in row.split()]))

    def map_value(self, v):
        print("    Mapping " + self.map_src + " -> " + self.map_dest)
        for r in self.ranges:
            if v >= r[1] and v < r[1] + r[2]:
                mapped_value = r[0] + v - r[1] 
                print("      in range  "  + str(r) + " -> " + str(mapped_value))
                return mapped_value
        print("      no mapping, keeping " + str(v))
        return v

    def __repr__(self):
        l = []
        l.append("Dest " + self.map_dest + ", Src " + self.map_src)
        for r in self.ranges:
            l.append(", ".join([str(a) for a in r]))
        return "\n".join(l)

class MappingColl:
    def __init__(self):
        self.mappings = []

    def find_mapping_src(self, src_type):
        for m in self.mappings:
            if m.map_src == src_type:
                return m
        raise Exception("No mapping for " + src_type + " found.")

def find_location(mapping_coll, res_type, v):
    print("  find location for " + str(v) + " of type " + res_type)
    if res_type == "location":
        print("  it's already location, return " + str(v))
        return v
    mapping = mapping_coll.find_mapping_src(res_type)
    print("  Relevant mapping" + str(mapping))
    mv = mapping.map_value(v)
    print("  mapped value is " + str(mv))
    return find_location(mapping_coll, mapping.map_dest, mv)

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

    seeds = [int(s) for s in lines[0].split(": ")[1].split()]
    grouper = Grouper()
    for l in lines[2:]:
        if len(l) == 0:
            grouper.next()
        else:
            grouper.add(l)
    mapping_coll = MappingColl()
    for group in grouper.groups:
        mapping_coll.mappings.append(Mapping(group))

    for m in mapping_coll.mappings:
        print("Mapping:")
        print(m)

    locations = []
    for s in seeds:

        print("Examine seed " + str(s))
        loc = find_location(mapping_coll, "seed", s) 
        print("location is " + str(loc))
        locations.append(loc)
    print(locations)
    print(min(locations))
