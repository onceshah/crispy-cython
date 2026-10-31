"""
Command-Line Route Planner using Cython Dijkstra
Calculates the shortest route from UPES Bidholi to Clock Tower (Ghanta Ghar)
visiting any combination of Petrol Pump, Friend's House, and Restaurant,
and exports the path to JSON.

Usage:
    python plan_route.py
    python plan_route.py --petrol --friend --restaurant
    python plan_route.py --stops 21,22,23 --output route_path.json
"""

import argparse
import os
import sys

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure local imports work
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from dehradun_map.route_solver import solve_multistop_route
from dehradun_map.dehradun_graph import NODES


def parse_args():
    parser = argparse.ArgumentParser(
        description="Calculate shortest route in Dehradun visiting user waypoints using Cython Dijkstra."
    )
    parser.add_argument("--origin", type=int, default=0, help="Origin node ID (default: 0 for UPES Bidholi)")
    parser.add_argument("--target", type=int, default=20, help="Destination node ID (default: 20 for Clock Tower)")
    parser.add_argument("--petrol", action="store_true", help="Stop at Indian Oil Petrol Pump (Pondha)")
    parser.add_argument("--friend", action="store_true", help="Stop at Friend's House (Manduwala)")
    parser.add_argument("--restaurant", action="store_true", help="Stop at The Village Restaurant (Manduwala)")
    parser.add_argument("--petrol2", action="store_true", help="Stop at HP Petrol Pump (Nanda Ki Chowki)")
    parser.add_argument("--friend2", action="store_true", help="Stop at Friend's House (Vasant Vihar)")
    parser.add_argument("--restaurant2", action="store_true", help="Stop at Black Pepper / Kalsang Restaurant")
    parser.add_argument("--stops", type=str, default="", help="Comma-separated node IDs to visit")
    parser.add_argument("--output", type=str, default="route_path.json", help="Path to export JSON route")
    parser.add_argument("--no-optimize", action="store_true", help="Visit waypoints in fixed order without permutation optimization")
    return parser.parse_args()


def main():
    args = parse_args()

    waypoint_ids = []
    if args.stops:
        waypoint_ids.extend([int(x.strip()) for x in args.stops.split(",") if x.strip()])
    else:
        # Default if no flags specified: user requested stops (petrol pump, friend's house, restaurant)
        if not (args.petrol or args.friend or args.restaurant or args.petrol2 or args.friend2 or args.restaurant2):
            args.petrol = True
            args.friend = True
            args.restaurant = True

        if args.petrol:
            waypoint_ids.append(21)
        if args.friend:
            waypoint_ids.append(22)
        if args.restaurant:
            waypoint_ids.append(23)
        if args.petrol2:
            waypoint_ids.append(24)
        if args.friend2:
            waypoint_ids.append(25)
        if args.restaurant2:
            waypoint_ids.append(26)

    print("=" * 80)
    print("      DEHRADUN MULTI-WAYPOINT ROUTE PLANNER (CYTHON DIJKSTRA)      ")
    print("=" * 80)
    print(f" Origin      : [{args.origin}] {NODES[args.origin]['name']}")
    print(f" Destination : [{args.target}] {NODES[args.target]['name']}")
    print(f" Stops to visit: {[NODES[w]['name'] for w in waypoint_ids]}")
    print("=" * 80)

    export_file = os.path.join(os.path.dirname(__file__), args.output) if not os.path.isabs(args.output) else args.output

    result = solve_multistop_route(
        origin_id=args.origin,
        target_id=args.target,
        waypoint_ids=waypoint_ids,
        optimize_order=not args.no_optimize,
        export_json_path=export_file
    )

    summary = result["summary"]
    print(f"\n[ROUTE COMPUTED SUCCESSFULLY]")
    print(f" * Total Shortest Distance : {summary['total_distance_km']} km ({summary['total_distance_meters']:,} meters)")
    print(f" * Estimated Driving Time  : ~{summary['estimated_driving_time_mins']} minutes")
    print(f" * Total Stops Visited     : {summary['total_stops']}")
    print(f" * Solver Engine           : {result['solver_engine']}")
    print(f"\nOptimal Route Order:")
    for idx, stop_name in enumerate(result["optimal_visitation_order"], 1):
        print(f"  {idx}. {stop_name}")

    print(f"\nTurn-by-turn Directions:")
    for step in result["turn_by_turn_directions"]:
        print(f"  Step {step['step']:02d}: [{step['category'].upper()}] {step['name']} (+{step['leg_meters']}m via {step['road']}) -> {step['cumulative_km']} km")

    print(f"\n[EXPORT COMPLETE] Route data exported to: {os.path.abspath(export_file)}")


if __name__ == "__main__":
    main()
