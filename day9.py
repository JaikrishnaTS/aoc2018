#!/usr/bin/env python3

class Node:
    def __init__(self, label):
        self.label = label
        self.next = None
        self.prev = None

    def __repr__(self):
        return '<' + str(self.label) + '>'

def print_this(head):
    node = head
    print(node, end=' ')
    node = node.next
    while node is not head:
        print(node, end=' ')
        node = node.next
    print()

def remove_7_cc(node):
    for _ in range(7):
        node = node.prev
    before, rm, after = node.prev, node, node.next
    before.next = after
    after.prev = before
    return rm.label, after

def marble_circles(num_players, last_marble):
    score = [0] * num_players
    zerom = Node(0)
    zerom.next = zerom.prev = zerom
    current = zerom
    for m in range(1, last_marble + 1):
        if m % 23 == 0:
            player = (m - 1) % num_players
            add_sc, current = remove_7_cc(current)
            score[player] += m + add_sc
        else:
            current = current.next
            follow = current.next
            new_current = Node(m)
            new_current.next = follow
            new_current.prev = current
            current.next = new_current
            follow.prev = new_current
            current = new_current
    return max(score), zerom
