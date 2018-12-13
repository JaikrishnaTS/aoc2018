#!/usr/bin/env python3

import sys
import re
import itertools

test_inp = len(sys.argv) > 1 and sys.argv[1] == '-t'
dayn = re.match(r'.*day(\d+)\.py', sys.argv[0]).group(1)
input_filename = 'inp' + dayn + ('_' if test_inp else '') + '.txt'

"""
- Horz
| Vert
\/ Turn - will say how to turn
+ Int

v^<> Cart
    props: dir, turn
"""
cartdir = {'^': 0, '>': 1, 'v': 2, '<': 3}

class Cart:
    __slots__ = 'pos', 'dir', 'crashed', 'turn'
    def __init__(self, pos, direction):
        self.pos = pos
        self.dir = direction
        self.turn = 0
        self.crashed = False

    def move(self):
        x, y = self.pos
        curr = mat[x][y]
        if curr == '-' or curr == '|':
            pass
        elif curr == '\\':
            if self.dir % 2 == 0:  # up or down
                self.dir = (self.dir - 1) % 4
            else:
                self.dir = (self.dir + 1) % 4
        elif curr == '/':
            if self.dir % 2 == 0:  # up or down
                self.dir = (self.dir + 1) % 4
            else:
                self.dir = (self.dir - 1) % 4
        elif curr == '+':
            if self.turn == 0:  # left
                self.dir = (self.dir - 1) % 4
            elif self.turn == 1:  # straight
                pass
            elif self.turn == 2:  # right
                self.dir = (self.dir + 1) % 4
            self.turn = (self.turn + 1) % 3
        else:
            raise ValueError(self)
        self.forward()

    def forward(self):  # move in the specified direction, one grid
        x, y = self.pos
        if self.dir == 0:
            self.pos = (x - 1, y)
        elif self.dir == 1:
            self.pos = (x, y + 1)
        elif self.dir == 2:
            self.pos = (x + 1, y)
        elif self.dir == 3:
            self.pos = (x, y - 1)
        else:
            raise ValueError("unknown dir", self)

    def __lt__(self, other):
        return self.pos < other.pos

    def __le__(self, other):
        return self.pos <= other.pos

    def __gt__(self, other):
        return self.pos > other.pos

    def __ge__(self, other):
        return self.pos >= other.pos

    def __eq__(self, other):
        return self.pos == other.pos

    def __ne__(self, other):
        return self.pos != other.pos

    def __repr__(self):
        return '<Cart {}: {} {}>'.format(self.pos, self.dir, self.turn)


mat = []
carts = []
with open(input_filename) as f:
    repdir = {'^': '|', '>': '-', 'v': '|', '<': '-'}
    for x, line in enumerate(f):
        line = list(line)
        assert line.pop() == '\n'
        for i in range(len(line)):
            if line[i] in cartdir:
                cdir = cartdir[line[i]]
                carts.append(Cart((x, i), cdir))
                line[i] = repdir[line[i]]
        mat.append(''.join(line))

if test_inp:
    for l in mat:
        print(l)
else:
    assert len(carts) % 2

currpos = {cart.pos: cart for cart in carts}

for tick in itertools.count():
    carts.sort()  # Top to bottom, left to right
    crash = False
    for cart in carts:
        if cart.crashed:
            continue
        currpos.pop(cart.pos)
        cart.move()
        if cart.pos in currpos:
            print("Crash at", cart.pos)
            crash = True
            cart.crashed = True
            # if 3rd collision were to happen here in same tick, prevent
            currpos.pop(cart.pos).crashed = True
        else:
            currpos[cart.pos] = cart
    if crash:  # if we crashed, remove those
        carts = [cart for cart in carts if not cart.crashed]
        if len(carts) == 1:
            print('Remaining:', carts[0].pos)
            break
