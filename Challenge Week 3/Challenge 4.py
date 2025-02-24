from collections import deque

def tambah_edge(x, y, adj):
    if x not in adj:
        adj[x] = []
    if y not in adj:
        adj[y] = []
    adj[x].append(y)
    adj[y].append(x)

def cetak_leaf_node(akar, adj):
    for node in adj:
        if len(adj[node]) == 1 and node != akar:
            print(node, end=" ")

def tinggi_tree(akar, adj):
    tinggi = 0
    q = deque([(akar, 0)])
    visited = {node: False for node in adj}
    visited[akar] = True

    while q:
        node, kedalaman = q.popleft()
        tinggi = max(tinggi, kedalaman)
        for tetangga in adj[node]:
            if not visited[tetangga]:
                visited[tetangga] = True
                q.append((tetangga, kedalaman + 1))

    return tinggi

def diameter_tree(akar, adj):
    diameter = 0
    nodes = list(adj.keys())
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            jarak = bfs_jarak(nodes[i], nodes[j], adj)
            diameter = max(diameter, jarak)
    return diameter

def bfs_jarak(start, end, adj):
    q = deque([(start, 0)])
    visited = {node: False for node in adj}
    visited[start] = True
    while q:
        node, jarak = q.popleft()
        if node == end:
            return jarak

        for neighbor in adj[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                q.append((neighbor, jarak + 1))
    return -1

def pre_order_traversal(node, adj, visited):
    if node not in visited:
        visited.add(node)
        result = [node]
        for neighbor in sorted(adj[node]):
            result += pre_order_traversal(neighbor, adj, visited)
        return result
    else:
        return []

def in_order_traversal(node, adj, visited, parent=None):
    if node not in visited:
        visited.add(node)
        result = []
        neighbors = sorted([n for n in adj[node] if n != parent])  # Filter parent

        if neighbors:
            # Kunjungi anak pertama
            result += in_order_traversal(neighbors[0], adj, visited, node)
            # Kunjungi node itu sendiri
            result.append(node)
            # Kunjungi anak-anak selanjutnya
            for neighbor in neighbors[1:]:
                result += in_order_traversal(neighbor, adj, visited, node)
        else:
            result.append(node)  # Jika tidak ada anak, tambahkan node itu sendiri
        return result
    else:
        return []

def post_order_traversal(node, adj, visited):
    if node not in visited:
        visited.add(node)
        result = []
        neighbors = sorted(adj[node])
        for neighbor in neighbors:
            result += post_order_traversal(neighbor, adj, visited)
        result.append(node)
        return result
    else:
        return []

def tentukan_akar(adj):
    return next(iter(adj))

def main():
    adj = {}

    tambah_edge("1", "2", adj)
    tambah_edge("2", "3", adj)
    tambah_edge("2", "4", adj)
    tambah_edge("2", "5", adj)
    tambah_edge("4", "6", adj)
    tambah_edge("4", "7", adj)
    tambah_edge("6", "8", adj)
    tambah_edge("6", "9", adj)
    tambah_edge("7", "10", adj)
    tambah_edge("7", "11", adj)

    akar = tentukan_akar(adj)
    print("Akar dari tree adalah:", akar)
    print("\nNode leaf dari tree adalah:")
    cetak_leaf_node(akar, adj)
    print("\n\nTinggi tree adalah:", tinggi_tree(akar, adj))
    print("\nDiameter tree adalah:", diameter_tree(akar, adj))

    # Traversal dengan format rapi
    print("\nPre-order traversal:")
    pre_nodes = pre_order_traversal(akar, adj, set())
    print(" → ".join(pre_nodes))

    print("\nIn-order traversal:")
    in_nodes = in_order_traversal(akar, adj, set())
    print(" → ".join(in_nodes))

    print("\nPost-order traversal:")
    post_nodes = post_order_traversal(akar, adj, set())
    print(" → ".join(post_nodes))

main()
