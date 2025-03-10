from collections import deque
import heapq


def create_graph():
    graph = {
        0: [(1, 230), (2, 200)],
        1: [(0, 230), (2, 60)],
        2: [(0, 200), (1, 60), (3, 270), (4, 710)],
        3: [(2, 270), (14, 600)],
        4: [(2, 710), (5, 300)],
        5: [(4, 300), (6, 300)],
        6: [(5, 300), (7, 70)],
        7: [(6, 70), (8, 400)],
        8: [(7, 400), (9, 700)],
        9: [(8, 700), (10, 300)],
        10: [(9, 300), (11, 1000)],
        11: [(10, 1000), (12, 100)],
        12: [(11, 100), (13, 200)],
        13: [(12, 200), (14, 200)],
        14: [(13, 200), (15, 40), (16, 400)],
        15: [(14, 40)],
        16: [(14, 400), (17, 400)],
        17: [(16, 400), (18, 100)],
        18: [(17, 100)]
    }
    return graph

# BFS for finding the shortest path
def bfs_shortest_path(graph, start, end):
    # Initialize queue, visited set, and parent dictionary
    queue = deque([(start, [start], 0)])  # (node, path, distance)
    visited = set([start])
    
    while queue:
        node, path, distance = queue.popleft()
        
        if node == end:
            return path, distance
        
        for neighbor, weight in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = path + [neighbor]
                new_distance = distance + weight
                queue.append((neighbor, new_path, new_distance))
    
    return None, float('inf')  # No path found

# DFS for finding a path (not necessarily the shortest)
def dfs_path(graph, start, end):
    # Initialize stack, visited set
    stack = [(start, [start], 0)]  # (node, path, distance)
    visited = set()
    
    while stack:
        node, path, distance = stack.pop()
        
        if node not in visited:
            visited.add(node)
            
            if node == end:
                return path, distance
            
            for neighbor, weight in reversed(graph[node]):
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    new_distance = distance + weight
                    stack.append((neighbor, new_path, new_distance))
    
    return None, float('inf')  # No path found

# Dijkstra's algorithm for finding the shortest path (optimal)
def dijkstra_shortest_path(graph, start, end):
    # Priority queue for (distance, node, path)
    pq = [(0, start, [start])]
    visited = set()
    
    while pq:
        distance, node, path = heapq.heappop(pq)
        
        if node == end:
            return path, distance
        
        if node in visited:
            continue
            
        visited.add(node)
        
        for neighbor, weight in graph[node]:
            if neighbor not in visited:
                new_distance = distance + weight
                new_path = path + [neighbor]
                heapq.heappush(pq, (new_distance, neighbor, new_path))
    
    return None, float('inf')  # No path found

# Define locations mapping for better readability
locations = {
    0: "Lobby Apartemen Puncak Dharmahusada",
    1: "Pintu Gerbang Apartemen Puncak Dharmahusada",
    2: "Jalan Dr. H. Soekarno",
    3: "Jalan Raya Kertajaya Indah",
    4: "Jalan Mulyorejo",
    5: "Jalan Kaliwaron",
    6: "Jalan Kedung Tarukan",
    7: "Jalan Tambang Boyo",
    8: "Jalan Prof. DR. Moestopo",
    9: "Jalan Gubeng Pojok",
    10: "Jalan Pemuda",
    11: "Jalan Panglima Sudirman",
    12: "Jalan Urip Sumoharjo",
    13: "Jalan Pandegiling",
    14: "Jalan Dinoyo",
    15: "UKWMS Kampus Dinoyo",
    16: "Jalan Manyar Kertoarjo",
    17: "Jalan Kertajaya",
    18: "Jalan Sulawesi"
}

# Main function to find paths using all methods
def find_paths(start_vertex, end_vertex):
    graph = create_graph()
    
    # Using BFS
    bfs_path, bfs_distance = bfs_shortest_path(graph, start_vertex, end_vertex)
    
    # Using DFS
    dfs_path, dfs_distance = dfs_path(graph, start_vertex, end_vertex)
    
    # Using Dijkstra (optimal)
    dijkstra_path, dijkstra_distance = dijkstra_shortest_path(graph, start_vertex, end_vertex)
    
    print(f"Finding path from {locations[start_vertex]} to {locations[end_vertex]}:\n")
    
    # Print BFS results
    print("BFS Results:")
    if bfs_path:
        print(f"Path: {' → '.join(str(v) for v in bfs_path)}")
        print(f"Path names: {' → '.join(locations[v] for v in bfs_path)}")
        print(f"Total distance: {bfs_distance} meters\n")
    else:
        print("No path found using BFS\n")
    
    # Print DFS results
    print("DFS Results:")
    if dfs_path:
        print(f"Path: {' → '.join(str(v) for v in dfs_path)}")
        print(f"Path names: {' → '.join(locations[v] for v in dfs_path)}")
        print(f"Total distance: {dfs_distance} meters\n")
    else:
        print("No path found using DFS\n")
    
    # Print Dijkstra results
    print("Dijkstra Results (Optimal):")
    if dijkstra_path:
        print(f"Path: {' → '.join(str(v) for v in dijkstra_path)}")
        print(f"Path names: {' → '.join(locations[v] for v in dijkstra_path)}")
        print(f"Total distance: {dijkstra_distance} meters")
    else:
        print("No path found using Dijkstra")

if __name__ == "__main__":
    find_paths(0, 15)
