"""
Benchmark Script for TSP Solvers (Pure Python vs C++ wrapped with Cython)

Evaluates performance across graph sizes N = 8, 10, 11 as specified in:
"Graph Algorithms in Production - Part 1: The Traveling Salesperson Problem"
"""

import math
import platform
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

    print("=" * 86)
    print("        TRAVELING SALESPERSON PROBLEM (TSP) PRODUCTION BENCHMARK        ")
    print("             Pure Python (itertools) vs C++ (Cython Wrapper)            ")
    print("=" * 86)
    print(f" CPU / System : {platform.processor()} | {platform.system()} {platform.release()} (64-bit)")
    print(f" Python Env   : Python {platform.python_version()} ({platform.architecture()[0]})")
    print(" Timing Method: timeit.default_timer (High-precision monotonic hardware clock)")
    print(" Sampling     : Multi-run averaging (10 runs for N=8,10 Cython; 5 runs for N=8 Python)")
    print("=" * 86)

    header = f"{'Graph Size (N)':<16} | {'Possible Routes (N-1)!':<24} | {'Python Time':<13} | {'Cython Time':<13} | {'Speedup':<10}"
    separator = "-" * len(header)
    print(header)
    print(separator)

    benchmark_rows = []

    for n in test_sizes:
        dist_matrix = generate_distance_matrix(n)
        routes = math.factorial(n - 1)

        # Benchmark Cython solver (multi-run average to eliminate OS thread jitter)
        cython_runs = 10 if n <= 10 else 3
        start_cy = timeit.default_timer()
        for _ in range(cython_runs):
            cython_cost = tsp_cython(dist_matrix)
        end_cy = timeit.default_timer()
        cython_time = (end_cy - start_cy) / cython_runs

        # Benchmark Pure Python solver
        python_runs = 5 if n == 8 else 1
        start_py = timeit.default_timer()
        for _ in range(python_runs):
            python_cost = tsp_python(dist_matrix)
        end_py = timeit.default_timer()
        python_time = (end_py - start_py) / python_runs

        # Assert results match for algorithmic correctness
        assert python_cost == cython_cost, (
            f"Result mismatch for N={n}: Python={python_cost}, Cython={cython_cost}"
        )

        speedup = python_time / cython_time if cython_time > 0 else float("inf")

        cython_time_str = f"{cython_time:.6f}s" if cython_time >= 0.001 else f"{cython_time * 1000:.2f}ms"
        python_time_str = f"{python_time:.4f}s" if python_time >= 0.001 else f"{python_time * 1000:.2f}ms"
        speedup_str = f"{speedup:.1f}x"

        row = (
            f"N = {n:<12} | {routes:<24,d} | {python_time_str:<13} | {cython_time_str:<13} | {speedup_str:<10}"
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
    print("\n[SUCCESS] Benchmark completed. All tour costs matched between Python & C++ Cython.")
    return benchmark_rows


if __name__ == "__main__":
    run_benchmark()
