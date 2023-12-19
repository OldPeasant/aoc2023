import sys
from copy import deepcopy

XMAS = "xmas"

def initial_ratings():
    r = Ratings()
    for c in r.intervals.keys():
        r.intervals[c].append( (1, 4000) )
    return r

def split_intervals_by_conditional(intervals, cond):
    result_match = []
    result_rest = []
    for i in intervals:
        if cond.cmp == '<':
            if i[0] < cond.val:
                if i[1] < cond.val:
                    result_match.append(i)
                else:
                    result_match.append( (i[0], cond.val - 1) )
                    result_rest.append( (cond.val, i[1]) )
            else:
                result_rest.append(i)
        elif cond.cmp == '>':
            if i[0] > cond.val:
                result_match.append(i)
            else:
                if i[1] > cond.val:
                    result_match.append( (cond.val + 1, i[1]) )
                    result_rest.append( (i[0], cond.val) )
                else:
                    result_rest.append(i)
        else:
            raise Exception()
    return (result_match, result_rest)

class Ratings:
    def __init__(self):
        self.intervals = {}
        for c in XMAS:
            self.intervals[c] = []

    def split_by(self, cond):
        if cond.is_conditional():
            matching = Ratings()
            rest = Ratings()
            for c in XMAS:
                if c == cond.var:
                    matching.intervals[c], rest.intervals[c] = split_intervals_by_conditional(self.intervals[c], cond)
                else:
                    matching.intervals[c] = deepcopy(self.intervals[c])
                    rest.intervals[c] = deepcopy(self.intervals[c])
            return (matching, rest)
        else:
            return (self, None)

    def __repr__(self):
        return "Ratings({})".format(self.intervals)

class Conditional:
    def __init__(self, var, cmp, val, tgt):
        self.var = var
        self.cmp = cmp
        self.val = int(val)
        self.tgt = tgt
    def is_conditional(self):
        return True

    def __repr__(self):
        return "Conditional({}, {}, {}, {})".format(self.var, self.cmp, self.val, self.tgt)

class Unconditional:
    def __init__(self, result):
        self.result = result
    def is_conditional(self):
        return False

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

    def __repr__(self):
        return "Workflow[{}]".format(self.name)

class Analyser:
    def __init__(self, workflows):
        self.workflows = workflows
        self.accepted_ratings = []

        self.deep_thought(initial_ratings(), 'in')

    def deep_thought(self, curr_rating, wf_name):
        if curr_rating is None:
            return
        if wf_name == 'R':
            pass
        elif wf_name == 'A':
            self.accepted_ratings.append(curr_rating)
        else:
            workflow = self.workflows[wf_name]
            rating = curr_rating
            for r in workflow.rules:
                matching, mismatching = rating.split_by(r)
                if matching is not None:
                    if r.is_conditional():
                        self.deep_thought(matching, r.tgt)
                    else:
                        self.deep_thought(matching, r.result)
                if mismatching is not None:
                    rating = mismatching
            
with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

    parsing_workflows = True
    workflows = {}
    for l in lines:
        if len(l) == 0:
            break
        wf = Workflow(l)
        workflows[wf.name] = wf

    analyser = Analyser(workflows)
    total = 0
    for ar in analyser.accepted_ratings:
        c = 1
        for k, v in ar.intervals.items():
            if len(v) != 1:
                raise Exception()
            i = v[0]
            c *= i[1] - i[0] + 1
        total += c
    print(total)
