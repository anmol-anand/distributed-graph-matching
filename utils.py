import os
import matplotlib.pyplot as plt

RESULTS_DIR = 'results'

colors = ['red', 'green', 'blue', 'purple', 'orange', 'brown']

def create_plot(epsilon_values, num_machines_list, latencies_for_epsilon_values, graph):
    for e in range(len(epsilon_values)):
        plt.plot(num_machines_list, latencies_for_epsilon_values[e], marker='o',
                linestyle='-', color=colors[e], label=f'epsilon={epsilon_values[e]}')
    plt.title(graph.get_title())
    plt.xlabel('Number of machines')
    plt.ylabel('Latency')
    plt.legend()
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)
    plt.savefig(f'{RESULTS_DIR}/V_{str(graph.get_num_nodes())}_E_{str(graph.get_num_edges())}.png')
    plt.show()