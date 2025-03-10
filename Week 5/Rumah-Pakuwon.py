# Representation of the graph
graph = {
    0: [(1, 230)],           
    1: [(2, 60)],            
    2: [(3, 1020), (12, 710)], 
    3: [(4, 1300)],          
    4: [(5, 600)],           
    5: [(6, 1900)],           
    6: [(7, 700)],           
    7: [(8, 400)],           
    8: [(9, 300)],          
    9: [(10, 400)],
    10: [(11, 700)],                    
    12: [(5, 1500)]                      
}

# Function to calculate path distance
def calculate_path_distance(graph, path):
    total_distance = 0
    for i in range(len(path) - 1):
        for neighbor, weight in graph.get(path[i], []):
            if neighbor == path[i + 1]:
                total_distance += weight
                break
    return total_distance

# DFS implementation to find paths
def dfs_paths(graph, start, goal):
    stack = [(start, [start])]  # (current_node, path)
    all_paths = []
    
    while stack:
        (node, path) = stack.pop()
        
        if node == goal:
            all_paths.append(path)
            continue
            
        for neighbor, _ in graph.get(node, []):
            if neighbor not in path:  # Avoid cycles
                stack.append((neighbor, path + [neighbor]))
    
    return all_paths

# BFS implementation to find shortest path
def bfs_shortest_path(graph, start, goal):
    queue = [(start, [start])]  # (current_node, path)
    visited = set()
    
    while queue:
        (node, path) = queue.pop(0)
        
        if node == goal:
            return path
            
        if node not in visited:
            visited.add(node)
            
            for neighbor, _ in graph.get(node, []):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
    
    return None  # No path found

# Main analysis
print("1. Fastest path from Rumah (Lobby, 0) to UKWMS Pakuwon (11) using BFS:")
bfs_path = bfs_shortest_path(graph, 0, 11)
bfs_distance = calculate_path_distance(graph, bfs_path)
print(f"Path: {' → '.join(map(str, bfs_path))}")
print(f"Distance: {bfs_distance} meters")

print("\n2. All paths from Rumah (Lobby, 0) to UKWMS Pakuwon (11) using DFS:")
dfs_all_paths = dfs_paths(graph, 0, 11)
for i, path in enumerate(dfs_all_paths, 1):
    distance = calculate_path_distance(graph, path)
    print(f"Path {i}: {' → '.join(map(str, path))}")
    print(f"Distance: {distance} meters")

# Find shortest path from DFS results
if dfs_all_paths:
    dfs_shortest_path = min(dfs_all_paths, key=lambda p: calculate_path_distance(graph, p))
    dfs_shortest_distance = calculate_path_distance(graph, dfs_shortest_path)
    print("\n3. Shortest path from DFS results:")
    print(f"Path: {' → '.join(map(str, dfs_shortest_path))}")
    print(f"Distance: {dfs_shortest_distance} meters")
