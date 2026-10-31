"""
Multi-Stop Route Solver with Cython Dijkstra Engine
Finds the shortest route from Point A to Point B visiting any selected
intermediate stops (Petrol Pump, Friend's House, Restaurant) and exports to JSON.
"""

import json
import itertools
import os
import sys

# Ensure local imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dehradun_map.dehradun_graph import (
    NODES,
    EDGES,
    NODES_COORDS,
    EDGES_DICTS,
    NODES_META,
    build_dehradun_distance_matrix,
)

try:
    from dijkstra_fast_solver import dijkstra_path_cython
except ImportError:
    try:
        from dijkstra_wrapper import dijkstra_path_cython
    except ImportError:
        from python_solver import dijkstra_path_python as dijkstra_path_cython


def solve_multistop_route(
    origin_id: int = 0,
    target_id: int = 20,
    waypoint_ids: list[int] = None,
    optimize_order: bool = True,
    export_json_path: str = None
) -> dict:
    """
    Solves the shortest path from origin to target visiting all specified waypoints
    using the compiled Cython Dijkstra engine.
    
    Parameters:
        origin_id: Starting node index (default: 0 for UPES Bidholi).
        target_id: Destination node index (default: 20 for Clock Tower).
        waypoint_ids: List of node IDs to visit in between (e.g. Petrol Pump, Friend's House, Restaurant).
        optimize_order: If True, tests all permutations to find the optimal order of visitation.
        export_json_path: If provided, writes the complete route payload to a JSON file.
        
    Returns:
        dict: Complete structured route payload ready for frontend and API consumers.
    """
    matrix = build_dehradun_distance_matrix()
    if waypoint_ids is None:
        waypoint_ids = []

    # Map edges for quick road name, length, and curved geometry lookup
    edge_map = {}
    for e in EDGES_DICTS:
        u = e["s"]
        v = e["d"]
        edge_map[(min(u, v), max(u, v))] = {
            "s": u,
            "d": v,
            "dist": e["w"],
            "name": e["name"],
            "coords": e.get("coords", [NODES_COORDS[u], NODES_COORDS[v]]),
        }

    # If no waypoints requested, direct Dijkstra
    if not waypoint_ids:
        ordered_waypoints = []
        legs = [(origin_id, target_id)]
    else:
        # Determine visitation order
        if optimize_order and len(waypoint_ids) > 1:
            best_order = None
            min_total_cost = float("inf")

            for perm in itertools.permutations(waypoint_ids):
                current_cost = 0
                prev = origin_id
                for wp in perm:
                    leg_cost, _ = dijkstra_path_cython(matrix, prev, wp)
                    current_cost += leg_cost
                    prev = wp
                final_leg, _ = dijkstra_path_cython(matrix, prev, target_id)
                current_cost += final_leg

                if current_cost < min_total_cost:
                    min_total_cost = current_cost
                    best_order = list(perm)

            ordered_waypoints = best_order
        else:
            ordered_waypoints = list(waypoint_ids)

        # Build list of legs: origin -> wp1 -> wp2 -> ... -> target
        sequence = [origin_id] + ordered_waypoints + [target_id]
        legs = [(sequence[i], sequence[i + 1]) for i in range(len(sequence) - 1)]

    # Compute detailed path for each leg using Cython Dijkstra
    full_node_path = []
    legs_details = []
    total_distance_m = 0

    for idx, (src_node, dst_node) in enumerate(legs):
        leg_dist, leg_nodes = dijkstra_path_cython(matrix, src_node, dst_node)
        total_distance_m += leg_dist

        src_info = NODES[src_node]
        dst_info = NODES[dst_node]

        legs_details.append({
            "leg_index": idx + 1,
            "from_id": src_node,
            "from_name": src_info["name"],
            "to_id": dst_node,
            "to_name": dst_info["name"],
            "distance_meters": leg_dist,
            "distance_km": round(leg_dist / 1000.0, 2),
            "node_sequence": leg_nodes,
        })

        if not full_node_path:
            full_node_path.extend(leg_nodes)
        else:
            # Avoid repeating the joint node
            full_node_path.extend(leg_nodes[1:])

    # Generate step-by-step turn-by-turn navigation list
    steps = []
    cumulative_m = 0
    for idx in range(len(full_node_path)):
        node_id = full_node_path[idx]
        node = NODES[node_id]
        leg_m = 0
        road_name = "Start Point"

        if idx > 0:
            prev_id = full_node_path[idx - 1]
            e_info = edge_map.get(
                (min(prev_id, node_id), max(prev_id, node_id)),
                {"dist": 0, "name": "Connecting Link"}
            )
            leg_m = e_info["dist"]
            road_name = e_info["name"]
            cumulative_m += leg_m

        is_waypoint = node_id in waypoint_ids
        is_origin = (node_id == origin_id)
        is_dest = (node_id == target_id)

        step_type = "transit"
        if is_origin:
            step_type = "origin"
        elif is_dest:
            step_type = "destination"
        elif is_waypoint:
            step_type = "waypoint"

        steps.append({
            "step": idx + 1,
            "node_id": node_id,
            "name": node["name"],
            "category": node.get("category", "transit"),
            "icon": node.get("icon", ""),
            "lat": node["lat"],
            "lng": node["lng"],
            "desc": node["desc"],
            "step_type": step_type,
            "leg_meters": leg_m,
            "cumulative_km": round(cumulative_m / 1000.0, 2),
            "road": road_name,
        })

    # Build detailed curved polyline following actual roads (not straight line chords)
    coordinates = []
    for i in range(len(full_node_path) - 1):
        u = full_node_path[i]
        v = full_node_path[i + 1]
        pair_key = (min(u, v), max(u, v))
        e_info = edge_map.get(pair_key, {})
        seg_coords = e_info.get("coords")
        if not seg_coords:
            seg_coords = [NODES_COORDS[u], NODES_COORDS[v]]
        else:
            seg_coords = list(seg_coords)

        # If traversing in reverse direction (from d to s)
        if e_info.get("s") == v and e_info.get("d") == u:
            seg_coords = list(reversed(seg_coords))

        if not coordinates:
            coordinates.extend(seg_coords)
        else:
            coordinates.extend(seg_coords[1:])

    # Fallback if single node
    if not coordinates and full_node_path:
        coordinates = [NODES_COORDS[full_node_path[0]]]

    # Driving time estimate (Hilly/urban Dehradun ~25 km/h -> ~2.75 min/km)
    total_km = round(total_distance_m / 1000.0, 2)
    est_driving_mins = int(round(total_km * 2.75))

    origin_node = NODES[origin_id]
    target_node = NODES[target_id]

    # Assemble structured response
    result_payload = {
        "status": "success",
        "solver_engine": "Cython C++ Dijkstra",
        "graph_format": "Google Maps Road Graph (nodes: [[x, y]], edges: [{s, d, w, name}])",
        "nodes": NODES_COORDS,
        "edges": EDGES_DICTS,
        "nodes_metadata": NODES_META,
        "origin": {
            "id": origin_node["id"],
            "name": origin_node["name"],
            "lat": origin_node["lat"],
            "lng": origin_node["lng"],
            "icon": origin_node.get("icon", "")
        },
        "destination": {
            "id": target_node["id"],
            "name": target_node["name"],
            "lat": target_node["lat"],
            "lng": target_node["lng"],
            "icon": target_node.get("icon", "")
        },
        "waypoints_requested": [
            {
                "id": NODES[wid]["id"],
                "name": NODES[wid]["name"],
                "category": NODES[wid].get("category", "waypoint"),
                "icon": NODES[wid].get("icon", ""),
                "lat": NODES[wid]["lat"],
                "lng": NODES[wid]["lng"]
            }
            for wid in waypoint_ids
        ],
        "optimal_visitation_order": [
            NODES[nid]["name"] for nid in ([origin_id] + ordered_waypoints + [target_id])
        ],
        "summary": {
            "total_distance_meters": total_distance_m,
            "total_distance_km": total_km,
            "estimated_driving_time_mins": est_driving_mins,
            "total_stops": len(ordered_waypoints),
            "total_nodes_traversed": len(full_node_path),
        },
        "legs": legs_details,
        "full_node_path": full_node_path,
        "coordinates_polyline": coordinates,
        "turn_by_turn_directions": steps
    }

    # Export to JSON file if requested
    if export_json_path:
        with open(export_json_path, "w", encoding="utf-8") as f:
            json.dump(result_payload, f, indent=2)
        print(f"[SUCCESS] Shortest path exported to: {os.path.abspath(export_json_path)}")

    return result_payload

