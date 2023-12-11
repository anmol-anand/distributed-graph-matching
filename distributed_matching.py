import random
import time
import math

class SlaveMachine:
    def __init__(self, num_nodes, edges):
        self.edges = edges
        self.num_nodes = num_nodes

    def get_marked_edges(self, marking_probability):
        marked_edges = []
        for edge in self.edges:
            if random.random() < marking_probability:
                marked_edges.append(edge)
        return marked_edges
    
    def remove_edges_with_endpoints(self, nodes_to_remove):
        assert(len(nodes_to_remove) == self.num_nodes)
        new_edges = []
        for edge in self.edges:
            if nodes_to_remove[edge[0]] or nodes_to_remove[edge[1]]:
                continue
            new_edges.append(edge)
        self.edges = new_edges

    def get_num_edges(self):
        return len(self.edges)

    def has_edges(self):
        return self.get_num_edges > 0


class MasterMachine:
    def __init__(self, num_nodes, num_edges, degree_of_nodes):
        ################ The following variables remain constant througout the distributed algorithm ################

        self.num_nodes = num_nodes
        assert(len(degree_of_nodes) == num_nodes) # integer array
        self.degree_of_nodes = degree_of_nodes
        
        ################ The following variables need to be updated with each round ################
        
        self.marked_vertices = [False for _ in range(num_nodes)]
        self.maximal_matching = [] # Final result: Edges in the maximal matching

    def update_matching(self, marked_edges):
        for edge in marked_edges:
            u = edge[0]
            v = edge[1]
            if (not self.marked_vertices[u]) and (not self.marked_vertices[v]):
                self.marked_vertices[u] = True
                self.marked_vertices[v] = True
                self.maximal_matching.append(edge)

    def get_marked_vertices(self):
        return self.marked_vertices

    def get_maximal_matching(self):
        return self.maximal_matching


class DistributedMatchingDriver:
    def __init__(self, graph, num_machines, epsilon):

        self.eta = pow(graph.get_num_nodes(), 1 + epsilon)
        self.graph = graph

        ################ Initializing master machine ################
        degree_of_nodes = [0 for _ in range(graph.get_num_nodes())]
        for edge in graph.get_edges():
            u = edge[0]
            v = edge[1]
            degree_of_nodes[u] = degree_of_nodes[u] + 1
            degree_of_nodes[v] = degree_of_nodes[v] + 1
        self.master_machine = MasterMachine(graph.get_num_nodes(), graph.get_num_edges(), degree_of_nodes)
        self.total_master_latency = 0

        ################ Initializing slave machines ################
        edges = graph.get_edges()
        num_edges = graph.get_num_edges()
        num_edges_per_machine = math.ceil(num_edges / float(num_machines))
        self.slave_machines = []
        for i in range(0, num_machines):
            slave_machine_edges = edges[(i * num_edges_per_machine) : min((i + 1) * num_edges_per_machine, num_edges)]
            self.slave_machines.append(SlaveMachine(graph.get_num_nodes(), slave_machine_edges))
        self.total_slave_latency = 0

        ################ Run distributed matching algorithm ################
        print(f'\n\n\nRunning distributed matching for {graph.get_title()} || #machines: {num_machines} || epsilon: {epsilon}')
        self.run()
        print('\n\n\n')

    def run(self):
        while True:

            num_remaining_edges = sum(slave_machine.get_num_edges() for slave_machine in self.slave_machines)
            if(num_remaining_edges == 0):
                break
            print(f'Number of remaining edges: {num_remaining_edges}')
            marking_probability = self.eta / 2.0 / num_remaining_edges
            print(f'********************** Marking probability: {marking_probability} **********************')

            aggregated_marked_edges = []
            max_slave_latency = 0
            for slave_machine in self.slave_machines:
                start_time = time.time()
                marked_edges = slave_machine.get_marked_edges(marking_probability)
                aggregated_marked_edges.extend(marked_edges)
                end_time = time.time()
                max_slave_latency = max(max_slave_latency, end_time - start_time)
            self.total_slave_latency = self.total_slave_latency + max_slave_latency

            start_time = time.time()
            self.master_machine.update_matching(aggregated_marked_edges)
            latest_marked_vertices = self.master_machine.get_marked_vertices()
            end_time = time.time()
            self.total_master_latency = self.total_master_latency + end_time - start_time

            max_slave_latency = 0
            for slave_machine in self.slave_machines:
                start_time = time.time()
                slave_machine.remove_edges_with_endpoints(latest_marked_vertices)
                end_time = time.time()
                max_slave_latency = max(max_slave_latency, end_time - start_time)
            self.total_slave_latency = self.total_slave_latency + max_slave_latency
        
        assert_maximal_matching(self.graph, self.master_machine.get_maximal_matching())

    def get_latency(self):
        return self.total_master_latency + self.total_slave_latency

def assert_maximal_matching(graph, maximal_matching):
    num_nodes = graph.get_num_nodes()
    num_edges = graph.get_num_edges()
    marked_vertices = [False for _ in range(num_nodes)]
    # Checking if it is a valid matching
    for edge in maximal_matching:
        u = edge[0]
        v = edge[1]
        assert(not marked_vertices[u])
        assert(not marked_vertices[v])
        marked_vertices[u] = True
        marked_vertices[v] = True
    # Checking if the matching is maximal
    for edge in graph.get_edges():
        u = edge[0]
        v = edge[1]
        assert(marked_vertices[u] or marked_vertices[v])
        
