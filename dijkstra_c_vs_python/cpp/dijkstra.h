#ifndef DIJKSTRA_H
#define DIJKSTRA_H

#include <vector>
#include <climits>

// Use a safe large constant for INF that prevents overflow on addition
constexpr int INF_DIST = 1000000000; // 1e9

struct DijkstraResult {
    std::vector<int> dist;
    std::vector<int> parent;
};

/**
 * Computes shortest distances from source vertex to all vertices
 * in an adjacency matrix representation using Dijkstra's algorithm.
 *
 * @param graph Flattened 1D vector of size V * V.
 *              graph[u * V + v] represents the edge weight from u to v.
 *              A weight <= 0 indicates no edge (except self-loops where weight is 0).
 * @param V Number of vertices.
 * @param src Source vertex index (0-indexed).
 * @return std::vector<int> Array of shortest distances from src to all vertices.
 */
std::vector<int> dijkstra_matrix(const std::vector<int>& graph, int V, int src);

/**
 * Computes shortest distances and tracks parent pointers to allow
 * full shortest-path reconstruction.
 *
 * @param graph Flattened 1D vector of size V * V.
 * @param V Number of vertices.
 * @param src Source vertex index.
 * @return DijkstraResult Containing dist and parent vectors.
 */
DijkstraResult dijkstra_matrix_with_path(const std::vector<int>& graph, int V, int src);

/**
 * Reconstructs the shortest path from src to target using the parent array.
 *
 * @param parent Predecessor vector from dijkstra_matrix_with_path.
 * @param src Source vertex index.
 * @param target Destination vertex index.
 * @return std::vector<int> Path sequence [src, ..., target], or empty if unreachable.
 */
std::vector<int> get_shortest_path(const std::vector<int>& parent, int src, int target);

#endif // DIJKSTRA_H

