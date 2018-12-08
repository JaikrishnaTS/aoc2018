#!/usr/bin/env python3

"""
adjacent units of same type and opposite polarity -> destroyed
"""

with open('inp5.txt') as f:
    poly_input = f.read().strip()


def collapse_polymer(poly_stream):
    curr_poly = []
    for p in poly_stream:
        if curr_poly:  # if we have items in stack
            lp = curr_poly[-1]
            if (p.isupper() ^ lp.isupper()) and (p.swapcase() == lp):
                curr_poly.pop()
            else:
                curr_poly.append(p)
        else:  # no items in stack
            curr_poly.append(p)
    return len(curr_poly)

def part1():
    print(collapse_polymer(poly_input))

def part2():
    both_cases = lambda x: {x, x.swapcase()}
    print(min(collapse_polymer(p for p in poly_input if p not in to_rm)
             for to_rm in map(both_cases, map(chr, range(65, 91)))))

part2()
