#!/usr/bin/env python3

import curses
import sys
import re

import itertools

test_inp = len(sys.argv) > 1 and sys.argv[1] == '-t'
dayn = re.match(r'.*day(\d+)\.py', sys.argv[0]).group(1)
input_filename = 'inp' + dayn + ('_' if test_inp else '') + '.txt'

posvel_re = re.compile(r'position=<([\-\d\, ]+)> velocity=<([\-\d, ]+)>')

ptsx, ptsy = [], []
velocity = []

with open(input_filename) as f:
    for line in f:
        match = posvel_re.match(line.strip())
        pos_str, vel_str = match.group(1), match.group(2)
        x, y = map(int, pos_str.split(','))
        dx, dy = map(int, vel_str.split(','))
        ptsx.append(x)
        ptsy.append(y)
        velocity.append((dx, dy))

N = len(velocity)

def draw(stdscr):
    # iterate till we can actually create a line of text
    for t in itertools.count():
        if max(ptsy) - min(ptsy) < 16:
            break
        for i in range(N):
            ptsx[i] += velocity[i][0]
            ptsy[i] += velocity[i][1]

    # normalize to screen size
    sy, sx = stdscr.getmaxyx()
    minx, miny = min(ptsx) - sx // 3, min(ptsy) - sy // 2
    for i in range(N):
        ptsx[i] -= minx
        ptsy[i] -= miny

    # provide navigation to scroll through time
    kp = 0
    while kp != ord('q'):
        stdscr.clear()
        if kp == ord('l'):  # next second
            t += 1
            for i in range(N):
                ptsx[i] += velocity[i][0]
                ptsy[i] += velocity[i][1]
        elif kp == ord('h'):  # prev second
            t -= 1
            for i in range(N):
                ptsx[i] -= velocity[i][0]
                ptsy[i] -= velocity[i][1]

        for x, y in zip(ptsx, ptsy):
            stdscr.addch(y, x, '#')
        stdscr.addstr(sy - 1, 0, 'Time is {} seconds'.format(t))
        stdscr.refresh()
        kp = stdscr.getch()

curses.wrapper(draw)
