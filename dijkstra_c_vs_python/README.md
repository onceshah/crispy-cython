# DoonRoute · High-Performance Cython C++ Dijkstra Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python: 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![C++17](https://img.shields.io/badge/C++-17-00599C.svg?logo=c%2B%2B)](https://en.cppreference.com/w/cpp/17)
[![Cython](https://img.shields.io/badge/Cython-3.0+-gold.svg)](https://cython.org/)
[![Platform: Windows | Linux | macOS](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](#)

A high-performance **Dijkstra Shortest Path Engine** and **Multi-Stop Route Optimizer** combining native **C++** with a compiled **Cython** wrapper, benchmarked side-by-side against **Pure Python** across three distinct hardware machines. 

Built on a real-world **Dehradun Road Network Graph** navigating from **UPES Bidholi Campus** to the **Clock Tower (Ghanta Ghar)**, featuring live OpenStreetMap road snapping, liquid glassmorphic web visualization, and an industry-standard JSON routing payload.

---

## Table of Contents
- [1. Introduction](#1-introduction)
- [2. Project Layout](#2-project-layout)
- [3. Requirements & Installation](#3-requirements--installation)
- [4. About Algorithms](#4-about-algorithms)
  - [Dijkstra's Algorithm](#dijkstras-algorithm)
  - [Multi-Stop Permutation Optimization](#multi-stop-permutation-optimization)
  - [Why Cython C++ Beats Pure Python](#why-cython-c-beats-pure-python)
- [5. Intersection Snapping & Road Geometry](#5-intersection-snapping--road-geometry)
- [6. Benchmarking Methodology & Multi-Machine Results](#6-benchmarking-methodology--multi-machine-results)
  - [Cross-Machine Benchmark Chart](#cross-machine-benchmark-chart)
  - [Performance Comparison Table](#performance-comparison-table)
  - [Terminal Verification Runs](#terminal-verification-runs)
- [7. About the JSON Specification (`route_path.json`)](#7-about-the-json-specification-route_pathjson)
- [8. Frontend Architecture](#8-frontend-architecture)
  - [Liquid Glassmorphism](#liquid-glassmorphism)
  - [Interactive Draggable Pins](#interactive-draggable-pins)
  - [Dual Running Options](#dual-running-options)
- [9. How to Run](#9-how-to-run)
- [10. License & Acknowledgements](#10-license--acknowledgements)

---

## 1. Introduction

In modern GPS navigation and metropolitan route planning, graph routing queries must be solved in sub-millisecond latencies across hundreds of thousands of vertices. While Python offers rapid prototyping and high expressiveness, its interpreted bytecode loops, dynamic type dispatch, and object overhead impose severe performance penalties during heavy graph relaxation routines.

**DoonRoute** solves this by implementing Dijkstra's algorithm directly in native **C++**, compiled to machine code and linked to Python via **Cython**:
- **Speed**: Delivers **up to 31x acceleration** over pure Python across dense and real-world graphs.
- **Real-World Corridor**: Models the 19.5 km transit corridor connecting **UPES Bidholi Campus $\to$ Indian Oil Petrol Pump $\to$ Manduwala $\to$ Premnagar $\to$ Clock Tower (Ghanta Ghar)**.
- **Interoperability**: Decouples the compiled C++ solver from frontend visualization through a comprehensive JSON data contract (`route_path.json`).

---

## 2. Project Layout

```
dijkstra_c_vs_python/
├── cpp/
│   ├── dijkstra.h                      # Native C++ solver declarations & structs
│   └── dijkstra.cpp                    # High-performance C++ Dijkstra (O(V^2) & priority relaxation)
├── cython_wrapper/
│   ├── dijkstra_wrapper.pxd            # Cython C++ external declarations
│   └── dijkstra_wrapper.pyx            # Cython bridge converting Python types to std::vector
├── python_solver/
│   ├── __init__.py                     # Pure Python reference module
│   └── dijkstra_pure.py                # Pure Python matrix Dijkstra baseline & path reconstruction
├── dijkstra_fast_solver/               # Pip-installable Python package
│   ├── __init__.py                     # Package entry point (exposes dijkstra_cython & dijkstra_python)
│   └── dijkstra_pure.py                # Embedded Python reference fallback
├── dehradun_map/
│   ├── dehradun_graph.py               # Dehradun road graph nodes, GPS coordinates, & edge matrices
│   ├── route_solver.py                 # Multi-stop permutation solver & route_path.json exporter
│   └── generate_map.py                 # Generates standalone interactive HTML map
├── tests/
│   └── test_dijkstra.py                # Pytest suite verifying 100% mathematical parity
├── assets/
│   └── dijkstra_benchmark_3machines.jpg # Multi-machine 3-laptop benchmark infographic chart
├── Command prompt test/                # Terminal screenshots from 3 test laptops (3 runs each)
│   ├── VANSH 1 (1).png                 # Vansh (i7-13700HX) - Run 1
│   ├── VANSH 1 (2).png                 # Vansh (i7-13700HX) - Run 2
│   ├── VANSH 1 (3).png                 # Vansh (i7-13700HX) - Run 3
│   ├── AMBRISH 1.jpeg                  # Ambrish (i5-1135G7) - Run 1
│   ├── AMBRIS 2 AND 3.jpeg             # Ambrish (i5-1135G7) - Runs 2 & 3
│   └── LUX 1.jpeg                      # Lux (i5-12500H) - Runs 1, 2 & 3
├── app.py                              # Pure Python liquid glass web application (http.server)
├── streamlit_app.py                    # Streamlit component application
├── benchmark.py                        # Automated multi-tier benchmarking harness
├── plan_route.py                       # Command-line multi-stop route planner
├── route_path.json                     # Generated route payload specification
├── dehradun_shortest_path.html         # Standalone full-featured web app
├── setup.py                            # Setuptools compiler script with MSVC / MinGW auto-detection
├── pyproject.toml                      # Modern PEP 517/518 build specification
└── requirements.txt                    # Python environment dependencies
```

---

## 3. Requirements & Installation

### Prerequisites
- Python **3.8+** (Tested on Python 3.12.1 and 3.13.7)
- C++ Compiler (Optional for running with pure Python fallback; required for Cython acceleration):
  - **Windows**: Microsoft Visual C++ (MSVC via Build Tools) or MinGW-w64 (`gcc` / `g++`)
  - **Linux**: `gcc` / `g++` (`sudo apt install build-essential`)
  - **macOS**: `clang` (`xcode-select --install`)

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/onceshah/crispy-cython.git
   cd crispy-cython/dijkstra_c_vs_python
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Compile the Cython C++ extension in-place:**
   ```bash
   pip install -e .
   ```
   > *Note: If a C++ compiler is not present, `setup.py` automatically falls back to pure Python without failing.*

4. **Verify installation with tests:**
   ```bash
   pytest tests/test_dijkstra.py -v
   ```

---

## 4. About Algorithms

### Dijkstra's Algorithm
Dijkstra's algorithm finds the shortest path between nodes in a weighted graph with non-negative edge weights.
- **Time Complexity**: $O(V^2)$ on dense adjacency matrices, reducible to $O((V + E) \log V)$ with a binary min-heap priority queue.
- **Space Complexity**: $O(V)$ for distance arrays, visited bitsets, and parent tracking.
- **Path Reconstruction**: After the shortest path distances are finalized, backtracking through the `parent` array reconstructs the exact sequence of graph vertices.

### Multi-Stop Permutation Optimization
When visiting $K$ intermediate stops (such as Refueling $\to$ Friend's House $\to$ Restaurant) between Start Point $S$ and Destination $D$, the visitation order drastically impacts total travel time.
- The solver computes the cost matrix between all requested waypoints.
- It tests all $K!$ permutations to discover the optimal permutation that minimizes:
  $$\text{Total Distance} = \text{dist}(S, P_{\pi(1)}) + \sum_{i=1}^{K-1} \text{dist}(P_{\pi(i)}, P_{\pi(i+1)}) + \text{dist}(P_{\pi(K)}, D)$$
- For $K \le 6$ waypoints, evaluating permutations runs in under $0.5\,\text{ms}$ in Cython C++.

### Why Cython C++ Beats Pure Python

| Metric | Pure Python | Cython C++ | Architectural Advantage |
| :--- | :--- | :--- | :--- |
| **Data Representation** | Nested `list` of Python `int` objects | Contiguous 1D/2D `int*` C array | Continuous memory cache locality, zero pointer chasing |
| **Inner Loop Traversal** | Bytecode evaluation via CPython VM | Direct machine instructions | Eliminates Python VM evaluation overhead |
| **Type Dispatch** | Dynamic type checks on every addition | Static C++ type compilation | Compiles to zero-overhead CPU instructions |
| **GIL Impact** | Subject to GIL locking | Can release GIL (`nogil`) | True multi-threaded execution across graphs |

---

## 5. Intersection Snapping & Road Geometry

Standard graph theory algorithms treat edges as straight euclidean lines (chords), which cuts across buildings and rivers. **DoonRoute** implements true road-following geometry:

1. **Curved Polyline Mapping**: Every edge in the Dehradun graph stores dense GPS coordinate arrays tracing real terrain bends.
2. **Live OpenStreetMap (OSRM) Road Snapping**: The web interface queries OpenStreetMap's routing engine to snap lines directly to physical road geometry with lane-level fidelity.
3. **Universal Real-Time Geocoding**: Users can search any location globally via the OpenStreetMap Photon Geocoder or click any arbitrary point on the map.
4. **Duplicate Waypoint Prevention**: Implements a 30-meter Euclidean proximity threshold to prevent adding stops that coincide with existing endpoints.

---

## 6. Benchmarking Methodology & Multi-Machine Results

Benchmarks were conducted using high-precision monotonic timing (`timeit.default_timer()`) across multiple vertex counts ($V=41$ real Dehradun road graph, and synthetic graphs from $V=200$ to $V=1500$, generating up to $2,250,000$ matrix cells).

To ensure scientific rigor, benchmarks were executed **3 times on each of 3 separate laptops**:
1. **Machine 1 (Vansh)**: Intel Core i7-13700HX (24 Logical Threads), 15.7 GB RAM, Python 3.13.7
2. **Machine 2 (Ambrish)**: Intel Core i5-1135G7 (8 Logical Threads), 7.7 GB RAM, Python 3.12.1
3. **Machine 3 (Lux)**: Intel Core i5-12500H (16 Logical Threads), 15.6 GB RAM, Python 3.12.1

### Cross-Machine Benchmark Chart

![Dijkstra Multi-Machine Benchmark](assets/dijkstra_benchmark_3machines.jpg)

### Performance Comparison Table

| Graph / Benchmark Tier | Matrix Size ($V^2$) | i5-1135G7 (7.7 GB) | i5-12500H (15.6 GB) | i7-13700HX (15.7 GB) |
| :--- | :---: | :---: | :---: | :---: |
| **Dehradun Map ($V=41$)** | 1,681 cells | **$10\times$ faster** | **$9\times$ faster** | **$14\times$ faster** |
| **Dehradun Road (60 edges)** | 60 edges | **$31\times$ faster** | **$29\times$ faster** | **$28\times$ faster** |
| **Synthetic $V = 200$** | 40,000 cells | **$14\times$ faster** | **$15\times$ faster** | **$17\times$ faster** |
| **Synthetic $V = 500$** | 250,000 cells | **$11\times$ faster** | **$14\times$ faster** | **$15\times$ faster** |
| **Synthetic $V = 1000$** | 1,000,000 cells | **$12\times$ faster** | **$15\times$ faster** | **$16\times$ faster** |
| **Synthetic $V = 1500$ (Python vs Cython)** | 2,250,000 cells | $192\,\text{ms} \to 14.9\,\text{ms}$ (**$13\times$**) | $176\,\text{ms} \to 11.1\,\text{ms}$ (**$16\times$**) | $125\,\text{ms} \to 7.5\,\text{ms}$ (**$17\times$**) |

### Terminal Verification Runs

#### Machine 1: Intel Core i7-13700HX (Vansh Shah)
| Run 1 | Run 2 | Run 3 |
| :---: | :---: | :---: |
| <img src="Command%20prompt%20test/VANSH%201%20(1).png" width="280" /> | <img src="Command%20prompt%20test/VANSH%201%20(2).png" width="280" /> | <img src="Command%20prompt%20test/VANSH%201%20(3).png" width="280" /> |

#### Machine 2: Intel Core i5-1135G7 (Ambrish)
| Run 1 | Runs 2 & 3 |
| :---: | :---: |
| <img src="Command%20prompt%20test/AMBRISH%201.jpeg" width="420" /> | <img src="Command%20prompt%20test/AMBRIS%202%20AND%203.jpeg" width="420" /> |

#### Machine 3: Intel Core i5-12500H (Lux)
| Multi-Run Terminal Output |
| :---: |
| <img src="Command%20prompt%20test/LUX%201.jpeg" width="550" /> |

---

## 7. About the JSON Specification (`route_path.json`)

The algorithm exports the solved route into an industry-standard API contract (`route_path.json`). This decouples the C++ solver from any frontend client and enables automated unit testing.

```json
{
  "status": "success",
  "solver_engine": "Cython C++ Dijkstra",
  "summary": {
    "total_distance_meters": 19500,
    "total_distance_km": 19.5,
    "estimated_driving_time_mins": 54,
    "total_stops": 3,
    "total_nodes_traversed": 17
  },
  "origin": {
    "id": 0,
    "name": "UPES Bidholi Campus",
    "lat": 30.41589,
    "lng": 77.96644
  },
  "destination": {
    "id": 20,
    "name": "Clock Tower (Ghanta Ghar)",
    "lat": 30.32443,
    "lng": 78.04184
  },
  "optimal_visitation_order": [
    "UPES Bidholi Campus",
    "Indian Oil Petrol Pump (Pondha)",
    "Friend's House (Manduwala)",
    "The Village Cafe & Restaurant",
    "Clock Tower (Ghanta Ghar)"
  ],
  "legs": [ ... ],
  "coordinates_polyline": [ ... ],
  "turn_by_turn_directions": [ ... ]
}
```

- **`summary`**: Aggregated travel metrics (distance, driving time, number of waypoints).
- **`optimal_visitation_order`**: Mathematically optimal sequence of stop points.
- **`coordinates_polyline`**: Dense GPS points formatted for Leaflet, Mapbox, or Google Maps polylines.
- **`turn_by_turn_directions`**: Human-readable navigation steps with distance increments.

---

## 8. Frontend Architecture

### Liquid Glassmorphism
The user interface is designed using translucent liquid glass principles:
- Frosted glass cards with `backdrop-filter: blur(24px) saturate(190%)`.
- Google Quicksand typography with zero emojis for an uncluttered look.
- Centered floating layout positioned directly above the bottom summary dashboard.
- Smooth CSS `transform: translateY` transition that automatically slides the planner down and hides it once the route is optimized.

### Interactive Draggable Pins
- **Start Point (Green Pin A)**, **Destination (Blue Pin B)**, and **Intermediate Stops (Amber numbered pins)** can be dragged anywhere on the map without snap-back.
- Moving any pin immediately recalculates the Cython shortest path and snaps to live road curves.

### Dual Running Options
1. **Option A: Pure Python Standard Library (`http.server`)**
   - Zero external server dependencies, instant startup.
   ```bash
   python app.py
   ```
2. **Option B: Streamlit Web Application**
   - Built for environments where a Streamlit interface is required.
   ```bash
   streamlit run streamlit_app.py
   ```

---

## 9. How to Run

### 1. Launch the Interactive Web Application
```bash
python dijkstra_c_vs_python/app.py
# Open http://localhost:8000 in your browser
```

### 2. Run the Benchmark Harness
```bash
python dijkstra_c_vs_python/benchmark.py
```

### 3. Run Command-Line Route Optimization
```bash
python dijkstra_c_vs_python/plan_route.py --petrol --friend --restaurant
```

### 4. Execute the Test Suite
```bash
pytest dijkstra_c_vs_python/tests/test_dijkstra.py -v
```

---

## 10. License & Acknowledgements
- **License**: MIT Open Source License.
- **Map Data**: © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors, OSRM Project.
- **Developed for**: UPES B.Tech Computer Science & Engineering (Semester 7).
