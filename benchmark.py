"""
Benchmark Script for TSP Solvers (Pure Python vs C++ wrapped with Cython)

Evaluates performance across graph sizes N = 8, 10, 11 as specified in:
"Graph Algorithms in Production - Part 1: The Traveling Salesperson Problem"
"""

import math
import random
import sys
import timeit

# Import both solvers
try:
    from tsp_fast_solver import tsp_python, tsp_cython
except ImportError:
    from python_solver import tsp_python
    from tsp_wrapper import tsp_cython


def generate_distance_matrix(n: int, seed: int = 42) -> list[list[int]]:
    """
    Generates a symmetric NxN distance matrix with 0 on diagonals
    and random integer distances between 10 and 100.
    """
    rng = random.Random(seed + n)
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            val = rng.randint(10, 100)
            matrix[i][j] = val
            matrix[j][i] = val
    return matrix


def run_benchmark():
    test_sizes = [8, 10, 11]

    print("=" * 80)
    print("      TRAVELING SALESPERSON PROBLEM (TSP) BENCHMARK      ")
    print("           Pure Python vs C++ (Cython Wrapper)           ")
    print("=" * 80)

    header = f"{'Graph Size (N)':<16} | {'Possible Routes (N-1)!':<24} | {'Python Time':<14} | {'Cython Time':<14} | {'Speedup':<10}"
    separator = "-" * len(header)
    print(header)
    print(separator)

    benchmark_rows = []

    for n in test_sizes:
        dist_matrix = generate_distance_matrix(n)
        routes = math.factorial(n - 1)

        # Benchmark Cython solver
        # For N=8 and 10, run multiple iterations for statistical stability
        cython_runs = 10 if n <= 10 else 3
        start_cy = timeit.default_timer()
        for _ in range(cython_runs):
            cython_cost = tsp_cython(dist_matrix)
        end_cy = timeit.default_timer()
        cython_time = (end_cy - start_cy) / cython_runs

        # Benchmark Pure Python solver
        # 1 run for large N to avoid long waits
        python_runs = 5 if n == 8 else 1
        start_py = timeit.default_timer()
        for _ in range(python_runs):
            python_cost = tsp_python(dist_matrix)
        end_py = timeit.default_timer()
        python_time = (end_py - start_py) / python_runs

        # Assert results match for correctness
        assert python_cost == cython_cost, (
            f"Result mismatch for N={n}: Python={python_cost}, Cython={cython_cost}"
        )

        speedup = python_time / cython_time if cython_time > 0 else float("inf")

        cython_time_str = f"{cython_time:.6f}s" if cython_time >= 0.001 else f"{cython_time * 1000:.2f}ms"
        python_time_str = f"{python_time:.4f}s"
        speedup_str = f"{speedup:.1f}x"

        row = (
            f"N = {n:<12} | {routes:<24,d} | {python_time_str:<14} | {cython_time_str:<14} | {speedup_str:<10}"
        )
        print(row)

        benchmark_rows.append({
            "n": n,
            "routes": routes,
            "python_time": python_time,
            "cython_time": cython_time,
            "python_time_str": python_time_str,
            "cython_time_str": cython_time_str,
            "speedup_str": speedup_str,
            "cost": python_cost,
        })

    print(separator)
    print("\nBenchmark completed successfully! All tour costs matched between solvers.")
    return benchmark_rows


if __name__ == "__main__":
    run_benchmark()
