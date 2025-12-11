import numpy as np
import matplotlib.pyplot as plt


inputfile = "11/input.txt"

with open(inputfile) as f:
    data = f.read().strip().splitlines()

graph = {}

for i, line in enumerate(data):
    source, children = line.split(": ")
    source = source.strip()
    children = [c.strip() for c in children.split(" ")]
    graph[source] = children


# build a connection matrix from graph
basis = list(graph.keys()) + [
    child for children in graph.values() for child in children
]
basis = list(set(basis))
basis.sort()
index = {b: i for i, b in enumerate(basis)}
n = len(basis)
conn = np.zeros((n, n), dtype=int)
for source, children in graph.items():
    for child in children:
        conn[index[source], index[child]] = 1

plt.imshow(conn, cmap="Greys_r", interpolation="nearest")
plt.xticks(ticks=np.arange(n), labels=basis, rotation=90)
plt.yticks(ticks=np.arange(n), labels=basis)
plt.tight_layout()
plt.savefig("11/connection_matrix.png")

# find number of paths from start to end with matrix exponentiation
start_a = (
    "you" if "you" in basis else "svr"
)  # this is just so it does not fail on test2 input
end_a = "out"
start_idx_a = index[start_a]
end_idx_a = index[end_a]
count_paths_a = 0

# B
idx_svr = index["svr"]
idx_dac = index["dac"]
idx_fft = index["fft"]
idx_out = index["out"]

count_paths_svr_to_dac = 0
count_paths_dac_to_out = 0
count_paths_dac_to_fft = 0

count_paths_svr_to_fft = 0
count_paths_fft_to_out = 0
count_paths_fft_to_dac = 0


conn_exp = conn.copy()
while np.any(conn_exp > 0):
    conn_exp = conn_exp @ conn
    count_paths_a += conn_exp[start_idx_a, end_idx_a]

    count_paths_svr_to_dac += conn_exp[idx_svr, idx_dac]
    count_paths_dac_to_out += conn_exp[idx_dac, idx_out]
    count_paths_dac_to_fft += conn_exp[idx_dac, idx_fft]
    count_paths_svr_to_fft += conn_exp[idx_svr, idx_fft]
    count_paths_fft_to_out += conn_exp[idx_fft, idx_out]
    count_paths_fft_to_dac += conn_exp[idx_fft, idx_dac]

print("A) ", count_paths_a)

# paths from svr to out via dac and fft
total_paths_b = (
    count_paths_svr_to_dac * count_paths_dac_to_fft * count_paths_fft_to_out
    + count_paths_svr_to_fft * count_paths_fft_to_dac * count_paths_dac_to_out
)
print("B) ", total_paths_b)
