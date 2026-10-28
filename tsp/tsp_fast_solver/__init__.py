"""
tsp-fast-solver: A blazing fast C++ TSP solver wrapped in Cython.
"""

from .tsp_pure import tsp_python

try:
    from .tsp_wrapper import tsp_cython, solve_tsp_cython
except ImportError:
    try:
        from tsp_wrapper import tsp_cython, solve_tsp_cython
    except ImportError:
        tsp_cython = None
        solve_tsp_cython = None

__version__ = "0.1.0"
__all__ = ["tsp_python", "tsp_cython", "solve_tsp_cython"]
