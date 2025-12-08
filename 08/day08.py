import numpy as np

filename = "08/test.txt"
n_shortest_paths = 1000

with open(filename) as f:
    data = f.read()
    data = data.split("\n")
    data = [line for line in data if line.strip()]
    data = np.array([[int(num) for num in line.strip().split(",")] for line in data])

##### PART A #####
distance_matrix = np.full((data.shape[0], data.shape[0]), np.inf)
upper_triangle_indices = np.triu_indices(data.shape[0], k=0)
for i in range(data.shape[0]):
    for j in range(i + 1, data.shape[0]):
        if i != j:
            distance_matrix[i, j] = np.linalg.norm(data[i] - data[j])
            # distance_matrix[j, i] = distance_matrix[i, j]

connection_matrix = np.full(distance_matrix.shape, 0, dtype=int)

for _ in range(n_shortest_paths):
    shortest_path_idx = np.unravel_index(
        np.argmin(
            distance_matrix
            + connection_matrix
            * (np.amax(distance_matrix[distance_matrix < np.inf]) + 10)
        ),
        distance_matrix.shape,
    )
    connection_matrix[shortest_path_idx] = 1
    connection_matrix[(shortest_path_idx[1], shortest_path_idx[0])] = 1

# find connected components
visited = set()
n_components = 0
circuits = {}
for start_node in range(connection_matrix.shape[0]):
    if start_node not in visited:
        n_components += 1
        circuits[n_components] = {start_node}
        to_visit = [start_node]
        while to_visit:
            current_node = to_visit.pop()
            visited.add(current_node)
            neighbors = np.where(connection_matrix[current_node] == 1)[0]
            for neighbor in neighbors:
                if neighbor not in visited:
                    to_visit.append(neighbor)
                    circuits[n_components].add(neighbor)
size_circuits = [len(nodes) for nodes in circuits.values()]
# three largest circuits
size_circuits.sort(reverse=True)
print("Sizes of three largest circuits: ", size_circuits[:3])
print("A) ", np.prod(size_circuits[:3]))


##### PART B #####
distance_tuples = []
for i in range(data.shape[0]):
    for j in range(i + 1, data.shape[0]):
        if i != j:
            distance_tuples.append((i, j, np.linalg.norm(data[i] - data[j])))
distance_tuples.sort(key=lambda x: x[2])


class CircuitDetector:
    def __init__(self, n_nodes: int):
        self.parent = list(range(n_nodes))
        self.rank = [0] * n_nodes
        self.components = n_nodes

    def find_origin(self, node: int) -> int:
        if self.parent[node] != node:
            self.parent[node] = self.find_origin(self.parent[node])
        return self.parent[node]

    def connect(self, node1: int, node2: int) -> bool:
        origin1 = self.find_origin(node1)
        origin2 = self.find_origin(node2)

        # if the are already in the same circuit, return False
        if origin1 == origin2:
            return False

        if self.rank[origin1] < self.rank[origin2]:
            self.parent[origin1] = origin2
        elif self.rank[origin1] > self.rank[origin2]:
            self.parent[origin2] = origin1
        else:
            self.parent[origin2] = origin1
            self.rank[origin1] += 1
        self.components -= 1
        return True  # connection made


circuit_detector = CircuitDetector(data.shape[0])
total_distance = 0.0
for node1, node2, distance in distance_tuples:
    merged_circuit = circuit_detector.connect(node1, node2)
    if merged_circuit:
        total_distance += distance
        if circuit_detector.components == 1:
            coords1 = data[node1]
            coords2 = data[node2]
            print("B) ", coords1[0] * coords2[0])
            break
