#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <stdbool.h>
#include <time.h>

#define MAX_V 2000
#define INF INT_MAX

// Graph representation: Adjacency matrix
int graph[MAX_V][MAX_V];
int dist[MAX_V];
bool visited[MAX_V];

// Function to find the vertex with minimum distance value
int minDistance(int V) {
    int min = INF, min_index = -1;
    for (int v = 0; v < V; v++) {
        if (!visited[v] && dist[v] <= min) {
            min = dist[v];
            min_index = v;
        }
    }
    return min_index;
}

// Dijkstra's algorithm for adjacency matrix
void dijkstra(int V, int src) {
    for (int i = 0; i < V; i++) {
        dist[i] = INF;
        visited[i] = false;
    }
    dist[src] = 0;

    for (int count = 0; count < V - 1; count++) {
        int u = minDistance(V);
        if (u == -1) break;
        visited[u] = true;

        for (int v = 0; v < V; v++) {
            if (!visited[v] && graph[u][v] > 0 && dist[u] != INF
                && dist[u] + graph[u][v] < dist[v]) {
                dist[v] = dist[u] + graph[u][v];
            }
        }
    }
}

int main(int argc, char *argv[]) {
    int V = (argc > 1) ? atoi(argv[1]) : 1000;
    if (V < 1 || V > MAX_V) V = 1000;
    int repeats = (argc > 2) ? atoi(argv[2]) : 1;
    if (repeats < 1) repeats = 1;

    // 1. Graph representation: Adjacency matrix with non-negative edge weights
    for (int i = 0; i < V; i++) {
        for (int j = 0; j < V; j++) {
            graph[i][j] = (i == j) ? 0 : ((i + j) % 10 + 1);
        }
    }

    // 2. Timing method: C's clock()
    clock_t start = clock();
    for (int r = 0; r < repeats; r++) {
        dijkstra(V, 0); // Source vertex: Vertex 0
    }
    clock_t end = clock();

    double total_time = ((double)(end - start)) / CLOCKS_PER_SEC;
    double execution_time = total_time / repeats;

    // 3. Output: Execution time
    printf("Algorithm: Dijkstra's\n");
    printf("Language: C\n");
    printf("Graph representation: Adjacency matrix\n");
    printf("Edge weights: Non-negative integers\n");
    printf("Source vertex: 0\n");
    printf("Graph size: %d vertices\n", V);
    printf("Timing method: clock()\n");
    printf("Shortest distance from vertex 0 to vertex %d: %d\n", V - 1, dist[V - 1]);
    printf("Execution time: %.6f seconds (%.3f ms)\n", execution_time, execution_time * 1000.0);

    return 0;
}
