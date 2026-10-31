"""
dijkstra-fast-solver: High-performance C++ Dijkstra algorithm solver wrapped in Cython.
"""

from .dijkstra_pure import dijkstra_python, dijkstra_path_python, dijkstra_from_edges_python

try:
    from .dijkstra_wrapper import (
        dijkstra_cython,
        dijkstra_path_cython,
        dijkstra_from_edges_cython,
        solve_dijkstra_cython,
    )
except ImportError:
    try:
        from dijkstra_wrapper import (
            dijkstra_cython,
            dijkstra_path_cython,
            dijkstra_from_edges_cython,
            solve_dijkstra_cython,
        )
    except ImportError:
        dijkstra_cython = None
        dijkstra_path_cython = None
        dijkstra_from_edges_cython = None
        solve_dijkstra_cython = None

__version__ = "0.1.0"
__all__ = [
    "dijkstra_python",
    "dijkstra_path_python",
    "dijkstra_from_edges_python",
    "dijkstra_cython",
    "dijkstra_path_cython",
    "dijkstra_from_edges_cython",
    "solve_dijkstra_cython",
]

