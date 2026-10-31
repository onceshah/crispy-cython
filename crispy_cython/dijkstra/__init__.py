"""
Dijkstra Shortest Path Module for crispy-cython.
Provides high-performance C++ Dijkstra shortest path algorithms wrapped in Cython,
with automatic fallback to pure Python if compiled binaries are unavailable.
"""

from crispy_cython.dijkstra.dijkstra_pure import (
    dijkstra_python,
    dijkstra_path_python,
    dijkstra_from_edges_python,
)

try:
    from crispy_cython.dijkstra.dijkstra_wrapper import (
        dijkstra_cython,
        dijkstra_path_cython,
        dijkstra_from_edges_cython,
    )
    HAS_CYTHON = True
except ImportError:
    # Graceful fallback to pure Python
    dijkstra_cython = dijkstra_python
    dijkstra_path_cython = dijkstra_path_python
    dijkstra_from_edges_cython = dijkstra_from_edges_python
    HAS_CYTHON = False

# Convenient high-level aliases
dijkstra = dijkstra_cython
dijkstra_path = dijkstra_path_cython

__all__ = [
    "dijkstra",
    "dijkstra_path",
    "dijkstra_cython",
    "dijkstra_path_cython",
    "dijkstra_from_edges_cython",
    "dijkstra_python",
    "dijkstra_path_python",
    "dijkstra_from_edges_python",
    "HAS_CYTHON",
]
