#!/usr/bin/env python3

import datetime
import operator

from collections import defaultdict, Counter

TM_FORMAT = '[%Y-%m-%d %H:%M]'
TM_LEN, TM_LEN_1 = 18, 19
inp = []

with open('inp4.txt') as f:
    for line in f:
        tm = datetime.datetime.strptime(line[:TM_LEN], TM_FORMAT)
        actions = line[TM_LEN_1:].split()
        inp.append((tm, actions[1]))

inp.sort(key=operator.itemgetter(0))

guard_sleep = defaultdict(datetime.timedelta)
max_guard_minute = defaultdict(Counter)
sleeptime = None
guardid = None

for tm, action in inp:
    if action[0] == '#':  # new guard
        guardid = action
    elif action == 'asleep':
        sleeptime = tm
    elif action == 'up':
        guard_sleep[guardid] += (tm - sleeptime)
        max_guard_minute[guardid].update(range(sleeptime.minute, tm.minute))
    else:
        raise ValueError(action)

max_sleep = max(guard_sleep.keys(), key=guard_sleep.get)
print('The guard that slept most', max_sleep, guard_sleep[max_sleep])
print('Slept commonly with (min, freq):', max_guard_minute[max_sleep].most_common(1))

same_min_guard = max(max_guard_minute.keys(), 
                     key=lambda x:max_guard_minute[x].most_common(1)[0][1])
print('The guard that slept most often in same minute:', same_min_guard)
print('The (min, freq):', max_guard_minute[same_min_guard].most_common(1))
