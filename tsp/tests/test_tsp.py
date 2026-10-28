import pytest
import math
from tsp_fast_solver import tsp_python, tsp_cython
import tsp_wrapper

def test_empty_and_single_node():
    assert tsp_python([]) == 0
    assert tsp_cython([]) == 0
    assert tsp_python([[0]]) == 0
    assert tsp_cython([[0]]) == 0

def test_two_nodes():
    matrix = [
        [0, 15],
        [25, 0]
    ]
    # 0 -> 1 -> 0: cost = 15 + 25 = 40
    assert tsp_python(matrix) == 40
    assert tsp_cython(matrix) == 40

def test_four_nodes_known_solution():
    matrix = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    # Optimal route: 0 -> 1 -> 3 -> 2 -> 0 => 10 + 25 + 30 + 15 = 80
    assert tsp_python(matrix) == 80
    assert tsp_cython(matrix) == 80
    assert tsp_wrapper.tsp_cython(matrix) == 80

def test_five_nodes_symmetric():
    matrix = [
        [0, 12, 10, 19, 8],
        [12, 0, 3, 7, 2],
        [10, 3, 0, 6, 20],
        [19, 7, 6, 0, 4],
        [8, 2, 20, 4, 0]
    ]
    py_cost = tsp_python(matrix)
    cy_cost = tsp_cython(matrix)
    assert py_cost == cy_cost
    assert py_cost == 32  # 0 -> 4 -> 1 -> 2 -> 3 -> 0: 8 + 2 + 3 + 6 + 19 = 38, or 0 -> 4 -> 3 -> 2 -> 1 -> 0: 8 + 4 + 6 + 3 + 12 = 33, or 0->2->1->4->3->0: 10+3+2+4+19=38, or 0->1->4->3->2->0: 12+2+4+6+10 = 34, or 0->4->1->3->2->0: 8+2+7+6+10 = 33, or 0->2->3->4->1->0: 10+6+4+2+12 = 34, 0->4->1->2->3->0: 8+2+3+6+19=38, 0->4->3->1->2->0: 8+4+7+3+10 = 32!

def test_consistency_random_matrix():
    import random
    rng = random.Random(12345)
    for n in [6, 7, 8]:
        matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                val = rng.randint(5, 50)
                matrix[i][j] = val
                matrix[j][i] = val
        assert tsp_python(matrix) == tsp_cython(matrix)
