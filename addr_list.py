class conn_node:

    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr

    def __str__(self):
        return self.addr[0]

    def __eq__(self, other):
        return self.conn == other.conn or \
                self.addr == other.addr

class conn_list:

    def __init__(self, contents=None):
        self.num_items = 0
        if contents is None:
            self.contents = []
        else:
            self.contents = contents

    def __repr__(self):
        return self.contents

    def get_conn_index(self, node):
        for counter in self.contents:
            if node == self.contents[counter]:
                return counter
        return -1

    def get_conn_node(self, addr):
        return self.contents[self.get_conn_index(conn_node(None, addr))]

    def insert(self, conn, addr):
        self.contents.append(conn_node(conn, addr))
        self.num_items += 1

    def delete(self, node):
        self.contents.pop(self.get_conn_index(node))
        self.num_items -= 1

    def get_size(self):
        return self.num_items