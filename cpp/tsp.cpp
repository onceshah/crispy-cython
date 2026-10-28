#include "tsp.h"
#include <vector>
#include <algorithm>
#include <climits>
#include <numeric>

int solve_tsp(const std::vector<int>& dist_matrix, int n) {
    if (n <= 1) {
        return 0;
    }
    if (n == 2) {
        return dist_matrix[0 * n + 1] + dist_matrix[1 * n + 0];
    }

    // Permute cities 1 through n-1, keeping city 0 fixed as origin
    std::vector<int> cities(n - 1);
    std::iota(cities.begin(), cities.end(), 1); // [1, 2, ..., n-1]

    int min_cost = INT_MAX;

    // Explore all (n - 1)! possible route permutations
    do {
        // Start from city 0 to the first visited city
        int current_cost = dist_matrix[0 * n + cities[0]];

        // Visit each subsequent city in the permutation
        for (int i = 0; i < n - 2; ++i) {
            current_cost += dist_matrix[cities[i] * n + cities[i + 1]];
        }

        // Return from the last city back to origin (city 0)
        current_cost += dist_matrix[cities[n - 2] * n + 0];

        if (current_cost < min_cost) {
            min_cost = current_cost;
        }
    } while (std::next_permutation(cities.begin(), cities.end()));

    return min_cost;
}
