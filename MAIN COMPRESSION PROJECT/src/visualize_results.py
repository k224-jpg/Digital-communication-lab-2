#  THIS SCRIPT
#  - Compares Huffman (blocked) and Arithmetic Coding results
#  - Plots compression efficiency, entropy vs avg length, etc.

import matplotlib.pyplot as plt
import numpy as np
import os


# Step 1: Defining the recorded results for the Bernoulli Sequence

methods = ["Huffman-2", "Huffman-3", "Huffman-4", "Arithmetic"]

# Entropy (bits/symbol)
entropy_vals = [0.8636, 0.8639, 0.8562, 0.8661]

# Average code length (bits/symbol)
avg_code_len = [0.8750, 0.8902, 0.8620, 0.8661]

# Compression efficiency (%)
efficiency = [98.70, 97.04, 99.33, 100.00]

# Original and compressed bit lengths
original_bits = [1000, 1002, 1000, 1000]
compressed_bits = [875, 892, 862, 866.12]


# Step 2: Preparing output directory

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
results_dir = os.path.join(base_dir, "results")
os.makedirs(results_dir, exist_ok=True)


# Step 3: Ploting Compression Efficiency

plt.figure(figsize=(7, 4))
plt.bar(methods, efficiency, color=["#6baed6", "#9ecae1", "#4292c6", "#2171b5"])
plt.title("Compression Efficiency: Huffman vs Arithmetic")
plt.ylabel("Efficiency (%)")
plt.ylim(90, 102)
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig(os.path.join(results_dir, "efficiency_comparison.png"))
plt.close()


# Step 4: Ploting Entropy vs Average Code Length

x = np.arange(len(methods))
width = 0.35
plt.figure(figsize=(7, 4))
plt.bar(x - width/2, entropy_vals, width, label="Entropy", color="#74c476")
plt.bar(x + width/2, avg_code_len, width, label="Avg Code Length", color="#238b45")
plt.xticks(x, methods)
plt.ylabel("Bits per Symbol")
plt.title("Entropy vs Average Code Length per Symbol")
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig(os.path.join(results_dir, "entropy_vs_avglen.png"))
plt.close()


# Step 5: Ploting Block Size vs Efficiency (Huffman only)

block_sizes = [2, 3, 4]
huffman_eff = efficiency[:3]

plt.figure(figsize=(7, 4))
plt.plot(block_sizes, huffman_eff, marker="o", color="#08519c", linewidth=2)
plt.title("Effect of Block Size on Huffman Compression Efficiency")
plt.xlabel("Block Size")
plt.ylabel("Efficiency (%)")
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig(os.path.join(results_dir, "blocksize_efficiency.png"))
plt.close()


# Step 6: Ploting Original vs Compressed Bit Lengths

x = np.arange(len(methods))
plt.figure(figsize=(7, 4))
plt.bar(x - width/2, original_bits, width, label="Original", color="#fdae6b")
plt.bar(x + width/2, compressed_bits, width, label="Compressed", color="#e6550d")
plt.xticks(x, methods)
plt.ylabel("Bit Length")
plt.title("Original vs Compressed Bit Lengths")
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig(os.path.join(results_dir, "bitlength_comparison.png"))
plt.close()


# Done

print("\nAll comparison plots have been generated and saved to:")
print(results_dir)