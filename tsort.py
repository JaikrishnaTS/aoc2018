#!/usr/bin/env python3

import heapq

def tsort(deplist, N):
    indegree = [0] * N
    unblocks = [ [] for _ in range(N) ]
    # list of X must be done before Y
    for dep, node in deplist:
        indegree[node] += 1
        unblocks[dep].append(node)
    unblocked = []
    result = []
    for i, d in enumerate(indegree):
        if d == 0:
            heapq.heappush(unblocked, i)
    while unblocked:
        rm = heapq.heappop(unblocked)
        result.append(rm)
        for d in unblocks[rm]:
            indegree[d] -= 1
            if indegree[d] == 0:
                heapq.heappush(unblocked, d)
    if len(result) != N:
        raise ValueError("Acyclic graph")
    return result


def calculate_time(deplist, N, num_workers):
    indegree = [0] * N
    unblocks = [ [] for _ in range(N) ]
    # list of X must be done before Y
    for dep, node in deplist:
        indegree[node] += 1
        unblocks[dep].append(node)

    # Find seeds to start with (0 indegree)
    todo = []
    for i, d in enumerate(indegree):
        if d == 0:
            heapq.heappush(todo, i)

    # allocate workers for initial seeds
    workers = []
    while todo and len(workers) < num_workers:
        rm = heapq.heappop(todo)
        heapq.heappush(workers, [rm + 61, rm])  # time, node
    # rest remain in todo to be taken later

    total_time = 0
    while workers:  # while we have at least one item to work on
        time_spent, node = heapq.heappop(workers)  # node getting complete
        total_time += time_spent
        # decrease timer for currently processing tasks
        for i in range(len(workers)):
            workers[i][0] -= time_spent  # could make more things 0 (not -ve)
        # decrease inorder
        for d in unblocks[node]:
            indegree[d] -= 1
            if indegree[d] == 0:
                heapq.heappush(todo, d)
        # allocate jobs to workers when we have cores/workers
        while todo and len(workers) < num_workers:
            rm = heapq.heappop(todo)
            heapq.heappush(workers, [rm + 61, rm])
    return total_time

steps = []
symbols = set()

with open('inp7.txt') as f:
    for line in f:
        words = line.split()
        dep, node = ord(words[1]) - 65, ord(words[7]) - 65
        steps.append((dep, node))
        symbols.add(dep)
        symbols.add(node)

print(''.join(chr(x + 65) for x in tsort(steps, len(symbols))))
print(calculate_time(steps, len(symbols), 5))
