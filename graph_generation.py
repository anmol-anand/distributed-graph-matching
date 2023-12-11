import random

class Graph:
    def __init__(self, num_nodes, num_edges):
        self.num_nodes = num_nodes
        self.edges = []
        adjacency_matrix = [[False for _ in range(num_nodes)] for _ in range(num_nodes)]
        while len(self.edges) < num_edges:
            while True:
                u = random.randint(0, num_nodes - 1)
                v = random.randint(0, num_nodes - 1)
                if u == v or adjacency_matrix[u][v]:
                    continue
                adjacency_matrix[u][v] = True
                adjacency_matrix[v][u] = True
                self.edges.append([u, v])
                break
        del adjacency_matrix

    def get_title(self):
        return f'Graph G(V, E): |V|={self.num_nodes}, |E|={self.get_num_edges()}'

    def get_num_nodes(self):
        return self.num_nodes

    def get_num_edges(self):
        return len(self.edges)

    def get_edges(self):
        return self.edges