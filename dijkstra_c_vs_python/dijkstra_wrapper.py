"""
Bridge shim allowing direct `import dijkstra_wrapper`.
"""
try:
    from dijkstra_fast_solver.dijkstra_wrapper import (
        dijkstra_cython,
        dijkstra_path_cython,
        dijkstra_from_edges_cython,
        solve_dijkstra_cython,
    )
except ImportError:
    try:
        from .dijkstra_wrapper import (
            dijkstra_cython,
            dijkstra_path_cython,
            dijkstra_from_edges_cython,
            solve_dijkstra_cython,
        )
    except ImportError:
        pass

__all__ = [
    "dijkstra_cython",
    "dijkstra_path_cython",
    "dijkstra_from_edges_cython",
    "solve_dijkstra_cython",
]

