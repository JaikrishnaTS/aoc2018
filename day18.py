#!/usr/bin/env python3

import sys
import re

test_inp = len(sys.argv) > 1 and sys.argv[1] == '-t'
dayn = re.match(r'.*day(\d+)\.py', sys.argv[0]).group(1)
input_filename = 'inp' + dayn + ('_' if test_inp else '') + '.txt'

grid = []
charmap = {'.': 0, '|': 1, '#': 2}
with open(input_filename) as f:
    for y, line in enumerate(f):
        grid.append(list(map(charmap.__getitem__, line.strip())))

Y, X = len(grid), len(grid[0])

def nei(y, x):
    nei_diff = ((-1, -1), (-1, 0), (-1, 1), 
                (0, -1), (0, 1),
                (1, -1), (1, 0), (1, 1))
    return ((y + j, x + i) for j, i in nei_diff 
            if ((0 <= y + j < Y) and (0 <= x + i < X)))

def hash_grid():
    lines = []
    for line in grid:
        lhash = 0
        for x in line:
            lhash <<= 2
            lhash |= x
        lines.append(lhash)
    return hash(tuple(lines))

def print_grid(day):
    print('Day: {}'.format(day))
    print_chars = ['.', '|', '#']
    for line in grid:
        print(''.join(print_chars[i] for i in line))
    print()
print_grid(0)

wrapdiff = None
stopday = None
seen = {0: hash_grid()}
target = 1000000000
for day in range(1, 10000):
    for y in range(Y):
        for x in range(X):
            if grid[y][x] == 0:  # open
                if sum((grid[ay][ax] & 3) == 1 for ay, ax in nei(y, x)) >= 3:
                    grid[y][x] |= 4 # (1 << 2)
                # else remains open
            elif grid[y][x] == 1:  # tree
                if sum((grid[ay][ax] & 3) == 2 for ay, ax in nei(y, x)) >= 3:
                    grid[y][x] |= 8 # (2 << 2)
                else:   # remain a tree
                    grid[y][x] |= 4 # (1 << 2)
            elif grid[y][x] == 2:  # lumber
                alum, atree = False, False
                for ay, ax in nei(y, x):
                    alum |= (grid[ay][ax] & 3 == 2)
                    atree |= (grid[ay][ax] & 3 == 1)
                if alum and atree:
                    grid[y][x] |= 8 # (2 << 2)
                # else remains open
            else:
                raise ValueError(y, x, grid[y][x])

    # advance the day
    for y in range(Y):
        for x in range(X):
            grid[y][x] >>= 2

    # optimize for part2
    curr_hash = hash_grid()
    if curr_hash in seen:
        print('Day {} seen in day {}'.format(day, seen[curr_hash]))
        if wrapdiff is None:
            first_day = seen[curr_hash]
            wrapdiff = day - first_day
            # stop after confirming one complete cycle
            stopday = day + wrapdiff + ((target - first_day) % wrapdiff)
        if wrapdiff != day - seen[curr_hash]:
            raise ValueError('cannot compute')
        if day == stopday:
            break
    seen[curr_hash] = day
    #print_grid(day)

count_trees = count_lumber = 0
for y in range(Y):
    for x in range(X):
        if grid[y][x] == 1:
            count_trees += 1
        elif grid[y][x] == 2:
            count_lumber += 1
print(count_trees * count_lumber)
