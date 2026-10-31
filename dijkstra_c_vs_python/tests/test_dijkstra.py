"""
Comprehensive Unit Tests for Dijkstra Solvers (Pure Python vs Cython C++)
"""

import os
import sys
import random
import pytest

# Ensure local dijkstra_fast_solver package is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dijkstra_fast_solver import (
    dijkstra_python,
    dijkstra_cython,
    dijkstra_path_python,
    dijkstra_path_cython,
    dijkstra_from_edges_python,
    dijkstra_from_edges_cython,
)
from dehradun_map.dehradun_graph import (
    build_dehradun_distance_matrix,
    NODES_COORDS,
    EDGES_DICTS,
)
from dehradun_map.route_solver import solve_multistop_route


def generate_random_graph(v: int, seed: int = 42) -> list[list[int]]:
    """Generates a dense symmetric graph matrix of size V x V."""
    rng = random.Random(seed)
    matrix = [[0] * v for _ in range(v)]
    for i in range(v):
        for j in range(i + 1, v):
            weight = rng.randint(1, 100)
            matrix[i][j] = weight
            matrix[j][i] = weight
    return matrix


def test_small_diamond_graph():
    # 0 -> 1 (weight 2), 0 -> 2 (weight 5), 1 -> 2 (weight 1), 1 -> 3 (weight 4), 2 -> 3 (weight 1)
    graph = [
        [0, 2, 5, 0],
        [2, 0, 1, 4],
        [5, 1, 0, 1],
        [0, 4, 1, 0],
    ]
    py_dist = dijkstra_python(graph, 0)
    cy_dist = dijkstra_cython(graph, 0)

    assert py_dist == cy_dist
    assert cy_dist == [0, 2, 3, 4]

    py_cost, py_path = dijkstra_path_python(graph, 0, 3)
    cy_cost, cy_path = dijkstra_path_cython(graph, 0, 3)

    assert py_cost == cy_cost == 4
    assert py_path == cy_path == [0, 1, 2, 3]


def test_dehradun_graph_parity():
    matrix = build_dehradun_distance_matrix()
    origin = 0   # UPES Bidholi
    target = 20  # Clock Tower

    py_dist = dijkstra_python(matrix, origin)
    cy_dist = dijkstra_cython(matrix, origin)

    assert py_dist == cy_dist, "Full distance array must match between Python and Cython"

    py_cost, py_path = dijkstra_path_python(matrix, origin, target)
    cy_cost, cy_path = dijkstra_path_cython(matrix, origin, target)

    assert py_cost == cy_cost, "Dehradun shortest distance must be identical"
    assert py_path == cy_path, "Dehradun shortest path sequence must be identical"
    assert cy_cost == 13800, f"Expected 13800m shortest route, got {cy_cost}"
    assert cy_path == [0, 1, 2, 3, 14, 15, 20]


@pytest.mark.parametrize("size", [20, 50, 100])
def test_random_matrices(size):
    graph = generate_random_graph(size, seed=100 + size)
    py_dist = dijkstra_python(graph, 0)
    cy_dist = dijkstra_cython(graph, 0)

    assert py_dist == cy_dist, f"Distance mismatch on random matrix V={size}"


def test_edge_dict_representation():
    """Validates the direct nodes [[x, y]] and edges [{s, d, w}] representation."""
    cy_cost, cy_path = dijkstra_from_edges_cython(NODES_COORDS, EDGES_DICTS, 0, 20)
    py_cost, py_path = dijkstra_from_edges_python(NODES_COORDS, EDGES_DICTS, 0, 20)

    assert cy_cost == py_cost == 13800
    assert cy_path == py_path == [0, 1, 2, 3, 14, 15, 20]


def test_multistop_route_json_export(tmp_path):
    """Validates multi-stop route calculation and JSON schema compliance."""
    test_json = tmp_path / "test_route.json"
    result = solve_multistop_route(
        origin_id=0,
        target_id=20,
        waypoint_ids=[21, 22, 23],  # Petrol pump, Friend, Restaurant
        optimize_order=True,
        export_json_path=str(test_json)
    )

    assert result["status"] == "success"
    assert result["summary"]["total_stops"] == 3
    assert result["summary"]["total_distance_km"] == 19.5
    assert len(result["nodes"]) == len(NODES_COORDS)
    assert len(result["edges"]) == len(EDGES_DICTS)
    assert test_json.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
