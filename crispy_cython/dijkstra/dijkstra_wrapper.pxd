# distutils: language = c++

from libcpp.vector cimport vector

cdef extern from "dijkstra.h":
    cdef struct DijkstraResult:
        vector[int] dist
        vector[int] parent

    vector[int] dijkstra_matrix(const vector[int]& graph, int V, int src)
    DijkstraResult dijkstra_matrix_with_path(const vector[int]& graph, int V, int src)
    vector[int] get_shortest_path(const vector[int]& parent, int src, int target)

