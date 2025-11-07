import os
import math
from collections import Counter
import heapq


# Build Huffman tree

class Node:
    def __init__(self, symbol=None, prob=0):
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
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        new_node = Node(prob=left.prob + right.prob)
        new_node.left, new_node.right = left, right
        heapq.heappush(heap, new_node)

    return heap[0]


def generate_codes(node, prefix="", codebook={}):
    if node is None:
        return
    if node.symbol is not None:
        codebook[node.symbol] = prefix
    generate_codes(node.left, prefix + "0", codebook)
    generate_codes(node.right, prefix + "1", codebook)
    return codebook



# 1. Load the generated Bernoulli sequence

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_file = os.path.join(base_dir, "data", "bernoulli_bits.txt")

with open(data_file, "r") as f:
    sequence = [int(line.strip()) for line in f.readlines() if line.strip() != ""]

total = len(sequence)
counts = Counter(sequence)
probs = {k: v / total for k, v in counts.items()}

print("\n--- HUFFMAN COMPRESSION (no blocks) ---")
print(f"Sequence length: {total}")
for k, v in probs.items():
    print(f"Symbol {k}: p={v:.4f}")


# 2. Build Huffman codes

root = build_huffman_tree(probs)
codes = generate_codes(root)

print("\nHuffman codes:")
for sym, code in codes.items():
    print(f"  Symbol {sym}: {code} (len={len(code)})")


# 3. Encoding and Decoding

encoded = "".join(codes[b] for b in sequence)

reverse_codes = {v: k for k, v in codes.items()}

decoded = []
code = ""
for bit in encoded:
    code += bit
    if code in reverse_codes:
        decoded.append(reverse_codes[code])
        code = ""

decoded_ok = decoded == sequence


# 4. Entropy and efficiency

def entropy(p_list):
    return -sum(p * math.log2(p) for p in p_list if p > 0)

H = entropy(list(probs.values()))
avg_len = sum(probs[sym] * len(code) for sym, code in codes.items())
efficiency = (H / avg_len) * 100

print(f"\nEntropy: {H:.4f} bits per symbol")
print(f"Average code length: {avg_len:.4f} bits")
print(f"Compression efficiency: {efficiency:.2f}%")
print(f"Encoded bitstream length: {len(encoded)} bits")
print(f"Decoded matches original? {decoded_ok}")

# 5. Save results 

results_dir = os.path.join(base_dir, "results")
os.makedirs(results_dir, exist_ok=True)
out_file = os.path.join(results_dir, "huffman_basic.txt")

with open(out_file, "w") as f:
    f.write("--- HUFFMAN COMPRESSION (No Blocks) ---\n")
    f.write(f"Sequence length: {total}\n")
    for k, v in probs.items():
        f.write(f"Symbol {k}: p={v:.4f}\n")
    f.write("\nHuffman Codes:\n")
    for sym, code in codes.items():
        f.write(f"  Symbol {sym}: {code} (len={len(code)})\n")
    f.write("\nResults:\n")
    f.write(f"Entropy: {H:.4f} bits per symbol\n")
    f.write(f"Average code length: {avg_len:.4f} bits\n")
    f.write(f"Compression efficiency: {efficiency:.2f}%\n")
    f.write(f"Encoded bitstream length: {len(encoded)} bits\n")
    f.write(f"Decoded matches original? {decoded_ok}\n")

print(f"\nResults saved to: {out_file}")