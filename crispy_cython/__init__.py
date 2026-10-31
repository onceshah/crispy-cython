"""
crispy-cython: High-Performance Graph Algorithms in C++ Wrapped in Cython.

Features:
- Dijkstra Shortest Path: Sub-millisecond single-source shortest path and path reconstruction.
- Traveling Salesperson Problem (TSP): Factorial brute-force solver using C++ std::next_permutation.
- Pure Python Fallbacks: Guaranteed execution across all platforms even without a C++ compiler.
"""

from crispy_cython import dijkstra
from crispy_cython import tsp

from crispy_cython.dijkstra import (
    dijkstra_cython,
    dijkstra_python,
    dijkstra_path,
    dijkstra_path_cython,
    dijkstra_path_python,
    dijkstra_from_edges_cython,
    dijkstra_from_edges_python,
)
from crispy_cython.tsp import (
    solve_tsp,
    tsp_cython,
    tsp_python,
)

# Convenient top-level alias for dijkstra
solve_dijkstra = dijkstra.dijkstra

__version__ = "0.1.0"
__author__ = "Vansh Shah"
__license__ = "MIT"

__all__ = [
    "__version__",
    "dijkstra",
    "tsp",
    "solve_dijkstra",
    "dijkstra_path",
    "dijkstra_cython",
    "dijkstra_python",
    "dijkstra_path_cython",
    "dijkstra_path_python",
    "dijkstra_from_edges_cython",
    "dijkstra_from_edges_python",
    "solve_tsp",
    "tsp_cython",
    "tsp_python",
]
