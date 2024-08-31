class EdgeCounter:
    def __init__(self):
        self.counts = {}
        self.max_edge = None
        self.max_count = 0

    def increment(self, edge):
        if edge not in self.counts:
            self.counts[edge] = 0
        self.counts[edge] += 1

        if self.counts[edge] > self.max_count:
            self.max_edge = edge
            self.max_count = self.counts[edge]

    def get_max_edge(self):
        return self.max_edge

class EdgeMatrix:
    def __init__(self):
        self.edge_matrix = {}

    def update_edge(self, start, end, path):
        if start not in self.edge_matrix:
            self.edge_matrix[start] = {}
        if end not in self.edge_matrix[start]:
            self.edge_matrix[start][end] = EdgeCounter()

        for edge in path[1:-1]:
            self.edge_matrix[start][end].increment(edge)

    def get_most_frequent_edge(self, start, end):
        if start in self.edge_matrix and end in self.edge_matrix[start]:
            return self.edge_matrix[start][end].get_max_edge()
        return None
    
    def to_dict (self):
        edge_matrix_dict = {}
        for start, ends in self.edge_matrix.items():
            edge_matrix_dict[start] = {}
            for end, edge_counter in ends.items():
                max_edge = edge_counter.get_max_edge()
                if max_edge is not None:
                    edge_matrix_dict[start][end] = max_edge
                else:
                    edge_matrix_dict[start][end] = None
        return edge_matrix_dict

