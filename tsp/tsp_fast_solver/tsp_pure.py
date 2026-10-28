import itertools
import math

def tsp_python(distance_matrix):
    """
    Calculates the shortest path cost through a fully connected graph represented
    by a 2D distance matrix using pure Python and itertools.permutations.

    Fixes city 0 as the starting/ending city and permutes the remaining (N - 1) cities,
    exploring (N - 1)! possible closed tours.

    Parameters:
        distance_matrix (list of list of int/float): 2D distance matrix.

    Returns:
        int: Shortest closed tour cost.
    """
    n = len(distance_matrix)
    if n <= 1:
        return 0
    if n == 2:
        return distance_matrix[0][1] + distance_matrix[1][0]

    # Fix city 0, permute cities 1 through n-1
    cities = list(range(1, n))
    min_cost = math.inf

    for perm in itertools.permutations(cities):
        # Start at 0, visit first city in permutation
        cost = distance_matrix[0][perm[0]]

        # Traverse remaining cities in order
        for i in range(len(perm) - 1):
            cost += distance_matrix[perm[i]][perm[i + 1]]

        # Return from last city back to city 0
        cost += distance_matrix[perm[-1]][0]

        if cost < min_cost:
            min_cost = cost

    return min_cost
