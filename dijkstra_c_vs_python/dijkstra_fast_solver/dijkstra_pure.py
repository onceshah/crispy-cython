"""
Pure Python Reference Implementation of Dijkstra's Algorithm
Uses Adjacency Matrix representation.
"""

INF = 1000000000  # 1e9 sentinel


def min_distance(dist: list[int], visited: list[bool], V: int) -> int:
    """Finds the unvisited vertex with the minimum distance value."""
    min_val = INF
    min_index = -1
    for v in range(V):
        if not visited[v] and dist[v] < min_val:
            min_val = dist[v]
            min_index = v
    return min_index


def dijkstra_python(distance_matrix: list[list[int]], src: int = 0) -> list[int]:
    """
    Calculates shortest distances from source vertex to all vertices
    through a graph represented by a 2D adjacency matrix.
    
    Parameters:
        distance_matrix: 2D list-of-lists (V x V) of non-negative edge weights.
        src: Source vertex index (default 0).
        
    Returns:
        list of int: Shortest distance to each vertex.
    """
    V = len(distance_matrix)
    if V == 0:
        return []

    dist = [INF] * V
    visited = [False] * V
    dist[src] = 0

    for _ in range(V - 1):
        u = min_distance(dist, visited, V)
        if u == -1 or dist[u] == INF:
            break
        visited[u] = True

        row_u = distance_matrix[u]
        dist_u = dist[u]

        for v in range(V):
            weight = row_u[v]
            if not visited[v] and weight > 0:
                candidate = dist_u + weight
                if candidate < dist[v]:
                    dist[v] = candidate

    return dist


def dijkstra_path_python(distance_matrix: list[list[int]], src: int, target: int) -> tuple[int, list[int]]:
    """
    Finds the shortest path and distance between src and target.
    
    Parameters:
        distance_matrix: 2D list-of-lists (V x V).
        src: Source vertex.
        target: Destination vertex.
        
    Returns:
        tuple: (total_distance, path_list) where path_list is [src, ..., target].
    """
    V = len(distance_matrix)
    if V == 0:
        return (0, [])

    dist = [INF] * V
    parent = [-1] * V
    visited = [False] * V
    dist[src] = 0

    for _ in range(V - 1):
        u = min_distance(dist, visited, V)
        if u == -1 or dist[u] == INF:
            break
        visited[u] = True

        row_u = distance_matrix[u]
        dist_u = dist[u]

        for v in range(V):
            weight = row_u[v]
            if not visited[v] and weight > 0:
                candidate = dist_u + weight
                if candidate < dist[v]:
                    dist[v] = candidate
                    parent[v] = u

    # Reconstruct path
    path = []
    curr = target
    while curr != -1:
        path.append(curr)
        if curr == src:
            break
        curr = parent[curr]

    if not path or path[-1] != src:
        return (INF, [])

    path.reverse()
    return (dist[target], path)


def dijkstra_from_edges_python(
    nodes_coords: list,
    edges_dicts: list[dict],
    src: int,
    target: int
) -> tuple[int, list[int]]:
    """
    Computes shortest path in Pure Python directly from Google Maps graph structure:
    nodes: Array of [x, y] coordinates
    edges: Array of dictionaries [{'s': source, 'd': destination, 'w': weight, ...}, ...]

    Parameters:
        nodes_coords: list of [x, y] coordinates
        edges_dicts: list of dicts with 's', 'd', 'w'
        src: source node index
        target: target node index

    Returns:
        tuple: (total_distance, path_list)
    """
    n = len(nodes_coords)
    if n == 0:
        return (0, [])
    matrix = [[0] * n for _ in range(n)]
    for e in edges_dicts:
        u = e["s"]
        v = e["d"]
        w = e["w"]
        if 0 <= u < n and 0 <= v < n:
            matrix[u][v] = w
            matrix[v][u] = w
    return dijkstra_path_python(matrix, src, target)


