class FibonacciHeapNode:
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.parent = None
        self.child = None
        self.left = self
        self.right = self
        self.marked = False

class FibonacciHeap:
    def __init__(self):
        self.min_node = None
        self.num_nodes = 0

    def insert(self, key):
        new_node = FibonacciHeapNode(key)
        if self.min_node:
            new_node.left = self.min_node
            new_node.right = self.min_node.right
            self.min_node.right = new_node
            new_node.right.left = new_node
            if key < self.min_node.key:
                self.min_node = new_node
        else:
            self.min_node = new_node
        self.num_nodes += 1

    def minimum(self):
        return self.min_node.key if self.min_node else None

    def union(self, other_heap):
        if other_heap.min_node:
            if self.min_node:
                self.min_node.right.left = other_heap.min_node.left
                other_heap.min_node.left.right = self.min_node.right
                self.min_node.right = other_heap.min_node
                other_heap.min_node.left = self.min_node
                if other_heap.min_node.key < self.min_node.key:
                    self.min_node = other_heap.min_node
            else:
                self.min_node = other_heap.min_node
        self.num_nodes += other_heap.num_nodes

    def extract_min(self):
        min_node = self.min_node
        if min_node:
            if min_node.child:
                children = [x for x in self.iterate_nodes(min_node.child)]
                for child in children:
                    child.parent = None
                    child.left = min_node.left
                    child.right = min_node.right
                    min_node.right.left = child
                    min_node.left.right = child
                min_node.child = None
            min_node.left.right = min_node.right
            min_node.right.left = min_node.left
            if min_node == min_node.right:
                self.min_node = None
            else:
                self.min_node = min_node.right
                self.consolidate()
            self.num_nodes -= 1
        return min_node.key if min_node else None

    def consolidate(self):
        degree_table = [None] * self.num_nodes
        nodes = [x for x in self.iterate_nodes(self.min_node)]
        for node in nodes:
            degree = node.degree
            while degree_table[degree]:
                other = degree_table[degree]
                if node.key > other.key:
                    node, other = other, node
                self.link(other, node)
                degree_table[degree] = None
                degree += 1
            degree_table[degree] = node
        self.min_node = None
        for node in degree_table:
            if node:
                if self.min_node:
                    node.left = self.min_node.left
                    node.right = self.min_node
                    self.min_node.left.right = node
                    self.min_node.left = node
                    if node.key < self.min_node.key:
                        self.min_node = node
                else:
                    self.min_node = node

    def link(self, child, parent):
        child.left.right = child.right
        child.right.left = child.left
        child.parent = parent
        if parent.child:
            child.right = parent.child
            child.left = parent.child.left
            parent.child.left.right = child
            parent.child.left = child
        else:
            parent.child = child
            child.right = child
            child.left = child
        parent.degree += 1
        child.marked = False

    def decrease_key(self, node, new_key):
        if new_key > node.key:
            raise ValueError("New key is greater than current key")
        node.key = new_key
        parent = node.parent
        if parent and node.key < parent.key:
            self.cut(node, parent)
            self.cascading_cut(parent)
        if node.key < self.min_node.key:
            self.min_node = node

    def cut(self, child, parent):
        if child == child.right:
            parent.child = None
        else:
            child.right.left = child.left
            child.left.right = child.right
            if parent.child == child:
                parent.child = child.right
        parent.degree -= 1
        child.left = self.min_node
        child.right = self.min_node.right
        self.min_node.right.left = child
        self.min_node.right = child
        child.parent = None
        child.marked = False

    def cascading_cut(self, node):
        parent = node.parent
        if parent:
            if not node.marked:
                node.marked = True
            else:
                self.cut(node, parent)
                self.cascading_cut(parent)

    def delete(self, node):
        self.decrease_key(node, float('-inf'))
        self.extract_min()

    def iterate_nodes(self, start):
        current = start
        while True:
            yield current
            current = current.right
            if current == start:
                break

# Example Usage:
if __name__ == "__main__":
    heap = FibonacciHeap()
    heap.insert(5)
    heap.insert(3)
    heap.insert(7)
    heap.insert(2)
    heap.insert(9)
    print("Minimum:", heap.minimum())  # Output: Minimum: 2
    print("Extracted Minimum:", heap.extract_min())  # Output: Extracted Minimum: 2
    print("Minimum after extraction:", heap.minimum())  # Output: Minimum after extraction: 3
