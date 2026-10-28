# distutils: language = c++

from libcpp.vector cimport vector

cdef extern from "tsp.h":
    int solve_tsp(const vector[int]& dist_matrix, int n)
