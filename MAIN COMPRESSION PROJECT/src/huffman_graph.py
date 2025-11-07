
import os
import math
from collections import Counter
import heapq


# Step 1: Load the generated Graph data

data_path = os.path.join(os.path.dirname(__file__), "..", "data", "graph_bits.txt")

if not os.path.exists(data_path):
    raise FileNotFoundError("Missing 'graph_bits.txt' in data/ folder. Run data generation first!")

with open(data_path, "r") as f:
    content = f.read().strip()
    sequence = [int(c) for c in content if c in "01"]

total = len(sequence)
counts = Counter(sequence)
p0 = counts[0] / total
p1 = counts[1] / total

print("\n--- HUFFMAN CODING (Graph Data) ---")
print(f"Sequence length: {total}")
print(f"Symbol 0: p={p0:.4f}")
print(f"Symbol 1: p={p1:.4f}")


# Step 2: Compute entropy

def entropy(p_list):
    return -sum(p * math.log2(p) for p in p_list if p > 0)

H = entropy([p0, p1])
print(f"Entropy of source: {H:.4f} bits/symbol\n")


# Step 3: Build Huffman tree

class Node:
    def __init__(self, symbol=None, prob=None):
        self.symbol = symbol
        self.prob = prob
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.prob < other.prob

def build_huffman_tree(prob_dict):
    heap = [Node(sym, p) for sym, p in prob_dict.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        new_node = Node(prob=a.prob + b.prob)
        new_node.left = a
        new_node.right = b
        heapq.heappush(heap, new_node)
    return heap[0]

def assign_codes(node, code="", codebook=None):
    if codebook is None:
        codebook = {}
    if node.symbol is not None:
        codebook[node.symbol] = code
    else:
        assign_codes(node.left, code + "0", codebook)
        assign_codes(node.right, code + "1", codebook)
    return codebook

probs = {0: p0, 1: p1}
root = build_huffman_tree(probs)
codes = assign_codes(root)


# Step 4: Encoding and decoding

encoded = "".join(codes[bit] for bit in sequence)
decoded = []
code_to_symbol = {v: k for k, v in codes.items()}

buffer = ""
for bit in encoded:
    buffer += bit
    if buffer in code_to_symbol:
        decoded.append(code_to_symbol[buffer])
        buffer = ""

is_lossless = decoded == sequence


# Step 5: Calculating statistics

avg_len = sum(len(codes[sym]) * probs[sym] for sym in probs)
efficiency = (H / avg_len) * 100
encoded_len = len(encoded)


# Step 6: Display results

print("Huffman Codes:")
for sym, code in codes.items():
    print(f"  Symbol {sym}: {code} (len={len(code)})")

print(f"\nEntropy: {H:.4f} bits/symbol")
print(f"Average code length: {avg_len:.4f} bits/symbol")
print(f"Compression efficiency: {efficiency:.2f}%")
print(f"Encoded bitstream length: {encoded_len} bits")
print(f"Original bit length: {total} bits")
print(f"Decoded sequence equals original? {is_lossless}")


# Step 7: Save results

results_dir = os.path.join(os.path.dirname(__file__), "..", "results")
os.makedirs(results_dir, exist_ok=True)
save_path = os.path.join(results_dir, "huffman_graph.txt")

with open(save_path, "w") as f:
    f.write("--- HUFFMAN CODING (Graph Data) ---\n")
    f.write(f"Sequence length: {total}\n")
    f.write(f"Symbol 0: p={p0:.4f}\n")
    f.write(f"Symbol 1: p={p1:.4f}\n\n")
    f.write("Huffman Codes:\n")
    for sym, code in codes.items():
        f.write(f"  Symbol {sym}: {code} (len={len(code)})\n")
    f.write(f"\nEntropy: {H:.4f} bits/symbol\n")
    f.write(f"Average code length: {avg_len:.4f} bits/symbol\n")
    f.write(f"Compression efficiency: {efficiency:.2f}%\n")
    f.write(f"Encoded bitstream length: {encoded_len} bits\n")
    f.write(f"Original bit length: {total} bits\n")
    f.write(f"Decoded sequence equals original? {is_lossless}\n")

print(f"\nResults saved to: {os.path.abspath(save_path)}")