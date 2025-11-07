import os
import math
from collections import Counter
import heapq


# CONFIGURATION

block_size = 3  # <--- we'll change this to  3 then 4 later to compare


# Utility: Huffman tree

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



# Load the generated Bernoulli sequence

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_file = os.path.join(base_dir, "data", "bernoulli_bits.txt")

with open(data_file, "r") as f:
    bits = [int(line.strip()) for line in f.readlines() if line.strip() != ""]

# Pad if needed
while len(bits) % block_size != 0:
    bits.append(0)

# Group into blocks
blocks = ["".join(str(x) for x in bits[i:i+block_size])
          for i in range(0, len(bits), block_size)]

total_blocks = len(blocks)
counts = Counter(blocks)
probs = {b: counts[b] / total_blocks for b in counts}

print(f"\n--- BLOCKED HUFFMAN (block size={block_size}) ---")
print(f"Total bits: {len(bits)}, Total blocks: {total_blocks}")


# Build Huffman codes

root = build_huffman_tree(probs)
codes = generate_codes(root)

print("\nHuffman codes:")
for b, c in codes.items():
    print(f"  Block {b}: {c} (len={len(c)})")


# Encoding & Decoding

encoded = "".join(codes[b] for b in blocks)
reverse = {v: k for k, v in codes.items()}

decoded_blocks = []
temp = ""
for bit in encoded:
    temp += bit
    if temp in reverse:
        decoded_blocks.append(reverse[temp])
        temp = ""

decoded_bits = [int(b) for blk in decoded_blocks for b in blk]
decoded_ok = decoded_bits[:len(bits)] == bits


# Entropy and efficiency

def entropy(p_list):
    return -sum(p * math.log2(p) for p in p_list if p > 0)

H_block = entropy(list(probs.values()))
H_bit = H_block / block_size
avg_len_block = sum(probs[b] * len(codes[b]) for b in codes)
avg_len_bit = avg_len_block / block_size
efficiency = (H_bit / avg_len_bit) * 100

print(f"\nEntropy per block: {H_block:.4f} bits")
print(f"Entropy per bit:   {H_bit:.4f} bits")
print(f"Average code length per block: {avg_len_block:.4f} bits")
print(f"Average code length per bit:   {avg_len_bit:.4f} bits")
print(f"Compression efficiency: {efficiency:.2f}%")
print(f"Decoded correctly? {decoded_ok}")
encoded_len = len(encoded)
original_len = len(bits)
print(f"Encoded bitstream length: {encoded_len} bits")
print(f"Original bit length: {original_len} bits")
