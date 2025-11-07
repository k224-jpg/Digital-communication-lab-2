import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import os


np.random.seed(42)          # for reproducibility
bern_p = 0.3                # probability of 1 in Bernoulli sequence
bern_length = 1000          # sequence length
graph_n = 10                # number of nodes
graph_p = 0.3               # edge probability


# Ensuring that output directories exist

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_dir, "data")
results_dir = os.path.join(base_dir, "results")
os.makedirs(data_dir, exist_ok=True)
os.makedirs(results_dir, exist_ok=True)


# 1. Generating Bernoulli sequence

bernoulli_seq = np.random.binomial(1, bern_p, bern_length)
bern_file = os.path.join(data_dir, "bernoulli_bits.txt")
np.savetxt(bern_file, bernoulli_seq, fmt='%d')
print(f"Saved Bernoulli sequence to {bern_file} (length={bern_length}, p={bern_p})")


# 2. Generating Erdős–Rényi random graph

G = nx.erdos_renyi_graph(graph_n, graph_p)
adj_matrix = nx.to_numpy_array(G, dtype=int)

# Flattening the upper triangular part (no self-loops, avoid duplicates)
adj_bits = []
for i in range(graph_n):
    for j in range(i + 1, graph_n):
        adj_bits.append(int(adj_matrix[i, j]))

adj_file = os.path.join(data_dir, "graph_bits.txt")
np.savetxt(adj_file, adj_bits, fmt='%d')
print(f"Saved flattened adjacency bits to {adj_file} (nodes={graph_n}, p={graph_p})")


# 3. Visualizing and saving the graph

plt.figure(figsize=(5, 4))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color="skyblue", edge_color="gray", node_size=800)
plt.title(f"Erdős–Rényi G({graph_n}, {graph_p})")
graph_img = os.path.join(results_dir, "graph_plot.png")
plt.savefig(graph_img)
plt.close()
print(f"Graph visualization saved to {graph_img}")


# 4. Print summary

print("\n--- Data Generation Summary ---")
print(f"Bernoulli sequence: length={bern_length}, p={bern_p}")
print(f"Random graph: nodes={graph_n}, edge prob={graph_p}")
print(f"Adjacency bits count: {len(adj_bits)}")