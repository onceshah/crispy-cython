# distutils: language = c++
# cython: language_level = 3
# cython: boundscheck = False
# cython: wraparound = False

from libcpp.vector cimport vector
from dijkstra_wrapper cimport dijkstra_matrix, dijkstra_matrix_with_path, get_shortest_path, DijkstraResult

def dijkstra_cython(object distance_matrix, int src = 0):
    """
    Computes shortest distances from source vertex using compiled C++ Dijkstra via Cython.
    
    Parameters:
        distance_matrix: 2D list-of-lists (V x V) representing adjacency matrix.
        src: Source vertex index (default 0).
        
    Returns:
        list of int: Shortest distances from src to all vertices.
    """
    cdef int n = len(distance_matrix)
    if n == 0:
        return []

    cdef vector[int] vec
    vec.reserve(n * n)

    cdef int i, j
    for i in range(n):
        row = distance_matrix[i]
        for j in range(n):
            vec.push_back(<int>row[j])

    cdef vector[int] res = dijkstra_matrix(vec, n, src)
    cdef list output = [res[i] for i in range(n)]
    return output

def dijkstra_path_cython(object distance_matrix, int src, int target):
    """
    Finds the shortest path and distance between src and target.
    
    Parameters:
        distance_matrix: 2D list-of-lists (V x V) representing adjacency matrix.
        src: Source vertex index.
        target: Destination vertex index.
        
    Returns:
        tuple: (total_distance, path_list) where path_list is [src, ..., target].
    """
    cdef int n = len(distance_matrix)
    if n == 0:
        return (0, [])

    cdef vector[int] vec
    vec.reserve(n * n)

    cdef int i, j
    for i in range(n):
        row = distance_matrix[i]
        for j in range(n):
            vec.push_back(<int>row[j])

    cdef DijkstraResult res = dijkstra_matrix_with_path(vec, n, src)
    cdef vector[int] path_vec = get_shortest_path(res.parent, src, target)

    cdef int total_dist = res.dist[target]
    cdef list path = [path_vec[k] for k in range(path_vec.size())]

    return (total_dist, path)

def dijkstra_from_edges_cython(list nodes_coords, list edges_dicts, int src, int target):
    """
    Computes shortest path directly from Google Maps graph structure:
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
    cdef int n = len(nodes_coords)
    if n == 0:
        return (0, [])

    cdef vector[int] vec = vector[int](n * n, 0)
    cdef dict e
    cdef int u, v, w
    for item in edges_dicts:
        e = <dict>item
        u = <int>e["s"]
        v = <int>e["d"]
        w = <int>e["w"]
        if 0 <= u < n and 0 <= v < n:
            vec[u * n + v] = w
            vec[v * n + u] = w

    cdef DijkstraResult res = dijkstra_matrix_with_path(vec, n, src)
    cdef vector[int] path_vec = get_shortest_path(res.parent, src, target)

    cdef int total_dist = res.dist[target]
    cdef list path = [path_vec[k] for k in range(path_vec.size())]

    return (total_dist, path)

# Aliases
def solve_dijkstra_cython(object distance_matrix, int src = 0):
    return dijkstra_cython(distance_matrix, src)

