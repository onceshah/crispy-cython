"""
Dehradun Multi-Waypoint Interactive Map Generator
Generates standalone HTML map with multi-stop planning (Petrol Pump, Friend's House, Restaurant),
interactive waypoint selection, and JSON export.
"""

import os
import sys

# Ensure local imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dehradun_map.route_solver import solve_multistop_route
from app import get_html_content


def generate_interactive_map(output_path: str = "dehradun_shortest_path.html", export_json: str = "route_path.json"):
    # Default waypoints: Indian Oil Petrol (21), Friend Manduwala (22), Village Restaurant (23)
    default_waypoints = [21, 22, 23]

    # Solve route via Cython Dijkstra and export JSON
    route_data = solve_multistop_route(
        origin_id=0,
        target_id=20,
        waypoint_ids=default_waypoints,
        optimize_order=True,
        export_json_path=export_json
    )

    html_content = get_html_content()

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[SUCCESS] Multi-waypoint interactive map generated at: {os.path.abspath(output_path)}")
    print(f"Optimal Shortest Distance: {route_data['summary']['total_distance_km']} km")
    return output_path


if __name__ == "__main__":
    pkg_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    out_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(pkg_dir, "dehradun_shortest_path.html")
    out_json = os.path.join(pkg_dir, "route_path.json")
    generate_interactive_map(out_file, export_json=out_json)
