#!/usr/bin/env python3

class Node:
    def __init__(self, num_child, meta_size):
        self.remaining_child = num_child
        self.meta_size = meta_size
        self.child = []
        self.meta = []

    @property
    def value(self):
        if not self.child:
            return sum(self.meta)
        return sum(self.child[m - 1].value
                   for m in self.meta
                   if 0 < m <= len(self.child))

    def __repr__(self):
        return '<' + str(len(self.child)) + ', M:' + str(self.meta) + '>'


with open('inp8_.txt') as f:
    nums = list(map(int, f.read().split()))

def get_meta_sum(node):
    return sum(node.meta) + sum(map(get_meta_sum, node.child))

root = Node(1, 0)
st = [root]
i = 0

while i < len(nums):
    if st[-1].remaining_child == 0:
        node = st.pop()
        node.meta = nums[i: i + node.meta_size]
        st[-1].child.append(node)
        st[-1].remaining_child -= 1
        i += node.meta_size
    else:
        st.append(Node(nums[i], nums[i + 1]))
        i += 2

assert len(st) == 1 and st[0] is root

print(get_meta_sum(root))
print(root.child[0].value)
