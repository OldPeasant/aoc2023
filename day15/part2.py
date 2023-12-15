import sys

sys.path.append('../lib')
from pmg import *

def aoc_hash(s):
    cv = 0
    for c in s.encode('ascii'):
        cv += c
        cv *= 17
        cv = cv % 256
    return cv

def perform_eq(boxes, label, cnt):
    index = aoc_hash(label)
    box = boxes[index]
    for e in box:
        if e[0] == label:
            e[1] = cnt
            return
    box.append( [label, cnt]  )

def perform_min(boxes, label):
    index = aoc_hash(label)
    box = boxes[index]
    for e in box:
        if e[0] == label:
            box.remove(e)
            return

def print_boxes(boxes):
    for i, b in enumerate(boxes):
        if len(b) > 0:
            print("Box {}".format(i))
            for l in b:
                print("", l)

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()
    boxes = [ list([]) for i in range(256)]

    for l in lines:
        for s in l.split(','):
            if '=' in s:
                label, cnt_s = s.split('=')
                perform_eq(boxes, label, int(cnt_s))
            else:
                if not s.endswith('-'):
                    raise Exception()
                label = s.split('-')[0]
                perform_min(boxes, label)
            print("After \"{}\"".format(s))
            print_boxes(boxes)

    focusing_power = 0
    for box_index, box in enumerate(boxes):
        for lense_index, lense in enumerate(box):
            fp = (box_index + 1) * (lense_index+1) * lense[1]
            print(box_index, lense, fp)
            focusing_power += fp
    print(focusing_power)
