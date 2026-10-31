"""
Unit tests for the unified crispy-cython package.
Verifies that:
1. Dijkstra shortest path finds correct distances and paths.
2. TSP solver calculates optimal tour cost.
3. Both Cython and Python fallback implementations produce 100% identical results.
"""

import pytest
import crispy_cython as cc
from crispy_cython import dijkstra, tsp


def test_dijkstra_matrix_correctness():
    # 4-node directed graph
    matrix = [
        [0, 4, 1, 0],
        [0, 0, 0, 1],
        [0, 2, 0, 5],
        [0, 0, 0, 0]
    ]

    expected = [0, 3, 1, 4]
    res_py = dijkstra.dijkstra_python(matrix, src=0)
    res_cy = dijkstra.dijkstra_cython(matrix, src=0)
    res_top = cc.solve_dijkstra(matrix, src=0)
    res_sub = dijkstra.dijkstra(matrix, src=0)

    assert res_py == expected
    assert res_cy == expected
    assert res_top == expected
    assert res_sub == expected


def test_dijkstra_path_reconstruction():
    matrix = [
        [0, 4, 1, 0],
        [0, 0, 0, 1],
        [0, 2, 0, 5],
        [0, 0, 0, 0]
    ]

    dist, path = cc.dijkstra_path(matrix, src=0, target=3)
    dist_sub, path_sub = dijkstra.dijkstra_path(matrix, src=0, target=3)

    assert dist == 4
    assert path == [0, 2, 1, 3]
    assert dist_sub == 4
    assert path_sub == [0, 2, 1, 3]


def test_tsp_solver_correctness():
    dist_matrix = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    expected_cost = 80

    cost_py = tsp.tsp_python(dist_matrix)
    cost_cy = tsp.tsp_cython(dist_matrix)
    cost_top = cc.solve_tsp(dist_matrix)
    cost_sub = tsp.solve_tsp(dist_matrix)

    assert cost_py == expected_cost
    assert cost_cy == expected_cost
    assert cost_top == expected_cost
    assert cost_sub == expected_cost


def test_package_metadata_and_acceleration():
    assert hasattr(cc, "__version__")
    assert cc.__version__ == "0.1.1"
    assert dijkstra.HAS_CYTHON is True
    assert tsp.HAS_CYTHON is True
