# crispy-cython

[![PyPI version](https://img.shields.io/pypi/v/crispy-cython.svg)](https://pypi.org/project/crispy-cython/)
[![PyPI - TSP Fast Solver](https://img.shields.io/badge/pypi-tsp--fast--solver-blue.svg)](https://pypi.org/project/tsp-fast-solver/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![C++17](https://img.shields.io/badge/C++-17-00599C.svg?logo=c%2B%2B)](https://en.cppreference.com/w/cpp/17)
[![Cython](https://img.shields.io/badge/Cython-3.0+-gold.svg)](https://cython.org/)

A collection of high-performance graph algorithms comparing **Pure Python** against **Native C/C++** accelerated using **Cython**.

Features two production-grade modules:
1. **Cython C++ Dijkstra Implementation**: Fast matrix and path reconstruction engine featuring a **real-world Dehradun road routing engine** from **UPES Bidholi to Clock Tower (Ghanta Ghar)** and **Mussoorie** with multi-stop optimization, live OpenStreetMap road snapping, liquid glassmorphism, and empirical multi-machine hardware benchmarks.
2. **Traveling Salesperson Problem (TSP)**: Exact factorial brute-force solver published on PyPI as [`tsp-fast-solver`](https://pypi.org/project/tsp-fast-solver/).

---

## Module 1) Cython C++ Dijkstra Implementation

Located in [`dijkstra_c_vs_python/`](dijkstra_c_vs_python/). Solves single-source shortest paths and reconstructs optimal multi-stop routes on dense matrix graphs and real-world metropolitan networks.

### 1. Project Introduction
In modern navigation systems, ride-hailing networks, and freight dispatch platforms, pathfinding engines must resolve complex graph routing queries in sub-millisecond latencies across hundreds of thousands of vertices. While Python offers rapid development, rich visualization tools, and clean syntax, its interpreted runtime introduces heavy overhead: dynamic typing checks, heap pointer indirection, and Python virtual machine (VM) bytecode execution loops.

This project implements an ultra-optimized hybrid routing system where performance-critical graph traversal routines are implemented in compiled **native C++ (C++17)**, bridged directly into Python using **Cython**, and visualized through an interactive **web dashboard**:
- **Computational Speedup**: Delivers **up to 31x acceleration** over pure Python across dense matrices and real-world topological networks.
- **Real-World Corridor**: Models the entire transit corridor connecting **Starting location -> Stop Points ->End Destination**
- **Multi-Stop Route Permutation Solver**: Automatically computes the mathematically optimal visitation sequence across multiple requested waypoints in minimal total travel distance and driving time.
- **Industry-Standard JSON Contract**: Decouples the compiled numerical solver from consumer interfaces through a structured data payload (`route_path.json`).

### 2. Cross-Machine Benchmark Evaluation (3 Laptops, 3 Runs Each)

![Dijkstra Multi-Machine Benchmark](https://raw.githubusercontent.com/onceshah/crispy-cython/main/assets/dijkstra_benchmark_3machines.jpg)

#### Hardware Comparison & Speedup Table

| Graph / Benchmark Tier | Matrix Size ($V^2$) | Intel Core i5-1135G7 (7.7 GB RAM) | Intel Core i5-12500H (15.6 GB RAM) | Intel Core i7-13700HX (15.7 GB RAM) |
| :--- | :---: | :---: | :---: | :---: |
| **Dehradun Map ($V=41$)** | 1,681 cells | **$10\times$ faster** | **$9\times$ faster** | **$14\times$ faster** |
| **Dehradun Road (60 edges)** | 60 edges | **$31\times$ faster** | **$29\times$ faster** | **$28\times$ faster** |
| **Synthetic $V = 200$** | 40,000 cells | **$14\times$ faster** | **$15\times$ faster** | **$17\times$ faster** |
| **Synthetic $V = 500$** | 250,000 cells | **$11\times$ faster** | **$14\times$ faster** | **$15\times$ faster** |
| **Synthetic $V = 1000$** | 1,000,000 cells | **$12\times$ faster** | **$15\times$ faster** | **$16\times$ faster** |
| **Synthetic $V = 1500$** | 2,250,000 cells | $192\,\text{ms} \to 14.9\,\text{ms}$ (**$13\times$**) | $176\,\text{ms} \to 11.1\,\text{ms}$ (**$16\times$**) | $125\,\text{ms} \to 7.5\,\text{ms}$ (**$17\times$**) |

#### Terminal Benchmark Runs (3 Machines, 3 Runs Each)

##### Machine 1: Intel Core i7-13700HX (Vansh)
| Run 1 | Run 2 | Run 3 |
| :---: | :---: | :---: |
| <img src="https://raw.githubusercontent.com/onceshah/crispy-cython/main/dijkstra_c_vs_python/Command%20prompt%20test/VANSH%201%20(1).png" width="300" /> | <img src="https://raw.githubusercontent.com/onceshah/crispy-cython/main/dijkstra_c_vs_python/Command%20prompt%20test/VANSH%201%20(2).png" width="300" /> | <img src="https://raw.githubusercontent.com/onceshah/crispy-cython/main/dijkstra_c_vs_python/Command%20prompt%20test/VANSH%201%20(3).png" width="300" /> |

##### Machine 2: Intel Core i5-1135G7 (Ambrish)
| Run 1 | Run 2 | Run 3 |
| :---: | :---: | :---: |
| <img src="https://raw.githubusercontent.com/onceshah/crispy-cython/main/dijkstra_c_vs_python/Command%20prompt%20test/AMBRISH%201.jpeg" width="300" /> | <img src="https://raw.githubusercontent.com/onceshah/crispy-cython/main/dijkstra_c_vs_python/Command%20prompt%20test/ambrish%202.jpeg" width="300" /> | <img src="https://raw.githubusercontent.com/onceshah/crispy-cython/main/dijkstra_c_vs_python/Command%20prompt%20test/AMBRIS%203.jpeg" width="300" /> |

##### Machine 3: Intel Core i5-12500H (Lakshya)
| Run 1 | Run 2 | Run 3 |
| :---: | :---: | :---: |
| <img src="https://raw.githubusercontent.com/onceshah/crispy-cython/main/dijkstra_c_vs_python/Command%20prompt%20test/LUX%201.jpeg" width="300" /> | <img src="https://raw.githubusercontent.com/onceshah/crispy-cython/main/dijkstra_c_vs_python/Command%20prompt%20test/LUX%202.jpeg" width="300" /> | <img src="https://raw.githubusercontent.com/onceshah/crispy-cython/main/dijkstra_c_vs_python/Command%20prompt%20test/LUX%203.jpeg" width="300" /> |

---

### 3. How Cython Works Under the Hood to Find the Most Optimal Path
1. **Contiguous 1D Memory Layout**:
   - Python 2D graphs are nested lists of lists where each row is a pointer to an array of pointers referencing individual Python integer objects.
   - The Cython wrapper (`cython_wrapper/dijkstra_wrapper.pyx`) immediately flattens the $V \times V$ matrix into a contiguous 1D C++ vector (`std::vector<int>`) with capacity pre-allocated via `vec.reserve(n * n)`.
   - Accessing edge $(u, v)$ requires simple linear arithmetic `graph[u * V + v]`, providing direct CPU cache locality and enabling hardware prefetching.
2. **Native Machine Code Execution (`cpp/dijkstra.cpp`)**:
   - Vertex relaxation runs natively without the Python Global Interpreter Lock (GIL), compiled via `-O3` to pure machine instructions.
   - Predecessor pointers in `parent[v] = u` allow exact $O(V)$ path reconstruction.
3. **Multi-Stop Permutation Optimization**:
   - When visiting $K$ intermediate waypoints between Start $S$ and Destination $D$, the solver precomputes all-pairs shortest paths using Cython Dijkstra and evaluates all $K!$ permutations:
     $$\text{Total Cost}(\pi) = \text{dist}(S, W_{\pi(1)}) + \sum_{i=1}^{K-1} \text{dist}(W_{\pi(i)}, W_{\pi(i+1)}) + \text{dist}(W_{\pi(K)}, D)$$
   - It discovers and selects the globally optimal sequence in under $0.5\,\text{ms}$.

---

### 4. Interactive Frontend Architecture

#### Frontend Screenshots

##### Route Selection Dialog
The user selects a Start Point, Destination, and multiple intermediate stops (e.g., Mussoorie Mall Road, Kempty Falls, Jharipani Waterfall, Clock Tower). The planner floats centrally above the map:

![Frontend Route Planner](https://raw.githubusercontent.com/onceshah/crispy-cython/main/assets/frontend_route_planner.jpg)

##### Turn-by-Turn Navigation & Itinerary Drawer
Clicking the "Directions" button opens the slide-out navigation panel, rendering step-by-step driving maneuvers, leg distances, and road names while preserving live map visibility:

![Frontend Trip Directions](https://raw.githubusercontent.com/onceshah/crispy-cython/main/assets/frontend_trip_directions.jpg)

##### Live Route Overview & Floating Metrics Dashboard
Once the route is solved, the central route planner slides down and hides, providing an unobstructed view of the complete mountain route with custom marker pins and the bottom summary dashboard:

![Frontend Route Overview](https://raw.githubusercontent.com/onceshah/crispy-cython/main/assets/frontend_route_overview.jpg)


---

### 5. How Driving Time and Distance are Calculated
Travel time is a nonlinear function of physical distance, terrain topography, road classifications, speed limits, and intersection turning delays:

1. **Live OSRM Real-Road Engine (Primary)**:
   - Queries OpenStreetMap's OSRM driving engine (`/route/v1/driving/...`).
   - OSRM incorporates road speed profiles: expressways / bypasses (~$50-65\text{ km/h}$), urban arterials (~$30-40\text{ km/h}$), and mountain passes (~$25-35\text{ km/h}$) accounting for sharp hairpin bends and elevation gradients.
   - It returns exact cumulative distance in meters (`route.distance`) and driving duration in seconds (`route.duration`):
     $$\text{Distance (km)} = \frac{\text{route.distance}}{1000}, \quad \text{Duration (minutes)} = \text{round}\left(\frac{\text{route.duration}}{60}\right)$$
   - *Example from the Screenshot*: For the $130\text{ km}$ mountain route encompassing Dehradun, Mussoorie, Kempty Falls, and Dhanaulti, the engine computes $179\text{ minutes}$, reflecting an average travel speed of:
     $$\text{Average Speed} = \frac{130\text{ km}}{179 / 60\text{ hours}} \approx 43.5\text{ km/h}$$
     This precisely mirrors real-world driving conditions on Uttarakhand mountain highways.

2. **Offline Graph Engine Fallback**:
   - If network connectivity is unavailable, the local solver (`route_solver.py`) computes route metrics using the Dehradun road graph.
   - Duration is estimated using an empirical urban/hilly travel rate of $25\text{ km/h}$ ($\approx 2.75\text{ minutes per km}$):
     $$\text{Estimated Driving Mins} = \text{int}(\text{round}(\text{total\_distance\_km} \times 2.75))$$

---

### 6. About the JSON File (`route_path.json`)

#### Why Generate a JSON File?
1. **Decoupling Numerical Solver from User Interfaces**: The compiled C++ and Cython calculation engines remain dedicated solely to graph theory. Emitting an industry-standard JSON schema creates a clean API boundary, allowing the identical route output to be consumed interchangeably by web browsers (Leaflet.js), Streamlit dashboards, mobile applications (iOS/Android), or autonomous vehicle navigation systems without changing C++ code.
2. **Automated Unit Testing & Continuous Integration (CI)**: Test suites (`tests/test_dijkstra.py`) deserialize `route_path.json` headlessly to verify path conservation, node sequence integrity, and waypoint order adherence without spinning up a browser.
3. **Portability & GIS Integration**: Universal standard format exportable into GeoJSON, QGIS, ArcGIS, or REST/WebSocket APIs.
4. **Telemetry & Turn-by-Turn Replay**: Records the exact solver version, timestamp, node IDs, distance increments, and maneuver steps.

#### JSON Payload Structure

```json
{
  "status": "success",
  "solver_engine": "Cython C++ Dijkstra",
  "summary": {
    "total_distance_km": 130.0,
    "total_distance_meters": 130000,
    "estimated_driving_time_mins": 179,
    "total_stops": 4,
    "total_nodes_traversed": 28,
    "road_snapped": true
  },
  "origin": {
    "id": 0,
    "name": "Start Point (30.4581, 78.2141)",
    "lat": 30.4581,
    "lng": 78.2141
  },
  "destination": {
    "id": 20,
    "name": "UPES Bidholi Campus",
    "lat": 30.41589,
    "lng": 77.96644
  },
  "optimal_visitation_order": [
    "Start Point (30.4581, 78.2141)",
    "Mussoorie (Mall Road / Library Chowk)",
    "Kempty Fall, Dhanaulti, Uttarakhand",
    "Jharipani Waterfall, Khalagon, Uttarakhand",
    "Clock Tower (Ghanta Ghar)",
    "UPES Bidholi Campus"
  ],
  "legs": [ ... ],
  "turn_by_turn_directions": [ ... ],
  "coordinates_polyline": [ ... ]
}
```

---

### 7. Running the Application
```bash
# Run web application
python dijkstra_c_vs_python/app.py

# Run Streamlit interface
streamlit run dijkstra_c_vs_python/streamlit_app.py
```

---

## Module 2: Traveling Salesperson Problem (TSP)

Located in `tsp/`. Exact factorial brute-force solver exploring all $(N - 1)!$ closed tours.

![TSP Benchmark Comparison](https://raw.githubusercontent.com/onceshah/crispy-cython/main/tsp_benchmark_comparison.png)

### Performance Benchmark (Pure Python vs C++ Cython)

| Graph Size ($N$) | Routes $(N-1)!$ | Pure Python | C++ (Cython) | Speedup |
| :---: | :---: | :---: | :---: | :---: |
| $N = 8$ | 5,040 | 2.1 ms | 0.033 ms | **~66x** |
| $N = 10$ | 362,880 | 149 ms | 1.42 ms | **~105x** |
| $N = 11$ | 3,628,800 | 1.63 s | 14.3 ms | **~114x** |

**Hardware & Methodology:**
- **CPU**: 13th Gen Intel Core i7-13700HX (16 cores, 24 threads)
- **RAM**: 16 GB DDR5
- **OS**: Windows 11 (64-bit)
- **Python**: 3.13.7
- **Compiler**: Clang / LLVM-MinGW (`-O3 -std=c++17 -static`)
- **Timing**: `timeit.default_timer()` monotonic QPC hardware clock.

---

## Why is C++ with Cython So Much Faster?

1. **Memory Layout & Cache Locality**: C++ stores graph matrices and distance tables in contiguous 1D memory buffers (`graph[u * V + v]`). These buffers fit directly into CPU L1/L2 caches, eliminating cache misses. In contrast, Python nested lists contain heap-allocated pointer arrays pointing to boxed integer objects scattered across memory.
2. **Zero Heap Allocation in Inner Loops**: C++ performs in-place array scans with raw pointers (`const int* row = &graph[u * V]`). Python creates temporary iterator and tuple objects that trigger garbage collection overhead.
3. **No Interpreter Overhead**: Python decodes bytecode, checks dynamic types, and increments/decrements reference counts on every cycle. Compiled C++ executes pure machine assembly.

---

## Repository Structure

```
Cython/
├── dijkstra_c_vs_python/               # Module 1: Dijkstra Shortest Path Solver
│   ├── cpp/
│   │   ├── dijkstra.h                  # C++ solver header
│   │   └── dijkstra.cpp                # C++ implementation with path tracking
│   ├── cython_wrapper/
│   │   ├── dijkstra_wrapper.pxd        # Cython declarations
│   │   └── dijkstra_wrapper.pyx        # Cython wrapper
│   ├── python_solver/
│   │   └── dijkstra_pure.py            # Pure Python baseline
│   ├── dijkstra_fast_solver/           # Packaged module
│   ├── dehradun_map/
│   │   ├── dehradun_graph.py           # Real Dehradun road network graph
│   │   └── generate_map.py             # Generates interactive Leaflet HTML map
│   ├── Command prompt test/            # Terminal verification runs (3 runs on 3 laptops)
│   ├── assets/                         # Visual assets & frontend screenshots
│   ├── tests/
│   │   └── test_dijkstra.py            # Pytest test suite
│   ├── benchmark.py                    # Dijkstra benchmark script
│   ├── generate_chart.py               # Visual comparison chart generator
│   ├── setup.py                        # Setuptools build script
│   └── pyproject.toml                  # PEP 517 configuration
├── tsp/                                # Module 2: Traveling Salesperson Problem Solver
│   ├── cpp/
│   ├── cython_wrapper/
│   ├── python_solver/
│   ├── tsp_fast_solver/
│   ├── tests/
│   ├── benchmark.py
│   ├── setup.py
│   └── pyproject.toml
├── assets/                             # Repository global assets & diagrams
├── dehradun_shortest_path.html         # Interactive map (view in browser)
├── dijkstra_benchmark_comparison.png   # Dijkstra performance infographic
├── tsp_benchmark_comparison.png        # TSP performance infographic
├── LICENSE
└── README.md
```

---

## Quick Commands

### 1. Build and Run Dijkstra Solvers
```bash
cd dijkstra_c_vs_python

# Build C++ Cython extension in-place
python setup.py build_ext --inplace

# Run the comprehensive benchmark
python benchmark.py

# Generate the interactive Dehradun map
python dehradun_map/generate_map.py

# Run unit tests
python -m pytest tests/test_dijkstra.py -v

# Package sdist for PyPI
python -m build --sdist --no-isolation
```

### 2. Build and Run TSP Solvers
```bash
cd tsp

# Build Cython extension
python setup.py build_ext --inplace

# Run benchmark
python benchmark.py

# Run unit tests
python -m pytest tests/
```

---

## License
MIT License. See [LICENSE](LICENSE) for details.
