# Representation of the graph
graph = {
    0: [(1, 230)],           # Lobby Apartemen to Pintu Gerbang
    1: [(2, 60)],            # Pintu Gerbang to Jalan Dr. H. Soekarno
    2: [(3, 410), (9, 300)], # Jalan Dr. H. Soekarno to Jalan Kalijudan and Jalan Mulyorejo Indah I
    3: [(4, 1200)],          # Jalan Kalijudan to UKWMS kampus Kalijudan
    4: [(5, 400)],           # UKWMS kampus Kalijudan to Jalan Kalijudan
    5: [(6, 200)],           # Jalan Kalijudan to Jalan Kalikepiting
    6: [(7, 150)],           # Jalan Kalikepiting to Jalan Kaliwaron
    7: [(8, 450)],           # Jalan Kaliwaron to Jalan Mulyorejo
    8: [(9, 600)],           # Jalan Mulyorejo to Jalan Mulyorejo Indah I
    9: [(2, 300)]            # Jalan Mulyorejo Indah I to Jalan Dr. H. Soekarno
}

# Finding simple paths (without repetition of vertices)
def find_simple_paths(graph, start, goal):
    def dfs(node, path, visited):
        if node == goal:
            paths.append(path.copy())
            return
            
        visited.add(node)
        
        for neighbor, _ in graph.get(node, []):
            if neighbor not in visited:
                path.append(neighbor)
                dfs(neighbor, path, visited.copy())
                path.pop()
    
    paths = []
    dfs(start, [start], set())
    return paths

# Function to calculate the distance of a path
def calculate_path_distance(graph, path):
    total_distance = 0
    for i in range(len(path) - 1):
        for neighbor, weight in graph.get(path[i], []):
            if neighbor == path[i + 1]:
                total_distance += weight
                break
    return total_distance

# Function to identify cycles in the graph
def find_cycles(graph):
    cycles = []
    
    def dfs_cycle(node, path, start_node):
        # If we've reached our starting node again and path has at least 3 nodes (a valid cycle)
        if node == start_node and len(path) > 2:
            cycles.append(path.copy())
            return
            
        for neighbor, _ in graph.get(node, []):
            if neighbor not in path or neighbor == start_node:
                if neighbor not in path or (neighbor == start_node and len(path) > 2):
                    path.append(neighbor)
                    dfs_cycle(neighbor, path, start_node)
                    path.pop()
    
    # Check cycles starting from each node
    for node in graph:
        dfs_cycle(node, [node], node)
    
    # Remove duplicate cycles (same cycle but different starting points)
    unique_cycles = []
    for cycle in cycles:
        # Normalize cycle by rotating to have smallest node first
        min_idx = cycle.index(min(cycle))
        normalized = cycle[min_idx:] + cycle[1:min_idx+1]
        if normalized not in unique_cycles:
            unique_cycles.append(normalized)
    
    return unique_cycles

# Finding paths from Lobby (0) to UKWMS Kalijudan (4)
simple_paths = find_simple_paths(graph, 0, 4)

print("1. Paths from Rumah (Lobby, 0) to UKWMS Kalijudan (4):")
for i, path in enumerate(simple_paths, 1):
    distance = calculate_path_distance(graph, path)
    print(f"   Path {i}: {' → '.join(map(str, path))}")
    print(f"   Distance: {distance} meters")

# Finding shortest and longest paths
path_distances = [(path, calculate_path_distance(graph, path)) for path in simple_paths]
shortest_path = min(path_distances, key=lambda x: x[1])
longest_path = max(path_distances, key=lambda x: x[1])

print("\n2. Shortest walk from Rumah to UKWMS Kalijudan:")
print(f"   Path: {' → '.join(map(str, shortest_path[0]))}")
print(f"   Distance: {shortest_path[1]} meters")

print("\n   Longest walk from Rumah to UKWMS Kalijudan:")
print(f"   Path: {' → '.join(map(str, longest_path[0]))}")
print(f"   Distance: {longest_path[1]} meters")

# Identifying cycles in the graph
cycles = find_cycles(graph)

print("\n3. Cycles in the graph:")
for i, cycle in enumerate(cycles, 1):
    print(f"   Cycle {i}: {' → '.join(map(str, cycle))}")

# Counting number of possible cycles from Rumah to UKWMS
# First, identify which cycles are relevant to our path
relevant_cycles = []
for cycle in cycles:
    # If the cycle contains both vertex 2 and vertex 4
    # (we need vertex 2 because that's where we can enter the cycle from the path 0→1→2)
    # (we need vertex 4 because that's our destination)
    if 2 in cycle and 4 in cycle:
        relevant_cycles.append(cycle)

print(f"\n   Number of cycles relevant to path from Rumah to UKWMS Kalijudan: {len(relevant_cycles)}")
for i, cycle in enumerate(relevant_cycles, 1):
    print(f"   Relevant Cycle {i}: {' → '.join(map(str, cycle))}")
