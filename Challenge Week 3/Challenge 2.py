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

def pre_order_traversal(node, adj, visited, parent=None):
    if node not in visited:
        visited.add(node)
        result = [node]
        # Ambil anak-anak (exclude parent)
        children = sorted([n for n in adj[node] if n != parent])
        for child in children:
            result += pre_order_traversal(child, adj, visited, node)
        return result
    else:
        return []

def in_order_traversal(node, adj, visited, parent=None):
    if node not in visited:
        visited.add(node)
        result = []
        # Ambil anak-anak (exclude parent)
        children = sorted([n for n in adj[node] if n != parent])
        if children:
            # Proses anak pertama sebagai "kiri"
            result += in_order_traversal(children[0], adj, visited, node)
        result.append(node)
        # Proses anak-anak sisanya sebagai "kanan"
        for child in children[1:]:
            result += in_order_traversal(child, adj, visited, node)
        return result
    else:
        return []

def post_order_traversal(node, adj, visited, parent=None):
    if node not in visited:
        visited.add(node)
        result = []
        # Ambil anak-anak (exclude parent)
        children = sorted([n for n in adj[node] if n != parent])
        for child in children:
            result += post_order_traversal(child, adj, visited, node)
        result.append(node)
        return result
    else:
        return []

def tentukan_akar(adj):
    return next(iter(adj))

def main():
    adj = {}

    tambah_edge("1", "2", adj)
    tambah_edge("1", "3", adj)
    tambah_edge("3", "4", adj)
    tambah_edge("3", "5", adj)
    tambah_edge("3", "6", adj)

    akar = tentukan_akar(adj)
    print("Akar dari tree adalah:", akar)
    
    print("\nNode leaf dari tree adalah:")
    cetak_leaf_node(akar, adj)
    
    print("\n\nTinggi tree adalah:", tinggi_tree(akar, adj))
    print("\nDiameter tree adalah:", diameter_tree(akar, adj))

    # Traversal
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
