import sys

sys.path.append('../lib')
from pmg import *

def calc_seeds_intervals(seeds_input):
    intervals = []
    for i in range(0, len(seeds_input), 2):
        intervals.append( (seeds_input[i], seeds_input[i] + seeds_input[i+1]) )
    intervals.sort(key=lambda a:a[0])
    return intervals

class Mapping:
    def __init__(self, mapping_lines):
        title = mapping_lines[0]
        elems = title.split(" ")[0].split("-")
        self.map_src = elems[0]
        self.map_dest = elems[2]
        tmp_ranges = []
        for row in mapping_lines[1:]:
            dest, src, length = [int(v) for v in row.split()]
            i_lower = src
            i_offset = dest - src
            i_upper = i_lower + length
            tmp_ranges.append( (i_lower, i_upper, i_offset) )
        tmp_ranges.sort(key=lambda a:a[0])
        tmp2_ranges = []
        tmp2_ranges.append( ("low", tmp_ranges[0][0], 0) )
        for index in range(len(tmp_ranges)-1):
            tmp2_ranges.append(tmp_ranges[index])
            tmp2_ranges.append( (tmp_ranges[index][1], tmp_ranges[index+1][0], 0) )
        tmp2_ranges.append(tmp_ranges[-1])
        tmp2_ranges.append( (tmp_ranges[-1][1], "high", 0) )

        self.ranges =  []
        for r in tmp2_ranges:
            if r[0] != r[1]:
                self.ranges.append(r)
            
    def map_single(self, interval):
        result = []
        for r in self.ranges:
            i_from = (interval[0] if r[0] == "low" else max(interval[0], r[0])) + r[2]
            i_to = (interval[1] if r[1] == "high" else min(interval[1], r[1])) + r[2]
            if i_from < i_to:
                result.append( (i_from, i_to) )
            
        return result

class MappingColl:
    def __init__(self):
        self.mappings = []

    def find_mapping(self, src_type):
        for m in self.mappings:
            if m.map_src == src_type:
                return m
        raise Exception("No mapping for " + src_type + " found.")

def transform(mapping_coll, input_intervals, name):
    mapping = mapping_coll.find_mapping(name)
    result_intervals = []
    for ii in input_intervals:
        mapped = mapping.map_single(ii)
        result_intervals.extend(mapped)
    result_intervals.sort(key=lambda a: a[0])
    if mapping.map_dest == 'location':
        return result_intervals
    else:
        return transform(mapping_coll, result_intervals, mapping.map_dest)

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

    seeds_input = [int(s) for s in lines[0].split(": ")[1].split()]
    seeds_intervals = calc_seeds_intervals(seeds_input)
    grouper = Grouper()
    for l in lines[2:]:
        if len(l) == 0:
            grouper.next()
        else:
            grouper.add(l)
    mapping_coll = MappingColl()
    for group in grouper.groups:
        mapping_coll.mappings.append(Mapping(group))
    result = transform(mapping_coll, seeds_intervals, "seed")
    print(result[0][0])
