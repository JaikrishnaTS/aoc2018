#!/usr/bin/env python3

import heapq
import numpy as np
import operator

points = []
np.set_printoptions(threshold=np.nan)

with open('inp6.txt') as f:
    for line in f:
        line = line.strip()
        x, _, y = line.partition(', ')
        points.append((int(y), int(x)))
#print(points)

areas = [0] * len(points)

minx = min(points, key=operator.itemgetter(0))[0] - 1
miny = min(points, key=operator.itemgetter(1))[1] - 1
maxx = max(points, key=operator.itemgetter(0))[0] + 1
maxy = max(points, key=operator.itemgetter(1))[1] + 1

mat = np.zeros((maxx+1, maxy+1), dtype=int)

print(minx, miny, maxx, maxy)

mandist = lambda pt1, pt2: abs(pt1[0] - pt2[0]) + abs(pt1[1] - pt2[1])
closearea = 0

for x in range(minx, maxx + 1):
    for y in range(miny, maxy + 1):
        pt = (x, y)
        dists = []
        for i, point in enumerate(points):
            dists.append((mandist(pt, point), i))
        totaldist = sum(g[0] for g in dists)
        if totaldist < 10000:
            closearea += 1
        heapq.heapify(dists)
        #print(pt, dists)
        mind = dists[0][0]
        if dists[1][0] == mind or dists[2][0] == mind:
            # same dist
            continue
        areas[dists[0][1]] += 1
        mat[pt] = dists[0][1] + 1

avoid = set()
avoid.update(mat[minx, :])
avoid.update(mat[maxx, :])
avoid.update(mat[miny, :])
avoid.update(mat[maxy, :])
avoid.remove(0)
print(avoid)
for i in avoid:
    areas[i-1] = 0
print(max(areas))
#print(areas)
print(closearea)
#print(mat)
#print(mat[minx:maxx+1, miny:maxy+1])
