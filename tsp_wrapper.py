"""
Bridge shim allowing direct `import tsp_wrapper` as required by the assignment.
"""
try:
    from tsp_fast_solver.tsp_wrapper import (
        tsp_cython,
        solve_tsp_cython,
        tsp_cpp_wrapper
    )
except ImportError:
    try:
        from .tsp_wrapper import (
            tsp_cython,
            solve_tsp_cython,
            tsp_cpp_wrapper
        )
    except ImportError:
        pass

__all__ = ["tsp_cython", "solve_tsp_cython", "tsp_cpp_wrapper"]
