
import os
import math
import heapq
from collections import Counter


# Step 1: Load the generated graph bit data

data_path = os.path.join(os.path.dirname(__file__), "..", "data", "graph_bits.txt")

if not os.path.exists(data_path):
    raise FileNotFoundError("Missing 'graph_bits.txt' in data/ folder. Run data generation first!")

with open(data_path, "r") as f:
    content = f.read().strip()
    bits = [int(c) for c in content if c in "01"]


# Step 2: Choose block size

block_size = 3   # <<< we'll change this to  3, then 4... to test different setups
total_bits = len(bits)
num_blocks = total_bits // block_size

# Trim any leftover bits that don't fill a block
bits = bits[: num_blocks * block_size]

# Grouping into blocks 
blocks = ["".join(map(str, bits[i:i+block_size])) for i in range(0, len(bits), block_size)]

print(f"\n--- BLOCKED HUFFMAN (Graph Data, block size={block_size}) ---")
print(f"Total bits: {total_bits}, Total blocks: {num_blocks}")


# Step 3: Computing block probabilities

counts = Counter(blocks)
total_blocks = len(blocks)
probs = {blk: counts[blk] / total_blocks for blk in counts}

def entropy(p_list):
    return -sum(p * math.log2(p) for p in p_list if p > 0)

H_block = entropy(list(probs.values()))
H_bit = H_block / block_size

print("\nBlock counts and probabilities:")
for blk, p in probs.items():
    print(f"  {blk}: count={counts[blk]}, p={p:.4f}")

print(f"\nEntropy per block: {H_block:.4f} bits")
print(f"Entropy per bit:   {H_bit:.4f} bits")


# Step 4: Build Huffman tree for blocks

class Node:
    def __init__(self, symbol=None, prob=None):
        self.symbol = symbol
        self.prob = prob
        self.left = None
        self.right = None
    def __lt__(self, other):
        return self.prob < other.prob

def build_tree(prob_dict):
    heap = [Node(sym, p) for sym, p in prob_dict.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        parent = Node(prob=a.prob + b.prob)
        parent.left = a
        parent.right = b
        heapq.heappush(heap, parent)
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

root = build_tree(probs)
codes = assign_codes(root)


# Step 5: Encoding and decoding

encoded = "".join(codes[b] for b in blocks)
code_to_block = {v: k for k, v in codes.items()}

# Decode
decoded_blocks = []
temp = ""
for bit in encoded:
    temp += bit
    if temp in code_to_block:
        decoded_blocks.append(code_to_block[temp])
        temp = ""

decoded_bits = [int(x) for block in decoded_blocks for x in block]
is_lossless = decoded_bits == bits


# Step 6: Stats

avg_len_block = sum(probs[b] * len(codes[b]) for b in codes)
avg_len_bit = avg_len_block / block_size
efficiency = (H_bit / avg_len_bit) * 100
encoded_len = len(encoded)


# Step 7: Display results

print("\nHuffman codes (per block):")
for blk, code in codes.items():
    print(f"  {blk}: {code} (len={len(code)})")

print(f"\nAverage code length per block: {avg_len_block:.4f} bits")
print(f"Average code length per bit:   {avg_len_bit:.4f} bits")
print(f"Compression efficiency: {efficiency:.2f}%")
print(f"Encoded bitstream length: {encoded_len} bits")
print(f"Original bit length: {total_bits} bits")
print(f"Decoded correctly? {is_lossless}")
