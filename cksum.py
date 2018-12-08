#!/usr/bin/env python3

from collections import Counter
import sys

with open('inp2.txt') as f:
    box_ids = f.read().split('\n')

def chardiff(str1, str2):
    return sum(c1 != c2 for c1, c2 in zip(str1, str2))

for i in range(len(box_ids)):
    for j in range(i + 1, len(box_ids)):
        if chardiff(box_ids[i], box_ids[j]) == 1:
            print(box_ids[i])
            print(box_ids[j])
            sys.exit(0)

sys.exit(0)

twos = threes = 0

for bid in box_ids:
    cnt = Counter(bid)
    if 2 in cnt.values():
        twos += 1
    if 3 in cnt.values():
        threes += 1

print(twos, threes, twos*threes)
