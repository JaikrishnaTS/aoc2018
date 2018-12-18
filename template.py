#!/usr/bin/env python3

import sys
import re

if len(sys.argv) > 1:
    input_filename = sys.argv[1]
else:
    dayn = re.match(r'.*day(\d+)\.py', sys.argv[0]).group(1)
    input_filename = 'inp' + dayn + '.txt'

with open(input_filename) as f:
    for line in f:
        pass
