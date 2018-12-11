#!/usr/bin/env python3

from collections import deque

N = 300

def get_cell_powers(grid_serial):
    cells = [ [0] * N for _ in range(N) ]
    for x in range(N):
        for y in range(N):
            rid = x + 11
            pl = rid * (y + 1) + grid_serial
            pl *= rid
            h = (pl // 100) % 10
            cells[x][y] = h - 5
    return cells

def find_max_power_3cell(grid_serial):
    cells = get_cell_powers(grid_serial)
    curmax = 0
    for x in range(N - 2):
        for y in range(N - 2):
            newmax = sum(sum(cells[i][y: y + 3]) for i in range(x, x + 3))
            if newmax >= curmax:
                curmax = newmax
                rx, ry = x, y
    return rx + 1, ry + 1

def find_max_power_any_cell_bruteforce(grid_serial):
    cells = get_cell_powers(grid_serial)
    curmax = 0
    for sq in range(1, N + 1):
        print(sq)
        for x in range(N - sq + 1):
            for y in range(N - sq + 1):
                newmax = sum(sum(cells[i][y: y + sq]) for i in range(x, x + sq))
                if newmax > curmax:
                    curmax = newmax
                    rx, ry = x, y
                    msq = sq
    return rx + 1, ry + 1, msq

def find_max_power_any_cell(grid_serial):
    cells = get_cell_powers(grid_serial)
    seen = {(0, 0, N)}
    tocompute = deque([(0, 0, N, sum(map(sum, cells)))])
    maxsum = 0
    result = None
    while tocompute:
        minx, miny, sq, currsum = tocompute.popleft()
        if currsum > maxsum:
            maxsum = currsum
            result = minx, miny, sq
        if sq == 1:
            continue
        maxx, maxy = minx + sq, miny + sq
        sq -= 1
        firstx = sum(cells[minx][miny : maxy])
        lastx = sum(cells[maxx - 1][miny : maxy])
        firsty = sum(cells[x][miny] for x in range(minx, maxx))
        lasty = sum(cells[x][maxy - 1] for x in range(minx, maxx))
        # options to chop off:
        # (firstx, firsty), (firstx, lasty), (lastx, firsty), (lastx, lasty)
        if (minx + 1, miny + 1, sq) not in seen:
            seen.add((minx + 1, miny + 1, sq))
            tmpsum = currsum - (firstx + firsty - cells[minx][miny])
            tocompute.append((minx + 1, miny + 1, sq, tmpsum))
        if (minx + 1, miny, sq) not in seen:
            seen.add((minx + 1, miny, sq))
            tmpsum = currsum - (firstx + lasty - cells[minx][maxy - 1])
            tocompute.append((minx + 1, miny, sq, tmpsum))
        if (minx, miny + 1, sq) not in seen:
            seen.add((minx, miny + 1, sq))
            tmpsum = currsum - (lastx + firsty - cells[maxx - 1][miny])
            tocompute.append((minx, miny + 1, sq, tmpsum))
        if (minx, miny, sq) not in seen:
            seen.add((minx, miny, sq))
            tmpsum = currsum - (lastx + lasty - cells[maxx - 1][maxy - 1])
            tocompute.append((minx, miny, sq, tmpsum))
    return result[0] + 1, result[1] + 1, result[2]

