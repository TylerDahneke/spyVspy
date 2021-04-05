class QueueNode:

    def __init__(self, data, prev=None, next=None):
        self.prev = prev
        self.next = next
        self.data = data

    def set_next(self, other):
        self.next = other
        other.prev = self

class Queue:

    def __init__(self, cap=50):
        self.first = self.last = None
        self.cap = cap
        self.num_items = 0

    def insert(self, data):
        if self.is_full():
            raise IndexError
        new_node = QueueNode(data)
        if self.is_empty():
            self.first = self.last = new_node
        else:
            self.last.set_next(new_node)
            self.last = new_node

    def pop(self):
        if not self.is_empty():
            ph = self.first.data
            self.first = self.first.next
            return ph

    def is_empty(self):
        return not self.num_items

    def is_full(self):
        return self.num_items == self.cap

    def get_size(self):
        return self.num_items
