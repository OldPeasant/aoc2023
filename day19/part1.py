import sys

sys.path.append('../lib')
from pmg import *

class PartRating:
    def __init__(self, line):
        self.values = {}
        for p in line[1:-1].split(','):
            var, val_str = p.split('=')
            self.values[var] = int(val_str)
    def sum_values(self):
        return sum(self.values.values())

class Conditional:
    def __init__(self, var, cmp, val, tgt):
        self.var = var
        self.cmp = cmp
        self.val = int(val)
        self.tgt = tgt
    def eval(self, rating):
        rat_val = rating.values[self.var]
        if self.cmp == '<' and rat_val < self.val:
            return self.tgt
        elif self.cmp == '>' and rat_val > self.val:
            return self.tgt
        else:
            return None

class Unconditional:
    def __init__(self, result):
        self.result = result
    def eval(self, rating):
        return self.result

class Workflow:
    def __init__(self, line):
        name, rest = line.split("{")
        self.name = name
        self.rules = []
        for rule in rest[:-1].split(','):
            if ":" in rule:
                cond, tgt = rule.split(':')
                var = cond[0]
                cmp = cond[1]
                val = cond[2:]
                self.rules.append(Conditional(var, cmp, val, tgt))
            else:
                self.rules.append(Unconditional(rule))
    def eval(self, rating):
        for r in self.rules:
            v = r.eval(rating)
            if v is not None:
                return v
        raise Exception("Could not evaulate")

def accepted(workflows, part_ratings, wf = 'in'):
    current_wf = workflows[wf]
    result = current_wf.eval(part_ratings)
    if result == 'A':
        return True
    elif result == 'R':
        return False
    else:
        return accepted(workflows, part_ratings, result)

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

    parsing_workflows = True
    workflows = {}
    part_ratings = []
    for l in lines:
        if len(l) == 0:
            if parsing_workflows is False:
                raise Exception()
            parsing_workflows = False
        elif parsing_workflows:
            wf = Workflow(l)
            workflows[wf.name] = wf
        else:
            part_ratings.append(PartRating(l))
        total = 0
        for pr in part_ratings:
            if accepted(workflows, pr):
                total += pr.sum_values()
    print(total)
