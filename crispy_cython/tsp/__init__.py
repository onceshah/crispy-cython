"""
Traveling Salesperson Problem (TSP) Module for crispy-cython.
Provides high-performance C++ next_permutation brute-force TSP solver wrapped in Cython,
with automatic fallback to pure Python itertools if compiled binaries are unavailable.
"""

from crispy_cython.tsp.tsp_pure import tsp_python

try:
    from crispy_cython.tsp.tsp_wrapper import tsp_cython
    HAS_CYTHON = True
except ImportError:
    # Graceful fallback to pure Python
    tsp_cython = tsp_python
    HAS_CYTHON = False

# Convenient high-level alias
solve_tsp = tsp_cython

__all__ = [
    "solve_tsp",
    "tsp_cython",
    "tsp_python",
    "HAS_CYTHON",
]
