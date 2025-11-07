
from decimal import Decimal, getcontext
from collections import Counter
import math
import os

# High precision for arithmetic coding
getcontext().prec = 500


# Step 1: Load the generated Bernoulli sequence

data_path = os.path.join(os.path.dirname(__file__), "..", "data", "bernoulli_bits.txt")

if not os.path.exists(data_path):
    raise FileNotFoundError("Missing 'bernoulli_bits.txt' in data/ folder. Generate it first!")

with open(data_path, "r") as f:
    content = f.read().strip()
    sequence = [int(c) for c in content if c in "01"]

total = len(sequence)
counts = Counter(sequence)
p0 = counts[0] / total
p1 = counts[1] / total

print("\n--- ARITHMETIC CODING  ---")
print(f"Sequence length: {total}")
print(f"Symbol 0: p={p0:.4f}")
print(f"Symbol 1: p={p1:.4f}")


# Step 2: Computing entropy

def entropy(p_list):
    return -sum(p * math.log2(p) for p in p_list if p > 0)

H = entropy([p0, p1])
print(f"Entropy of source: {H:.4f} bits/symbol\n")


# Step 3: Defining cumulative probability intervals

intervals = {
    0: (Decimal('0.0'), Decimal(str(p0))),
    1: (Decimal(str(p0)), Decimal('1.0'))
}

print("Symbol intervals (like Huffman codes):")
for sym, (low_i, high_i) in intervals.items():
    print(f"  Symbol {sym}: [{low_i:.6f}, {high_i:.6f})")


# Step 4: Arithmetic encoding

low = Decimal('0.0')
high = Decimal('1.0')

for bit in sequence:
    range_width = high - low
    sym_low, sym_high = intervals[bit]
    high = low + range_width * sym_high
    low = low + range_width * sym_low

encoded_value = (low + high) / 2
width = float(high - low)
if width <= 0:
    width = 1e-300

encoded_bits_est = -math.log2(width)
avg_code_len = encoded_bits_est / total
efficiency = (H / avg_code_len) * 100


# Step 5: Arithmetic decoding

decoded = []
low_d, high_d = Decimal('0.0'), Decimal('1.0')
code = encoded_value

for _ in range(total):
    range_width = high_d - low_d
    scaled_value = (code - low_d) / range_width

    # Check which symbol interval the scaled value falls into
    if scaled_value < intervals[0][1]:
        bit = 0
    else:
        bit = 1

    decoded.append(bit)

    sym_low, sym_high = intervals[bit]
    high_d = low_d + range_width * sym_high
    low_d = low_d + range_width * sym_low

is_lossless = decoded == sequence


# Step 6: Display results

print(f"\nEncoded range: [{low}, {high})")
print(f"Encoded value: {encoded_value}")
print(f"Encoded range width: {float(high - low):.3e}")
print(f"Estimated encoded length: {encoded_bits_est:.2f} bits")
print(f"Average code length per bit: {avg_code_len:.4f} bits/symbol")
print(f"Compression efficiency: {efficiency:.2f}%")
print(f"Original bit length: {total} bits")
print(f"Decoded sequence equals original? {is_lossless}")