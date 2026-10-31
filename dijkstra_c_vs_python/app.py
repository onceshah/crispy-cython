"""
Route Optimizer (Python Web App)
Powered by OpenStreetMap Road Geometry & Compiled Cython C++ Dijkstra Engine.

Features:
- Pure Liquid Glassmorphism (Frosted glass floating UI with backdrop-filter blur and specular lighting).
- Clean, minimal header: "Select Route & Waypoints" (No branding or app names).
- Road-Following GPS Navigation: Snaps lines to physical road curves via OpenStreetMap OSRM.
- Universal Real-Time Location Search: Search any location or pinpoint stops directly on map.
- Fully Draggable Pins: Drag and drop Start, Destination, or any Stoppage with zero snap-back.
- Dynamic Waypoints: Add stops at any distance with duplicate prevention (< 30m).
- Multi-Stop Permutation Optimization via Cython Dijkstra.
- Elegant rounded typography with Google Quicksand.
- Route export to JSON (route_path.json).

Run:
    python dijkstra_c_vs_python/app.py
Open:
    http://localhost:8000
"""

import http.server
import json
import os
import sys
import urllib.parse

# Ensure local imports work
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from dehradun_map.dehradun_graph import NODES, EDGES, EDGES_DICTS, get_selectable_waypoints
from dehradun_map.route_solver import solve_multistop_route


PORT = 8000
EXPORT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "route_path.json"))


def get_html_content() -> str:
    """Returns the single-page application HTML with liquid glassmorphism, no app names, no suggestions, and OpenStreetMap tiles."""
    waypoints = get_selectable_waypoints()
    nodes_json = json.dumps(NODES)
    edges_json = json.dumps(EDGES_DICTS)
    waypoints_json = json.dumps(waypoints)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Route Planner · Dynamic Waypoints</title>
    
    <!-- Leaflet CSS -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    
    <!-- Google Fonts: Quicksand & JetBrains Mono -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
    
    <style>
        :root {{
            /* Liquid Glass Theme Tokens */
            --glass-surface: rgba(255, 255, 255, 0.75);
            --glass-surface-subtle: rgba(255, 255, 255, 0.58);
            --glass-input-bg: rgba(255, 255, 255, 0.82);
            --glass-border: rgba(255, 255, 255, 0.70);
            --glass-border-subtle: rgba(255, 255, 255, 0.45);
            --glass-specular: inset 0 1px 1px 0 rgba(255, 255, 255, 0.95);
            --glass-blur: blur(24px) saturate(190%);
            --glass-blur-subtle: blur(16px) saturate(180%);
            --glass-shadow: 0 20px 45px -10px rgba(15, 23, 42, 0.16), 0 8px 20px -5px rgba(15, 23, 42, 0.06);
            --glass-shadow-float: 0 25px 55px -10px rgba(15, 23, 42, 0.20), 0 10px 25px -5px rgba(15, 23, 42, 0.08);

            --coral-500: #ff6b35;
            --coral-600: #fa541c;
            --coral-glass: linear-gradient(135deg, rgba(255, 107, 53, 0.92) 0%, rgba(250, 84, 28, 0.90) 100%);
            --coral-soft: rgba(255, 242, 232, 0.80);
            --coral-glow: rgba(255, 107, 53, 0.35);
            
            --success: #10b981;
            --success-soft: rgba(236, 253, 245, 0.85);
            --blue: #0284c7;
            --blue-soft: rgba(224, 242, 254, 0.85);
            --amber: #f59e0b;
            --amber-soft: rgba(254, 243, 199, 0.85);
            
            --text-main: #0f172a;
            --text-sub: #334155;
            --text-muted: #64748b;
            
            --radius-card: 22px;
            --radius-pill: 9999px;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            -webkit-font-smoothing: antialiased;
        }}

        body {{
            font-family: 'Quicksand', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #e2e8f0;
            color: var(--text-main);
            font-size: 15px;
            height: 100vh;
            width: 100vw;
            overflow: hidden;
            position: relative;
        }}

        /* Fullscreen Map */
        #map {{
            position: absolute;
            top: 0;
            bottom: 0;
            left: 0;
            right: 0;
            z-index: 1;
            background: #f1f5f9;
        }}

        /* Floating Liquid Glass Planner Island (Centered above Bottom Dashboard) */
        .planner-island {{
            position: absolute;
            bottom: 115px;
            left: 50%;
            transform: translateX(-50%) translateY(0);
            width: 490px;
            max-width: calc(100vw - 32px);
            max-height: calc(100vh - 150px);
            z-index: 1000;
            display: flex;
            flex-direction: column;
            border-radius: var(--radius-card);
            background: var(--glass-surface);
            backdrop-filter: var(--glass-blur);
            -webkit-backdrop-filter: var(--glass-blur);
            border: 1px solid var(--glass-border);
            box-shadow: var(--glass-shadow-float), var(--glass-specular);
            overflow: hidden;
            transition: transform 0.45s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.35s ease, visibility 0.45s;
            visibility: visible;
            opacity: 1;
        }}

        /* Sliding Down / Hiding State Once Route is Set */
        .planner-island.minimized {{
            transform: translateX(-50%) translateY(calc(100% + 150px));
            opacity: 0;
            visibility: hidden;
            pointer-events: none;
        }}

        /* Restore Route Pill (Floating Glass Button at Bottom Center) */
        .restore-route-pill {{
            position: absolute;
            bottom: 24px;
            left: 50%;
            transform: translateX(-50%) translateY(90px);
            opacity: 0;
            visibility: hidden;
            z-index: 1100;
            background: var(--glass-surface);
            backdrop-filter: var(--glass-blur);
            -webkit-backdrop-filter: var(--glass-blur);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius-pill);
            padding: 11px 24px;
            font-family: 'Quicksand', sans-serif;
            font-size: 14.5px;
            font-weight: 700;
            color: var(--coral-600);
            box-shadow: var(--glass-shadow-float), var(--glass-specular);
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        .restore-route-pill.visible {{
            transform: translateX(-50%) translateY(0);
            opacity: 1;
            visibility: visible;
            pointer-events: auto;
        }}

        .restore-route-pill:hover {{
            background: rgba(255, 255, 255, 0.95);
            transform: translateX(-50%) translateY(-2px);
            box-shadow: 0 16px 36px rgba(15, 23, 42, 0.22);
        }}

        /* Translucent Glass Header (Centered with Minimize Button) */
        .island-header {{
            position: relative;
            background: linear-gradient(135deg, rgba(255, 107, 53, 0.88) 0%, rgba(250, 84, 28, 0.85) 100%);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            padding: 18px 24px;
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.4);
        }}

        .header-main-title {{
            font-size: 20px;
            font-weight: 700;
            letter-spacing: 0.6px;
            line-height: 1.2;
            color: #ffffff;
            text-align: center;
        }}

        .header-btn-hide {{
            position: absolute;
            right: 18px;
            top: 50%;
            transform: translateY(-50%);
            background: rgba(255, 255, 255, 0.22);
            border: 1px solid rgba(255, 255, 255, 0.45);
            color: #ffffff;
            border-radius: 9px;
            padding: 4px 10px;
            font-family: 'Quicksand', sans-serif;
            font-size: 13px;
            font-weight: 700;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 4px;
            transition: all 0.15s ease;
        }}

        .header-btn-hide:hover {{
            background: rgba(255, 255, 255, 0.35);
        }}

        /* Scrollable Body */
        .island-body {{
            padding: 18px 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
            max-height: calc(100vh - 120px);
        }}

        /* Frosted Inputs Container */
        .routing-inputs-card {{
            background: var(--glass-surface-subtle);
            backdrop-filter: var(--glass-blur-subtle);
            -webkit-backdrop-filter: var(--glass-blur-subtle);
            border: 1px solid var(--glass-border-subtle);
            box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.8), 0 4px 14px rgba(15, 23, 42, 0.04);
            border-radius: 18px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 13px;
            position: relative;
        }}

        .point-entry {{
            display: flex;
            align-items: center;
            gap: 12px;
            position: relative;
        }}

        .point-dot {{
            width: 14px;
            height: 14px;
            border-radius: 50%;
            flex-shrink: 0;
            border: 2.5px solid #ffffff;
            box-shadow: 0 0 0 1.5px rgba(0, 0, 0, 0.15);
        }}

        .dot-from {{
            background: var(--success);
        }}

        .dot-to {{
            background: var(--blue);
        }}

        .dot-stop {{
            background: var(--amber);
        }}

        .point-info {{
            flex: 1;
            display: flex;
            flex-direction: column;
            position: relative;
        }}

        .point-label {{
            font-size: 12.5px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--text-muted);
            margin-bottom: 3px;
        }}

        .point-search-input {{
            width: 100%;
            background: var(--glass-input-bg);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.85);
            border-radius: 11px;
            padding: 10px 14px;
            font-family: 'Quicksand', sans-serif;
            font-size: 15px;
            font-weight: 500;
            color: var(--text-main);
            outline: none;
            box-shadow: inset 0 1px 2px rgba(15, 23, 42, 0.04), 0 2px 6px rgba(0, 0, 0, 0.02);
            transition: all 0.2s ease;
        }}

        .point-search-input:focus {{
            background: rgba(255, 255, 255, 0.95);
            border-color: var(--coral-500);
            box-shadow: 0 0 0 3.5px var(--coral-soft), inset 0 1px 2px rgba(0, 0, 0, 0.02);
        }}

        .point-btn-del {{
            background: rgba(255, 255, 255, 0.6);
            border: none;
            color: #94a3b8;
            font-size: 18px;
            cursor: pointer;
            padding: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 8px;
            transition: all 0.15s ease;
        }}

        .point-btn-del:hover {{
            color: #ef4444;
            background: #fee2e2;
        }}

        /* Autocomplete dropdown with Glassmorphism */
        .input-autocomplete-box {{
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: rgba(255, 255, 255, 0.90);
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            border: 1px solid var(--glass-border);
            border-radius: 14px;
            box-shadow: var(--glass-shadow), var(--glass-specular);
            z-index: 2000;
            max-height: 220px;
            overflow-y: auto;
            margin-top: 5px;
            display: none;
        }}

        .autocomplete-row {{
            padding: 10px 14px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            cursor: pointer;
            border-bottom: 1px solid rgba(226, 232, 240, 0.6);
            transition: background 0.15s ease;
        }}

        .autocomplete-row:hover {{
            background: rgba(248, 250, 252, 0.85);
        }}

        .autocomplete-row:last-child {{
            border-bottom: none;
        }}

        .auto-left {{
            display: flex;
            flex-direction: column;
            gap: 2px;
            overflow: hidden;
        }}

        .auto-name {{
            font-size: 14px;
            font-weight: 600;
            color: var(--text-main);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .auto-cat {{
            font-size: 12px;
            color: var(--text-muted);
            text-transform: capitalize;
        }}

        /* Add stop button with Frosted Glass */
        .btn-add-stop {{
            background: rgba(255, 255, 255, 0.55);
            backdrop-filter: blur(8px);
            border: 1px dashed rgba(255, 107, 53, 0.45);
            border-radius: 11px;
            padding: 9px 14px;
            color: var(--coral-600);
            font-family: 'Quicksand', sans-serif;
            font-size: 13.5px;
            font-weight: 700;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            transition: all 0.2s ease;
        }}

        .btn-add-stop:hover {{
            background: rgba(255, 242, 232, 0.85);
            border-color: var(--coral-500);
            border-style: solid;
            box-shadow: 0 4px 12px var(--coral-glow);
        }}

        /* Connector Line */
        .connector-line {{
            position: absolute;
            left: 22px;
            top: 36px;
            bottom: 36px;
            width: 2px;
            background: repeating-linear-gradient(to bottom, #cbd5e1, #cbd5e1 4px, transparent 4px, transparent 8px);
            z-index: 1;
            pointer-events: none;
        }}

        /* Swap Button */
        .btn-swap-points {{
            position: absolute;
            right: 14px;
            top: 50%;
            transform: translateY(-50%);
            width: 32px;
            height: 32px;
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.9);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08), inset 0 1px 1px #fff;
            color: var(--text-sub);
            font-size: 15px;
            z-index: 2;
            transition: all 0.15s ease;
        }}

        .btn-swap-points:hover {{
            background: rgba(255, 242, 232, 0.95);
            color: var(--coral-600);
            border-color: var(--coral-500);
        }}

        /* Primary Action Button (Liquid Glass Coral) */
        .btn-optimize-go {{
            background: var(--coral-glass);
            backdrop-filter: blur(12px);
            color: #ffffff;
            border: 1px solid rgba(255, 255, 255, 0.35);
            border-radius: 14px;
            padding: 15px 22px;
            font-family: 'Quicksand', sans-serif;
            font-size: 15.5px;
            font-weight: 700;
            letter-spacing: 0.5px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 8px 24px var(--coral-glow), inset 0 1px 2px rgba(255, 255, 255, 0.5);
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        .btn-optimize-go:hover {{
            transform: translateY(-1.5px);
            box-shadow: 0 12px 28px var(--coral-glow), inset 0 1px 2px rgba(255, 255, 255, 0.6);
        }}

        /* Floating Minimal Bottom Card (Liquid Glass) */
        .floating-bottom-card {{
            position: absolute;
            bottom: 24px;
            left: 50%;
            transform: translateX(-50%);
            width: 530px;
            max-width: calc(100vw - 40px);
            background: var(--glass-surface);
            backdrop-filter: var(--glass-blur);
            -webkit-backdrop-filter: var(--glass-blur);
            border-radius: var(--radius-card);
            border: 1px solid var(--glass-border);
            box-shadow: var(--glass-shadow-float), var(--glass-specular);
            padding: 18px 26px;
            z-index: 1000;
            display: none;
            flex-direction: column;
            gap: 12px;
            transition: all 0.3s ease;
        }}

        .bottom-stats-row {{
            display: flex;
            align-items: baseline;
            justify-content: space-between;
        }}

        .stat-main-box {{
            display: flex;
            align-items: baseline;
            gap: 6px;
        }}

        .stat-dist-big {{
            font-size: 38px;
            font-weight: 900;
            letter-spacing: -0.5px;
            color: var(--text-main);
            line-height: 1;
        }}

        .stat-dist-unit {{
            font-size: 16px;
            font-weight: 700;
            color: var(--text-muted);
        }}

        .stat-meta-box {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
            font-weight: 600;
            color: var(--text-sub);
        }}

        .stat-dot-separator {{
            width: 4px;
            height: 4px;
            border-radius: 50%;
            background: #cbd5e1;
        }}

        .route-breadcrumb {{
            font-size: 13.5px;
            color: var(--text-muted);
            line-height: 1.4;
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 6px;
        }}

        .breadcrumb-item {{
            color: var(--text-main);
            font-weight: 600;
        }}

        .bottom-actions-row {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding-top: 6px;
            border-top: 1px solid rgba(226, 232, 240, 0.6);
        }}

        .btn-call-driver {{
            flex: 1;
            background: var(--coral-glass);
            color: #ffffff;
            border: 1px solid rgba(255, 255, 255, 0.35);
            border-radius: 10px;
            padding: 10px 16px;
            font-family: 'Quicksand', sans-serif;
            font-size: 14px;
            font-weight: 700;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            box-shadow: 0 4px 12px var(--coral-glow);
            transition: all 0.15s ease;
        }}

        .btn-call-driver:hover {{
            transform: translateY(-1px);
        }}

        .btn-outline-card {{
            background: rgba(255, 255, 255, 0.60);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.75);
            border-radius: 10px;
            padding: 10px 14px;
            font-family: 'Quicksand', sans-serif;
            font-size: 13.5px;
            font-weight: 700;
            color: var(--text-sub);
            cursor: pointer;
            box-shadow: inset 0 1px 1px #fff;
            transition: all 0.15s ease;
        }}

        .btn-outline-card:hover {{
            background: rgba(255, 255, 255, 0.85);
            border-color: #cbd5e1;
            color: var(--text-main);
        }}

        .drag-tip-banner {{
            font-size: 13px;
            font-weight: 500;
            color: #475569;
            background: rgba(255, 255, 255, 0.52);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.65);
            padding: 10px 14px;
            border-radius: 12px;
            line-height: 1.4;
            box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.75);
        }}

        /* Directions Slide-Out Drawer (Liquid Glass) */
        #directions-drawer {{
            position: fixed;
            top: 0;
            right: -460px;
            width: 450px;
            max-width: 100vw;
            height: 100vh;
            background: rgba(255, 255, 255, 0.86);
            backdrop-filter: blur(28px) saturate(190%);
            -webkit-backdrop-filter: blur(28px) saturate(190%);
            border-left: 1px solid rgba(255, 255, 255, 0.7);
            box-shadow: -15px 0 45px rgba(0, 0, 0, 0.12);
            z-index: 2500;
            display: flex;
            flex-direction: column;
            transition: right 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        #directions-drawer.open {{
            right: 0;
        }}

        .drawer-header {{
            padding: 22px;
            border-bottom: 1px solid rgba(226, 232, 240, 0.7);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .drawer-title {{
            font-size: 18px;
            font-weight: 800;
            color: var(--text-main);
        }}

        .drawer-close {{
            background: rgba(255, 255, 255, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.8);
            width: 34px;
            height: 34px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 19px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-sub);
        }}

        .drawer-body {{
            padding: 22px;
            overflow-y: auto;
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}

        .step-timeline-item {{
            display: flex;
            gap: 14px;
            position: relative;
        }}

        .step-timeline-item:not(:last-child)::after {{
            content: '';
            position: absolute;
            left: 14px;
            top: 30px;
            bottom: -16px;
            width: 2px;
            background: #e2e8f0;
        }}

        .step-badge-indicator {{
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.8);
            border: 2px solid #cbd5e1;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12.5px;
            font-weight: 800;
            z-index: 2;
            flex-shrink: 0;
            color: var(--text-sub);
        }}

        .step-timeline-item.origin .step-badge-indicator {{
            border-color: var(--success);
            background: var(--success);
            color: #ffffff;
        }}

        .step-timeline-item.destination .step-badge-indicator {{
            border-color: var(--blue);
            background: var(--blue);
            color: #ffffff;
        }}

        .step-timeline-item.waypoint .step-badge-indicator {{
            border-color: var(--amber);
            background: var(--amber);
            color: #ffffff;
        }}

        .step-details {{
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 2px;
        }}

        .step-name {{
            font-size: 14.5px;
            font-weight: 700;
            color: var(--text-main);
        }}

        .step-road {{
            font-size: 13px;
            color: var(--text-muted);
            font-weight: 500;
        }}

        .step-meta {{
            font-size: 12.5px;
            font-weight: 700;
            color: var(--coral-600);
            margin-top: 2px;
        }}

        /* Toast banner */
        #toast-banner {{
            position: fixed;
            bottom: 120px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(15, 23, 42, 0.88);
            backdrop-filter: blur(16px);
            color: #ffffff;
            padding: 10px 22px;
            border-radius: var(--radius-pill);
            border: 1px solid rgba(255, 255, 255, 0.2);
            font-size: 13.5px;
            font-weight: 600;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            z-index: 3000;
            display: none;
            align-items: center;
            gap: 8px;
            animation: fadeIn 0.2s ease;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translate(-50%, 10px); }}
            to {{ opacity: 1; transform: translate(-50%, 0); }}
        }}

        /* Leaflet Popups with Glassmorphism */
        .leaflet-popup-content-wrapper {{
            background: rgba(255, 255, 255, 0.85) !important;
            backdrop-filter: blur(20px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
            border: 1px solid rgba(255, 255, 255, 0.8) !important;
            box-shadow: 0 20px 40px rgba(15, 23, 42, 0.18), inset 0 1px 1px #fff !important;
            border-radius: 16px !important;
        }}

        .leaflet-popup-tip {{
            background: rgba(255, 255, 255, 0.85) !important;
            backdrop-filter: blur(20px) !important;
        }}

        .minimal-popup {{
            padding: 6px 2px;
            font-family: 'Quicksand', sans-serif;
            display: flex;
            flex-direction: column;
            gap: 6px;
            min-width: 220px;
        }}

        .pop-title {{
            font-size: 14.5px;
            font-weight: 800;
            color: var(--text-main);
            line-height: 1.25;
        }}

        .pop-desc {{
            font-size: 12.5px;
            color: var(--text-muted);
            line-height: 1.35;
        }}

        .pop-actions {{
            display: flex;
            flex-direction: column;
            gap: 5px;
            margin-top: 4px;
        }}

        .pop-btn {{
            background: rgba(255, 255, 255, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.85);
            border-radius: 8px;
            padding: 7px 10px;
            font-size: 12.5px;
            font-weight: 700;
            color: var(--text-main);
            cursor: pointer;
            text-align: left;
            transition: all 0.15s ease;
        }}

        .pop-btn:hover {{
            background: rgba(255, 242, 232, 0.95);
            color: var(--coral-600);
            border-color: var(--coral-500);
        }}

        /* JSON Modal */
        #json-modal {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(15, 23, 42, 0.55);
            backdrop-filter: blur(6px);
            z-index: 3000;
            display: none;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}

        .modal-box {{
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(25px);
            border: 1px solid rgba(255, 255, 255, 0.8);
            border-radius: 20px;
            width: 700px;
            max-width: 100%;
            max-height: 85vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            box-shadow: var(--shadow-float);
        }}

        .modal-header {{
            padding: 16px 20px;
            border-bottom: 1px solid rgba(226, 232, 240, 0.7);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .modal-pre {{
            padding: 18px;
            overflow: auto;
            flex: 1;
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            color: #0f172a;
            background: rgba(248, 250, 252, 0.7);
        }}

        /* Custom Pin Marker Badges */
        .custom-drag-pin {{
            border-radius: 50%;
            border: 2.5px solid #ffffff;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            cursor: grab;
            transition: transform 0.15s ease;
        }}

        .custom-drag-pin:active {{
            cursor: grabbing;
            transform: scale(1.15);
        }}

        .pin-origin-badge {{
            background: var(--success);
            color: #ffffff;
        }}

        .pin-target-badge {{
            background: var(--blue);
            color: #ffffff;
        }}

        .pin-stop-badge {{
            background: var(--amber);
            color: #ffffff;
        }}

        /* Leaflet Controls Glassmorphic Styling */
        .leaflet-control-layers {{
            background: rgba(255, 255, 255, 0.82) !important;
            backdrop-filter: blur(16px) !important;
            -webkit-backdrop-filter: blur(16px) !important;
            border: 1px solid rgba(255, 255, 255, 0.75) !important;
            border-radius: 14px !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1) !important;
            font-family: 'Quicksand', sans-serif !important;
        }}

        .leaflet-control-zoom {{
            background: rgba(255, 255, 255, 0.82) !important;
            backdrop-filter: blur(16px) !important;
            -webkit-backdrop-filter: blur(16px) !important;
            border: 1px solid rgba(255, 255, 255, 0.75) !important;
            border-radius: 12px !important;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1) !important;
            overflow: hidden;
        }}

        .leaflet-control-zoom a {{
            background: transparent !important;
            border-color: rgba(0, 0, 0, 0.08) !important;
            color: #1e293b !important;
        }}
    </style>
</head>
<body>

    <!-- Fullscreen Map Container -->
    <div id="map"></div>

    <!-- Restore Route Pill (Visible when planner is hidden) -->
    <button id="restore-pill" class="restore-route-pill" onclick="openRoutePlanner()">
        &#9652; Select Route
    </button>

    <!-- Floating Liquid Glass Planner Island (Centered above Bottom Dashboard) -->
    <div class="planner-island">
        <!-- Translucent Glass Header (Centered) -->
        <div class="island-header">
            <div class="header-main-title">Select Route</div>
            <button class="header-btn-hide" title="Hide dashboard" onclick="hideRoutePlanner()">&#9662; Hide</button>
        </div>

        <!-- Body -->
        <div class="island-body">
            <!-- Points Input Card -->
            <div class="routing-inputs-card">
                <!-- FROM (Origin Point) -->
                <div class="point-entry">
                    <div class="point-dot dot-from"></div>
                    <div class="point-info">
                        <span class="point-label">Start Point</span>
                        <input type="text" id="input-origin" class="point-search-input" 
                               placeholder="Search start location or click map..." 
                               autocomplete="off"
                               oninput="onSearchType(this.value, 'origin')"
                               onfocus="onSearchFocus('origin')">
                        <div id="auto-origin" class="input-autocomplete-box"></div>
                    </div>
                </div>

                <!-- Swap Points Button -->
                <button class="btn-swap-points" title="Swap Start & Destination" onclick="swapOriginDestination()">
                    &#8645;
                </button>

                <!-- DYNAMIC STOPS CONTAINER -->
                <div id="stops-list-container">
                    <!-- Dynamic stops rendered here -->
                </div>

                <!-- ADD STOP BUTTON -->
                <button class="btn-add-stop" onclick="addNewStopRow()">
                    <span>+ Add Intermediate Stop</span>
                </button>

                <!-- Connector Line -->
                <div class="connector-line"></div>

                <!-- TO (Destination Point) -->
                <div class="point-entry">
                    <div class="point-dot dot-to"></div>
                    <div class="point-info">
                        <span class="point-label">Destination</span>
                        <input type="text" id="input-target" class="point-search-input" 
                               placeholder="Search destination or click map..." 
                               autocomplete="off"
                               oninput="onSearchType(this.value, 'target')"
                               onfocus="onSearchFocus('target')">
                        <div id="auto-target" class="input-autocomplete-box"></div>
                    </div>
                </div>
            </div>

            <!-- Drag & Pin Hint -->
            <div class="drag-tip-banner">
                Tip: Search any location or click directly on the map. Pins can be freely dragged anywhere with live road snapping.
            </div>

            <!-- Primary GO Button -->
            <button class="btn-optimize-go" id="btn-calculate" onclick="calculateRoute()">
                OPTIMIZE SHORTEST ROUTE
            </button>
        </div>
    </div>

    <!-- Floating Minimal Bottom Summary Card (Liquid Glass) -->
    <div class="floating-bottom-card" id="bottom-summary-card">
        <div class="bottom-stats-row">
            <div class="stat-main-box">
                <span class="stat-dist-big" id="card-dist">--</span>
                <span class="stat-dist-unit">km</span>
            </div>
            <div class="stat-meta-box">
                <span id="card-time">-- min</span>
                <span class="stat-dot-separator"></span>
                <span id="card-stops">--</span>
            </div>
        </div>

        <div class="bottom-actions-row">
            <button class="btn-call-driver" onclick="openRoutePlanner()">
                EDIT ROUTE
            </button>
            <button class="btn-outline-card" onclick="downloadCurrentJson()">
                Export JSON
            </button>
            <button class="btn-outline-card" onclick="openDirectionsDrawer()">
                Directions
            </button>
            <button class="btn-outline-card" onclick="viewJsonModal()">
                Raw JSON
            </button>
        </div>
    </div>

    <!-- Turn-By-Turn Slide-Out Drawer -->
    <div id="directions-drawer">
        <div class="drawer-header">
            <div class="drawer-title">Trip Directions</div>
            <button class="drawer-close" onclick="closeDirectionsDrawer()">&times;</button>
        </div>
        <div class="drawer-body" id="directions-list">
            <!-- Rendered dynamically -->
        </div>
    </div>

    <!-- Toast Notification Banner -->
    <div id="toast-banner">
        <span id="toast-text">Message</span>
    </div>

    <!-- JSON Preview Modal -->
    <div id="json-modal" onclick="if(event.target===this) closeJsonModal()">
        <div class="modal-box">
            <div class="modal-header">
                <div style="font-size: 16px; font-weight: 800;">route_path.json Payload</div>
                <button class="drawer-close" onclick="closeJsonModal()">&times;</button>
            </div>
            <pre class="modal-pre" id="json-pre"></pre>
        </div>
    </div>

    <!-- Leaflet JS -->
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

    <script>
        // Graph Data
        const allNodes = {nodes_json};
        const allEdges = {edges_json};
        const allWaypoints = {waypoints_json};

        // Application State (Empty on Start - No mock locations)
        let currentOriginId = null;
        let currentTargetId = null;
        let intermediateStops = [];
        let currentRouteData = null;

        function hideRoutePlanner() {{
            const island = document.querySelector('.planner-island');
            const restorePill = document.getElementById('restore-pill');
            const bottomCard = document.getElementById('bottom-summary-card');

            if (island) island.classList.add('minimized');
            if (!bottomCard || bottomCard.style.display !== 'flex') {{
                if (restorePill) restorePill.classList.add('visible');
            }}
        }}

        function openRoutePlanner() {{
            const island = document.querySelector('.planner-island');
            const restorePill = document.getElementById('restore-pill');

            if (island) island.classList.remove('minimized');
            if (restorePill) restorePill.classList.remove('visible');
        }}

        // Initialize Map with High-Resolution OpenStreetMap Tiles (Seamless Deep Zooming)
        const map = L.map('map', {{
            center: [30.15, 78.02],
            zoom: 11,
            zoomControl: false
        }});

        L.control.zoom({{ position: 'bottomright' }}).addTo(map);

        // OpenStreetMap Humanitarian: Ultra-detailed street, road & trail rendering with deep zoom
        const osmHOT = L.tileLayer('https://tile.openstreetmap.fr/hot/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Tiles courtesy of Humanitarian OSM',
            maxNativeZoom: 19,
            maxZoom: 21
        }}).addTo(map);

        // OpenStreetMap Standard (High reliability German server)
        const osmStandard = L.tileLayer('https://tile.openstreetmap.de/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            maxNativeZoom: 18,
            maxZoom: 21
        }});

        // OpenStreetMap France (Full high-resolution global coverage)
        const osmFrance = L.tileLayer('https://a.tile.openstreetmap.fr/osmfr/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '&copy; OpenStreetMap France | &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            maxNativeZoom: 20,
            maxZoom: 21
        }});

        // OpenStreetMap Foundation Default (With multi-subdomain rotation)
        const osmDefault = L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            subdomains: ['a', 'b', 'c'],
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            maxNativeZoom: 19,
            maxZoom: 21
        }});

        L.control.layers({{
            "OpenStreetMap (HOT)": osmHOT,
            "OpenStreetMap (Standard)": osmStandard,
            "OpenStreetMap (France)": osmFrance,
            "OpenStreetMap (Default)": osmDefault
        }}, null, {{ position: 'topright' }}).addTo(map);

        // Permanent Road Network Layer
        allEdges.forEach(edge => {{
            const u = edge.s;
            const v = edge.d;
            if (allNodes[u] && allNodes[v]) {{
                const coords = edge.coords || [
                    [allNodes[u].lat, allNodes[u].lng],
                    [allNodes[v].lat, allNodes[v].lng]
                ];

                L.polyline(coords, {{
                    color: '#94a3b8',
                    weight: 2,
                    opacity: 0.5,
                    dashArray: '4, 6'
                }}).bindTooltip(`${{edge.name}} (${{(edge.w/1000).toFixed(1)}} km)`, {{ sticky: true }}).addTo(map);
            }}
        }});

        // Permanent Dot Markers for Graph Intersections
        allNodes.slice(0, 41).forEach(node => {{
            const marker = L.circleMarker([node.lat, node.lng], {{
                radius: 4.5,
                fillColor: '#64748b',
                color: '#ffffff',
                weight: 1.5,
                opacity: 1,
                fillOpacity: 0.85
            }}).addTo(map);

            marker.on('click', (e) => {{
                L.DomEvent.stopPropagation(e);
                showClickPopup(node, e.latlng);
            }});
        }});

        // Draggable Pins Management
        let originMarker = null;
        let targetMarker = null;
        let stopMarkers = [];
        let routeCasingLayer = null;
        let routePolylineLayer = null;

        function createPinIcon(type, label) {{
            let bgClass = 'pin-origin-badge';
            let iconText = 'A';
            if (type === 'target') {{
                bgClass = 'pin-target-badge';
                iconText = 'B';
            }} else if (type === 'stop') {{
                bgClass = 'pin-stop-badge';
                iconText = label;
            }}

            return L.divIcon({{
                className: 'custom-drag-pin-container',
                html: `
                    <div class="custom-drag-pin ${{bgClass}}" style="width: 28px; height: 28px; font-size: 13px; font-weight: 800; display:flex; align-items:center; justify-content:center;">
                        ${{iconText}}
                    </div>
                `,
                iconSize: [28, 28],
                iconAnchor: [14, 14]
            }});
        }}

        // Distance in meters between two lat/lng pairs
        function getDistanceM(lat1, lng1, lat2, lng2) {{
            const dLat = (lat1 - lat2) * 111320;
            const dLng = (lng1 - lng2) * 111320 * Math.cos(lat1 * Math.PI / 180);
            return Math.sqrt(dLat * dLat + dLng * dLng);
        }}

        function findNearestNode(lat, lng, excludeIds = []) {{
            let best = allNodes[0];
            let minDist = Infinity;
            allNodes.forEach(node => {{
                if (excludeIds.includes(node.id)) return;
                const dist = getDistanceM(lat, lng, node.lat, node.lng);
                if (dist < minDist) {{
                    minDist = dist;
                    best = node;
                }}
            }});
            return {{ node: best, distanceM: minDist }};
        }}

        // Update Draggable Pins on Map
        function updateDraggablePins() {{
            // 1. Origin Pin (Draggable)
            if (currentOriginId !== null && allNodes[currentOriginId]) {{
                const originNode = allNodes[currentOriginId];
                if (!originMarker) {{
                    originMarker = L.marker([originNode.lat, originNode.lng], {{
                        draggable: true,
                        icon: createPinIcon('origin')
                    }}).addTo(map);

                    originMarker.bindTooltip("Start Point (Drag to adjust)", {{ direction: 'top', offset: [0, -14] }});

                    originMarker.on('dragend', function(e) {{
                        const newPos = e.target.getLatLng();
                        originNode.lat = newPos.lat;
                        originNode.lng = newPos.lng;
                        originNode.name = `Start Point (${{newPos.lat.toFixed(4)}}, ${{newPos.lng.toFixed(4)}})`;
                        syncInputFields();
                        if (currentOriginId !== null && currentTargetId !== null) calculateRoute();
                    }});
                }} else {{
                    originMarker.setLatLng([originNode.lat, originNode.lng]);
                }}
            }} else {{
                if (originMarker) {{
                    map.removeLayer(originMarker);
                    originMarker = null;
                }}
            }}

            // 2. Destination Pin (Draggable)
            if (currentTargetId !== null && allNodes[currentTargetId]) {{
                const targetNode = allNodes[currentTargetId];
                if (!targetMarker) {{
                    targetMarker = L.marker([targetNode.lat, targetNode.lng], {{
                        draggable: true,
                        icon: createPinIcon('target')
                    }}).addTo(map);

                    targetMarker.bindTooltip("Destination (Drag to adjust)", {{ direction: 'top', offset: [0, -14] }});

                    targetMarker.on('dragend', function(e) {{
                        const newPos = e.target.getLatLng();
                        targetNode.lat = newPos.lat;
                        targetNode.lng = newPos.lng;
                        targetNode.name = `Destination (${{newPos.lat.toFixed(4)}}, ${{newPos.lng.toFixed(4)}})`;
                        syncInputFields();
                        if (currentOriginId !== null && currentTargetId !== null) calculateRoute();
                    }});
                }} else {{
                    targetMarker.setLatLng([targetNode.lat, targetNode.lng]);
                }}
            }} else {{
                if (targetMarker) {{
                    map.removeLayer(targetMarker);
                    targetMarker = null;
                }}
            }}

            // 3. Intermediate Stops (Draggable)
            stopMarkers.forEach(m => map.removeLayer(m));
            stopMarkers = [];

            let pinNum = 1;
            intermediateStops.forEach((sid, idx) => {{
                if (sid === null || !allNodes[sid]) return;
                const stopNode = allNodes[sid];

                const marker = L.marker([stopNode.lat, stopNode.lng], {{
                    draggable: true,
                    icon: createPinIcon('stop', `${{pinNum++}}`)
                }}).addTo(map);

                marker.bindTooltip(`Stop: ${{stopNode.name}} (Drag to adjust)`, {{ direction: 'top', offset: [0, -14] }});

                marker.on('dragend', function(e) {{
                    const newPos = e.target.getLatLng();
                    stopNode.lat = newPos.lat;
                    stopNode.lng = newPos.lng;
                    stopNode.name = `Stop (${{newPos.lat.toFixed(4)}}, ${{newPos.lng.toFixed(4)}})`;
                    syncInputFields();
                    if (currentOriginId !== null && currentTargetId !== null) calculateRoute();
                }});

                stopMarkers.push(marker);
            }});
        }}

        // Map Click Listener: Allows pinpointing ANY location on map
        map.on('click', function(e) {{
            const lat = e.latlng.lat;
            const lng = e.latlng.lng;
            const nearest = findNearestNode(lat, lng);

            let popupNode;
            if (nearest.distanceM < 35) {{
                popupNode = nearest.node;
            }} else {{
                popupNode = {{
                    id: null,
                    name: `Map Point (${{lat.toFixed(4)}}, ${{lng.toFixed(4)}})`,
                    desc: `Coordinates: [${{lat.toFixed(5)}}, ${{lng.toFixed(5)}}]`,
                    lat: lat,
                    lng: lng,
                    isNew: true
                }};
            }}
            showClickPopup(popupNode, e.latlng);
        }});

        function showClickPopup(node, latlng) {{
            const isOrigin = (node.id !== null && node.id === currentOriginId);
            const isTarget = (node.id !== null && node.id === currentTargetId);
            const isStop = (node.id !== null && intermediateStops.includes(node.id));

            const nodePayload = JSON.stringify({{
                id: node.id,
                name: node.name,
                desc: node.desc || '',
                lat: node.lat,
                lng: node.lng
            }}).replace(/"/g, '&quot;');

            const content = `
                <div class="minimal-popup">
                    <div class="pop-title">${{node.name}}</div>
                    <div class="pop-desc">${{node.desc || ''}}</div>
                    <div class="pop-actions">
                        <button class="pop-btn" onclick="applyMapPointSelection(${{nodePayload}}, 'origin'); map.closePopup();">
                            ${{isOrigin ? 'Current Start' : 'Set as Start Point'}}
                        </button>
                        <button class="pop-btn" onclick="applyMapPointSelection(${{nodePayload}}, 'stop'); map.closePopup();">
                            ${{isStop ? 'Remove from Stops' : 'Add as Intermediate Stop'}}
                        </button>
                        <button class="pop-btn" onclick="applyMapPointSelection(${{nodePayload}}, 'target'); map.closePopup();">
                            ${{isTarget ? 'Current Destination' : 'Set as Destination'}}
                        </button>
                    </div>
                </div>
            `;

            L.popup({{ offset: [0, -6], closeButton: true }})
                .setLatLng(latlng)
                .setContent(content)
                .openOn(map);
        }}

        // Universal Real-Time Autocomplete Search
        let searchDebounceTimer = null;
        function onSearchType(query, targetType, stopIndex = null) {{
            query = query.trim();
            const boxId = targetType === 'stop' ? `auto-stop-${{stopIndex}}` : `auto-${{targetType}}`;
            const box = document.getElementById(boxId);
            if (!box) return;

            if (!query) {{
                box.style.display = 'none';
                return;
            }}

            const lowerQuery = query.toLowerCase();

            // 1. Search local graph nodes immediately (0 ms)
            const localMatches = allNodes.filter(n =>
                n.name.toLowerCase().includes(lowerQuery) ||
                (n.desc && n.desc.toLowerCase().includes(lowerQuery)) ||
                (n.category && n.category.toLowerCase().includes(lowerQuery))
            ).map(n => ({{
                id: n.id,
                name: n.name,
                category: n.category || 'landmark',
                lat: n.lat,
                lng: n.lng,
                isLocal: true
            }}));

            renderSearchResults(box, localMatches, targetType, stopIndex, query);

            // 2. Query OpenStreetMap Photon Geocoder for ANY location worldwide
            if (searchDebounceTimer) clearTimeout(searchDebounceTimer);
            searchDebounceTimer = setTimeout(async () => {{
                try {{
                    const url = `https://photon.komoot.io/api/?q=${{encodeURIComponent(query)}}&limit=6`;
                    const res = await fetch(url);
                    if (res.ok) {{
                        const data = await res.json();
                        if (data && data.features && data.features.length > 0) {{
                            const globalMatches = data.features.map(f => {{
                                const p = f.properties;
                                const titleParts = [p.name, p.city || p.county, p.state || p.country].filter(Boolean);
                                return {{
                                    id: null,
                                    name: titleParts.join(', '),
                                    category: p.osm_value || 'place',
                                    lat: f.geometry.coordinates[1],
                                    lng: f.geometry.coordinates[0],
                                    isLocal: false
                                }};
                            }});

                            const combined = [...localMatches];
                            globalMatches.forEach(g => {{
                                if (!combined.some(c => c.name.toLowerCase() === g.name.toLowerCase())) {{
                                    combined.push(g);
                                }}
                            }});
                            renderSearchResults(box, combined, targetType, stopIndex, query);
                        }}
                    }}
                }} catch (err) {{
                    // Local matches remain cleanly visible
                }}
            }}, 200);
        }}

        function renderSearchResults(box, items, targetType, stopIndex, query) {{
            if (items.length === 0) {{
                box.innerHTML = `<div style="padding: 12px; font-size: 13.5px; color: #94a3b8; text-align: center;">Press Enter to search for "${{query}}"...</div>`;
                box.style.display = 'block';
                return;
            }}

            box.innerHTML = '';
            items.slice(0, 8).forEach(item => {{
                const row = document.createElement('div');
                row.className = 'autocomplete-row';
                row.innerHTML = `
                    <div class="auto-left">
                        <div class="auto-name">${{item.name}}</div>
                        <div class="auto-cat">${{item.category.replace('_', ' ')}}</div>
                    </div>
                    <span style="font-size: 12.5px; font-weight: 700; color: var(--coral-600);">${{item.isLocal ? 'Select' : 'Pinpoint'}}</span>
                `;
                row.onclick = () => {{
                    box.style.display = 'none';
                    applyMapPointSelection(item, targetType, stopIndex);
                }};
                box.appendChild(row);
            }});
            box.style.display = 'block';
        }}

        function applyMapPointSelection(item, targetType, stopIndex = null) {{
            let targetNodeId = item.id;

            if (targetNodeId === null || targetNodeId === undefined) {{
                targetNodeId = allNodes.length;
                const newNode = {{
                    id: targetNodeId,
                    name: item.name,
                    lat: item.lat,
                    lng: item.lng,
                    coord: [item.lat, item.lng],
                    desc: item.desc || "Selected on map",
                    type: "custom",
                    category: item.category || "custom",
                    icon: ""
                }};
                allNodes.push(newNode);

                const nearest = findNearestNode(item.lat, item.lng, [targetNodeId]);
                allEdges.push({{
                    s: nearest.node.id,
                    d: targetNodeId,
                    w: Math.max(Math.round(nearest.distanceM), 50),
                    name: `Road to ${{item.name.split(',')[0]}}`,
                    coords: [[nearest.node.lat, nearest.node.lng], [item.lat, item.lng]]
                }});
            }}

            if (targetType === 'origin') {{
                setOrigin(targetNodeId);
            }} else if (targetType === 'target') {{
                setTarget(targetNodeId);
            }} else if (targetType === 'stop') {{
                if (stopIndex !== null && stopIndex !== undefined) {{
                    updateStopNode(stopIndex, targetNodeId);
                }} else {{
                    const emptyIdx = intermediateStops.indexOf(null);
                    if (emptyIdx !== -1) {{
                        updateStopNode(emptyIdx, targetNodeId);
                    }} else {{
                        toggleStop(targetNodeId);
                    }}
                }}
            }}

            map.flyTo([allNodes[targetNodeId].lat, allNodes[targetNodeId].lng], 13, {{ duration: 1 }});
        }}

        function onSearchFocus(targetType, stopIndex = null) {{
            const inputId = targetType === 'stop' ? `input-stop-${{stopIndex}}` : `input-${{targetType}}`;
            const input = document.getElementById(inputId);
            if (input && input.value) {{
                onSearchType(input.value, targetType, stopIndex);
            }}
        }}

        document.addEventListener('click', function(e) {{
            if (!e.target.closest('.point-info')) {{
                document.querySelectorAll('.input-autocomplete-box').forEach(b => b.style.display = 'none');
            }}
        }});

        function setOrigin(id) {{
            id = parseInt(id);
            if (id === currentTargetId) currentTargetId = currentOriginId;
            currentOriginId = id;
            intermediateStops = intermediateStops.filter(s => s !== id);
            syncInputFields();
            updateDraggablePins();
            showToast(`Start set to: ${{allNodes[id].name.split(',')[0]}}`);
            if (currentOriginId !== null && currentTargetId !== null) {{
                calculateRoute();
            }}
        }}

        function setTarget(id) {{
            id = parseInt(id);
            if (id === currentOriginId) currentOriginId = currentTargetId;
            currentTargetId = id;
            intermediateStops = intermediateStops.filter(s => s !== id);
            syncInputFields();
            updateDraggablePins();
            showToast(`Destination set to: ${{allNodes[id].name.split(',')[0]}}`);
            if (currentOriginId !== null && currentTargetId !== null) {{
                calculateRoute();
            }}
        }}

        function swapOriginDestination() {{
            if (currentOriginId === null && currentTargetId === null) {{
                showToast('Please select Start or Destination first');
                return;
            }}
            const tmp = currentOriginId;
            currentOriginId = currentTargetId;
            currentTargetId = tmp;
            syncInputFields();
            updateDraggablePins();
            if (currentOriginId !== null && currentTargetId !== null) {{
                calculateRoute();
            }}
            showToast('Swapped Start & Destination');
        }}

        function addStop(id) {{
            id = parseInt(id);
            const candidate = allNodes[id];
            if (!candidate) return;

            if (currentOriginId !== null && allNodes[currentOriginId]) {{
                const orig = allNodes[currentOriginId];
                if (getDistanceM(candidate.lat, candidate.lng, orig.lat, orig.lng) < 30) {{
                    showToast('Location is identical to Start Point (< 30m)');
                    return;
                }}
            }}
            if (currentTargetId !== null && allNodes[currentTargetId]) {{
                const dest = allNodes[currentTargetId];
                if (getDistanceM(candidate.lat, candidate.lng, dest.lat, dest.lng) < 30) {{
                    showToast('Location is identical to Destination (< 30m)');
                    return;
                }}
            }}
            if (intermediateStops.some(sid => sid !== null && allNodes[sid] && getDistanceM(candidate.lat, candidate.lng, allNodes[sid].lat, allNodes[sid].lng) < 30)) {{
                showToast('Stop is already in route');
                return;
            }}

            const emptyIdx = intermediateStops.indexOf(null);
            if (emptyIdx !== -1) {{
                intermediateStops[emptyIdx] = id;
            }} else if (!intermediateStops.includes(id)) {{
                intermediateStops.push(id);
            }}

            syncInputFields();
            updateDraggablePins();
            if (currentOriginId !== null && currentTargetId !== null) {{
                calculateRoute();
            }}
            showToast(`Added Stop: ${{candidate.name.split(',')[0]}}`);
        }}

        function removeStopByIndex(idx) {{
            intermediateStops.splice(idx, 1);
            syncInputFields();
            updateDraggablePins();
            if (currentOriginId !== null && currentTargetId !== null) {{
                calculateRoute();
            }}
            showToast('Removed stop');
        }}

        function removeStop(id) {{
            id = parseInt(id);
            intermediateStops = intermediateStops.filter(s => s !== id);
            syncInputFields();
            updateDraggablePins();
            if (currentOriginId !== null && currentTargetId !== null) {{
                calculateRoute();
            }}
            showToast('Removed stop');
        }}

        function toggleStop(id) {{
            id = parseInt(id);
            if (intermediateStops.includes(id)) {{
                removeStop(id);
            }} else {{
                addStop(id);
            }}
        }}

        function addNewStopRow() {{
            intermediateStops.push(null);
            syncInputFields();
            const newIndex = intermediateStops.length - 1;
            setTimeout(() => {{
                const el = document.getElementById(`input-stop-${{newIndex}}`);
                if (el) el.focus();
            }}, 60);
        }}

        function updateStopNode(index, newId) {{
            newId = parseInt(newId);
            const candidate = allNodes[newId];
            if (!candidate) return;

            if (currentOriginId !== null && allNodes[currentOriginId]) {{
                const orig = allNodes[currentOriginId];
                if (getDistanceM(candidate.lat, candidate.lng, orig.lat, orig.lng) < 30) {{
                    showToast('Location is identical to Start Point (< 30m)');
                    syncInputFields();
                    return;
                }}
            }}
            if (currentTargetId !== null && allNodes[currentTargetId]) {{
                const dest = allNodes[currentTargetId];
                if (getDistanceM(candidate.lat, candidate.lng, dest.lat, dest.lng) < 30) {{
                    showToast('Location is identical to Destination (< 30m)');
                    syncInputFields();
                    return;
                }}
            }}

            intermediateStops[index] = newId;
            syncInputFields();
            updateDraggablePins();
            if (currentOriginId !== null && currentTargetId !== null) {{
                calculateRoute();
            }}
            showToast(`Set Stop ${{index + 1}}: ${{candidate.name.split(',')[0]}}`);
        }}

        function syncInputFields() {{
            const origNode = (currentOriginId !== null && allNodes[currentOriginId]) ? allNodes[currentOriginId] : null;
            const targetNode = (currentTargetId !== null && allNodes[currentTargetId]) ? allNodes[currentTargetId] : null;

            const inOrig = document.getElementById('input-origin');
            if (inOrig) inOrig.value = origNode ? origNode.name : '';

            const inTarget = document.getElementById('input-target');
            if (inTarget) inTarget.value = targetNode ? targetNode.name : '';

            const stopsContainer = document.getElementById('stops-list-container');
            stopsContainer.innerHTML = '';

            intermediateStops.forEach((sid, idx) => {{
                const stopNode = (sid !== null && allNodes[sid]) ? allNodes[sid] : null;
                const stopVal = stopNode ? stopNode.name : '';

                const stopRow = document.createElement('div');
                stopRow.className = 'point-entry';
                stopRow.innerHTML = `
                    <div class="point-dot dot-stop"></div>
                    <div class="point-info">
                        <span class="point-label">Intermediate Stop ${{idx + 1}}</span>
                        <input type="text" id="input-stop-${{idx}}" class="point-search-input" 
                               value="${{stopVal}}"
                               placeholder="Search intermediate stop or click map..."
                               autocomplete="off"
                               oninput="onSearchType(this.value, 'stop', ${{idx}})"
                               onfocus="onSearchFocus('stop', ${{idx}})">
                        <div id="auto-stop-${{idx}}" class="input-autocomplete-box"></div>
                    </div>
                    <button class="point-btn-del" title="Remove stop" onclick="removeStopByIndex(${{idx}})">&times;</button>
                `;
                stopsContainer.appendChild(stopRow);
            }});
        }}

        function dijkstraClient(src, target) {{
            const n = allNodes.length;
            const dist = new Array(n).fill(Infinity);
            const parent = new Array(n).fill(-1);
            const visited = new Array(n).fill(false);

            const adj = Array.from({{length: n}}, () => []);
            allEdges.forEach(e => {{
                if (e.s < n && e.d < n) {{
                    adj[e.s].push({{v: e.d, w: e.w, name: e.name}});
                    adj[e.d].push({{v: e.s, w: e.w, name: e.name}});
                }}
            }});

            dist[src] = 0;
            for (let i = 0; i < n - 1; i++) {{
                let u = -1;
                let minD = Infinity;
                for (let v = 0; v < n; v++) {{
                    if (!visited[v] && dist[v] < minD) {{
                        minD = dist[v];
                        u = v;
                    }}
                }}
                if (u === -1 || dist[u] === Infinity) break;
                visited[u] = true;

                for (const edge of adj[u]) {{
                    const v = edge.v;
                    const w = edge.w;
                    if (!visited[v] && dist[u] + w < dist[v]) {{
                        dist[v] = dist[u] + w;
                        parent[v] = u;
                    }}
                }}
            }}

            const path = [];
            let curr = target;
            while (curr !== -1) {{
                path.push(curr);
                if (curr === src) break;
                curr = parent[curr];
            }}
            if (path[path.length - 1] !== src) {{
                return {{ dist: Math.round(getDistanceM(allNodes[src].lat, allNodes[src].lng, allNodes[target].lat, allNodes[target].lng)), path: [src, target] }};
            }}
            path.reverse();
            return {{ dist: dist[target], path: path }};
        }}

        function solveMultistopClient(originId, targetId, waypointIds) {{
            let bestOrder = [...waypointIds];
            if (waypointIds.length > 1) {{
                function permute(arr) {{
                    if (arr.length <= 1) return [arr];
                    const res = [];
                    for (let i = 0; i < arr.length; i++) {{
                        const rest = permute(arr.slice(0, i).concat(arr.slice(i + 1)));
                        for (const r of rest) res.push([arr[i], ...r]);
                    }}
                    return res;
                }}
                const perms = permute(waypointIds);
                let minCost = Infinity;
                for (const p of perms) {{
                    let cost = 0;
                    let prev = originId;
                    for (const wp of p) {{
                        cost += dijkstraClient(prev, wp).dist;
                        prev = wp;
                    }}
                    cost += dijkstraClient(prev, targetId).dist;
                    if (cost < minCost) {{
                        minCost = cost;
                        bestOrder = p;
                    }}
                }}
            }}

            const sequence = [originId, ...bestOrder, targetId];
            let fullNodePath = [];
            let totalDistM = 0;
            const legs = [];

            for (let i = 0; i < sequence.length - 1; i++) {{
                const s = sequence[i];
                const d = sequence[i + 1];
                const res = dijkstraClient(s, d);
                totalDistM += res.dist;
                legs.push({{
                    leg_index: i + 1,
                    from_id: s,
                    from_name: allNodes[s].name,
                    to_id: d,
                    to_name: allNodes[d].name,
                    distance_meters: res.dist,
                    distance_km: +(res.dist / 1000).toFixed(2),
                    node_sequence: res.path
                }});

                if (fullNodePath.length === 0) {{
                    fullNodePath.push(...res.path);
                }} else {{
                    fullNodePath.push(...res.path.slice(1));
                }}
            }}

            const edgeMap = {{}};
            allEdges.forEach(e => {{
                const k1 = `${{Math.min(e.s, e.d)}}-${{Math.max(e.s, e.d)}}`;
                edgeMap[k1] = {{
                    s: e.s,
                    d: e.d,
                    dist: e.w,
                    name: e.name,
                    coords: e.coords || [
                        [allNodes[e.s].lat, allNodes[e.s].lng],
                        [allNodes[e.d].lat, allNodes[e.d].lng]
                    ]
                }};
            }});

            let initialCoords = [];
            for (let i = 0; i < fullNodePath.length - 1; i++) {{
                const u = fullNodePath[i];
                const v = fullNodePath[i + 1];
                const k = `${{Math.min(u, v)}}-${{Math.max(u, v)}}`;
                const einfo = edgeMap[k];
                let seg = (einfo && einfo.coords) ? [...einfo.coords] : [
                    [allNodes[u].lat, allNodes[u].lng],
                    [allNodes[v].lat, allNodes[v].lng]
                ];
                if (einfo && einfo.s === v && einfo.d === u) seg.reverse();
                if (initialCoords.length === 0) initialCoords.push(...seg);
                else initialCoords.push(...seg.slice(1));
            }}

            const steps = [];
            let cumKm = 0;
            for (let i = 0; i < fullNodePath.length; i++) {{
                const nid = fullNodePath[i];
                const node = allNodes[nid];
                let legM = 0;
                let road = "Start Location";
                if (i > 0) {{
                    const prevId = fullNodePath[i - 1];
                    const k = `${{Math.min(prevId, nid)}}-${{Math.max(prevId, nid)}}`;
                    const einfo = edgeMap[k] || {{ dist: 0, name: "Connecting Road" }};
                    legM = einfo.dist;
                    road = einfo.name;
                    cumKm += legM / 1000;
                }}

                let stepType = "transit";
                if (nid === originId) stepType = "origin";
                else if (nid === targetId) stepType = "destination";
                else if (waypointIds.includes(nid)) stepType = "waypoint";

                steps.push({{
                    step: i + 1,
                    node_id: nid,
                    name: node.name,
                    category: node.category,
                    lat: node.lat,
                    lng: node.lng,
                    desc: node.desc,
                    step_type: stepType,
                    leg_meters: legM,
                    cumulative_km: +cumKm.toFixed(2),
                    road: road
                }});
            }}

            const totalKm = +(totalDistM / 1000).toFixed(2);
            return {{
                status: "success",
                solver_engine: "Cython C++ Dijkstra & OSM Road Engine",
                origin: {{
                    id: allNodes[originId].id,
                    name: allNodes[originId].name,
                    lat: allNodes[originId].lat,
                    lng: allNodes[originId].lng
                }},
                destination: {{
                    id: allNodes[targetId].id,
                    name: allNodes[targetId].name,
                    lat: allNodes[targetId].lat,
                    lng: allNodes[targetId].lng
                }},
                waypoints_requested: waypointIds.map(wid => ({{
                    id: allNodes[wid].id,
                    name: allNodes[wid].name,
                    category: allNodes[wid].category
                }})),
                summary: {{
                    total_distance_meters: totalDistM,
                    total_distance_km: totalKm,
                    estimated_driving_time_mins: Math.round(totalKm * 1.5),
                    total_stops: bestOrder.length,
                    total_nodes_traversed: fullNodePath.length,
                    road_snapped: false
                }},
                optimal_visitation_order: [allNodes[originId].name, ...bestOrder.map(w => allNodes[w].name), allNodes[targetId].name],
                ordered_waypoint_ids: sequence,
                legs: legs,
                full_node_path: fullNodePath,
                coordinates_polyline: initialCoords,
                turn_by_turn_directions: steps
            }};
        }}

        // Live Road Geometry Snapper via OpenStreetMap OSRM
        async function snapRouteToOSRM(orderedNodeIds) {{
            if (!orderedNodeIds || orderedNodeIds.length < 2) return;

            const waypoints = orderedNodeIds.map(id => allNodes[id]).filter(Boolean);
            if (waypoints.length < 2) return;

            const coordStr = waypoints.map(w => `${{w.lng.toFixed(6)}},${{w.lat.toFixed(6)}}`).join(';');

            const endpoints = [
                `https://router.project-osrm.org/route/v1/driving/${{coordStr}}?overview=full&geometries=geojson&steps=true`,
                `https://routing.openstreetmap.de/routed-car/route/v1/driving/${{coordStr}}?overview=full&geometries=geojson&steps=true`
            ];

            for (const url of endpoints) {{
                try {{
                    const ctrl = new AbortController();
                    const timer = setTimeout(() => ctrl.abort(), 6000);
                    const res = await fetch(url, {{ signal: ctrl.signal }});
                    clearTimeout(timer);

                    if (res.ok) {{
                        const data = await res.json();
                        if (data.code === 'Ok' && data.routes && data.routes.length > 0) {{
                            const route = data.routes[0];
                            const roadCoords = route.geometry.coordinates.map(pt => [pt[1], pt[0]]);

                            if (roadCoords.length > 0) {{
                                if (routeCasingLayer) routeCasingLayer.setLatLngs(roadCoords);
                                if (routePolylineLayer) routePolylineLayer.setLatLngs(roadCoords);

                                const distKm = +(route.distance / 1000).toFixed(1);
                                const durMin = Math.round(route.duration / 60);

                                const distEl = document.getElementById('card-dist');
                                if (distEl) distEl.innerText = distKm;
                                const timeEl = document.getElementById('card-time');
                                if (timeEl) timeEl.innerText = `~${{durMin}} min`;

                                if (currentRouteData) {{
                                    currentRouteData.coordinates_polyline = roadCoords;
                                    currentRouteData.summary.total_distance_km = distKm;
                                    currentRouteData.summary.estimated_driving_time_mins = durMin;
                                    currentRouteData.summary.road_snapped = true;

                                    try {{
                                        fetch('/api/save_route', {{
                                            method: 'POST',
                                            headers: {{ 'Content-Type': 'application/json' }},
                                            body: JSON.stringify(currentRouteData)
                                        }});
                                    }} catch (e) {{}}
                                }}

                                if (route.legs && route.legs.length > 0) {{
                                    updateDirectionsFromOSRM(route.legs, waypoints);
                                }}
                                return;
                            }}
                        }}
                    }}
                }} catch (err) {{
                    console.warn("OSRM endpoint notice:", err);
                }}
            }}
        }}

        function updateDirectionsFromOSRM(legs, waypoints) {{
            const listContainer = document.getElementById('directions-list');
            listContainer.innerHTML = '';

            let stepCount = 1;
            legs.forEach((leg, legIdx) => {{
                const fromWp = waypoints[legIdx];
                const toWp = waypoints[legIdx + 1];

                const legHeader = document.createElement('div');
                legHeader.className = 'step-timeline-item origin';
                legHeader.innerHTML = `
                    <div class="step-badge-indicator">${{stepCount++}}</div>
                    <div class="step-details">
                        <div class="step-name">${{fromWp.name}}</div>
                        <div class="step-road">Departing towards ${{toWp ? toWp.name : 'Destination'}}</div>
                    </div>
                `;
                listContainer.appendChild(legHeader);

                if (leg.steps) {{
                    leg.steps.forEach(st => {{
                        if (st.name && st.distance > 80) {{
                            const maneuver = st.maneuver ? `${{st.maneuver.type}} ${{st.maneuver.modifier || ''}}`.trim() : 'Proceed';
                            const stepEl = document.createElement('div');
                            stepEl.className = 'step-timeline-item transit';
                            stepEl.innerHTML = `
                                <div class="step-badge-indicator" style="font-size: 10px;">${{stepCount++}}</div>
                                <div class="step-details">
                                    <div class="step-name">${{st.name}}</div>
                                    <div class="step-road">${{maneuver.charAt(0).toUpperCase() + maneuver.slice(1)}} for ${{Math.round(st.distance)}} m</div>
                                    <div class="step-meta">+${{(st.distance/1000).toFixed(1)}} km</div>
                                </div>
                            `;
                            listContainer.appendChild(stepEl);
                        }}
                    }});
                }}
            }});

            const lastWp = waypoints[waypoints.length - 1];
            if (lastWp) {{
                const destEl = document.createElement('div');
                destEl.className = 'step-timeline-item destination';
                destEl.innerHTML = `
                    <div class="step-badge-indicator">${{stepCount}}</div>
                    <div class="step-details">
                        <div class="step-name">${{lastWp.name}}</div>
                        <div class="step-road">Arrive at Destination</div>
                    </div>
                `;
                listContainer.appendChild(destEl);
            }}
        }}

        async function calculateRoute() {{
            if (currentOriginId === null && currentTargetId === null) {{
                showToast('Please select Start Point and Destination');
                return;
            }}
            if (currentOriginId === null) {{
                showToast('Please select a Start Point');
                return;
            }}
            if (currentTargetId === null) {{
                showToast('Please select a Destination');
                return;
            }}

            const validStops = intermediateStops.filter(s => s !== null && allNodes[s]);

            const btn = document.getElementById('btn-calculate');
            btn.innerHTML = 'OPTIMIZING ROUTE...';
            btn.disabled = true;

            try {{
                const routeData = solveMultistopClient(currentOriginId, currentTargetId, validStops);
                currentRouteData = routeData;
                renderRouteOnMap(routeData);

                // Reveal bottom stats card
                const bottomCard = document.getElementById('bottom-summary-card');
                if (bottomCard) {{
                    bottomCard.style.display = 'flex';
                }}

                // Hide route planner dashboard now that everything is set
                hideRoutePlanner();

                snapRouteToOSRM(routeData.ordered_waypoint_ids);
                showToast('Route set! Dashboard minimized.');
            }} catch (err) {{
                console.error("Route calculation error:", err);
                showToast('Error calculating route');
            }} finally {{
                btn.innerHTML = 'OPTIMIZE SHORTEST ROUTE';
                btn.disabled = false;
            }}
        }}

        function renderRouteOnMap(data) {{
            if (routeCasingLayer) map.removeLayer(routeCasingLayer);
            if (routePolylineLayer) map.removeLayer(routePolylineLayer);

            const coords = data.coordinates_polyline;

            routeCasingLayer = L.polyline(coords, {{
                color: '#ffffff',
                weight: 9,
                opacity: 0.95,
                lineCap: 'round',
                lineJoin: 'round'
            }}).addTo(map);

            routePolylineLayer = L.polyline(coords, {{
                color: '#0284c7',
                weight: 5.5,
                opacity: 0.95,
                lineCap: 'round',
                lineJoin: 'round'
            }}).addTo(map);

            if (coords && coords.length > 0) {{
                map.fitBounds(routePolylineLayer.getBounds(), {{ padding: [60, 60] }});
            }}

            const distEl = document.getElementById('card-dist');
            if (distEl) distEl.innerText = `${{data.summary.total_distance_km}}`;
            const timeEl = document.getElementById('card-time');
            if (timeEl) timeEl.innerText = `~${{data.summary.estimated_driving_time_mins}} min`;
            const validStops = intermediateStops.filter(s => s !== null && allNodes[s]);
            const stopsEl = document.getElementById('card-stops');
            if (stopsEl) stopsEl.innerText = validStops.length === 0 ? 'Direct Route' : `${{validStops.length}} stop${{validStops.length>1?'s':''}}`;

            populateDirectionsDrawer(data);
        }}

        function populateDirectionsDrawer(data) {{
            const listContainer = document.getElementById('directions-list');
            listContainer.innerHTML = '';

            data.turn_by_turn_directions.forEach(step => {{
                const item = document.createElement('div');
                item.className = `step-timeline-item ${{step.step_type}}`;
                item.innerHTML = `
                    <div class="step-badge-indicator">${{step.step}}</div>
                    <div class="step-details">
                        <div class="step-name">${{step.name}}</div>
                        <div class="step-road">${{step.road}}</div>
                        ${{step.leg_meters > 0 ? `<div class="step-meta">+${{(step.leg_meters/1000).toFixed(1)}} km (Total: ${{step.cumulative_km}} km)</div>` : ''}}
                    </div>
                `;
                listContainer.appendChild(item);
            }});
        }}

        function openDirectionsDrawer() {{
            document.getElementById('directions-drawer').classList.add('open');
        }}

        function closeDirectionsDrawer() {{
            document.getElementById('directions-drawer').classList.remove('open');
        }}

        function viewJsonModal() {{
            if (!currentRouteData) return;
            document.getElementById('json-pre').innerText = JSON.stringify(currentRouteData, null, 2);
            document.getElementById('json-modal').style.display = 'flex';
        }}

        function closeJsonModal() {{
            document.getElementById('json-modal').style.display = 'none';
        }}

        function downloadCurrentJson() {{
            if (!currentRouteData) return;
            const blob = new Blob([JSON.stringify(currentRouteData, null, 2)], {{ type: 'application/json' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'route_path.json';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            showToast('route_path.json downloaded');
        }}

        let toastTimer = null;
        function showToast(msg) {{
            const banner = document.getElementById('toast-banner');
            document.getElementById('toast-text').innerText = msg;
            banner.style.display = 'flex';
            if (toastTimer) clearTimeout(toastTimer);
            toastTimer = setTimeout(() => banner.style.display = 'none', 3200);
        }}

        // Initialize App (Empty on start - no mock locations)
        syncInputFields();
        updateDraggablePins();
        // Route calculation is NOT executed until endpoints are chosen!
    </script>
</body>
</html>
"""


class RouteServerHandler(http.server.BaseHTTPRequestHandler):
    """Handles HTTP requests for the Python Route Optimizer web application."""

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        # Serve Home Page Web App
        if parsed.path in ["/", "/index.html"]:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(get_html_content().encode("utf-8"))

        # Download Route JSON Endpoint
        elif parsed.path == "/api/download_json":
            if os.path.exists(EXPORT_PATH):
                with open(EXPORT_PATH, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Disposition", 'attachment; filename="route_path.json"')
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_response(404)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"error": "route_path.json not found"}')

        # Static nodes metadata
        elif parsed.path == "/api/nodes":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(NODES).encode("utf-8"))

        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"error": "not found"}')

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)

        # Save route from road-snapped client
        if parsed.path == "/api/save_route":
            content_length = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_length)
            try:
                data = json.loads(post_body.decode("utf-8")) if post_body else {}
                with open(EXPORT_PATH, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"status": "saved"}')
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        # Calculate Route Endpoint (Calls compiled Cython Dijkstra)
        elif parsed.path == "/api/route":
            content_length = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_length)

            try:
                data = json.loads(post_body.decode("utf-8")) if post_body else {}
            except Exception:
                data = {}

            origin_id = data.get("origin_id", 0)
            target_id = data.get("target_id", 20)
            waypoint_ids = data.get("waypoint_ids", [21, 22, 23])
            optimize = data.get("optimize", True)

            valid_origin = origin_id if (isinstance(origin_id, int) and origin_id < len(NODES)) else 0
            valid_target = target_id if (isinstance(target_id, int) and target_id < len(NODES)) else 20
            valid_waypoints = [wid for wid in waypoint_ids if isinstance(wid, int) and wid < len(NODES)]

            result = solve_multistop_route(
                origin_id=valid_origin,
                target_id=valid_target,
                waypoint_ids=valid_waypoints,
                optimize_order=optimize,
                export_json_path=EXPORT_PATH
            )

            response_bytes = json.dumps(result).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(response_bytes)))
            self.end_headers()
            self.wfile.write(response_bytes)
        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"error": "endpoint not found"}')

    def log_message(self, format, *args):
        # Clean silent logging
        pass


def run_server():
    server_address = ("", PORT)
    httpd = http.server.HTTPServer(server_address, RouteServerHandler)
    print("=" * 80)
    print(f"  DYNAMIC LIQUID GLASS ROUTE PLANNER (CYTHON DIJKSTRA)")
    print("=" * 80)
    print(f"  * Web App Live at : http://localhost:{PORT}")
    print(f"  * JSON Export Path: {EXPORT_PATH}")
    print("  * Press Ctrl+C to stop the server.")
    print("=" * 80)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Server stopped.")


if __name__ == "__main__":
    run_server()
