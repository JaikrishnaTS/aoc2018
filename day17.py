#!/usr/bin/env python3

import sys
import re

if len(sys.argv) > 1:
    input_filename = sys.argv[1]
else:
    dayn = re.match(r'.*day(\d+)\.py', sys.argv[0]).group(1)
    input_filename = 'inp' + dayn + '.txt'

INF = 10**10
lines = []
minx, maxx = INF, -INF
miny, maxy = INF, -INF
SPRINGX, SPRINGY = 500, 0

with open(input_filename) as f:
    for line in f:
        axis, _, perp_range  = line.partition(', ')
        assert _
        start, _, stop = perp_range[2:].strip().partition('..')
        assert _
        start, stop = int(start), int(stop)
        if axis[0] == 'x':  # parallel to y axis
            x = int(axis[2:])
            minx = min(minx, x)
            maxx = max(maxx, x)
            miny = min(miny, start)
            maxy = max(maxy, stop)
            lines.append(('x', x, start, stop))
        else:  # parallel to x axis
            y = int(axis[2:])
            miny = min(miny, y)
            maxy = max(maxy, y)
            minx = min(minx, start)
            maxx = max(maxx, stop)
            lines.append(('y', y, start, stop))

minx = min(minx, SPRINGX)
maxx = max(maxx, SPRINGX)

# extend x boundaries to flow if bucket in edge
minx -= 1
maxx += 1

# find length of resultant axes
X = maxx - minx + 1
Y = maxy - miny + 1

grid = [[0] * X for _ in range(Y)]

print('Size:', Y, X)
sys.setrecursionlimit(Y * 2)

for axis, fixed, start, stop in lines:
    if axis == 'x':
        x = fixed - minx
        for y in range(start - miny, stop - miny + 1):
            grid[y][x] = 3
    else:
        y = fixed - miny
        for x in range(start - minx, stop - minx + 1):
            grid[y][x] = 3

def print_state():
    PRINT_CHAR = [' ', '|', '~', '#', 'B']
    for line in grid:
        print(''.join(PRINT_CHAR[c] for c in line))
    print('-' * X)

"""
0 . nil
1 | flowing water
2 ~ settled water
3 # bucket edge
4 M max-boundary
"""
def flow(y, x):
    if y == len(grid):  # beyond maxy cannot settle
        return 4
    if grid[y][x] != 0:
        return grid[y][x]
    down = flow(y + 1, x)
    if down == 4 or down == 1:  # reached max
        grid[y][x] = 1
        #print_state()
        return 4
    elif down == 2 or down == 3:  # there's an edge downwards
        grid[y][x] = 1  #  we're at least flowing from here
        #print_state()
        left = flow(y, x - 1)
        right = flow(y, x + 1)
        #print_state()
        if left == 3 and right == 3:  # hit an edge both sides
            j = x  # settle left
            while grid[y][j] == 1:
                grid[y][j] = 2
                j -= 1
            j = x + 1  # settle right
            while grid[y][j] == 1:
                grid[y][j] = 2
                j += 1
            return 2
        elif left == 4 or right == 4:  # either side hit maxy
            return 4
        elif left == 3 or right == 3:  # either side hit edge
            return 3
        elif left == right == 1:
            return 4
        else:
            raise ValueError(left, right, y, x)
        #print_state()
    else:
        raise ValueError(down, y, x)

#print_state()
flow(0, SPRINGX - minx)
#print_state()

settle_count = flow_count = 0
for line in grid:
    flow_count += line.count(1)
    settle_count += line.count(2)
print(flow_count + settle_count, settle_count)
