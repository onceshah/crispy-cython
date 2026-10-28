#ifndef TSP_H
#define TSP_H

#include <vector>

/**
 * Solves the Traveling Salesperson Problem (TSP) using a brute-force approach.
 * Fixes city 0 as the starting and ending city and explores all (n-1)! permutations
 * using std::next_permutation.
 *
 * @param dist_matrix Flattened 1D vector representing the n x n distance matrix
 *                    where dist_matrix[i * n + j] is the distance from city i to j.
 * @param n Number of cities (nodes) in the graph.
 * @return The minimum tour cost visiting every city once and returning to city 0.
 */
int solve_tsp(const std::vector<int>& dist_matrix, int n);

#endif // TSP_H
