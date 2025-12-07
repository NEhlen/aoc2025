import numpy as np
from pathlib import Path

input_file = Path("07/input.txt")

with open(input_file) as f:
    data = f.read()
    data = data.split("\n")
    data = [line for line in data if line.strip()]
    data = np.array([[char for char in line.strip()] for line in data])
    sy, sx = np.where(data == "S")
    start_pos = (sx[0], sy[0])

grid = (data == "^").astype(int)
nrows, ncols = grid.shape
beams_to_check = [start_pos]
checked_beams = set()
splitters_hit = set()
num_splits = 0
while beams_to_check:
    x, y = beams_to_check.pop()
    checked_beams.add((x, y))
    if np.any(grid[y:, x] == 1):
        split_y = np.where(grid[y:, x] == 1)[0][0] + y
        splitters_hit.add((x, split_y))
        num_splits += 1
        if x + 1 < ncols:
            if (x + 1, split_y) not in checked_beams:
                beams_to_check.append((x + 1, split_y))
        if x > 0:
            if (x - 1, split_y) not in checked_beams:
                beams_to_check.append((x - 1, split_y))

print("A) ", len(splitters_hit))


##### PART B ####
# build a dag from the splitters, start at the start position
dag = {}
dag[start_pos] = [(start_pos[0], 2)]
for splitter in splitters_hit:
    x, y = splitter
    dag[splitter] = []
    # check down left
    for check_y in range(y + 1, nrows):
        if grid[check_y, x - 1] == 1:
            dag[splitter].append((x - 1, check_y))
            break
    # if no splitter found, connect to a terminal node at the bottom
    else:
        dag[splitter].append((x - 1, nrows))
    # check down right
    for check_y in range(y + 1, nrows):
        if grid[check_y, x + 1] == 1:
            dag[splitter].append((x + 1, check_y))
            break

    else:
        dag[splitter].append((x + 1, nrows))
# order dag by y position
ordered_nodes = sorted(dag.keys(), key=lambda pos: pos[1])
# plot graph with networkx
import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
for node, edges in dag.items():
    for edge in edges:
        G.add_edge(node, edge)
pos = {node: (node[0], -node[1] * 2000) for node in G.nodes()}

# topo_order = list(nx.topological_sort(G))
# node_labels = {node: str(i) for i, node in enumerate(topo_order)}
levels = nx.single_source_shortest_path_length(G, start_pos)
level_order = sorted(G.nodes(), key=lambda n: (levels.get(n, float("inf")), n[1], n[0]))
node_labels = {node: str(i) for i, node in enumerate(level_order)}
nx.draw(
    G,
    pos,
    node_size=100,
    linewidths=0.2,
    arrowsize=4,
    with_labels=True,
    labels=node_labels,
    font_size=6,
)

savename = input_file.parent / f"graph_{input_file.stem}.png"
plt.savefig(savename)
# plt.show()


def count_paths(dag, start):
    memo = {}

    # do a recursive depth first search with memoization
    def dfs(node):
        # put it in memo to avoid recalculating and cycles
        if node in memo:
            return memo[node]

        # get the children of the node
        children = dag.get(node, [])
        # if the node has no children, it is a terminal node
        # and thus has one path to output
        if not children:
            memo[node] = 1
        else:
            # recursively count the paths from the children
            memo[node] = sum(dfs(c) for c in children)
        return memo[node]

    return dfs(start), memo


num_paths, all_paths = count_paths(dag, start_pos)
print("B) ", num_paths)
