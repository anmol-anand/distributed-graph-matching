from graph_generation import Graph
from distributed_matching import DistributedMatchingDriver
from utils import create_plot

graphs = []
# graphs.append(Graph(num_nodes=1000, num_edges=5000))
# graphs.append(Graph(num_nodes=1000, num_edges=10000))
# graphs.append(Graph(num_nodes=1000, num_edges=20000))
graphs.append(Graph(num_nodes=1000, num_edges=50000))

epsilon_values = [0.01, 0.05, 0.1, 0.2, 0.5]

num_machines_list = [1, 2, 5, 10, 20, 50, 100]

for graph in graphs:
    latencies_for_epsilon_values = []
    for epsilon in epsilon_values: 
        latencies = []
        for num_machines in num_machines_list:
            matching = DistributedMatchingDriver(graph, num_machines, epsilon)
            latencies.append(matching.get_latency()) # Returns the runtime latency of distributed matching
        latencies_for_epsilon_values.append(latencies)
    create_plot(epsilon_values, num_machines_list, latencies_for_epsilon_values, graph)
