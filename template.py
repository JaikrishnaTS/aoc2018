#!/usr/bin/env python3

import sys
import re

test_inp = len(sys.argv) > 1 and sys.argv[1] == '-t'
dayn = re.match(r'.*day(\d+)\.py', sys.argv[0]).group(1)
input_filename = 'inp' + dayn + ('_' if test_inp else '') + '.txt'

with open(input_filename) as f:
    nums = map(int, f.read().strip())
