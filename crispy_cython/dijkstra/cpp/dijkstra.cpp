#include "dijkstra.h"
#include <vector>
#include <algorithm>
#include <cstdint>

std::vector<int> dijkstra_matrix(const std::vector<int>& graph, int V, int src) {
    if (V <= 0 || src < 0 || src >= V) {
        return {};
    }

    std::vector<int> dist(V, INF_DIST);
    std::vector<uint8_t> visited(V, 0);

    dist[src] = 0;

    for (int count = 0; count < V - 1; ++count) {
        int min_val = INF_DIST;
        int u = -1;

        // Find unvisited vertex with minimum distance
        for (int v = 0; v < V; ++v) {
            if (!visited[v] && dist[v] < min_val) {
                min_val = dist[v];
                u = v;
            }
        }

        if (u == -1 || min_val == INF_DIST) {
            break; // Remaining vertices are unreachable
        }

        visited[u] = 1;
        const int* row = &graph[u * V];
        const int dist_u = dist[u];

        for (int v = 0; v < V; ++v) {
            const int weight = row[v];
            if (!visited[v] && weight > 0) {
                const int candidate = dist_u + weight;
                if (candidate < dist[v]) {
                    dist[v] = candidate;
                }
            }
        }
    }

    return dist;
}

DijkstraResult dijkstra_matrix_with_path(const std::vector<int>& graph, int V, int src) {
    if (V <= 0 || src < 0 || src >= V) {
        return {{}, {}};
    }

    std::vector<int> dist(V, INF_DIST);
    std::vector<int> parent(V, -1);
    std::vector<uint8_t> visited(V, 0);

    dist[src] = 0;

    for (int count = 0; count < V - 1; ++count) {
        int min_val = INF_DIST;
        int u = -1;

        for (int v = 0; v < V; ++v) {
            if (!visited[v] && dist[v] < min_val) {
                min_val = dist[v];
                u = v;
            }
        }

        if (u == -1 || min_val == INF_DIST) {
            break;
        }

        visited[u] = 1;
        const int* row = &graph[u * V];
        const int dist_u = dist[u];

        for (int v = 0; v < V; ++v) {
            const int weight = row[v];
            if (!visited[v] && weight > 0) {
                const int candidate = dist_u + weight;
                if (candidate < dist[v]) {
                    dist[v] = candidate;
                    parent[v] = u;
                }
            }
        }
    }

    return {dist, parent};
}

std::vector<int> get_shortest_path(const std::vector<int>& parent, int src, int target) {
    if (target < 0 || target >= static_cast<int>(parent.size())) {
        return {};
    }
    if (src == target) {
        return {src};
    }

    std::vector<int> path;
    int curr = target;

    while (curr != -1) {
        path.push_back(curr);
        if (curr == src) {
            break;
        }
        curr = parent[curr];
    }

    if (path.empty() || path.back() != src) {
        return {}; // No path exists
    }

    std::reverse(path.begin(), path.end());
    return path;
}

