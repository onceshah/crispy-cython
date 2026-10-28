import sys
import time

INF = float('inf')


def min_distance(dist, visited, V):
    """Find the vertex with the minimum distance value from the set of unvisited vertices."""
    min_val = INF
    min_index = -1
    for v in range(V):
        if not visited[v] and dist[v] <= min_val:
            min_val = dist[v]
            min_index = v
    return min_index


def dijkstra(graph, V, src=0):
    """Dijkstra's algorithm for graph represented as an adjacency matrix."""
    dist = [INF] * V
    visited = [False] * V
    dist[src] = 0

    for _ in range(V - 1):
        u = min_distance(dist, visited, V)
        if u == -1:
            break
        visited[u] = True

        for v in range(V):
            weight = graph[u][v]
            if not visited[v] and weight > 0 and dist[u] != INF:
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight

    return dist


def main():
    V = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    repeats = int(sys.argv[2]) if len(sys.argv) > 2 else 1

    # 1. Graph representation: Adjacency matrix with non-negative edge weights
    graph = [[0 if i == j else (i + j) % 10 + 1 for j in range(V)] for i in range(V)]

    # 2. Timing method: Python's time.perf_counter()
    dist = None
    start = time.perf_counter()
    for _ in range(repeats):
        dist = dijkstra(graph, V, src=0)  # Source vertex: Vertex 0
    end = time.perf_counter()

    total_time = end - start
    execution_time = total_time / repeats

    # 3. Output: Execution time
    print("Algorithm: Dijkstra's")
    print("Language: Python")
    print("Graph representation: Adjacency matrix")
    print("Edge weights: Non-negative integers")
    print("Source vertex: 0")
    print(f"Graph size: {V} vertices")
    print("Timing method: time.perf_counter()")
    print(f"Shortest distance from vertex 0 to vertex {V - 1}: {dist[V - 1]}")
    print(f"Execution time: {execution_time:.6f} seconds ({execution_time * 1000:.3f} ms)")


if __name__ == "__main__":
    main()
