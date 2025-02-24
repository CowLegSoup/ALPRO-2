from collections import deque

def tambah_edge(x, y, adj):
    if x not in adj:
        adj[x] = []
    if y not in adj:
        adj[y] = []
    adj[x].append(y)
    adj[y].append(x)

def cetak_parent(node, adj, parent):
    if parent == "":
        print("{}-->".format(node))
    else:
        print("{}-->{}".format(node, parent))

    for cur in adj[node]:
        if cur != parent:
            cetak_parent(cur, adj, node)

def cetak_child(akar, adj):
    q = deque()
    q.append(akar)
    visited = {node: False for node in adj}
    while q:  # BFS
        node = q.popleft()
        visited[node] = True
        print("{}-->".format(node), end="")
        for cur in adj[node]:
            if not visited[cur]:
                print(cur, end=" ")
                q.append(cur)
        print()

def cetak_leaf_node(akar, adj):
    for node in adj:
        if len(adj[node]) == 1 and node != akar:
            print(node, end=" ")

def cetak_derajat(akar, adj):
    for node in adj:
        print("{} :".format(node), end=" ")
        if node == akar:
            print(len(adj[node]))
        else:
            print(len(adj[node]) - 1)

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

def depth_tree(node, adj, target):
    depth = -1
    q = deque([(node, 0)])
    visited = {node: False for node in adj}
    visited[node] = True
    while q:
        current, kedalaman = q.popleft()
        if current == target:
            depth = kedalaman
            break
        for tetangga in adj[current]:
            if not visited[tetangga]:
                visited[tetangga] = True
                q.append((tetangga, kedalaman + 1))
    return depth

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

def main():
    akar = "A1"
    adj = {}

    tambah_edge("A1", "A2", adj)
    tambah_edge("A1", "A3", adj)
    tambah_edge("A2", "A4", adj)
    tambah_edge("A2", "A5", adj)
    tambah_edge("A3", "A6", adj)
    tambah_edge("A6", "A7", adj)
    tambah_edge("A6", "A8", adj)
    tambah_edge("A6", "A9", adj)

    print("Parent dari setiap node adalah:")
    cetak_parent(akar, adj, "")

    print("\nChild dari setiap node adalah:")
    cetak_child(akar, adj)

    print("\nNode leaf dari tree adalah:")
    cetak_leaf_node(akar, adj)

    print("\nDerajat dari setiap node adalah:")
    cetak_derajat(akar, adj)

    print("\nTinggi tree adalah:", tinggi_tree(akar, adj))

    print("\nDepth tree adalah:", depth_tree(akar, adj, "A9"))

    print("\nDiameter tree adalah:", diameter_tree(akar, adj))

main()
