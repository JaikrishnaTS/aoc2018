#!/usr/bin/env python3

def chocolate_charts(N):
    N += 10
    rec = [3, 7]
    a, b = 0, 1  # curr recipes
    while len(rec) < N:
        n = rec[a] + rec[b]
        if n >= 10:
            rec.append(1)
            n -= 10
        rec.append(n)
        a = (a + 1 + rec[a]) % len(rec)
        b = (b + 1 + rec[b]) % len(rec)
    return ''.join(map(str, rec[N-10:N]))

def chocolate_charts_search(pattern):
    pattern = list(map(int, pattern))
    plast = pattern[-1]
    P = len(pattern)
    rec = [3, 7]
    a, b = 0, 1  # curr recipes
    while True:
        n = rec[a] + rec[b]
        if n >= 10:
            rec.append(1)
            if plast == 1 and rec[-P:] == pattern:
                return len(rec) - P
            n -= 10
        rec.append(n)
        if plast == n and rec[-P:] == pattern:
            return len(rec) - P
        a = (a + 1 + rec[a]) % len(rec)
        b = (b + 1 + rec[b]) % len(rec)
    return ''.join(map(str, rec[N-10:N]))

