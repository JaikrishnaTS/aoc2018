#!/usr/bin/env python3

import json
import sys
import re

test_inp = len(sys.argv) > 1 and sys.argv[1] == '-t'
dayn = re.match(r'.*day(\d+)\.py', sys.argv[0]).group(1)
input_filename = 'inp' + dayn + ('_' if test_inp else '') + '.txt'

"""
4 registers 0-3
16 OPs
Instruction: opcode inputA inputB outputC

"value A" -> immediate
register A -> read from reg no

addr  A  B  C
addi  A 'B' C
mulr
muli
banr
bani
borr
bori
setr  A  -  C
seti 'A' -  C
gtir 'A' B  C
gtri  A 'B' C
gtrr  A  B  C
eqir
eqri
eqrr
"""
samples = []
program = []
sample_mode = True
before_str, after_str = 'Before: ', 'After:  '
with open(input_filename) as f:
    for line in f:
        if sample_mode:
            if line.startswith(before_str):
                batch = [None, json.loads(line[len(before_str):]), None]
            elif line.startswith(after_str):
                batch[2] = json.loads(line[len(after_str):])
                assert all(batch)
                samples.append(batch)
            elif line[0].isdigit():
                batch[0] = list(map(int, line.split()))
            elif line.startswith('---'):
                sample_mode = False
        else:
            program.append(list(map(int, line.split())))

print('Number of samples:', len(samples))
print('Instructions in program:', len(program))

# Operations
def addr(reg, a, b):
    return reg[a] + reg[b]

def addi(reg, a, b):
    return reg[a] + b

def mulr(reg, a, b):
    return reg[a] * reg[b]

def muli(reg, a, b):
    return reg[a] * b

def banr(reg, a, b):
    return reg[a] & reg[b]

def bani(reg, a, b):
    return reg[a] & b

def borr(reg, a, b):
    return reg[a] | reg[b]

def bori(reg, a, b):
    return reg[a] | b

def setr(reg, a, b):
    return reg[a]

def seti(reg, a, b):
    return a

def gtir(reg, a, b):
    return 1 if (a > reg[b]) else 0

def gtri(reg, a, b):
    return 1 if (reg[a] > b) else 0

def gtrr(reg, a, b):
    return 1 if (reg[a] > reg[b]) else 0

def eqir(reg, a, b):
    return 1 if (a == reg[b]) else 0

def eqri(reg, a, b):
    return 1 if (reg[a] == b) else 0

def eqrr(reg, a, b):
    return 1 if (reg[a] == reg[b]) else 0

operations = (addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir,
              gtri, gtrr, eqir, eqri, eqrr)
assert len(operations) == 16

def check_match(inst, reg_before, reg_after):
    # Check and return operations which match the register states
    op, a, b, c = inst
    for i in range(4):
        if reg_before[i] != reg_after[i]:
            assert i == c
    ans = reg_after[c]  # result of operation
    return set(opid for opid, op in enumerate(operations)
               if op(reg_before, a, b) == ans)

count = 0  # count of samples matching >= 3 insts
# candidates for each instruction in their order
candidates = [set(range(16)) for _ in range(16)]

for inst, reg_before, reg_after in samples:
    match_inst = check_match(inst, reg_before, reg_after)
    if len(match_inst) >= 3:
        count += 1
    candidates[inst[0]].intersection_update(match_inst)
print('PartA:', count)

# translation index from their index to our function
opfunc = [None] * 16
while not all(opfunc):
    for i, c in enumerate(candidates):
        if len(c) == 1:
            g = c.pop()
            opfunc[i] = operations[g]
            for x in candidates:
                x.discard(g)

# execute test program
curr_reg = [0, 0, 0, 0]
for op, a, b, c in program:
    curr_reg[c] = opfunc[op](curr_reg, a, b)
print('PartB result:', curr_reg)
