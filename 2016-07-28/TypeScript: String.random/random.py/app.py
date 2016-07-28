#!/usr/bin/env python

from matplotlib import pyplot as pp
import numpy as np
import sys

def levenstein(source, target):
    if len(source) < len(target):
        return levenstein(target, source)
    if len(target) == 0:
        return len(source)

    source = np.array(tuple(source))
    target = np.array(tuple(target))

    prev_row = np.arange(target.size + 1)
    for s in source:
        curr_row = prev_row + 1
        curr_row[1:] = np.minimum(
                curr_row[1:], np.add(prev_row[:-1], target != s))
        curr_row[1:] = np.minimum(
                curr_row[1:], curr_row[0:-1] + 1)
        prev_row = curr_row

    return prev_row[-1]

with open(sys.argv[1]) as file:
    lines = list(map(lambda l: l[:-1], file.readlines()))

ds, l0 = [], lines[0]
for line in lines[1:]:
    d = levenstein(line, l0)
    if d > 0: ds.append(d)

pp.title('Levenstein Differences')
pp.hist(ds, bins=13)
pp.grid()
pp.show()
