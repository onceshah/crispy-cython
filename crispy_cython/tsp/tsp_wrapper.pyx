# distutils: language = c++
# cython: language_level = 3

from libcpp.vector cimport vector
from crispy_cython.tsp.tsp_wrapper cimport solve_tsp

def tsp_cython(object distance_matrix):
    """
    Solves TSP using the native C++ brute-force solver via Cython.
    
    Parameters:
        distance_matrix: 2D list-of-lists representing the pairwise distance matrix.
        
    Returns:
        int: The minimum total travel cost for the closed TSP tour.
    """
    cdef int n = len(distance_matrix)
    if n <= 1:
        return 0
    if n == 2:
        return int(distance_matrix[0][1] + distance_matrix[1][0])

    cdef vector[int] vec
    vec.reserve(n * n)

    cdef int i, j
    for i in range(n):
        row = distance_matrix[i]
        for j in range(n):
            vec.push_back(<int>row[j])

    return solve_tsp(vec, n)

# Convenient aliases
def solve_tsp_cython(object distance_matrix):
    return tsp_cython(distance_matrix)

def tsp_cpp_wrapper(object distance_matrix):
    return tsp_cython(distance_matrix)
